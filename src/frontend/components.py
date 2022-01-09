# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
import plotly.graph_objects as go
import pandas as pd
from .utils import float_to_str_sig
from ..backend import dofs, id_to_label, label_to_id


__all__ = ['layout', 'gen_table_data']


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


def input_mat(**params):
    material = params['material']
    return html.Div(
        [
            dbc.InputGroup(
                [
                    dbc.Input(
                        id='material',
                        placeholder="material",
                        type="text",
                        value=material),
                ],
                className="mb-3",
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
                    dbc.InputGroupText("kN/cm2"),
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
    

def layout(**params):
    # total width is 12 units
    table_data = gen_table_data(**params)
    columns=[{"name": i, "id": i} for i in table_data.columns]
    return html.Div([dbc.Container(
        dbc.Row([
            # left column
            dbc.Col(
                [
                    html.H1(children='AxisVM Dash'),
                    html.P(
                        "An AxisVM dashboard.",
                        className="lead",
                    ),
                    input_panel(**params)
                ],
                width=3
            ),
            # right column
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
        ]),
        fluid=True,
    )])
