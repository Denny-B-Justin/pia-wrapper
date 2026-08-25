"""
constants.py
------------
Static content and configuration for the standalone PIA app.

This is the PIA-only slice of what used to be the PIM-PAM Digital Workspace
aggregator (which bundled PIA + GoAT + CBD behind one workbench). Splitting
it out means PIA can be shared or deployed entirely on its own, with its own
repo/site, without needing the other two tools.
"""

# ---------------------------------------------------------------------------
# Brand / design tokens
# ---------------------------------------------------------------------------
COLORS = {
    "bg": "#FFFFFF",
    "surface": "#F7F8FB",
    "surface_2": "#FFFFFF",
    "text": "#14192B",
    "muted": "#5B6478",
    "accent": "#1f9d67",  # PIA's accent (green), carried over from the workspace palette
}

APP_TITLE = "Public Infrastructure Access Tool"

LOGO_FILENAME = "pia_logo.png"

# ---------------------------------------------------------------------------
# Tool copy
# ---------------------------------------------------------------------------
TOOL_NAME = "Public Infrastructure Access Tool"

TOOL_DESCRIPTION = (
    "PIA is a geospatial optimizer that helps governments decide where to place new "
    "hospitals to maximize how many people gain reasonable access to them. It runs a "
    "maximum covering location model over hexagonal grids of population and travel-time "
    "data, then lets planners explore the recommended sites on an interactive map."
)

TOOL_BULLETS = [
    "Deployed separately for 19 countries: Zambia, Malawi, Serbia, Nepal, Uzbekistan, Pakistan, Cambodia, Burkina Faso, Côte d’Ivoire, Chad, Gabon, Guinea, The Gambia, Cameroon, Mali, Niger, Afghanistan, Somalia, Sudan, and Bangladesh.",
    "Built on H3 hexagonal indexing, population rasters, and OpenStreetMap data.",
    "PIA gives planners and policymakers an interactive way to explore infrastructure gaps on the ground.",
]

# ---------------------------------------------------------------------------
# PIA deployment - one base Posit Connect app, five country instances
# served via a query string (?country=slug).
# ---------------------------------------------------------------------------
PIA_BASE_URL = "https://datanalytics.worldbank.org/content/1cc36c57-f12d-4aa8-92a2-196bb0ea605f/"

PIA_COUNTRIES = [
    {"id": "afghanistan", "name": "Afghanistan", "region": "South Asia"},
    {"id": "bangladesh", "name": "Bangladesh", "region": "South Asia"},
    {"id": "burkina_faso", "name": "Burkina Faso", "region": "West Africa"},
    {"id": "cambodia", "name": "Cambodia", "region": "Southeast Asia"},
    {"id": "cameroon", "name": "Cameroon", "region": "Central Africa"},
    {"id": "chad", "name": "Chad", "region": "Central Africa"},
    {"id": "cote_d_ivoire", "name": "Côte d’Ivoire", "region": "West Africa"},
    {"id": "gabon", "name": "Gabon", "region": "Central Africa"},
    {"id": "guinea", "name": "Guinea", "region": "West Africa"},
    {"id": "malawi", "name": "Malawi", "region": "Southern Africa"},
    {"id": "mali", "name": "Mali", "region": "West Africa"},
    {"id": "nepal", "name": "Nepal", "region": "South Asia"},
    {"id": "niger", "name": "Niger", "region": "West Africa"},
    {"id": "pakistan", "name": "Pakistan", "region": "South Asia"},
    {"id": "serbia", "name": "Serbia", "region": "Western Balkans"},
    {"id": "somalia", "name": "Somalia", "region": "East Africa"},
    {"id": "sudan", "name": "Sudan", "region": "North Africa"},
    {"id": "the_gambia", "name": "The Gambia", "region": "West Africa"},
    {"id": "uzbekistan", "name": "Uzbekistan", "region": "Central Asia"},
    {"id": "zambia", "name": "Zambia", "region": "Southern Africa"},
]

PIA_DEFAULT_COUNTRY = "afghanistan"


def pia_url_for(country_id: str) -> str:
    """Build the PIA deployment URL for a given country slug."""
    valid_ids = {c["id"] for c in PIA_COUNTRIES}
    if country_id not in valid_ids:
        return PIA_BASE_URL
    return f"{PIA_BASE_URL}?country={country_id}"


# Embedded tool renders inside a fixed-aspect-ratio box rather than a flat
# pixel height, so it resizes cleanly across screen widths. Keep the dashboard
# in its standard widescreen format and widen the page layout instead.
IFRAME_ASPECT_RATIO = "16 / 8"