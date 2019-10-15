import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np

from dash.dependencies import Input, Output
from plotly import graph_objs as go
import datetime
from statistics import mean
from flask import Flask
import os

server = Flask(__name__)
server.secret_key = os.environ.get('secret_key', 'secret')
app = dash.Dash(name = __name__, server = server)
app.title='Dronagro - Farm Control and Analytics'

#app = dash.Dash(
#    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
#)
#server = app.server
farm_reports = pd.read_csv(
    "farm_report.csv",
)

farm_report=farm_reports.set_index('Dates')
farm_report.index = pd.to_datetime(farm_report.index)

months={'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10,'November':11,'December':12}
structures={2014:'12', 2015:'15', 2016:'16', 2017:'19', 2018:'22',2019:'24' }

# Layout of Dash App
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.Img(
                            className="logo", src=app.get_asset_url("dronagro.png")
                        ),
                        html.H2("DRONAGRO - FARM ANALYTICS APP"),
                        html.P(
                            """Slide using the Rangeslider below the chart to narrow or expand the time range. Select class, month and year. Hover over any point on the line graph to get detailed value."""
                        ),
                        
                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="class-selector",
                                            options=[
                                                {"label": i, "value": i}
                                                for i in ['Livestock','Weed','Vegetation']
                                            ],
                                            placeholder="Select a class",
                                            value='Livestock',
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown to select times
                                        dcc.Dropdown(
                                            id="month-selector",
                                            options=[
                                                {
                                                    "label": i,
                                                    "value": i,
                                                }
                                                for i in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October','November','December']
                                            ],

                                            placeholder="Select a month",
                                            value='April',
                                        )
                                    ],
                                ),
                                html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.Slider(
						        id='year-slider',
						        min=2014,
						        max=2019,
						        value=2019,
						        marks={str(year): str(year) for year in [2014,2015,2016,2017,2018,2019]},
						        step=None
						    )
                            ],
                        ),

                        		html.Div(
                                    className="div-for-dropdown",
                                    id= 'important-detail'),
                                html.Div(
                                    className="div-for-dropdown",
                                    id= 'sum-detail'),        
                            ],
                        ),
                        
                        
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        #dcc.Graph(id="map-graph"),
                        html.Div(
                            className="text-padding",
                            
                        ),
                        dcc.Graph(id="histogram"),
                    ],
                ),
            ],
        )
    ]
)
"""
@app.callback(
	 Output('map-graph','figure'),
	[Input("class-selector",'value'), Input("month-selector", "value"),Input("year-slider", "value")],
)
def update_output(classe,month,year):
		
		
	filtered=farm_report[farm_report.index.year.isin([year])]
	filtered_report=filtered[filtered.index.month.isin([months['April']])]
	c= {
        'data': [go.Scatter(
            x=filtered_report['Weed_Count'],
            y=filtered_report[classe +'_Count'],
            text=classe,
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={'type': 'log', 'title': 'Dates'},
            yaxis={'title': classe + ' Count'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
            )
        }
	return go.Figure(data=c['data'],layout=c['layout'])
"""
@app.callback(
	 Output('histogram','figure'),
	[Input("class-selector",'value'), Input("month-selector", "value"),Input("year-slider", "value")],
)
def update_hist(classe,month,year):
	
		
	filtered_report=farm_report[farm_report.index.year.isin([year])]
	filtered_report=filtered_report[filtered_report.index.month.isin([months[month]])]
	
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=filtered_report.index, y=filtered_report['Livestock_Count'], name="Livestock",
                         mode='lines+markers', line=dict(color='blue')))

	fig.add_trace(go.Scatter(x=filtered_report.index, y=filtered_report['Vegetation_Count'], name="Vegetation",
                         mode='lines+markers', line=dict(color='green')))
	fig.add_trace(go.Scatter(x=filtered_report.index, y=filtered_report['Weed_Count'], name="Weed",
                         mode='lines+markers', line=dict(color='firebrick') ))

	fig.update_layout(title_text='Time Series with Rangeslider for Daily Count by the Drone',yaxis_title='Count',
                  xaxis_rangeslider_visible=True)
	return fig

@app.callback(
	 Output('important-detail','children'),
	[Input("year-slider", "value")],
)
def update_output_div(year):
	
	val=structures[year]

	return 'Number of Structures in {}: "{}"'.format(year,val)

@app.callback(
	 Output('sum-detail','children'),
	[Input("class-selector",'value'),Input("month-selector", "value"),Input("year-slider", "value")],
)
def update_output_div2(classe,month,year):
	
	filtered=farm_report[farm_report.index.year.isin([year])]
	filtered_report=filtered[filtered.index.month.isin([months[month]])]
	disparity=[]
	column=classe + '_Count'
	filtered_list=list(filtered_report[column])
	l=len(filtered_list)
	item=range(l)[:l-1]
	for x in filtered_list[1:]:
		for i in list(item):
			a= x-filtered_list[i]
			b=a/filtered_list[i]
			disparity.append(b)
			break
	rate=round(mean(disparity)*100,2)


	return 'Average rate of change of {} in {} {}: "{}%" '.format(classe,month,year,rate)


if __name__ == "__main__":
    app.server.run(debug=True, threaded=True)