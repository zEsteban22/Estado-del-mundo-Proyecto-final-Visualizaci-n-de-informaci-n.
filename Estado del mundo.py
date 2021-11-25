import plotly.express as px
import pandas as pd
import dash
from dash.dash_table import DataTable
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

# definición de variables para las animaciones
_año=2015
_añoFin=2020

#Cargamos los datos
#df_cambioClimatico = pd.read_excel('Datos/1_climate-change.xlsx')
df_precipitaciones = pd.read_excel('C:/Users/Renzo/Documents/VS Code Repository/Estado-del-mundo-Proyecto-final-Visualizacion-de-informacion/Datos/2_average-monthly-precipitation.xlsx')
df_CO2 = pd.read_excel('C:/Users/Renzo/Documents/VS Code Repository/Estado-del-mundo-Proyecto-final-Visualizacion-de-informacion/Datos/3_co-emissions-per-capita.xlsx')
df_gasesEfectoInvernadero = pd.read_excel('C:/Users/Renzo/Documents/VS Code Repository/Estado-del-mundo-Proyecto-final-Visualizacion-de-informacion/Datos/4_total-ghg-emissions-excluding-lufc.xlsx')
df_poblacion = pd.read_excel('C:/Users/Renzo/Documents/VS Code Repository/Estado-del-mundo-Proyecto-final-Visualizacion-de-informacion/Datos/5_future-population-projections-by-country.xlsx')

#Se crean los gráficos
graficoPoblacion=px.choropleth(df_poblacion[df_poblacion["Año"]==2015],locations='Código',color='Población',height=700,hover_name='Entidad',color_continuous_scale='ylorrd',title="Gráfico de proyección de población por país")

graficoCO2=px.choropleth(df_CO2[df_CO2["Año"]==2015],locations='Código',color='Emisiones',height=700,hover_name='Entidad',color_continuous_scale=['white',"yellow",'#0015FA','red'],title="Gráfico de emisiones de CO2 por país")

graficogasesEfectoInvernadero=px.choropleth(df_gasesEfectoInvernadero[df_gasesEfectoInvernadero["Año"]==2015],locations='Código',color='Emisiones',height=700,hover_name='Entidad',color_continuous_scale=["white",'yellow','blue'],title="Gráfico de emisiones de gases de efecto invernadero por país")

graficoPrecipitacion=px.scatter_geo(df_precipitaciones[df_precipitaciones["Año"]==2015],locations='Código',height=700,hover_name='Entidad', size='Promedio mensual de precipitación', color='Promedio mensual de precipitación', color_continuous_scale=['lightblue','darkblue'],title="Gráfico de precipitación")
#^Esto es para que al inicio solo muestre las poblaciones de 2015^

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
    dcc.Interval(id='interval1', interval=0, n_intervals=0),
    html.H1("El Estado del Mundo por año por país.",style={'textAlign': 'center',"marginTop":"20px"}),
    html.Hr(),
    dbc.Row([
        dbc.Col(html.Button("Play",id='play'),width=1),
        dbc.Col(
            dcc.RangeSlider(
                id='rango_poblacion',
                min=1970,
                max=2020,
                step=5,
                marks={str(year): str(year) for year in range(1970,2025,5)},
                value=[2015,2020]
            ))]),
    dcc.Graph(id='graficoPoblacion', figure=graficoPoblacion),
    html.P("En este gráfico vemos como China y la India están muy por encima del resto de países del mundo, pero después de ellos se pueden apreciar a ciertos otros países con tonos más intensos que los de sus vecinos, como Estados Unidos, Brasil, Nigeria, Indonesia y Rusia "),
    dcc.Graph(id='graficoCO2', figure=graficoCO2),
    html.P("En el gráfico anterior se puede apreciar una mayoría de países en tonos blancos y unos cuantos en tonos oscuros de amarillo los cuales son: Estados Unidos, Canadá, Omán, Kazajistán y Australia. Seguido de ellos, en tonos más azules se encuentran ciertos países árabes como lo son: Arabia Saudita, Emiratos Árabes Unidos y Kuwait, así como uno no árabe y que además se encuentra en América el cual es Trinidad y Tobago. Pero además casi imperseptible a simple vista debido a su pequeño territorio está el país con más emisiones de CO2 percápita del mundo: Qatar"),
    dcc.Graph(id='graficogasesEI', figure=graficogasesEfectoInvernadero),
    html.P("Con la anterior visualización podemos apreciar cómo China lidera el ranking mundial de emisiones de gases de efecto invernadero, teniendo además ciertos países que le siguen relativamente de cerca: Estados Unidos, La India, Rusia y Brazil"),
    dcc.Graph(id='graficoPrecipitaciones', figure=graficoPrecipitacion)
],width={"size": 8, "offset": 2})

#Se crean los enlaces entre los componentes visuales y los datos visualizados
@app.callback(
    Output(component_id='año',component_property='children'),
    [Input(component_id='rango_poblacion', component_property='value')]
)
def actualizarRango(rango):
    _año,_añoFin=rango
    play=False
    return str(rango[0])

@app.callback(
    Output(component_id='interval1',component_property='interval'),
    Input(component_id='play',component_property='n_clicks'),)
def iniciarAnimacion(cantidad_clicks):
    play=True
    return 5*1000
@app.callback(
    Output(component_id='interval1',component_property='interval'),
    Input(component_id='rango_poblacion',component_property='n_clicks'),)
def detenerAnimacion(cantidad_clicks):
    play=True
    return 5*1000

@app.callback(
    [
        Output(component_id='rango_poblacion',component_property="value"),
        Output(component_id='graficoPoblacion', component_property='figure'),
    ],
    [ Input(component_id='interval1',component_property='n_intervals') ]
    #faltan todos los demás gráficos y hasta el slider
)
def ejecutarAnimacion(año):
    if año >= _añoFin:
        play=False
    _año=año
    dff = df_poblacion.copy()
    ##FALTA ACTUALIZAR LOS OTROS GRÄFICOS
    dff = dff[dff["Year"].between(año,año+5)].groupby(['Entity','Code']).mean()
    dff.reset_index(inplace=True)
    return px.choropleth(dff,locations='Code',color='Population',hover_name='Entity',color_continuous_scale=["lightblue",'darkblue'],title="Grafico de población por país")

if __name__=='__main__':
    app.run_server()