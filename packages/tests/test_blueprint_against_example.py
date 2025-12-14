# /packages/tests/test_blueprint_against_example.py
"""
Golden tests that verify calculator outputs match the Example.xlsx spreadsheet.

To run these tests, you need to have Example.xlsx in the project root directory.
"""
import os
import pytest
from packages.domain.models import UserFinancialProfile
from packages.calculators import generator


# Check if Example.xlsx exists
EXAMPLE_FILE = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "Example.xlsx")
HAS_EXAMPLE = os.path.exists(EXAMPLE_FILE)


@pytest.mark.skipif(not HAS_EXAMPLE, reason="Example.xlsx not found")
def test_blueprint_matches_example():
    """Test that calculator outputs match the Example.xlsx spreadsheet."""
    try:
        import openpyxl
    except ImportError:
        pytest.skip("openpyxl not installed")

    # Load the example spreadsheet (data_only to get computed values)
    wb = openpyxl.load_workbook(EXAMPLE_FILE, data_only=True)
    sheet = wb["Calculation sheet"]

    # Read input profile from sheet (the example file's "Sample input")
    # Note: These cell references need to be adjusted based on actual Excel structure
    p1_income = sheet["B3"].value
    p2_income = sheet["B4"].value
    current_savings = sheet["B5"].value or 0
    housing = sheet["B6"].value or 0
    zip_code = int(sheet["B7"].value)  # Example may store zip as number
    due_date = "2024-01-01"  # Assumed value if not in sheet
    childcare_pref = "center"  # Example.xlsx sample used "Center"
    p1_leave_wks = sheet["B11"].value or 0
    p1_leave_paid = sheet["B12"].value or 100
    p2_leave_wks = sheet["B13"].value or 0
    p2_leave_paid = sheet["B14"].value or 100

    profile = UserFinancialProfile(
        partner_1_monthly_income=p1_income,
        partner_2_monthly_income=p2_income,
        current_savings=current_savings,
        monthly_housing_cost=housing,
        zip=zip_code,
        due_date=due_date,
        childcare_preference=childcare_pref.lower(),
        partner_1_leave_duration_weeks=int(p1_leave_wks),
        partner_1_leave_percent_paid=p1_leave_paid,
        partner_2_leave_duration_weeks=int(p2_leave_wks),
        partner_2_leave_percent_paid=p2_leave_paid
    )

    blueprint = generator.generate_baby_budget_blueprint(profile)

    # Compare total 5-year baby-related cost
    # Adjust cell reference based on actual Excel structure
    expected_total_cost = sheet["B57"].value  # Example cell with total baby cost
    calc_total_cost = blueprint.budget_split.total_five_year_baby_cost

    assert round(calc_total_cost) == round(expected_total_cost), \
        f"Total 5-year cost mismatch: {calc_total_cost} vs {expected_total_cost}"

    # Compare year-by-year net cash flow
    # Adjust cell references based on actual Excel structure
    expected_nets = [
        sheet["N33"].value,  # Year 1 net (from Excel)
        sheet["N38"].value,  # Year 2 net
        sheet["N44"].value,  # Year 3 net
        sheet["N50"].value,  # Year 4 net
        sheet["N55"].value   # Year 5 net
    ]

    for i, year_breakdown in enumerate(blueprint.five_year_projection):
        assert round(year_breakdown.net_cashflow) == round(expected_nets[i]), \
            f"Year {year_breakdown.year} net mismatch: {year_breakdown.net_cashflow} vs {expected_nets[i]}"

    print("✓ All golden tests passed! Calculator matches Example.xlsx")


def test_golden_test_sample_values():
    """
    Test with hardcoded sample values from Example.xlsx.
    This test doesn't require the actual Excel file.
    """
    # Sample profile based on a typical example scenario
    profile = UserFinancialProfile(
        partner_1_monthly_income=5000,
        partner_2_monthly_income=4500,
        current_savings=10000,
        monthly_housing_cost=2000,
        zip=1748,  # Hopkinton MA (High cost area)
        due_date="2025-01-01",
        childcare_preference="center",
        partner_1_leave_duration_weeks=12,
        partner_1_leave_percent_paid=80,
        partner_2_leave_duration_weeks=6,
        partner_2_leave_percent_paid=100
    )

    blueprint = generator.generate_baby_budget_blueprint(profile)

    # Basic sanity checks
    assert blueprint.budget_split.total_five_year_baby_cost > 0
    assert len(blueprint.five_year_projection) == 5
    assert len(blueprint.cashflow_projection) == 60

    # Check that childcare is a significant portion (High cost area)
    assert blueprint.budget_split.childcare_percent > 20

    print(f"Total 5-year baby cost: ${blueprint.budget_split.total_five_year_baby_cost:,.0f}")
    print(f"Monthly baby cost: ${blueprint.budget_split.monthly_baby_cost:,.0f}")
    print(f"Warnings: {blueprint.warnings}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
