import pandas as pd
import plotly.graph_objects as go
# from dash import Dash
# from dash import dcc
# from dash import html
# from dash.dependencies import Input,Output
import dash_core_components as dcc
import dash_html_components as html
#from dash.dependencies import Input, Output
from dash import Dash, Input, Output
import plotly.express as px

airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

app=dash.Dash(__name__)
app.layout=html.Div(children=[
    html.H1("Flight Delay Time Statistics",style={'textAlign':'center','color':'#503D36','font-size':30}),
    html.Div('',dcc.Input(id='input-year',value=2010,type='number',style={'height':35,'font-size':30})),
    html.Br(),
    html.Br(),
    html.Div([
        html.Div(dcc.Graph(id='carrier-plot')),
        html.Div(dcc.Graph(id='weather-plot')),
    ],style={'display': 'flex'}),
    html.Div([
        html.Div(dcc.Graph(id='nas-plot')),
        html.Div(dcc.Graph(id='security-plot')),
    ],style={'display': 'flex'}),
    html.Div([
        html.Div([dcc.Graph(id='late-plot')],style={'width':'65%'}),
    ])


])

def compute_info(airline_data, entered_year):
    # Select data
    df =  airline_data[airline_data['Year']==int(entered_year)]
    # Compute delay averages
    avg_car = df.groupby(['Month','Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    avg_weather = df.groupby(['Month','Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    avg_NAS = df.groupby(['Month','Reporting_Airline'])['NASDelay'].mean().reset_index()
    avg_sec = df.groupby(['Month','Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    avg_late = df.groupby(['Month','Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()
    return avg_car, avg_weather, avg_NAS, avg_sec, avg_late

@app.callback( [
               Output(component_id='carrier-plot', component_property='figure'),
               Output(component_id='weather-plot', component_property='figure'),
               Output(component_id='nas-plot', component_property='figure'), 
               Output(component_id='security-plot', component_property='figure'),
               Output(component_id='late-plot', component_property='figure'),
               ],
               Input(component_id='input-year',component_property='value'))
# Computation to callback function and return graph
def get_graph(entered_year):
    
    # Compute required information for creating graph from the data
    avg_car, avg_weather, avg_NAS, avg_sec, avg_late = compute_info(airline_data, entered_year)
            
    # Line plot for carrier delay
    carrier_fig = px.line(avg_car, x='Month', y='CarrierDelay', color='Reporting_Airline', title='Average carrier delay time (minutes) by airline')
    # Line plot for weather delay
    weather_fig =px.line(avg_weather,x='Month',y='WeatherDelay',color='Reporting_Airline',title='Average weather delay')
    # Line plot for nas delay
    nas_fig = px.line(avg_NAS,x='Month',y='NASDelay',color='Reporting_Airline',title='Average nas delay')
    # Line plot for security delay
    sec_fig = px.line(avg_sec,x='Month',y='SecurityDelay',color='Reporting_Airline',title='Average security delay')
    # Line plot for late aircraft delay
    late_fig = px.line(avg_late,x='Month',y='LateAircraftDelay',color='Reporting_Airline',title='Average aircraft delay')
            
    return[carrier_fig, weather_fig, nas_fig, sec_fig, late_fig]
# Run the app
if __name__ == '__main__':
    app.run_server()