# 🚀 NestWorth Quick Start Guide

Get NestWorth up and running in 5 minutes!

## Prerequisites

- Python 3.10 or higher
- Docker & Docker Compose (recommended for database)
- OR PostgreSQL 15+ installed locally

## Option 1: Quick Start (Recommended)

### 1. Install Dependencies

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python packages
pip install -r requirements.txt
```

### 2. Start PostgreSQL

```bash
# Using Docker Compose (easiest)
docker-compose up -d

# Wait a few seconds for PostgreSQL to start
```

### 3. Initialize Database

```bash
python init_db.py
```

### 4. Start the Server

```bash
# Using the convenience script
./run.sh

# OR manually
uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Test It Out!

Open your browser and visit:
- **API Documentation**: http://localhost:8000/docs
- **Demo Blueprint**: http://localhost:8000/blueprint/demo

## Option 2: Quick Test (No Database Required)

If you just want to test the calculators without setting up the database:

```bash
# Install minimal dependencies
pip install pydantic jinja2

# Run basic test
python test_basic.py
```

This will generate a sample baby budget and display the results in your terminal!

## Example API Call

### Using curl:

```bash
curl -X POST "http://localhost:8000/blueprint" \
  -H "Content-Type: application/json" \
  -d '{
    "partner_1_monthly_income": 6000,
    "partner_2_monthly_income": 5000,
    "current_savings": 15000,
    "monthly_housing_cost": 2500,
    "zip": 94107,
    "due_date": "2025-08-01",
    "childcare_preference": "center",
    "partner_1_leave_duration_weeks": 12,
    "partner_1_leave_percent_paid": 100,
    "partner_2_leave_duration_weeks": 8,
    "partner_2_leave_percent_paid": 80
  }'
```

### Using Python:

```python
import requests

profile = {
    "partner_1_monthly_income": 6000,
    "partner_2_monthly_income": 5000,
    "current_savings": 15000,
    "monthly_housing_cost": 2500,
    "zip": 94107,
    "due_date": "2025-08-01",
    "childcare_preference": "center",
    "partner_1_leave_duration_weeks": 12,
    "partner_1_leave_percent_paid": 100,
    "partner_2_leave_duration_weeks": 8,
    "partner_2_leave_percent_paid": 80
}

response = requests.post("http://localhost:8000/blueprint", json=profile)
blueprint = response.json()

print(f"Total 5-year baby cost: ${blueprint['budget_split']['total_five_year_baby_cost']:,.0f}")
print(f"Monthly baby cost: ${blueprint['budget_split']['monthly_baby_cost']:,.0f}")
print(f"Warnings: {blueprint['warnings']}")
```

## Understanding the Output

### Budget Split
- **Housing %**: Portion of income for housing
- **Childcare %**: Portion for childcare (daycare/nanny)
- **Baby Needs %**: Portion for diapers, formula, supplies
- **Remaining %**: Left for other expenses and savings

### Warnings
- `HOUSING_HIGH`: Housing costs >30% of income
- `CHILDCARE_HIGH`: Childcare costs >30% of income
- `CHILDCARE_UNSUSTAINABLE`: Childcare >80% of income
- `NEGATIVE_CASHFLOW`: Some months expenses exceed income
- `LOW_SAVINGS`: Current savings may be exhausted

### Childcare Options
1. **center**: Daycare centers (highest cost, varies by ZIP)
2. **home**: In-home nanny or family care (moderate cost)
3. **stay_home**: One parent stays home (no childcare cost, but one income lost)

## Troubleshooting

### Database Connection Error
```bash
# Check if PostgreSQL is running
docker-compose ps

# Restart PostgreSQL
docker-compose restart

# Check logs
docker-compose logs postgres
```

### Module Not Found Error
```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Port Already in Use
```bash
# Change port in command
uvicorn apps.api.main:app --reload --port 8001
```

## Next Steps

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Run Tests**: `pytest -v`
3. **Read Full Documentation**: See README.md
4. **Customize Assumptions**: Edit JSON files in `packages/assumptions/`
5. **Build a Frontend**: Use the API to build a web UI

## Need Help?

- Check README.md for full documentation
- Run `pytest` to verify your setup
- Open an issue on GitHub

---

**Happy Budget Planning! 🏡👶**
