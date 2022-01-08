# -*- coding: utf-8 -*-
from axisvm.com.client import start_AxisVM
from dewloosh.core.tools import float_to_str_sig
from src.backend.backend import build, generate_mesh, calculate, get_results
from src.frontend.components import fig2d, fig3d, input_mat, input_geom, \
    input_mesh, input_load, input_res
import dash_bootstrap_components as dbc
from dash import Dash as DashBoard, dcc, html, dash_table as dt
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np


axapp = start_AxisVM(visible=True, daemon=True)
app = DashBoard(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
timeout = 300


def pprint(x): return float_to_str_sig(x, sig=6, atol=1e-10)


dofs = UZ, ROTX, ROTY = list(range(3))
id_to_label = {UZ: 'UZ', ROTX: 'ROTX', ROTY: 'ROTY'}
label_to_id = {value: key for key, value in id_to_label.items()}
proj = '2d'


# inital parameters
params = {
    'material' : 'C16/20',
    'size' : (8., 6.),
    'thickness' : 0.2,
    'load' : {'xc' : 5., 'yc' : 4., 
              'w' : .5, 'h' : 1., 
              'q' : -2.0},
    'support' : {
        'left' : {'x' : 1e12, 'y' : 1e12, 'z' : 1e12, 
                  'xx' : 0, 'yy' : 0, 'zz' : 0},
        'right' : {'x' : 1e12, 'y' : 1e12, 'z' : 1e12, 
                   'xx' : 0, 'yy' : 0, 'zz' : 0},
        'top' : {'x' : 1e12, 'y' : 1e12, 'z' : 1e12, 
                 'xx' : 0, 'yy' : 0, 'zz' : 0},
        'bottom' : {'x' : 1e12, 'y' : 1e12, 'z' : 1e12, 
                    'xx' : 0, 'yy' : 0, 'zz' : 0}
        },
    'meshsize' : 0.6,
    'filename' : 'Modell.axs'
}


# initial solution
if proj == '3d':
    raise NotImplementedError
elif proj == '2d':
    build(axapp, **params)
    coords, _ = generate_mesh(axapp, **params)
    calculate(axapp, **params)
    res2d = get_results(axapp)

# figure
if proj == '3d':
    raise NotImplementedError
elif proj == '2d':
    fig = fig2d(coords, res2d[0, :], **params)


navigation_panel = html.Div(
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

# total width is 12 units
app.layout = html.Div([dbc.Container(
    dbc.Row([
        dbc.Col(
            [
                html.H1(children='AxisVM Dash'),
                html.P(
                    "An AxisVM dashboard.",
                    className="lead",
                ),
                navigation_panel
            ],
            width=3
        ),
        
        dbc.Col(
            [
                dcc.Graph(id='plot', figure=fig),
            ],
            width=9
        ),
    ]),
    fluid=True,
)])


@app.callback(
    Output('plot', 'figure'),
    Input('component', 'value')
)
def update_figure(comp):
    global res2d, params, coords
    dataId = label_to_id[comp]
    cmap = "Viridis"
    # figure
    if proj == '3d':
        raise NotImplementedError
    elif proj == '2d':
        fig = fig2d(coords, res2d[dataId, :], cmap=cmap, **params)
    return fig


@app.callback(
    Output('component', 'value'),
    Input('calc_button', 'n_clicks'),
    #geom
    State('Lx', 'value'),
    State('Ly', 'value'),
    State('t', 'value'),
    # material
    State('material', 'value'),
    # load
    State('xc', 'value'),
    State('yc', 'value'),
    State('w', 'value'),
    State('h', 'value'),
    State('q', 'value'),
    # mesh
    State('meshsize', 'value'),
    # results
    State('component', 'value'),
)
def recalc(n_clicks, Lx, Ly, t, material, xc, yc, w, h, q, meshsize, comp):
    global res2d, coords, params, axapp
    new_params = {
        'material' : material,
        'size' : (Lx, Ly),
        'thickness' : t,
        'load' : {'xc' : xc, 'yc': yc, 
                'w' : w, 'h': h, 'q' : q},
        'meshsize' : meshsize,
    }
    params.update(new_params)
    if proj == '3d':
        raise NotImplementedError
    elif proj == '2d':
        build(axapp, **params)
        coords, _ = generate_mesh(axapp, **params)
        calculate(axapp, **params)
        res2d = get_results(axapp)
    return comp


if __name__ == '__main__':
    try: 
        app.run_server(debug=True)
    finally:
        del axapp
    
