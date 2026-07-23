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
    "Deployed separately for five countries: Zambia, Malawi, Serbia, Nepal, and Uzbekistan.",
    "Built on H3 hexagonal indexing, population rasters, and OpenStreetMap data.",
    "PIA gives planners and policymakers an interactive way to explore infrastructure gaps on the ground.",
]

# ---------------------------------------------------------------------------
# PIA deployment - one base Posit Connect app, five country instances
# served via a query string (?country=slug).
# ---------------------------------------------------------------------------
PIA_BASE_URL = "https://datanalytics.worldbank.org/content/1cc36c57-f12d-4aa8-92a2-196bb0ea605f/"

PIA_COUNTRIES = [
    {"id": "zambia", "name": "Zambia", "region": "Southern Africa"},
    {"id": "malawi", "name": "Malawi", "region": "Southern Africa"},
    {"id": "serbia", "name": "Serbia", "region": "Western Balkans"},
    {"id": "nepal", "name": "Nepal", "region": "South Asia"},
    {"id": "uzbekistan", "name": "Uzbekistan", "region": "Central Asia"},
]
PIA_DEFAULT_COUNTRY = "zambia"


def pia_url_for(country_id: str) -> str:
    """Build the PIA deployment URL for a given country slug."""
    valid_ids = {c["id"] for c in PIA_COUNTRIES}
    if country_id not in valid_ids:
        return PIA_BASE_URL
    return f"{PIA_BASE_URL}?country={country_id}"


# Embedded tool renders inside a fixed-aspect-ratio box rather than a flat
# pixel height, so it resizes cleanly across screen widths. The dashboard is
# landscape (map + side panels), so a widescreen 16:9 ratio is used.
IFRAME_ASPECT_RATIO = "16 / 9"