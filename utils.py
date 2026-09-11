"""
utils.py
--------
Reusable component builders for the standalone PIA app.
Keeping these out of app.py keeps the layout/callback file readable.
"""

from dash import html, dcc

from constants import (
    TOOL_NAME,
    TOOL_DESCRIPTION,PIA_BLOG_URL,
    TOOL_BULLETS,
    PIA_COUNTRIES,
    IFRAME_ASPECT_RATIO,
    PIA_VIMEO_URL,
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
    bordered card it should read as part of the page itself, not as a
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
            html.P(
                [
                    TOOL_DESCRIPTION,
                    html.A(
                        " ↗",
                        href=PIA_BLOG_URL,
                        target="_blank",
                        rel="noopener noreferrer",
                        title="Read the PIA blog",
                        className="panel-blog-link",
                    ),
                ],
                className="panel-description",
            ),
            html.Ul(
                [html.Li(b) for b in TOOL_BULLETS],
                className="panel-bullets",
            ),
        ],
        className="panel-detail",
    )


def country_switcher(active_country_id):
    return html.Div(
        [
            html.Span("Country instance:", className="switcher-label"),
            dcc.Dropdown(
                id="country-dropdown",
                options=[
                    {"label": country["name"], "value": country["id"]}
                    for country in PIA_COUNTRIES
                ],
                value=active_country_id,
                clearable=False,
                searchable=False,
                className="country-dropdown",
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


def video_embed_panel(video_url=PIA_VIMEO_URL):
    """Right-hand overview video panel embedded from Vimeo."""
    return html.Div(
        [
            # html.H2("Overview video", className="video-panel-title"),
            html.Div(
                html.Iframe(
                    src=video_url,
                    title="PIA overview video",
                    className="vimeo-embed",
                    allow="autoplay; fullscreen; picture-in-picture; clipboard-write",
                ),
                className="video-embed-shell",
            ),
        ],
        className="video-panel",
    )

def VideoCard(title, vimeo_id, thumbnail_url=None):
    if thumbnail_url:
        overlay_bg = html.Img(src=thumbnail_url, alt="", className="w-full h-full object-cover")
    else:
        overlay_bg = None
    play_button = html.Button(
        [
            overlay_bg,
            html.Div(
                html.Div(Icon("play_triangle", size=28, color="#111111"), className="w-20 h-20 rounded-full bg-white shadow-xl flex items-center justify-center pl-1 group-hover:scale-110 transition-all duration-200"),
                className="absolute inset-0 flex items-center justify-center bg-black/10 group-hover:bg-black/20 transition-colors duration-200",
            ),
        ],
        id={"type": "video-play-btn", "index": vimeo_id},
        n_clicks=0,
        className="absolute inset-0 w-full h-full group",
        **{"aria-label": f"Play {title}"},
    )
    return html.Div([
        html.H3(title, className="text-base font-semibold text-gray-900 mb-3"),
        html.Div(
            play_button,
            id={"type": "video-container", "index": vimeo_id},
            className="aspect-video w-full rounded overflow-hidden bg-gray-900 border border-gray-200 relative",
        ),
    ])

