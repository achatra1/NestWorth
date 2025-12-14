# /packages/calculators/generator.py
from packages.calculators import assumptions_loader, baby_plan, budget_split
from packages.domain.models import BabyBudgetBlueprint, BlueprintNarrativeChunk


# Define some guardrail thresholds (could also be part of assumptions JSON)
HOUSING_RATIO_WARN = 0.3    # Warn if housing >30% of income
CHILDCARE_RATIO_WARN = 0.3  # Warn if childcare >30% of income
CHILDCARE_UNSUSTAINABLE = 0.8  # Critical warn if childcare >80% (edge case)
CURRENT_VERSION = "v1.0"


def generate_baby_budget_blueprint(profile):
    """High-level function to generate the BabyBudgetBlueprint for a given user profile.

    Args:
        profile: UserFinancialProfile from onboarding form

    Returns:
        BabyBudgetBlueprint with all calculations, warnings, and narrative sections
    """
    # 1. Load assumptions for the selected childcare mode
    assumptions = assumptions_loader.load_assumptions(profile.childcare_preference)
    assumptions_version = assumptions.get("version", "v1.0")

    # 2. Run the 5-year projection calculators
    five_year_projection, monthly_cashflow = baby_plan.calculate_5yr_plan(profile, assumptions)

    # 3. Compute budget split recommendation
    recommendation = budget_split.recommend_budget_split(profile, assumptions, five_year_projection)

    # 4. Analyze warnings based on guardrails
    warnings = []

    # Housing cost ratio warning
    combined_income = profile.partner_1_monthly_income + profile.partner_2_monthly_income
    effective_income = combined_income

    if profile.childcare_preference == "stay_home":
        effective_income = max(profile.partner_1_monthly_income, profile.partner_2_monthly_income)

    if effective_income > 0:
        if profile.monthly_housing_cost / effective_income > HOUSING_RATIO_WARN:
            warnings.append("HOUSING_HIGH")

        # Childcare cost warning (consider full childcare cost vs income)
        childcare_base = assumptions_loader.lookup_childcare_cost(profile.zip, assumptions)
        if childcare_base / effective_income > CHILDCARE_RATIO_WARN:
            warnings.append("CHILDCARE_HIGH")
        if childcare_base / effective_income > CHILDCARE_UNSUSTAINABLE:
            warnings.append("CHILDCARE_UNSUSTAINABLE")

    # Negative cashflow & savings warnings
    any_negative = any(mc.net < 0 for mc in monthly_cashflow)
    if any_negative:
        warnings.append("NEGATIVE_CASHFLOW")

    # If any month drives savings below zero, warn low savings
    any_depleted = any(mc.cumulative_savings < 0 for mc in monthly_cashflow)
    if any_depleted:
        warnings.append("LOW_SAVINGS")

    # 5. Prepare report narrative sections (bullets for PDF)
    report_sections = []

    # Overview section
    total_baby_cost = recommendation.total_five_year_baby_cost
    avg_monthly = recommendation.monthly_baby_cost
    overview_bullets = [
        f"Estimated total baby-related costs over 5 years: ${total_baby_cost:,.0f}",
        f"On average, about ${avg_monthly:,.0f} per month will go towards baby needs (including childcare).",
        f"Household take-home income: ${combined_income*12:,.0f} per year; expected budget allocated to baby: {round((avg_monthly*12)/(combined_income*12)*100,1) if combined_income>0 else 0}%.",
    ]
    report_sections.append(BlueprintNarrativeChunk(section="Overview", bullets=overview_bullets))

    # Arrival Costs section
    one_time_total = assumptions["one_time_total"]
    gear_items = assumptions.get("one_time_items", [])
    arrival_bullets = [f"One-time baby gear and setup costs (due around birth): ~${one_time_total:,} in total."]

    if gear_items:
        # List a few major gear items and their costs
        for item in gear_items:
            arrival_bullets.append(f"- {item['item']}: ${item['cost']}")

    if assumptions.get("medical_one_time_cost"):
        arrival_bullets.append(f"- Medical expenses (est.): ${assumptions['medical_one_time_cost']}")

    report_sections.append(BlueprintNarrativeChunk(section="Arrival Costs", bullets=arrival_bullets))

    # Year-by-Year Costs section
    yearly_bullets = []
    for yr in five_year_projection:
        year = yr.year
        # Show net cash flow for each year and highlight if negative or surplus
        sign = "surplus" if yr.net_cashflow >= 0 else "deficit"
        yearly_bullets.append(
            f"Year {year}: Total expenses ${yr.total_expenses:,.0f} vs income ${yr.total_income:,.0f} → net {sign} of ${abs(yr.net_cashflow):,.0f}"
        )
    report_sections.append(BlueprintNarrativeChunk(section="Year-by-Year Summary", bullets=yearly_bullets))

    # Cashflow Flags section (warnings turned into user-friendly bullets)
    flags_bullets = []
    if "NEGATIVE_CASHFLOW" in warnings:
        flags_bullets.append("⚠ Some months your expenses exceed income – plan to cover these with savings or budget cuts.")
    if "LOW_SAVINGS" in warnings:
        flags_bullets.append("⚠ Your current savings could be exhausted; consider building a larger cushion for emergencies.")
    if "HOUSING_HIGH" in warnings:
        flags_bullets.append("⚠ Housing costs take up a large portion of income (above recommended 30%).")
    if "CHILDCARE_HIGH" in warnings:
        flags_bullets.append("⚠ Childcare costs will be a significant budget item – ensure it's sustainable long-term.")
    if "CHILDCARE_UNSUSTAINABLE" in warnings:
        flags_bullets.append("⚠⚠ Childcare costs approach your sole income – this scenario may be financially unsustainable without changes.")
    if not flags_bullets:
        flags_bullets.append("✓ No major budget red flags – your plan is financially balanced based on the given data.")

    report_sections.append(BlueprintNarrativeChunk(section="Cashflow Flags", bullets=flags_bullets))

    # Assumptions section
    childcare_cost_for_display = assumptions_loader.lookup_childcare_cost(profile.zip, assumptions)
    assumptions_bullets = [
        f"Childcare cost basis: ${childcare_cost_for_display:,}/month for {profile.childcare_preference} care in your area.",
        f"Recurring baby costs: ${assumptions['recurring_monthly_total']:,}/month (diapers, formula, etc.).",
        f"Inflation/adjustments: childcare costs reduced 10% each year after first; baby needs costs +20% from year 4 onward.",
        f"Parental leave: Partner1 {profile.partner_1_leave_duration_weeks} weeks @ {profile.partner_1_leave_percent_paid}% pay, Partner2 {profile.partner_2_leave_duration_weeks} weeks @ {profile.partner_2_leave_percent_paid}% pay."
    ]
    report_sections.append(BlueprintNarrativeChunk(section="Assumptions", bullets=assumptions_bullets))

    # 6. Compile everything into the BabyBudgetBlueprint model
    blueprint = BabyBudgetBlueprint(
        profile=profile,
        assumptions_version=assumptions_version,
        calculator_version=CURRENT_VERSION,
        five_year_projection=five_year_projection,
        cashflow_projection=monthly_cashflow,
        budget_split=recommendation,
        warnings=warnings,
        report_sections=report_sections
    )

    return blueprint
