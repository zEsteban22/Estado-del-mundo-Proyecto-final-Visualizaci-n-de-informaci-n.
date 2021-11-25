import plotly.express as px
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
#Cargamos los datos
#df_cambioClimatico = pd.read_excel('Datos/1_climate-change.xlsx')
#df_precipitaciones = pd.read_excel('Datos/2_average-monthly-precipitation.xlsx')
df_CO2 = pd.read_excel('C:/Users/Renzo/Documents/VS Code Repository/Estado-del-mundo-Proyecto-final-Visualizacion-de-informacion/Datos/3_co-emissions-per-capita.xlsx')
df_gasesEfectoInvernadero = pd.read_excel('C:/Users/Renzo/Documents/VS Code Repository/Estado-del-mundo-Proyecto-final-Visualizacion-de-informacion/Datos/4_total-ghg-emissions-excluding-lufc.xlsx')
df_poblacion = pd.read_excel('C:/Users/Renzo/Documents/VS Code Repository/Estado-del-mundo-Proyecto-final-Visualizacion-de-informacion/Datos/5_future-population-projections-by-country.xlsx')

#Se crean los gráficos                      
graficoPoblacion=px.choropleth(df_poblacion[df_poblacion["Año"]==2015],locations='Código',color='Población',hover_name='Entidad',color_continuous_scale='ylorrd',title="Grafico de población por país",)
graficoCO2=px.choropleth(df_CO2[df_CO2["Year"]==2015],locations='Code',color='emisiones',hover_name='Entity',color_continuous_scale=["yellow",'blue','red'],title="Grafico de emisiones de CO2 por país",)
graficogasesEfectoInvernadero=px.choropleth(df_gasesEfectoInvernadero[df_gasesEfectoInvernadero["Year"]==2015],locations='Code',color='emisiones',hover_name='Entity',color_continuous_scale=["white",'yellow','blue'],title="Grafico de emisiones de gases de efecto invernadero  por país",)
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
    html.H1("El Estado del Mundo por año por país.",style={'textAlign': 'center',"marginTop":"20px"}),
    html.Hr(),
    dbc.Row([
        dbc.Col(html.Button("Play"),width=1),
        dbc.Col(
            dcc.RangeSlider(
                id='rango_poblacion',
                min=1970,
                max=2100,
                step=5,
                value=[2015,2020]
            ))]),
    html.H2("2015",id="año",style={'textAlign': 'center'}),
    dcc.Graph(id='graficoPoblacion',figure=graficoPoblacion),
    html.P("jaksjkasjfd"),
    dcc.Graph(id='graficoCO2',figure=graficoCO2),
    html.P("jaksjkasjfd"),
    dcc.Graph(id='graficogasesEI',figure=graficogasesEfectoInvernadero),
    html.P("jaksjkasjfd"),
],width={"size": 6, "offset": 3})


"""
#Se crean los enlaces entre los componentes visuales y los datos visualizados
@app.callback(
    [Output(component_id='graficoPoblacion', component_property='figure'),
    Output(component_id='año',component_property='children')],
    [Input(component_id='rango_poblacion', component_property='value')]
)
def actualizarGraficoPoblacion(rango):
    dff = df_poblacion.copy()
    dff = dff[dff["Year"].between(rango[0],rango[1])].groupby(['Entity','Code']).mean()
    dff.reset_index(inplace=True)
    return px.choropleth(dff,locations='Code',color='Population',hover_name='Entity',color_continuous_scale=["lightblue",'darkblue'],title="Grafico de población por país"),str(rango[0])
"""
if __name__=='__main__':
    app.run_server()