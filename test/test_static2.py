#!/usr/bin/env python
import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
import flask
import numpy as np

N = 1000
M = 500
xx = np.arange(N, dtype=np.float64)
yy = np.arange(M, dtype=np.float64)
x, y = np.meshgrid(xx, yy)
b = N/20.0
c = M/2.0
r = np.sqrt(((x-c)/b)**2 + ((y-c)/b)**2)
a = np.sin(r)

# Limits
xmin = xx[0]
xmax = xx[-1]
ymin = yy[0]
ymax = yy[-1]
amin = np.amin(a)
amax = np.amax(a)

from PIL import Image
from matplotlib import cm
from matplotlib.colors import Normalize

# Some normalization from matplotlib
cNorm = Normalize(vmin=amin, vmax=amax)
scalarMap  = cm.ScalarMappable(norm=cNorm, cmap='viridis' )
seg_colors = scalarMap.to_rgba(a) 
img = Image.fromarray(np.uint8(seg_colors*255))

import IPython
IPython.embed()

# Constants
img_width = 900
img_height = 600

# Now the plotly code
import plotly.graph_objects as go

# Create figure
fig = go.Figure()

# Add invisible scatter trace.
# This trace is added to help the autoresize logic work.
# We also add a color to the scatter points so we can have a colorbar next to our image
fig.add_trace(
    go.Scatter(
        x=[xmin, xmax],
        y=[ymin, ymax],
        mode="markers",
        marker={"color":[np.amin(a), np.amax(a)],
                "colorscale":'Viridis',
                "showscale":True,
                "colorbar":{"title":"Counts",
                            "titleside": "right"},
                "opacity": 0
               }
    )
)

# Add image
fig.update_layout(
    images=[go.layout.Image(
        x=xmin,
        sizex=xmax-xmin,
        y=ymax,
        sizey=ymax-ymin,
        xref="x",
        yref="y",
        opacity=1.0,
        layer="below",
        sizing="stretch",
        source=img)]
)

# Configure other layout
fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, range=[xmin, xmax]),
        yaxis=dict(showgrid=False, zeroline=False, range=[ymin, ymax]),
    width=img_width,
    height=img_height,
)

fig.show(config={'doubleClick': 'reset'})

server = flask.Flask('app')
app = dash.Dash('app', server=server)

app.layout = html.Div([
    html.H1('Static Image'),
    dcc.Graph(figure=fig)
], className="container")


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
