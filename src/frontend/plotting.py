# -*- coding: utf-8 -*-
import plotly.figure_factory as ff
import plotly.graph_objects as go


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
    fig['layout']['xaxis']['showticklabels'] = False
    fig['layout']['yaxis']['scaleanchor'] = 'x'
    fig['layout']['yaxis']['showticklabels'] = False
    fig['layout']['paper_bgcolor']= 'white'
    fig['layout']['plot_bgcolor'] = 'white'
    return fig