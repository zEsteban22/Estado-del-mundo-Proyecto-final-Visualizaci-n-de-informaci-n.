from math import inf
import plotly.express as px
import pandas as pd
import dash
from dash.dash_table import DataTable
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

# definición de variables para las animaciones
_año=1990
_añoFin=2020

#Cargamos los datos
#df_cambioClimatico = pd.read_excel('Datos/1_climate-change.xlsx')
#df_precipitaciones = pd.read_excel('Datos/2_average-monthly-precipitation.xlsx')
df_CO2 = pd.read_excel('Datos/3_co-emissions-per-capita.xlsx')
df_gasesEfectoInvernadero = pd.read_excel('Datos/4_total-ghg-emissions-excluding-lufc.xlsx')
df_poblacion = pd.read_excel('Datos/5_future-population-projections-by-country.xlsx')

#Se crean los gráficos                      
graficoPoblacion=px.choropleth(df_poblacion[df_poblacion["Year"]==_año],locations='Code',color='Población',height=700,hover_name='Entity',color_continuous_scale='ylorrd',title="Grafico de población por país",)
graficoCO2=px.choropleth(df_CO2[df_CO2["Year"]==_año],locations='Code',color='Emisiones',height=700,hover_name='Entity',color_continuous_scale=['white',"yellow",'#0015FA','red'],title="Grafico de Emisiones de CO2 por país",)
graficogasesEfectoInvernadero=px.choropleth(df_gasesEfectoInvernadero[df_gasesEfectoInvernadero["Year"]==_año],locations='Code',color='Emisiones',height=700,hover_name='Entity',color_continuous_scale=["white",'yellow','lightblue','#0015FA'],title="Grafico de Emisiones de gases de efecto invernadero por país",)
#                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Esto es para que al inicio solo muestre las poblaciones de 2015
"""Con esto puede ver el excel desde acá
#print(df_cambioClimatico)
#print(df_precipitaciones)
print(df_CO2)
print(df_gasesEfectoInvernadero)
print(df_poblacion)
"""
#Se crea la página
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Col([
    dcc.Interval(id='interval1', interval=0, n_intervals=inf),
    html.H1("El Estado del Mundo por año por país.",style={'textAlign': 'center',"marginTop":"20px"}),
    html.Hr(),
    dbc.Row([
        dbc.Col(html.Button("Play",id='play'),width=1),
        dbc.Col(
            dcc.RangeSlider(
                id='rango_poblacion',
                min=1990,
                max=2020,
                step=5,
                marks={str(year): str(year) for year in range(1970,2025,5)},
                value=[_año,2020]
            ))]),
    dcc.Graph(id='graficoPoblacion',figure=graficoPoblacion),
    html.P("En este gráfico vemos como China y la India están muy por encima del resto de países del mundo, pero después de ellos se pueden apreciar a ciertos otros países con tonos más intensos que los de sus vecinos, como Estados Unidos, Brasil, Nigeria, Indonesia y Rusia "),
    dcc.Graph(id='graficoCO2',figure=graficoCO2),
    html.P("En el gráfico anterior se puede apreciar una mayoría de países en tonos blancos y unos cuantos en tonos oscuros de amarillo los cuales son: Estados Unidos, Canadá, Omán, Kazajistán y Australia. Seguido de ellos, en tonos más azules se encuentran ciertos países árabes como lo son: Arabia Saudita, Emiratos Árabes Unidos y Kuwait, así como uno no árabe y que además se encuentra en América el cual es Trinidad y Tobago. Pero además casi imperseptible a simple vista debido a su pequeño territorio está el país con más Emisiones de CO2 percápita del mundo: Qatar"),
    dcc.Graph(id='graficogasesEI',figure=graficogasesEfectoInvernadero),
    html.P("Con la anterior visualización podemos apreciar cómo China lidera el ranking mundial de Emisiones de gases de efecto invernadero, teniendo además ciertos países que le siguen relativamente de cerca: Estados Unidos, La India, Rusia y Brazil"),
],width={"size": 8, "offset": 2})



#Se crean los enlaces entre los componentes visuales y los datos visualizados

@app.callback(
    Output(component_id='interval1',component_property='interval'),
    [Input(component_id='rango_poblacion', component_property='value')]
)
def actualizarRango(rango):
    _año,_añoFin=rango
    print(rango)
    play=False
    return inf

@app.callback(
    Output(component_id='interval1',component_property='interval'),
    Input(component_id='play',component_property='n_clicks'),)
def iniciarAnimacion(cantidad_clicks):
    print("iniciar")
    play=True
    return 5*1000


@app.callback(
    [
        Output(component_id='interval1',component_property='interval'),
        Output(component_id='rango_poblacion',component_property="value"),
        Output(component_id='graficoPoblacion', component_property='figure'),
    ],
    [ Input(component_id='interval1',component_property='n_intervals') ]
    #faltan todos los demás gráficos y hasta el slider
)
def ejecutarAnimacion(n_interval):
    global _año
    print("hola")    
    _año+=5
    dff = df_poblacion.copy()
    ##FALTA ACTUALIZAR LOS OTROS GRÄFICOS
    dff = dff[dff["Year"].between(_año,_año+5)].groupby(['Entity','Code']).mean()
    dff.reset_index(inplace=True)
    return (5000 if _año + 5 >= _añoFin else inf), [_año,_añoFin], px.choropleth(dff,locations='Code',color='Population',hover_name='Entity',color_continuous_scale=["lightblue",'darkblue'],title="Grafico de población por país")


if __name__=='__main__':
    app.run_server()