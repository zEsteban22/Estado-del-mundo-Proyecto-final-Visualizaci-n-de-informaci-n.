import plotly.express as px
import pandas as pd
import dash
from dash import dcc, html, Input, Output

#Cargamos los datos
#df_cambioClimatico = pd.read_excel('Datos/1_climate-change.xlsx')
#df_precipitaciones = pd.read_excel('Datos/2_average-monthly-precipitation.xlsx')
#df_CO2 = pd.read_excel('Datos/3_co-emissions-per-capita.xlsx')
#df_gasesEfectoInvernadero = pd.read_excel('Datos/4_total-ghg-emissions-excluding-lufc.xlsx')
df_poblacion = pd.read_excel('Datos/5_future-population-projections-by-country.xlsx')

#Se crean los gráficos                      
graficoPoblacion=px.choropleth(df_poblacion[df_poblacion["Year"]==2015],locations='Code',color='Population',hover_name='Entity')
#                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Esto es para que al inicio solo muestre las poblaciones de 2015
"""Con esto puede ver el excel desde acá
print(df_cambioClimatico)
print(df_precipitaciones)
print(df_CO2)
print(df_gasesEfectoInvernadero)
print(df_poblacion)
"""

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