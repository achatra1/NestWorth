# /apps/api/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID, uuid4
from datetime import datetime
from packages.domain.models import UserFinancialProfile, BabyBudgetBlueprint
from packages.calculators import generator
from packages.pdf import report_generator
from packages.domain import db


app = FastAPI(
    title="NestWorth API",
    version="1.0.0",
    description="AI-powered baby budget planner that generates personalized 5-year financial plans",
    docs_url="/docs"
)

# Add CORS middleware for web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "NestWorth API",
        "version": "1.0.0",
        "description": "AI-powered baby budget planner",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "create_blueprint": "POST /blueprint",
            "get_blueprint": "GET /blueprint/{blueprint_id}",
            "demo": "GET /blueprint/demo"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    try:
        # Test database connection
        if db.session:
            db.session.execute("SELECT 1")
            db_status = "connected"
        else:
            db_status = "not initialized"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "ok",
        "time": datetime.utcnow().isoformat(),
        "database": db_status
    }


@app.post("/blueprint", response_model=BabyBudgetBlueprint)
async def create_blueprint(profile: UserFinancialProfile):
    """Generate a new baby budget blueprint.

    Args:
        profile: UserFinancialProfile from onboarding questionnaire

    Returns:
        BabyBudgetBlueprint with 5-year projections and PDF report
    """
    try:
        # Call the deterministic generator to compute the budget blueprint
        blueprint = generator.generate_baby_budget_blueprint(profile)

        # Generate unique ID for this blueprint
        new_id = uuid4()

        # Generate PDF report for the blueprint
        pdf_path = report_generator.generate_pdf_report(blueprint, report_id=new_id)
        blueprint.pdf_url = pdf_path

        # Persist to database if available
        if db.session:
            try:
                db_blueprint = db.Blueprint(
                    id=new_id,
                    user_profile=profile.model_dump(),         # store raw profile JSON
                    blueprint_json=blueprint.model_dump(),     # store full blueprint JSON
                    assumptions_version=blueprint.assumptions_version,
                    calculator_version=blueprint.calculator_version,
                    created_at=datetime.utcnow(),
                    warnings=[w for w in blueprint.warnings],  # list of warning codes
                    pdf_url=pdf_path
                )
                db.session.add(db_blueprint)
                db.session.commit()
            except Exception as e:
                # If DB error, rollback but still return the blueprint
                db.session.rollback()
                print(f"Warning: Failed to save blueprint to database: {e}")
                # Continue anyway - the blueprint was generated successfully

        return blueprint

    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=f"Invalid configuration: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate blueprint: {str(e)}")


@app.get("/blueprint/{blueprint_id}", response_model=BabyBudgetBlueprint)
async def get_blueprint(blueprint_id: UUID):
    """Retrieve an existing blueprint by ID.

    Args:
        blueprint_id: UUID of the blueprint

    Returns:
        BabyBudgetBlueprint
    """
    if not db.session:
        raise HTTPException(status_code=503, detail="Database not available")

    bp = db.session.get(db.Blueprint, blueprint_id)
    if not bp:
        raise HTTPException(status_code=404, detail="Blueprint not found")

    # Return the stored blueprint (which includes all calculated fields)
    return BabyBudgetBlueprint.model_validate(bp.blueprint_json)


@app.get("/blueprint/demo", response_model=BabyBudgetBlueprint)
async def demo_blueprint():
    """Generate a demo blueprint with sample data.

    Returns:
        BabyBudgetBlueprint for a sample profile
    """
    demo_profile = UserFinancialProfile(
        partner_1_monthly_income=5000,
        partner_2_monthly_income=4500,
        current_savings=10000,
        monthly_housing_cost=2000,
        zip=94107,  # San Francisco (High cost area)
        due_date=datetime.today().date().isoformat(),
        childcare_preference="center",
        partner_1_leave_duration_weeks=12,
        partner_1_leave_percent_paid=80,
        partner_2_leave_duration_weeks=6,
        partner_2_leave_percent_paid=100
    )

    blueprint = generator.generate_baby_budget_blueprint(demo_profile)

    # Generate PDF for demo (but don't save to DB)
    blueprint.pdf_url = report_generator.generate_pdf_report(blueprint, report_id="demo")

    return blueprint


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
