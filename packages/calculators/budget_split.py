# /packages/calculators/budget_split.py
from packages.domain.models import BudgetRecommendation
from packages.calculators import assumptions_loader


def recommend_budget_split(profile, assumptions, five_year_projection):
    """Suggest a budget breakdown after baby arrives (percentages of income to major categories).

    Args:
        profile: UserFinancialProfile
        assumptions: Loaded assumptions dictionary
        five_year_projection: List of YearBreakdown objects

    Returns:
        BudgetRecommendation with percentage breakdowns and total costs
    """
    # Use combined monthly income (when both partners working) as baseline for percentages
    combined_monthly_income = profile.partner_1_monthly_income + profile.partner_2_monthly_income

    if profile.childcare_preference == "stay_home":
        # If one stays home, baseline income = higher earner's income
        combined_monthly_income = max(profile.partner_1_monthly_income, profile.partner_2_monthly_income)

    if combined_monthly_income <= 0:
        # Avoid division by zero if incomes are zero (unlikely in normal use)
        combined_monthly_income = 1e-9

    # Get baseline costs from assumptions
    housing = profile.monthly_housing_cost
    childcare_cost = 0.0

    if profile.childcare_preference in ("center", "home"):
        # Use the base childcare cost for the region (for a typical month after initial period)
        childcare_cost = assumptions_loader.lookup_childcare_cost(profile.zip, assumptions)

    baby_needs_cost = assumptions["recurring_monthly_total"]

    # Calculate percentages of income
    housing_pct = housing / combined_monthly_income
    childcare_pct = childcare_cost / combined_monthly_income
    baby_needs_pct = baby_needs_cost / combined_monthly_income
    used_pct = housing_pct + childcare_pct + baby_needs_pct
    remaining_pct = max(0.0, 1.0 - used_pct)

    # Average monthly baby-related cost (including childcare + recurring; ignoring housing)
    avg_baby_monthly = childcare_cost + baby_needs_cost

    # Total five-year baby-related cost (sum of all baby expenses from projection).
    # We can derive this from projection: total expenses minus housing.
    total_expenses = sum(y.total_expenses for y in five_year_projection)
    total_housing_5yr = profile.monthly_housing_cost * 12 * 5
    total_baby_5yr = total_expenses - total_housing_5yr

    return BudgetRecommendation(
        housing_percent=round(housing_pct * 100, 1),
        childcare_percent=round(childcare_pct * 100, 1),
        baby_needs_percent=round(baby_needs_pct * 100, 1),
        remaining_percent=round(remaining_pct * 100, 1),
        monthly_baby_cost=round(avg_baby_monthly, 2),
        total_five_year_baby_cost=round(total_baby_5yr, 2)
    )
