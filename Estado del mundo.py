from math import inf
import plotly.express as px
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

# definición de variables para las animaciones
_año=1990
_añoFin=2020

#Cargamos los datos
#df_cambioClimatico = pd.read_excel('Datos/1_climate-change.xlsx')
df_precipitaciones = pd.read_excel('Datos/2_average-monthly-precipitation.xlsx')
df_CO2 = pd.read_excel('Datos/3_co-emissions-per-capita.xlsx')
df_gasesEfectoInvernadero = pd.read_excel('Datos/4_total-ghg-emissions-excluding-lufc.xlsx')
df_poblacion = pd.read_excel('Datos/5_future-population-projections-by-country.xlsx')

#Se crean los gráficos
def generarGraficos(año):
    return \
        px.choropleth(df_poblacion[df_poblacion["Año"]==año],locations='Código',color='Población',height=700,hover_name='Entidad',color_continuous_scale='ylorrd',title="Gráfico de proyección de población por país"),\
        px.choropleth(df_CO2[df_CO2["Año"]==año],locations='Código',color='Emisiones',height=700,hover_name='Entidad',color_continuous_scale=['white',"yellow",'#0015FA','red'],title="Gráfico de emisiones de CO2 por país"),\
        px.choropleth(df_gasesEfectoInvernadero[df_gasesEfectoInvernadero["Año"]==año],locations='Código',color='Emisiones',height=700,hover_name='Entidad',color_continuous_scale=["white",'yellow','lightblue','#0015FA'],title="Gráfico de emisiones de gases de efecto invernadero por país"),\
        px.scatter_geo(df_precipitaciones[df_precipitaciones["Año"]==_año],locations='Código',height=700,hover_name='Entidad', size='Promedio mensual de precipitación', color='Promedio mensual de precipitación', color_continuous_scale=['lightblue','darkblue'],title="Gráfico de precipitación"),\

#Se crea la página
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Col([
    html.H1("El Estado del Mundo por año por país.",style={'textAlign': 'center',"marginTop":"20px"}),
    html.Hr(),
    dcc.RangeSlider(
                id='rango_poblacion',
                min=1990,
                max=2020,
                step=None,
                marks={str(year): str(year) for year in range(1970,2025,5)},
                value=[_año,2020]
            ),
    html.H2("1990",id="año",style={'textAlign': 'center',"marginTop":"20px"}),
    dcc.Graph(id='graficoPoblacion'),
    html.P("En este gráfico vemos como China y la India están muy por encima del resto de países del mundo, pero después de ellos se pueden apreciar a ciertos otros países con tonos más intensos que los de sus vecinos, como Estados Unidos, Brasil, Nigeria, Indonesia y Rusia "),
    dcc.Graph(id='graficoCO2'),
    html.P("En el gráfico anterior se puede apreciar una mayoría de países en tonos blancos y unos cuantos en tonos oscuros de amarillo los cuales son: Estados Unidos, Canadá, Omán, Kazajistán y Australia. Seguido de ellos, en tonos más azules se encuentran ciertos países árabes como lo son: Arabia Saudita, Emiratos Árabes Unidos y Kuwait, así como uno no árabe y que además se encuentra en América el cual es Trinidad y Tobago. Pero además casi imperseptible a simple vista debido a su pequeño territorio está el país con más emisiones de CO2 percápita del mundo: Qatar"),
    dcc.Graph(id='graficogasesEI'),
    html.P("Con la anterior visualización podemos apreciar cómo China lidera el ranking mundial de emisiones de gases de efecto invernadero, teniendo además ciertos países que le siguen relativamente de cerca: Estados Unidos, La India, Rusia y Brazil"),
    dcc.Graph(id='graficoPrecipitaciones')
], width={"size": 8, "offset": 2})#Disposición en pantalla como una sola columna ancha en el centro de la pantalla.

#Se crean los enlaces entre los componentes visuales y los datos visualizados
@app.callback(
    [    
        Output('año','children'),
        Output(component_id='graficoPoblacion', component_property='figure'),
        Output(component_id='graficoCO2', component_property='figure'),
        Output(component_id='graficogasesEI', component_property='figure'),
        Output(component_id='graficoPrecipitaciones', component_property='figure')],
        #Output(component_id='graficoDispersion', component_property='figure'),
    [Input(component_id='rango_poblacion', component_property='value')]
)
def actualizarRango(rango):
    return str(rango[0]),generarGraficos(rango[0])

if __name__=='__main__':
    app.run_server()