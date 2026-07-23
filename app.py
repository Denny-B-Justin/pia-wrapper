"""
app.py
------
PIA (Public Infrastructure Access) \u2014 standalone Dash app.

This is the single-tool version of the PIA embed that used to live inside
the PIM-PAM Digital Workspace aggregator (which bundled PIA + GoAT + CBD
behind one workbench). Splitting it out lets PIA be shared/deployed on its
own, with its own link and its own login, without pulling in the other two
tools.

Run locally with: python app.py
"""

import dash
from dash import html, dcc, Input, Output, ALL, ctx
import dash.exceptions

from constants import APP_TITLE, LOGO_FILENAME, PIA_DEFAULT_COUNTRY, pia_url_for
from utils import (
    brand_header,
    tool_detail_panel,
    country_switcher,
    embedded_frame,
)

app = dash.Dash(__name__, title=APP_TITLE, update_title=None)
server = app.server

LOGO_URL = app.get_asset_url(LOGO_FILENAME)
PIM_PAM_LOGO_URL = app.get_asset_url("PIM-PAM_Logo_Dark.png")

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

def build_layout():
    return html.Div(
        [
            # ---- store (client-side state, no server session needed) ----
            dcc.Store(id="active-country-store", data=PIA_DEFAULT_COUNTRY),

            # ---- top nav lockup with partner branding and title ----
            brand_header(
                LOGO_URL,
                secondary_logo_url=PIM_PAM_LOGO_URL,
                title="Public Infrastructure Access Tool",
            ),

            # ---- PIA detail + country switcher + embed ----
            html.Section(
                html.Div(
                    [
                        tool_detail_panel(LOGO_URL),
                        html.Div(id="country-switcher-wrap"),
                        html.Div(id="embed-wrap"),
                    ],
                    className="section-inner",
                ),
                className="pia-section",
                id="pia",
            ),

            html.Footer(
                html.Div(
                    "© Public Infrastructure Access \u00b7 The World Bank",
                    className="footer-inner",
                ),
                className="footer",
            ),
        ],
        className="app-shell",
    )


app.layout = build_layout


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------

@app.callback(
    Output("active-country-store", "data"),
    Input({"type": "country-select", "index": ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def set_active_country(_n_clicks):
    triggered = ctx.triggered_id
    if not triggered or not any(_n_clicks):
        raise dash.exceptions.PreventUpdate
    return triggered["index"]


@app.callback(
    Output("country-switcher-wrap", "children"),
    Input("active-country-store", "data"),
)
def render_switcher(active_country_id):
    return country_switcher(active_country_id)


@app.callback(
    Output("embed-wrap", "children"),
    Input("active-country-store", "data"),
)
def render_embed(active_country_id):
    url = pia_url_for(active_country_id)
    return embedded_frame(url, key=f"pia-{active_country_id}")


if __name__ == "__main__":
    app.run(debug=True)