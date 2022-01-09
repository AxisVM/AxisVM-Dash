# -*- coding: utf-8 -*-
from src.backend import solver, Sentinel, label_to_id
from src.frontend import layout, fig2d
import dash_bootstrap_components as dbc
from dash import Dash
from dash.dependencies import Input, Output, State
from queue import Queue
from threading import Thread
import plotly.graph_objects as go


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


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = layout(**params)
server = app.server
timeout = 300
coords, res2d = None, None
solver_queue, plotter_queue = Queue(), Queue()
solver_thread = Thread(target=solver, args=(solver_queue, plotter_queue))


@app.callback(
    Output('plot', 'figure'),
    Input('component', 'value')
)
def update_figure(comp):
    global plotter_queue, params, coords, res2d
    if plotter_queue.qsize() > 0:
        params, coords, res2d = plotter_queue.get()
    if res2d is not None:        
        dataId = label_to_id[comp]
        fig = fig2d(coords, res2d[dataId, :], cmap="Viridis", **params)
        print('{} Plotted!'.format(comp))
        return fig
    return go.Figure()


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
    solver_queue.put(Sentinel())
    solver_thread.join()
