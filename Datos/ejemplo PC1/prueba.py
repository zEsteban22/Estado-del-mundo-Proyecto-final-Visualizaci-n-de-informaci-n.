import plotly.express as px
import pandas as pd
import json
from math import log
import dash
from dash import dcc
from dash import html
with open("data.json") as doc:
    l = json.load(doc)['data']
    for i in range(len(l)):
        l[i].update(val=log(l[i]['Trade Value'], 2))
    df = pd.DataFrame(l)

colorDiscreteMap = {
    "Animal Products": "rgba(170,100, 57,1)",
    "Vegetable Products": "rgba( 45,134, 50,1)",
    "Animal and Vegetable Bi-Products": "rgba(170,170, 57,1)",
    "Foodstuffs": "rgba(155, 52, 78,1)",
    "Mineral Products": "rgba( 35, 98,103,1)",
    "Chemical Products": "rgba(108, 37,111,1)",
    "Plastics and Rubbers": "rgba( 51, 53,119,1)",
    "Animal Hides": "rgba(144,164, 55,1)",
    "Wood Products": "rgba( 35,100,103,1)",
    "Paper Goods": "rgba(  0,157,141,1)",
    "Textiles": "rgba( 62, 52, 35,1)",
    "Footwear and Headwear": "rgba( 38, 89,106,1)",
    "Stone And Glass": "rgba( 88,145,163,1)",
    "Precious Metals": "rgba(149, 75,  0,1)",
    "Metals": "rgba(149, 11,  0,1)",
    "Machines": "rgba( 31,  9,103,1)",
    "Transportation": "rgba(123,159, 53,1)",
    "Instruments": "rgba(170,169, 57,1)",
    "Weapons": "rgba( 77, 45,115,1)",
    "Miscellaneous": "rgba(103, 65, 64,1)",
    "Arts and Antiques": "rgba(151, 50, 83,1)"
}
sunburstFig = px.sunburst(df, path=['Year', 'Section', 'HS2', 'HS4'],
                          color='val', color_continuous_scale='rdbu',
                          title="Gráfico radial",
                          width=1400, height=800)
sunburstFig.update_layout(
    font_family="Verdana",
    font_color="blue",
    title_font_family="Times New Roman",
    legend_title_font_color="black"
)
treemapFig = px.icicle(df, path=['Year', 'Section', 'HS2', 'HS4'],
                       color='Section', values='Trade Value', title="Gráfico de icicle hacia la derecha.",
                       color_discrete_map=colorDiscreteMap,
                       width=1400, height=800)
treemapFig.update_layout(
    font_family="Verdana",
    font_color="blue",
    title_font_family="Times New Roman",
    legend_title_font_color="black"
)


icicleFig = px.icicle(df, path=['Year', 'Section', 'HS2', 'HS4'],
                      color='Section', values='Trade Value', color_discrete_map=colorDiscreteMap,
                      title="Gráfico de icicle hacia abajo.",
                      width=1400, height=800)
icicleFig.update_traces(tiling=dict(orientation='v'))
icicleFig.update_layout(
    font_family="Verdana",
    font_color="blue",
    title_font_family="Times New Roman",
    legend_title_font_color="black"
)
app = dash.Dash()
app.layout = html.Div([
    html.H1("Gráficos de las exportaciones ticas en el año 2019 generados por la liberaría plotly de python"),
    dcc.Graph(figure=sunburstFig),
    dcc.Graph(figure=treemapFig),
    dcc.Graph(figure=icicleFig)
])

app.run_server()
