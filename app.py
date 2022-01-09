# -*- coding: utf-8 -*-
from src.backend import solver, Sentinel, \
    label_to_id, id_to_label
from src.frontend import layout, fig2d, gen_table_data
import dash
import dash_bootstrap_components as dbc
from dash import Dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
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
    'filename' : 'DashModel.axs'
}


coords, res2d, plot_id = None, None, None
solver_queue, plotter_queue = Queue(), Queue()
material_names = []
solver_thread = Thread(target=solver, 
                       args=(solver_queue, plotter_queue, 
                             material_names),
                       kwargs={'visible' : False})
solver_thread.start()
solver_queue.put(params)
while plotter_queue.qsize() == 0:
    pass
params, coords, res2d = plotter_queue.get()


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
timeout = 300  # I use a large value here to give AxiVM enough time to wake up
app.layout = layout(material_names=material_names, **params)


@app.callback(
    Output('plot', 'figure'),
    Output('table', 'data'),
    Input('component', 'value')
)
def update(comp):
    global params, coords, res2d, plot_id
    if coords is not None and res2d is not None:        
        plot_id = label_to_id[comp]
        fig = fig2d(coords, res2d[plot_id, :], cmap="Viridis", **params)
    else:
        fig = go.Figure()
    table_data = gen_table_data(res2d=res2d, **params)
    return fig, table_data.to_dict('records')


@app.callback(
    Output('component', 'value'),
    Input('calc_button', 'n_clicks'),
    Input('table', 'active_cell'),
    # geom
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
    prevent_initial_call=True    
)
def recalc(n_clicks, active_cell, Lx, Ly, t, material, 
           xc, yc, w, h, q, meshsize, comp):
    
    # determine wich input fired
    ctx = dash.callback_context
    if not ctx.triggered:
        # we can get here from initial render
        pass
    else:
        ctx_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if ctx_id == 'table':
        # the user clicked on the table
        global plot_id
        if active_cell['row'] == plot_id:
            # no need to update plot
            raise PreventUpdate
        comp = id_to_label[active_cell['row']]
        return comp
    
    # if we are here, the user clicked on 'Calculate'
    global params, solver_queue, plotter_queue, coords, res2d
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
    while plotter_queue.qsize() == 0:
        pass
    params, coords, res2d = plotter_queue.get()
    return comp


if __name__ == '__main__':
    app.run_server(debug=False)
    solver_queue.put(Sentinel())
    solver_thread.join()
