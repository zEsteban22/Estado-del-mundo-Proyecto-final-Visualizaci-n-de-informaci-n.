import plotly.express as px
import pandas as pd
import dash
from dash import dcc
from dash import html
# read by default 1st sheet of an excel file
dataframe1 = pd.read_excel('Datos/1_climate-change.xlsx')
 
print(dataframe1)