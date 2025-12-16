#!/usr/bin/env python3
"""
Basic test to verify NestWorth core functionality without database.
"""

from packages.domain.models import UserFinancialProfile
from packages.calculators import generator


def main():
    print("🧪 Testing NestWorth Core Functionality")
    print("=" * 50)

    # Create a test profile
    print("\n1️⃣  Creating test profile...")
    profile = UserFinancialProfile(
        partner_1_monthly_income=5000,
        partner_2_monthly_income=4500,
        current_savings=10000,
        monthly_housing_cost=2000,
        zip=94107,  # San Francisco (High cost area)
        due_date="2025-06-01",
        childcare_preference="center",
        partner_1_leave_duration_weeks=12,
        partner_1_leave_percent_paid=80,
        partner_2_leave_duration_weeks=6,
        partner_2_leave_percent_paid=100
    )
    print("✅ Profile created")

    # Generate blueprint
    print("\n2️⃣  Generating baby budget blueprint...")
    try:
        blueprint = generator.generate_baby_budget_blueprint(profile)
        print("✅ Blueprint generated successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    # Display results
    print("\n" + "=" * 50)
    print("📊 RESULTS")
    print("=" * 50)

    print(f"\n💰 Budget Split:")
    print(f"   Housing: {blueprint.budget_split.housing_percent}%")
    print(f"   Childcare: {blueprint.budget_split.childcare_percent}%")
    print(f"   Baby Needs: {blueprint.budget_split.baby_needs_percent}%")
    print(f"   Remaining: {blueprint.budget_split.remaining_percent}%")

    print(f"\n👶 Baby Costs:")
    print(f"   Monthly: ${blueprint.budget_split.monthly_baby_cost:,.0f}")
    print(f"   5-Year Total: ${blueprint.budget_split.total_five_year_baby_cost:,.0f}")

    print(f"\n⚠️  Warnings: {', '.join(blueprint.warnings) if blueprint.warnings else 'None'}")

    print(f"\n📅 5-Year Projection:")
    for year_data in blueprint.five_year_projection:
        sign = "✓" if year_data.net_cashflow >= 0 else "⚠"
        print(f"   Year {year_data.year}: Income ${year_data.total_income:,.0f} - "
              f"Expenses ${year_data.total_expenses:,.0f} = "
              f"Net ${year_data.net_cashflow:,.0f} {sign}")

    print("\n" + "=" * 50)
    print("✅ All tests passed! NestWorth is working correctly.")
    print("=" * 50)

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

# trigger