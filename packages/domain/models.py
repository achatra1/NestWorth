# /packages/domain/models.py
from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from datetime import date


class UserFinancialProfile(BaseModel):
    """User input data from the onboarding questionnaire."""
    partner_1_monthly_income: float
    partner_2_monthly_income: float
    current_savings: float
    monthly_housing_cost: float
    zip: int  # 5-digit ZIP code (as int or could be string with leading zeros)
    due_date: str  # ISO date string
    childcare_preference: Literal["center", "home", "stay_home"]
    partner_1_leave_duration_weeks: int
    partner_1_leave_percent_paid: float  # percent (0-100)
    partner_2_leave_duration_weeks: int
    partner_2_leave_percent_paid: float  # percent (0-100)


class YearBreakdown(BaseModel):
    """Summary of one year's income, expenses, and net cashflow."""
    year: int
    total_income: float
    total_expenses: float
    net_cashflow: float


class MonthlyCashflow(BaseModel):
    """Detailed monthly projection of income, expenses, and running savings."""
    year: int
    month: int
    income: float
    expenses: float
    net: float
    cumulative_savings: float


class BudgetRecommendation(BaseModel):
    """Suggested budget allocation after baby arrives (monthly averages)."""
    housing_percent: float
    childcare_percent: float
    baby_needs_percent: float
    remaining_percent: float
    monthly_baby_cost: float  # average monthly baby-related cost (diapers+childcare etc.)
    total_five_year_baby_cost: float


class BlueprintNarrativeChunk(BaseModel):
    """Key bullet points for each section of the PDF narrative."""
    section: str
    bullets: List[str]  # key bullet points for that section


class BabyBudgetBlueprint(BaseModel):
    """Complete 5-year baby budget blueprint with all calculations and narrative."""
    profile: UserFinancialProfile
    assumptions_version: str
    calculator_version: str
    five_year_projection: List[YearBreakdown]
    cashflow_projection: List[MonthlyCashflow]
    budget_split: BudgetRecommendation
    warnings: List[str]  # e.g., ["HOUSING_HIGH", "LOW_SAVINGS"] codes
    report_sections: List[BlueprintNarrativeChunk]
    pdf_url: Optional[str] = None  # path or URL to the generated PDF report
