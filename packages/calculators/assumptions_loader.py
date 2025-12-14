# /packages/calculators/assumptions_loader.py
import json
import os


# Determine the directory of assumptions JSON files
ASSUMPTIONS_DIR = os.path.join(os.path.dirname(__file__), os.pardir, "assumptions")


def load_assumptions(childcare_pref: str) -> dict:
    """Load the assumptions JSON for the given childcare preference (center/home/stay_home)."""
    filename = f"{childcare_pref}_assumptions_v1.json"
    path = os.path.join(ASSUMPTIONS_DIR, filename)

    if not os.path.exists(path):
        raise FileNotFoundError(f"Assumptions file not found: {path}")

    with open(path, "r") as f:
        data = json.load(f)

    # Validate version field exists
    if "version" not in data:
        raise ValueError(f"Assumptions file {filename} missing 'version' field")

    return data


def lookup_childcare_cost(zip_code: int, assumptions: dict) -> float:
    """Return the monthly childcare cost based on ZIP code band (Low/Medium/High).

    Args:
        zip_code: 5-digit ZIP code (as int)
        assumptions: Loaded assumptions dictionary

    Returns:
        Monthly childcare cost for the region
    """
    # Default to Medium if no mapping or ZIP not found
    band = "Medium"

    if "zip_cost_band" in assumptions:
        band_map = assumptions["zip_cost_band"]
        # Convert int zip to zero-padded string for lookup
        str_zip = str(zip_code).zfill(5)

        if str_zip in band_map:
            band = band_map[str_zip]

    # Now use the band to get cost for this preference
    cost_by_band = assumptions.get("childcare_cost_by_band", {})
    return cost_by_band.get(band, 0.0)
