# /packages/tests/test_calculators_unit.py
import pytest
from packages.domain.models import UserFinancialProfile
from packages.calculators import generator, assumptions_loader


def test_parental_leave_income_drop():
    """Test that parental leave correctly reduces income during leave months."""
    profile = UserFinancialProfile(
        partner_1_monthly_income=4000,
        partner_2_monthly_income=4000,
        current_savings=0,
        monthly_housing_cost=1000,
        zip=36052,  # Low cost area
        due_date="2025-01-01",
        childcare_preference="center",
        partner_1_leave_duration_weeks=8,  # ~2 months
        partner_1_leave_percent_paid=50,   # 50% pay during leave
        partner_2_leave_duration_weeks=0,
        partner_2_leave_percent_paid=100
    )

    blueprint = generator.generate_baby_budget_blueprint(profile)
    monthly = blueprint.cashflow_projection

    # During first 2 months (8 weeks ≈ 2 months), partner1 income should drop to 50%
    # Month 1 income should be partner1 2000 + partner2 4000 = 6000
    assert round(monthly[0].income) == 6000, f"Expected 6000, got {monthly[0].income}"

    # Month 3 income should rebound to full 8000 (no leave)
    assert round(monthly[2].income) == 8000, f"Expected 8000, got {monthly[2].income}"


def test_stay_home_no_childcare_cost():
    """Test that stay_home preference results in zero childcare costs."""
    profile = UserFinancialProfile(
        partner_1_monthly_income=5000,
        partner_2_monthly_income=3000,
        current_savings=20000,
        monthly_housing_cost=1500,
        zip=94107,  # High cost area (would have high childcare costs)
        due_date="2025-01-01",
        childcare_preference="stay_home",
        partner_1_leave_duration_weeks=0,
        partner_1_leave_percent_paid=100,
        partner_2_leave_duration_weeks=0,
        partner_2_leave_percent_paid=100
    )

    blueprint = generator.generate_baby_budget_blueprint(profile)

    # Budget split should show 0% for childcare
    assert blueprint.budget_split.childcare_percent == 0.0, \
        f"Stay-at-home should have 0% childcare, got {blueprint.budget_split.childcare_percent}%"

    # Monthly baby cost should only be recurring costs (no childcare)
    assumptions = assumptions_loader.load_assumptions("stay_home")
    expected_baby_cost = assumptions["recurring_monthly_total"]
    assert blueprint.budget_split.monthly_baby_cost == expected_baby_cost, \
        f"Expected ${expected_baby_cost}, got ${blueprint.budget_split.monthly_baby_cost}"


def test_housing_high_warning():
    """Test that HOUSING_HIGH warning is triggered when housing exceeds 30% of income."""
    profile = UserFinancialProfile(
        partner_1_monthly_income=3000,
        partner_2_monthly_income=2000,
        current_savings=5000,
        monthly_housing_cost=2000,  # 40% of income (5000 total)
        zip=36052,
        due_date="2025-01-01",
        childcare_preference="center",
        partner_1_leave_duration_weeks=0,
        partner_1_leave_percent_paid=100,
        partner_2_leave_duration_weeks=0,
        partner_2_leave_percent_paid=100
    )

    blueprint = generator.generate_baby_budget_blueprint(profile)

    assert "HOUSING_HIGH" in blueprint.warnings, \
        f"Expected HOUSING_HIGH warning, got {blueprint.warnings}"


def test_childcare_high_warning():
    """Test that CHILDCARE_HIGH warning is triggered when childcare exceeds 30% of income."""
    profile = UserFinancialProfile(
        partner_1_monthly_income=4000,
        partner_2_monthly_income=3000,
        current_savings=10000,
        monthly_housing_cost=1500,
        zip=94107,  # High cost area with $2400/mo childcare
        due_date="2025-01-01",
        childcare_preference="center",
        partner_1_leave_duration_weeks=0,
        partner_1_leave_percent_paid=100,
        partner_2_leave_duration_weeks=0,
        partner_2_leave_percent_paid=100
    )

    blueprint = generator.generate_baby_budget_blueprint(profile)

    # $2400 childcare / $7000 income = 34% > 30%
    assert "CHILDCARE_HIGH" in blueprint.warnings, \
        f"Expected CHILDCARE_HIGH warning, got {blueprint.warnings}"


def test_five_year_projection_structure():
    """Test that the 5-year projection has correct structure."""
    profile = UserFinancialProfile(
        partner_1_monthly_income=5000,
        partner_2_monthly_income=4500,
        current_savings=10000,
        monthly_housing_cost=2000,
        zip=94107,
        due_date="2025-01-01",
        childcare_preference="center",
        partner_1_leave_duration_weeks=12,
        partner_1_leave_percent_paid=80,
        partner_2_leave_duration_weeks=6,
        partner_2_leave_percent_paid=100
    )

    blueprint = generator.generate_baby_budget_blueprint(profile)

    # Should have exactly 5 years
    assert len(blueprint.five_year_projection) == 5, \
        f"Expected 5 years, got {len(blueprint.five_year_projection)}"

    # Should have exactly 60 months
    assert len(blueprint.cashflow_projection) == 60, \
        f"Expected 60 months, got {len(blueprint.cashflow_projection)}"

    # Each year should have valid data
    for year_data in blueprint.five_year_projection:
        assert year_data.total_income > 0, f"Year {year_data.year} has no income"
        assert year_data.total_expenses > 0, f"Year {year_data.year} has no expenses"


def test_assumptions_loader():
    """Test that assumption files load correctly."""
    center_assumptions = assumptions_loader.load_assumptions("center")
    assert center_assumptions["version"] == "v1.0"
    assert "childcare_cost_by_band" in center_assumptions

    home_assumptions = assumptions_loader.load_assumptions("home")
    assert home_assumptions["version"] == "v1.0"

    stay_home_assumptions = assumptions_loader.load_assumptions("stay_home")
    assert stay_home_assumptions["childcare_cost_by_band"]["High"] == 0


def test_childcare_cost_lookup():
    """Test ZIP code to childcare cost lookup."""
    assumptions = assumptions_loader.load_assumptions("center")

    # Test High cost area
    high_cost = assumptions_loader.lookup_childcare_cost(94107, assumptions)
    assert high_cost == 2400, f"Expected 2400 for high cost area, got {high_cost}"

    # Test Low cost area
    low_cost = assumptions_loader.lookup_childcare_cost(36052, assumptions)
    assert low_cost == 800, f"Expected 800 for low cost area, got {low_cost}"

    # Test unknown ZIP (should default to Medium)
    unknown_cost = assumptions_loader.lookup_childcare_cost(99999, assumptions)
    assert unknown_cost == 1200, f"Expected 1200 for unknown area (Medium default), got {unknown_cost}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
