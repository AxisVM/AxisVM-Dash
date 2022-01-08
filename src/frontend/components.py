# -*- coding: utf-8 -*-
import plotly.figure_factory as ff
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
import plotly.figure_factory as ff
import plotly.graph_objects as go

__all__ = ['fig3d', 'fig2d', 'input_mat', 'input_load', 'input_res',
           'input_geom', 'input_mesh']

dofs = UZ, ROTX, ROTY = list(range(3))
id_to_label = {UZ: 'UZ', ROTX: 'ROTX', ROTY: 'ROTY'}


def fig3d(coords, triangles, res2d, cmap="Viridis", **params):
    Lx = params['Lx']
    Ly = params['Ly']
    aspects = {'x': 1.0, 'y': Ly/Lx, 'z': 1.0}
    fig = ff.create_trisurf(x=coords[:, 0], y=coords[:, 1], z=coords[:, 2],
                            simplices=triangles, color_func=res2d,
                            colormap=cmap, title='',
                            aspectratio=aspects, showbackground=True)
    fig.update_layout(transition_duration=500,
                      scene=dict(
                          annotations=[
                              dict(
                                  showarrow=False,
                                  x=0.,
                                  y=0.,
                                  z=0.,
                                  text="A",
                                  xanchor="left",
                                  font=dict(
                                      color="black",
                                      size=20
                                  ),
                              ),
                              dict(
                                  showarrow=False,
                                  x=Lx,
                                  y=0.,
                                  z=0.,
                                  text="B",
                                  xanchor="left",
                                  font=dict(
                                      color="black",
                                      size=20
                                  ),
                              ),
                              dict(
                                  showarrow=False,
                                  x=Lx,
                                  y=Ly,
                                  z=0.,
                                  text="C",
                                  xanchor="left",
                                  font=dict(
                                      color="black",
                                      size=20
                                  ),
                              ),
                              dict(
                                  showarrow=False,
                                  x=0.,
                                  y=Ly,
                                  z=0.,
                                  text="D",
                                  xanchor="left",
                                  font=dict(
                                      color="black",
                                      size=20
                                  ),
                              ),
                          ]
                      )
                      )
    return fig


def fig2d(coords, res2d, **params):
    zmin = res2d.min()
    zmax = res2d.max()
    fig = go.Figure(data=go.Contour(
        x=coords[:, 0],
        y=coords[:, 1],
        z=res2d,
        zmin=zmin, zmax=zmax
    ))
    fig['layout']['yaxis']['scaleanchor'] = 'x'
    return fig


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
