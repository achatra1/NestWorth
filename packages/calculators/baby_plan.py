# /packages/calculators/baby_plan.py
from datetime import datetime
from math import ceil
from packages.calculators import assumptions_loader
from packages.domain.models import UserFinancialProfile, YearBreakdown, MonthlyCashflow


def calculate_5yr_plan(profile: UserFinancialProfile, assumptions: dict):
    """Simulate the 5-year financial projection (month-by-month) for the given profile and assumptions.

    Args:
        profile: User's financial profile from onboarding
        assumptions: Loaded cost assumptions dictionary

    Returns:
        Tuple of (five_year_projection, monthly_cashflow)
        - five_year_projection: List of YearBreakdown objects (5 years)
        - monthly_cashflow: List of MonthlyCashflow objects (60 months)
    """
    # Extract profile fields for convenience
    p1_income = profile.partner_1_monthly_income
    p2_income = profile.partner_2_monthly_income
    current_savings = profile.current_savings
    housing_cost = profile.monthly_housing_cost
    childcare_mode = profile.childcare_preference

    # Calculate how many months of leave for each partner (round up weeks/4)
    months_leave1 = ceil(profile.partner_1_leave_duration_weeks / 4.0)
    months_leave2 = ceil(profile.partner_2_leave_duration_weeks / 4.0)

    # Fraction of income received during leave (e.g., 90% paid -> 0.9 of income during leave)
    p1_paid_fraction = profile.partner_1_leave_percent_paid / 100.0
    p2_paid_fraction = profile.partner_2_leave_percent_paid / 100.0

    # One-time costs and recurring costs from assumptions
    one_time_cost = assumptions["one_time_total"]  # total one-time baby gear cost at birth
    monthly_recurring_base = assumptions["recurring_monthly_total"]  # baseline monthly recurring baby costs

    # Get childcare base cost based on region (for center/home; stay_home will be zero)
    base_childcare_cost = assumptions_loader.lookup_childcare_cost(profile.zip, assumptions)

    # Determine inflation or cost adjustment factors from assumptions
    childcare_factor_by_year = assumptions.get("childcare_cost_factors_by_year", {})
    recurring_factor_by_year = assumptions.get("recurring_cost_factor_by_year", {})

    # Simulation: 60 months from due_date
    monthly_cashflow = []
    savings_balance = current_savings

    for month_index in range(0, 60):
        # Calculate year and month number in plan (year 1 = baby age 0-1)
        year = month_index // 12 + 1
        month_of_year = month_index % 12 + 1

        # Determine income for this month
        if childcare_mode == "stay_home":
            # If one parent stays home, assume the lower income is forfeited from birth.
            # The household income = max(p1_income, p2_income), and we ignore leave (since it's a permanent change).
            income = max(p1_income, p2_income)
        else:
            # For "center" or "home" modes, both may work, apply leave reductions if applicable.
            p1_effective = p1_income
            p2_effective = p2_income

            # If within leave duration, reduce pay for that partner:
            if month_index < months_leave1:
                p1_effective = p1_income * p1_paid_fraction
            if month_index < months_leave2:
                p2_effective = p2_income * p2_paid_fraction

            income = p1_effective + p2_effective

        # Determine expenses for this month
        expense = 0.0

        # Housing cost every month
        expense += housing_cost

        # Recurring baby costs (e.g. diapers, food), apply inflation factor if any for this year
        recurring_cost = monthly_recurring_base
        if str(year) in recurring_factor_by_year:
            recurring_cost *= recurring_factor_by_year[str(year)]
        expense += recurring_cost

        # One-time costs at the arrival month (assume due_date month as when baby arrives)
        if month_index == 0:
            expense += one_time_cost + assumptions.get("medical_one_time_cost", 0.0)

        # Childcare costs: start when parental leave is over.
        # For simplicity, assume childcare starts after both leaves, or by month 6 at the latest
        # (MVP assumption: first ~6 months at home, then childcare).
        if childcare_mode in ("center", "home"):
            childcare_start_month = max(months_leave1, months_leave2, 6)
            if month_index >= childcare_start_month:
                # Use base childcare cost adjusted by factor for that year
                # (cost may reduce as child ages, per assumptions)
                factor = 1.0
                if str(year) in childcare_factor_by_year:
                    factor = childcare_factor_by_year[str(year)]
                expense += base_childcare_cost * factor

        # Calculate net cash flow for the month and update cumulative savings
        net = income - expense
        savings_balance += net

        # Record this month's details
        monthly_cashflow.append(MonthlyCashflow(
            year=year,
            month=month_of_year,
            income=round(income, 2),
            expenses=round(expense, 2),
            net=round(net, 2),
            cumulative_savings=round(savings_balance, 2)
        ))

    # Aggregate yearly totals from monthly data
    five_year_projection = []
    for y in range(1, 6):
        year_income = sum(m.income for m in monthly_cashflow if m.year == y)
        year_expenses = sum(m.expenses for m in monthly_cashflow if m.year == y)
        year_net = sum(m.net for m in monthly_cashflow if m.year == y)
        five_year_projection.append(YearBreakdown(
            year=y,
            total_income=round(year_income, 2),
            total_expenses=round(year_expenses, 2),
            net_cashflow=round(year_net, 2)
        ))

    return five_year_projection, monthly_cashflow
