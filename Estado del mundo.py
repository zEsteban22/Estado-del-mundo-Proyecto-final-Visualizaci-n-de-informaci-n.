from math import inf
import plotly.express as px
import pandas as pd
import dash
from dash import html,dcc
import dash_bootstrap_components as dbc
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform

#Variables globales
_año=1990
listaPaisesVisibles=[]
listaPaisesInvisibles=[]

#Cargamos los datos

#Datos Renzo
#df_cambioClimatico = pd.read_excel('C:/Users/Renzo/Documents/VS Code Repository/Estado-del-mundo-Proyecto-final-Visualizacion-de-informacion/Datos/1_climate-change.xlsx')
#df_precipitaciones = pd.read_excel('C:/Users/Renzo/Documents/VS Code Repository/Estado-del-mundo-Proyecto-final-Visualizacion-de-informacion/Datos/2_average-monthly-precipitation.xlsx')
#df_CO2 = pd.read_excel('C:/Users/Renzo/Documents/VS Code Repository/Estado-del-mundo-Proyecto-final-Visualizacion-de-informacion/Datos/3_co-emissions-per-capita.xlsx')
#df_gasesEfectoInvernadero = pd.read_excel('C:/Users/Renzo/Documents/VS Code Repository/Estado-del-mundo-Proyecto-final-Visualizacion-de-informacion/Datos/4_total-ghg-emissions-excluding-lufc.xlsx')
#df_poblacion = pd.read_excel('C:/Users/Renzo/Documents/VS Code Repository/Estado-del-mundo-Proyecto-final-Visualizacion-de-informacion/Datos/5_future-population-projections-by-country.xlsx')
#df_continentes=pd.read_excel('C:/Users/Renzo/Documents/VS Code Repository/Estado-del-mundo-Proyecto-final-Visualizacion-de-informacion/Datos/6_paises-por-continente.xlsx')


#Datos Esteban
#df_cambioClimatico = pd.read_excel('Datos/1_climate-change.xlsx')
df_precipitaciones = pd.read_excel('Datos/2_average-monthly-precipitation.xlsx')
df_CO2 = pd.read_excel('Datos/3_co-emissions-per-capita.xlsx')
df_gasesEfectoInvernadero = pd.read_excel('Datos/4_total-ghg-emissions-excluding-lufc.xlsx')
df_poblacion = pd.read_excel('Datos/5_future-population-projections-by-country.xlsx')
df_continentes=pd.read_excel('Datos/6_paises-por-continente.xlsx')
df_continentes.ISO=df_continentes.ISO.apply(str).str.strip()
df_continentes.Continente=df_continentes.Continente.apply(str).str.strip()

#Para hacer el gráfico de dispersión con todos los datos, se deben meter todos los datos en un mismo dataframe

df_universal=pd.DataFrame([ 
    {#                                                _.-=/ Esta parte es para sacar los registros en un rango de 5 años \=-._                _.-=/ Aquí se hace el pegue por código \=-._                 v Para finalmente sacar el promedio del indicador
        'Gases de efecto invernadero':df_gasesEfectoInvernadero[df_gasesEfectoInvernadero['Año'].between(registro_poblacion['Año']-4,registro_poblacion['Año'])][df_gasesEfectoInvernadero['Código']==registro_poblacion['Código']]['Emisiones'].mean()/registro_poblacion['Población'],
        'Emisiones de CO2 per cápita':df_CO2[df_CO2['Año'].between(registro_poblacion['Año']-4,registro_poblacion['Año'])][df_CO2['Código']==registro_poblacion['Código']]['Emisiones'].mean(),
        'Precipitaciones':df_precipitaciones[df_precipitaciones['Año'].between(registro_poblacion['Año']-4,registro_poblacion['Año'])][df_precipitaciones['Código']==registro_poblacion['Código']]['Promedio mensual de precipitación'].mean(),
        'Año': registro_poblacion['Año'], 
        'Entidad': registro_poblacion['Entidad'], 
        'Código': registro_poblacion['Código'], 
        'Población': registro_poblacion['Población'],
        'Continente': df_continentes[df_continentes['ISO']==registro_poblacion['Código']]['Continente'].values[0]
    }
    for i, registro_poblacion in df_poblacion.iterrows() 
    if (registro_poblacion['Código'] == df_precipitaciones['Código']).any() and (registro_poblacion['Código'] == df_CO2['Código']).any() and (registro_poblacion['Código'] == df_gasesEfectoInvernadero['Código']).any()  
])
listaPaisesVisibles=df_universal['Entidad'].unique().tolist()

#Se crean los gráficos
def generarGraficos(año):
    df_temp=df_universal[df_universal['Año']==año]
    return \
        px.choropleth(df_temp,
            locations='Código',
            color='Población',
            height=700,
            hover_name='Entidad',
            color_continuous_scale='ylorrd',
            title="Gráfico de proyección de población por país"),\
        px.choropleth(df_temp,
            locations='Código',
            color='Emisiones de CO2 per cápita',
            height=700,
            hover_name='Entidad',
            color_continuous_scale=['green',"yellow",'orange','red'],
            title="Gráfico de emisiones de CO2 por país"),\
        px.choropleth(df_temp,
            locations='Código',
            color='Gases de efecto invernadero',
            height=700,
            hover_name='Entidad',
            color_continuous_scale=['green',"yellow",'orange','red'],
            title="Gráfico de emisiones de gases de efecto invernadero por país"),\
        px.scatter_geo(df_temp,
            locations='Código',
            height=700,
            hover_name='Entidad',
            size='Precipitaciones',
            color='Continente',
            title="Gráfico de precipitación"),\
        *otrosGraficos(df_temp)#,\
        #px.scatter(df_cambioClimatico[df_cambioClimatico['Día'].between_time(año-2,año+3)]['temperature_anomaly'].mean(),
        #    size=df_cambioClimatico[df_cambioClimatico['Día'].between_time(año-2,año+3)],
        #    color='temperature_anomaly',
        #    x='Día',
        #    y='temperature_anomaly',
        #    height=700,
        #    hover_name='Entidad'
        #)
def otrosGraficos(df_temp=None):
    if not isinstance(df_temp,pd.DataFrame):
        df_temp=df_universal[df_universal['Año']==_año]
    df_temp['contColor']=df_temp['Continente'].map({'Asia':2,'América':0,'Europa':1,'África':3,'Oceanía':4})
    return\
        px.scatter(df_temp[df_temp['Entidad'].isin(listaPaisesVisibles)],
            size='Población',
            color='Continente',
            x='Emisiones de CO2 per cápita',
            y='Gases de efecto invernadero',
            height=700,
            size_max=100,
            hover_name='Entidad'),\
        px.parallel_coordinates(df_temp[df_temp['Entidad'].isin(listaPaisesVisibles)],
            dimensions=['Población','Emisiones de CO2 per cápita','Gases de efecto invernadero','Precipitaciones'],
            height=700,
            color='contColor',
            color_continuous_scale=[(0.0, "red"),(1/5, "red"),
                                    (1/5, "yellow"),(2/5, "yellow"),
                                    (2/5, "green"),(3/5, "green"),
                                    (3/5, "cyan"),(4/5, "cyan"),
                                    (4/5, "blue"),(5/5, "blue")]
        )

def mostrarPaises():
    string=listaPaisesVisibles[0]
    for pais in listaPaisesVisibles[1:]:
        string+=', '+pais
    return string
#Se crea la página
app = DashProxy(external_stylesheets=[dbc.themes.BOOTSTRAP],transforms=[MultiplexerTransform()])
app.layout = dbc.Col([
    dcc.Interval(id="timer",disabled=True,interval=5000),
    html.H1("El Estado del Mundo por año por país.",style={'textAlign': 'center',"marginTop":"20px"}),
    html.Hr(),
    dcc.Slider(
                id='slider_años',
                min=1990,
                max=2015,
                step=5,
                marks={str(year): str(year) for year in range(1970,2020,5)},
                value=_año
            ),
    dcc.Graph(id='graficoPoblacion'),
    html.P("En este gráfico vemos como China y la India están muy por encima del resto de países del mundo, pero después de ellos se pueden apreciar a ciertos otros países con tonos más intensos que los de sus vecinos, como Estados Unidos, Brasil, Nigeria, Indonesia y Rusia "),
    dcc.Graph(id='graficoCO2'),
    html.P("En el gráfico anterior se puede apreciar una mayoría de países en tonos blancos y unos cuantos en tonos oscuros de amarillo los cuales son: Estados Unidos, Canadá, Omán, Kazajistán y Australia. Seguido de ellos, en tonos más azules se encuentran ciertos países árabes como lo son: Arabia Saudita, Emiratos Árabes Unidos y Kuwait, así como uno no árabe y que además se encuentra en América el cual es Trinidad y Tobago. Pero además casi imperseptible a simple vista debido a su pequeño territorio está el país con más emisiones de CO2 percápita del mundo: Qatar"),
    dcc.Graph(id='graficogasesEI'),
    html.P("Con la anterior visualización podemos apreciar cómo Estados Unidos lidera el ranking mundial de emisiones de gases de efecto invernadero, teniendo además ciertos países que le siguen relativamente de cerca: China, La India, Rusia y Brazil"),
    dcc.Graph(id='graficoPrecipitaciones'),
    html.P("Los países que se van a visualizar en los siguientes gráficos con los siguientes: "),
    html.P(id='paisesListados',children=mostrarPaises()),
    dcc.Graph(id='graficoDispersion'),
    html.P("En el siguiente gráfico América es de color azul, Europa es rojo, Asia amarillo, Oceanía cyan y África es verde"),
    dcc.Graph(id='graficoEjesParalelos')
], width={"size": 8, "offset": 2})#Disposición en pantalla como una sola columna ancha en el centro de la pantalla.
#Se crean los enlaces entre los componentes visuales y los datos visualizados
@app.callback(
    [    
        Output(component_id='graficoPoblacion', component_property='figure'),
        Output(component_id='graficoCO2', component_property='figure'),
        Output(component_id='graficogasesEI', component_property='figure'),
        Output(component_id='graficoPrecipitaciones', component_property='figure'),
        Output(component_id='graficoDispersion', component_property='figure'),
        Output(component_id='graficoEjesParalelos', component_property='figure'),
    ],
    [Input(component_id='slider_años', component_property='value')]
)
def actualizarRango(año):
    global _año
    _año=año
    return generarGraficos(año=año)

@app.callback(
    [
        Output('paisesListados', 'children'),
        Output(component_id='graficoDispersion', component_property='figure'),
        Output(component_id='graficoEjesParalelos', component_property='figure'),
    ],
    [
        Input('graficoPoblacion', 'selectedData'),
        Input('graficoCO2', 'selectedData'),
        Input('graficogasesEI', 'selectedData'),
        Input('graficoPrecipitaciones', 'selectedData')
    ]
)
def callback4(selectedData1,selectedData2,selectedData3,selectedData4):
    return [
        display_selected_data(selectedData1,selectedData2,selectedData3,selectedData4),
        *otrosGraficos(),
    ]
    
def display_selected_data(selectedData1,selectedData2,selectedData3,selectedData4):
    global listaPaisesInvisibles, listaPaisesVisibles
    listaPaisesInvisibles=df_universal['Entidad'].unique().tolist()
    listaPaisesVisibles=[]
    if [selectedData1,selectedData2,selectedData3,selectedData4]==[None,None,None,None]:
        listaPaisesVisibles=df_universal['Entidad'].unique().tolist()
        listaPaisesInvisibles=[]
    else:
        if selectedData1!=None:
            for data in selectedData1['points']:
                listaPaisesVisibles+=[data['hovertext']]
                if data['hovertext'] in listaPaisesInvisibles: listaPaisesInvisibles.remove(data['hovertext'])
        if selectedData2!=None:
            for data in selectedData2['points']:
                listaPaisesVisibles+=[data['hovertext']]
                if data['hovertext'] in listaPaisesInvisibles: listaPaisesInvisibles.remove(data['hovertext'])
        if selectedData3!=None:
            for data in selectedData3['points']:
                listaPaisesVisibles+=[data['hovertext']]
                if data['hovertext'] in listaPaisesInvisibles: listaPaisesInvisibles.remove(data['hovertext'])
        if selectedData4!=None:
            for data in selectedData4['points']:
                listaPaisesVisibles+=[data['hovertext']]
                if data['hovertext'] in listaPaisesInvisibles: listaPaisesInvisibles.remove(data['hovertext'])
    return mostrarPaises()
        


if __name__=='__main__':
    app.run_server()