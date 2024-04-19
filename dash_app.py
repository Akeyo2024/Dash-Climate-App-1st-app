import pandas as pd 
import dash
from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output, State
import plotly.express as px
from dash import dash_table
import dash_bootstrap_components as dbc



df_NewYork = pd.read_csv('weather_forcast_newyork.csv')

#table
table = dash_table.DataTable(df_NewYork.to_dict('records'),
                                  [{"name": i, "id": i} for i in df_NewYork.columns],
                               style_data={'color': 'white','backgroundColor': "#222222"},
                              style_header={
                                  'backgroundColor': 'rgb(210, 210, 210)',
                                  'color': 'black','fontWeight': 'bold'}, 
                                     style_table={ 
                                         'minHeight': '400px', 'height': '400px', 'maxHeight': '400px',
                                         'minWidth': '900px', 'width': '900px', 'maxWidth': '900px',
                                         'marginLeft': 'auto', 'marginRight': 'auto',
                                         'marginTop': 0, 'marginBottom': "30"}
                                     )

#Bar graph

fig1 = px.bar(df_NewYork, 
              x="month", 
              y=["avg_temp_per_month", "avg_chance_of_rain_per_month"],
              barmode="group", 
              title="Average Temperature and Chance of Rain Per Month", height=500, width=1100)

fig1 = fig1.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white", 
    #margin=dict(l=20, r=20, t=0, b=20)
)
    

graph1 = dcc.Graph(figure=fig1)


#Line graph
fig2 = px.line(df_NewYork, x="month", y=["avg_temp_per_month", "avg_chance_of_rain_per_month"], 
              title="Average Temperature and Chance of Rain Per Month for New York 2023", height=500, width=1100, markers=True)
fig2 = fig2.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )
graph2 = dcc.Graph(figure=fig2)

#Map
fig3 = px.choropleth(df_NewYork, locations='iso_alpha', 
                    projection='natural earth', animation_frame="month",
                    scope='USA',   #adding the scope as USA
                    color='avg_temp_per_month', locationmode='ISO-3', 
                    color_continuous_scale=px.colors.sequential.ice)

fig3 = fig3.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white", geo_bgcolor="#222222"
    )

# here we needed to change the geo color also to make the world black

graph3 = dcc.Graph(figure=fig3)



app =dash.Dash(external_stylesheets=[dbc.themes.DARKLY])
server = app.server
app.layout = html.Div([html.H1('Average Temperature Forecast for New-York City, 2023', style={'textAlign': 'center', 'color': '#636EFA'}), 
                       html.Div(html.P("A review of average temperatures forcast data for New York City for 8months"), 
                                style={'marginLeft': 50, 'marginRight': 25}),
                       html.Div([html.Div('New York', 
                                          style={'backgroundColor': '#636EFA', 'color': 'white', 
                                                 'width': '900px', 'marginLeft': 'auto', 'marginRight': 'auto'}),
                                 table, graph1,  graph2, graph3])

                    
])

if __name__ == '__main__':
     app.run_server()