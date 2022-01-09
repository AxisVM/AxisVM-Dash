# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
import plotly.graph_objects as go
import pandas as pd
from .utils import float_to_str_sig
from ..backend import dofs, id_to_label, label_to_id


__all__ = ['layout', 'gen_table_data']


AXISVM_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"


def input_res(**params):
    return html.Div(
        [
            html.P('Component'),
            dcc.Dropdown(
                id='component',
                options=[{'label': id_to_label[dof],
                          'value': id_to_label[dof]}
                         for dof in dofs],
                value='UZ'
            ),
        ]
    )


def input_mat(*args, material_names=None, **params):
    material = params['material']
    if material_names is None:
        material_names = [material,]
    return html.Div(
        [
            dcc.Dropdown(
                id='material',
                options=[{'label': m,
                          'value': m}
                         for m in material_names],
                value=material
            ),
        ]
    )


def input_geom(**params):
    Lx, Ly = params['size']
    t = params['thickness']
    return html.Div(
        [
            html.P("Side lengths" +
                   " in X and Y directions."),
            dbc.InputGroup(
                [
                    dbc.InputGroupText("Lx"),
                    dbc.Input(
                        id='Lx',
                        placeholder="Side length x",
                        type="number",
                        value=Lx),
                    dbc.InputGroupText("m"),
                ],
                className="mb-3",
            ),
            dbc.InputGroup(
                [
                    dbc.InputGroupText("Ly"),
                    dbc.Input(
                        id='Ly',
                        placeholder="Side length y",
                        type="number",
                        value=Ly),
                    dbc.InputGroupText("m"),
                ],
                className="mb-3",
            ),
            html.P("Thickness"),
            dbc.InputGroup(
                [
                    dbc.InputGroupText("t"),
                    dbc.Input(
                        id='t',
                        placeholder="thickness",
                        type="number",
                        value=t),
                    dbc.InputGroupText("m"),
                ],
                className="mb-3",
            ),
        ]
    )


def input_load(**params):
    xc = params['load']['xc']
    yc = params['load']['yc']
    w = params['load']['w']
    h = params['load']['h']
    q = params['load']['q']
    return html.Div(
        [
            html.P("Center of the patch" +
                   " in X and Y directions."),
            dbc.InputGroup(
                [
                    dbc.InputGroupText("xc"),
                    dbc.Input(
                        id='xc',
                        placeholder="x coordinate of center",
                        type="number",
                        value=xc),
                    dbc.InputGroupText("m"),
                ],
                className="mb-3",
            ),
            dbc.InputGroup(
                [
                    dbc.InputGroupText("yc"),
                    dbc.Input(
                        id='yc',
                        placeholder="y coordinate of center",
                        type="number",
                        value=yc),
                    dbc.InputGroupText("m"),
                ],
                className="mb-3",
            ),
            html.P("Width and height of the patch"),
            dbc.InputGroup(
                [
                    dbc.InputGroupText("w"),
                    dbc.Input(
                        id='w',
                        placeholder="width",
                        type="number",
                        value=w),
                    dbc.InputGroupText("m"),
                ],
                className="mb-3",
            ),
            dbc.InputGroup(
                [
                    dbc.InputGroupText("h"),
                    dbc.Input(
                        id='h',
                        placeholder="height",
                        type="number",
                        value=h),
                    dbc.InputGroupText("m"),
                ],
                className="mb-3",
            ),
            html.P("Load intensity"),
            dbc.InputGroup(
                [
                    dbc.InputGroupText("q"),
                    dbc.Input(
                        id='q',
                        placeholder="load intensity",
                        type="number",
                        value=q),
                    dbc.InputGroupText("kN/m2"),
                ],
                className="mb-3",
            ),
        ]
    )


def input_mesh(**params):
    meshsize = params['meshsize']
    return html.Div(
        [
            html.P("Mesh size"),
            dbc.InputGroup(
                [
                    dbc.Input(
                        id='meshsize',
                        type="number",
                        value=meshsize),
                    dbc.InputGroupText("m"),
                ],
                className="mb-3",
            ),
        ]
    )
    
    
def input_panel(**params):
    return html.Div(
        [
            dbc.Accordion(
                [
                    dbc.AccordionItem(
                        [
                            input_geom(**params),
                        ],
                        title="Geometry",
                    ),
                    dbc.AccordionItem(
                        [
                            input_mat(**params),
                        ],
                        title="Material",
                    ),
                    dbc.AccordionItem(
                        [
                            input_load(**params),
                        ],
                        title="Load",
                    ),
                    dbc.AccordionItem(
                        [
                            input_mesh(**params),
                        ],
                        title="Mesh",
                    ),
                    dbc.AccordionItem(
                        [
                            input_res(**params)
                        ],
                        title="Results",
                    ),
                ],
            ),
            html.Br(),
            dbc.Button(
                "Calculate",
                id='calc_button',
                color="primary"
            )
        ]
    )
    

def gen_table_data(*args, res2d=None, sig=6, atol=1e-10, **kwargs):
    def pprint(x): return float_to_str_sig(x, sig=sig, atol=atol)
    tbldata = []
    if res2d is not None:
        for comp, ind in label_to_id.items():
            tbldata.append([comp, 
                            pprint(res2d[ind].min()), 
                            pprint(res2d[ind].max())])
    else:
        for comp, ind in label_to_id.items():
            tbldata.append([comp, 'nan', 'nan'])
    return pd.DataFrame(tbldata, columns=['', 'min', 'max'])
    

def navigation_bar():
    nav_item = dbc.NavItem(dbc.NavLink("Link", href="#"))
    dropdown = dbc.DropdownMenu(
        children=[
            dbc.DropdownMenuItem("Entry 1"),
            dbc.DropdownMenuItem("Entry 2"),
            dbc.DropdownMenuItem(divider=True),
            dbc.DropdownMenuItem("Entry 3"),
        ],
        nav=True,
        in_navbar=True,
        label="Menu",
    )
    return dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=AXISVM_LOGO, height="30px")),
                            dbc.Col(dbc.NavbarBrand("AxisVM Dash", className="ms-2")),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="https://axisvm.eu",
                    style={"textDecoration": "none"},
                ),
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                dbc.Collapse(
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Input(type="search", placeholder="Search")
                            ),
                            dbc.Col(
                                dbc.Button(
                                    "Search", color="primary", className="ms-2"
                                ),
                                # set width of button column to auto to allow
                                # search box to take up remaining space.
                                width="auto",
                            ),
                            dbc.Col(
                                dbc.Nav(
                                    [nav_item, dropdown],
                                    className="ms-auto",
                                    navbar=True,
                                ),
                            )
                        ],
                        # add a top margin to make things look nice when the navbar
                        # isn't expanded (mt-3) remove the margin on medium or
                        # larger screens (mt-md-0) when the navbar is expanded.
                        # keep button and search box on same row (flex-nowrap).
                        # align everything on the right with left margin (ms-auto).
                        className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
                        align="center",
                    ),
                    
                    id="navbar-collapse",
                    navbar=True,
                ),
            ],
        ),
        color="dark",
        dark=True,
        className="mb-5",
    )


def layout(**params):
    # total width is 12 units
    table_data = gen_table_data(**params)
    columns=[{"name": i, "id": i} for i in table_data.columns]
    return html.Div(
        children =
            [
                navigation_bar(),
                
                html.Div([
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    input_panel(**params)
                                ],
                                width=3
                                ),
                            dbc.Col(
                                [
                                    dcc.Graph(id='plot', figure=go.Figure()),
                                    dash_table.DataTable(
                                        id='table', 
                                        data=table_data.to_dict('records'),
                                        columns=columns,
                                    ),
                                ],
                                width=9
                                ),
                        ]
                        ),
                    ], style={'padding': '0px 20px 20px 20px'}), # top, right, bottom, left
                ]
        )
