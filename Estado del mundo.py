import plotly.express as px
import pandas as pd
import dash
from dash import dcc, html, Input, Output

#Cargamos los datos

#Datos Renzo
#df_cambioClimatico = pd.read_excel('C:/Users/Renzo/Documents/VS Code Repository/Estado-del-mundo-Proyecto-final-Visualizacion-de-informacion/Datos/1_climate-change.xlsx')
#df_precipitaciones = pd.read_excel('C:/Users/Renzo/Documents/VS Code Repository/Estado-del-mundo-Proyecto-final-Visualizacion-de-informacion/Datos/2_average-monthly-precipitation.xlsx')
#df_CO2 = pd.read_excel('C:/Users/Renzo/Documents/VS Code Repository/Estado-del-mundo-Proyecto-final-Visualizacion-de-informacion/Datos/3_co-emissions-per-capita.xlsx')
#df_gasesEfectoInvernadero = pd.read_excel('C:/Users/Renzo/Documents/VS Code Repository/Estado-del-mundo-Proyecto-final-Visualizacion-de-informacion/Datos/4_total-ghg-emissions-excluding-lufc.xlsx')
#df_poblacion = pd.read_excel('C:/Users/Renzo/Documents/VS Code Repository/Estado-del-mundo-Proyecto-final-Visualizacion-de-informacion/Datos/5_future-population-projections-by-country.xlsx')

#Datos Esteban
#df_cambioClimatico = pd.read_excel('Datos/1_climate-change.xlsx')
df_precipitaciones = pd.read_excel('Datos/2_average-monthly-precipitation.xlsx')
df_CO2 = pd.read_excel('Datos/3_co-emissions-per-capita.xlsx')
df_gasesEfectoInvernadero = pd.read_excel('Datos/4_total-ghg-emissions-excluding-lufc.xlsx')
df_poblacion = pd.read_excel('Datos/5_future-population-projections-by-country.xlsx')

#Para hacer el gráfico de dispersión con todos los datos, se deben meter todos los datos en un mismo dataframe
df_universal=pd.DataFrame([ 
    {#                                                _.-=/ Esta parte es para sacar los registros en un rango de 5 años \=-._                _.-=/ Aquí se hace el pegue por código \=-._                 v Para finalmente sacar el promedio del indicador
        'gasesEI':df_gasesEfectoInvernadero[df_gasesEfectoInvernadero['Año'].between(registro_poblacion['Año']-2,registro_poblacion['Año']+3)][df_gasesEfectoInvernadero['Código']==registro_poblacion['Código']]['Emisiones'].mean(),
        'CO2Percap':df_CO2[df_CO2['Año'].between(registro_poblacion['Año']-2,registro_poblacion['Año']+3)][df_CO2['Código']==registro_poblacion['Código']]['Emisiones'].mean(),
        'Precipitaciones':df_precipitaciones[df_precipitaciones['Año'].between(registro_poblacion['Año']-2,registro_poblacion['Año']+3)][df_precipitaciones['Código']==registro_poblacion['Código']]['Promedio mensual de precipitación'].mean(),
        'Año': registro_poblacion['Año'], 
        'Entidad': registro_poblacion['Entidad'], 
        'Código': registro_poblacion['Código'], 
        'Población': registro_poblacion['Población']
    }
    for i, registro_poblacion in df_poblacion.iterrows() 
    if (registro_poblacion['Código'] == df_precipitaciones['Código']).any() and (registro_poblacion['Código'] == df_CO2['Código']).any() and (registro_poblacion['Código'] == df_gasesEfectoInvernadero['Código']).any()  
])

#Se crean los gráficos
def generarGraficos(año):
    return\
        px.choropleth(df_poblacion[df_poblacion["Año"]==año],
            locations='Código',
            color='Población',
            height=700,
            hover_name='Entidad',
            color_continuous_scale='ylorrd',
            title="Gráfico de proyección de población por país"),\
        px.choropleth(df_CO2[df_CO2["Año"].between(año-2,año+3)].groupby(['Entidad','Código']).mean().reset_index(),
            locations='Código',
            color='Emisiones',
            height=700,
            hover_name='Entidad',
            color_continuous_scale=['green',"yellow",'orange','red'],
            title="Gráfico de emisiones de CO2 por país"),\
        px.choropleth(df_gasesEfectoInvernadero[df_gasesEfectoInvernadero["Año"].between(año-2,año+3)].groupby(['Entidad','Código']).mean().reset_index(),
            locations='Código',
            color='Emisiones',
            height=700,
            hover_name='Entidad',
            color_continuous_scale=['green',"yellow",'orange','red'],
            title="Gráfico de emisiones de gases de efecto invernadero por país"),\
        px.scatter_geo(df_precipitaciones[df_precipitaciones["Año"].between(año-2,año+3)].groupby(['Entidad','Código']).mean().reset_index(),
            locations='Código',
            height=700,
            hover_name='Entidad',
            size='Promedio mensual de precipitación',
            color='Promedio mensual de precipitación',
            color_continuous_scale=['lightblue','darkblue'],
            title="Gráfico de precipitación"),\
        px.scatter(df_universal[df_universal['Año']==año],
            size='Precipitaciones',
            color='Población',
            x='CO2Percap',
            y='gasesEI',
            height=700,
            hover_name='Entidad')

#Se crea la página
app = dash.Dash()
app.layout = html.Div([
    html.H1("El Estado del Mundo por año por país."),
    dcc.RangeSlider(
        id='rango_poblacion',
        min=1970,
        max=2100,
        step=5,
        value=[2015,2020]
    ),
    dcc.Graph(id='graficoPoblacion',figure=graficoPoblacion),
])

#Se crean los enlaces entre los componentes visuales y los datos visualizados
@app.callback(
    Output(component_id='graficoPoblacion', component_property='figure'),
    [Input(component_id='rango_poblacion', component_property='value')]
)
def actualizarGraficoPoblacion(rango):
    dff = df_poblacion.copy()
    dff = dff[dff["Year"].between(rango[0],rango[1])].groupby(['Entity','Code']).mean()
    dff.reset_index(inplace=True)
    return px.choropleth(dff,locations='Code',color='Population',hover_name='Entity')

if __name__=='__main__':
    app.run_server()