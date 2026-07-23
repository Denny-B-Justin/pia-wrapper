"""
utils.py
--------
Reusable component builders for the standalone PIA app.
Keeping these out of app.py keeps the layout/callback file readable.
"""

from dash import html

from constants import (
    TOOL_NAME,
    TOOL_DESCRIPTION,
    TOOL_BULLETS,
    PIA_COUNTRIES,
    IFRAME_ASPECT_RATIO,
)


def brand_header(logo_url, secondary_logo_url=None, title=None):
    """Top nav lockup with the primary tool logo and an optional partner logo.

    The header now presents the brand stack as a compact lockup instead of a
    single floating logo.
    """
    brand_images = []
    if secondary_logo_url:
        brand_images.append(
            html.Img(
                src=secondary_logo_url,
                alt="PIM-PAM",
                className="brand-logo brand-logo--secondary",
            )
        )

    brand_images.append(
        html.Img(src=logo_url, alt="PIA", className="brand-logo")
    )

    logo_group = html.Div(
        brand_images + ([html.H1(title, className="brand-title")] if title else []),
        className="brand-lockup",
    )

    return html.Header(
        html.Div(logo_group, className="top-nav-inner"),
        className="top-nav",
    )


def tool_detail_panel(logo_url):
    """Description block for PIA.

    Rendered directly against the page/section background rather than in a
    bordered card \u2014 it should read as part of the page itself, not as a
    boxed-in info panel sitting on top of it.
    """
    return html.Div(
        [
            html.Div(
                [
                    html.Img(src=logo_url, alt="PIA", className="panel-logo"),
                    html.H1(TOOL_NAME, className="panel-title"),
                ],
                className="panel-header",
            ),
            html.P(TOOL_DESCRIPTION, className="panel-description"),
            html.Ul(
                [html.Li(b) for b in TOOL_BULLETS],
                className="panel-bullets",
            ),
        ],
        className="panel-detail",
    )


def country_chip(country, is_active):
    return html.Button(
        html.Span(country["name"], className="chip-name"),
        id={"type": "country-select", "index": country["id"]},
        n_clicks=0,
        className=f"country-chip {'is-active' if is_active else ''}",
        title=country["region"],
    )


def country_switcher(active_country_id):
    return html.Div(
        [
            html.Span("Country instance:", className="switcher-label"),
            html.Div(
                [country_chip(c, c["id"] == active_country_id) for c in PIA_COUNTRIES],
                className="country-chip-row",
            ),
        ],
        className="country-switcher",
    )


def embedded_frame(url, key):
    """An iframe embed with a fallback 'open in new tab' affordance.

    The World Bank / Posit Connect deployment may set frame-ancestor or
    X-Frame-Options headers that block embedding entirely; the fallback
    link keeps the tool reachable even if the frame itself renders blank.

    The iframe sits inside a fixed-aspect-ratio container (instead of a
    flat pixel height) so it scales cleanly at any screen width without
    cropping the bottom of the embedded dashboard.
    """
    return html.Div(
        [
            html.Div(
                html.A(
                    "Open full window \u2197",
                    href=url,
                    target="_blank",
                    rel="noopener noreferrer",
                    className="frame-fallback-link",
                ),
                className="frame-toolbar",
            ),
            html.Div(
                html.Iframe(src=url, key=key, className="tool-iframe"),
                className="tool-iframe-aspect",
                style={"aspectRatio": IFRAME_ASPECT_RATIO},
            ),
        ],
        className="frame-wrapper",
    )