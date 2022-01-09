# -*- coding: utf-8 -*-
from axisvm.com.client import start_AxisVM
from dewloosh.core.tools import float_to_str_sig
from src.backend.backend import build, generate_mesh, calculate, get_results
from src.frontend.components import input_panel
from src.frontend.plotting import fig2d, fig3d
import dash_bootstrap_components as dbc
from dash import Dash as DashBoard, dcc, html, dash_table as dt
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from queue import Queue
from threading import Thread

#comtypes.CoUninitialize()
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
    'filename' : 'Modell222.axs'
}


coords, res2d = None, None
_sentinel = object()


def solver(in_queue, out_queue):
    import comtypes
    comtypes.CoInitialize()
    axapp = start_AxisVM(visible=True, daemon=True)
    while True:
        # Get data
        in_data = in_queue.get()
        if in_data is _sentinel:
            break
        print('New Problem!')
        
        # Process data
        axapp.Models.New()  # cleans everything up
        axmodel = axapp.Models[1]
        build(axapp=axapp, axmodel=axmodel, **in_data)
        coords, _ = generate_mesh(axmodel=axmodel, **in_data)
        calculate(axmodel=axmodel, **in_data)
        res2d = get_results(axmodel=axmodel)
        
        # Mark task as solved, optional
        print('Problem Solved!')
        in_queue.task_done()
        
        # Forward result to plotter
        out_queue.put((in_data, coords, res2d))
        print('Results Put!')

        
solver_queue, plotter_queue = Queue(), Queue()
solver_thread = Thread(target=solver, args=(solver_queue, plotter_queue))


# total width is 12 units
app.layout = html.Div([dbc.Container(
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
    global plotter_queue, params, coords, res2d
    if plotter_queue.qsize() > 0:
        params, coords, res2d = plotter_queue.get()        
    dataId = label_to_id[comp]
    fig = fig2d(coords, res2d[dataId, :], cmap="Viridis", **params)
    print('{} Plotted!'.format(comp))
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
def recalc(n_clicks, Lx, Ly, t, material, 
           xc, yc, w, h, q, meshsize, comp):
    global params, solver_queue
    new_params = {
        'material' : material,
        'size' : (Lx, Ly),
        'thickness' : t,
        'load' : {'xc' : xc, 'yc': yc, 
                'w' : w, 'h': h, 'q' : q},
        'meshsize' : meshsize,
    }
    params.update(new_params)
    solver_queue.put(params)
    return comp


if __name__ == '__main__':
    solver_thread.start()
    app.run_server(debug=False)
    solver_queue.put(_sentinel)
    solver_queue.join() 
    plotter_queue.join()
