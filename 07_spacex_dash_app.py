# Import required libraries
import pandas as pd
import dash
#import dash_html_components as html
from dash import html
#import dash_core_components as dcc
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                  dcc.Dropdown(id='id',
                                    options=[
                                            {'label': 'All Sites', 'value': 'ALL'},
                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
                                    value='ALL',
                                    placeholder="Select a launch site here",
                                    searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    value=[0, 10000]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'), 
            Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    chart_data = spacex_df.groupby('Launch Site')
    #percent of successed launch rate of each site in all succeed launches
    chart1 = chart_data['class'].sum() / sum(chart_data['class'].sum())
    chart2 = chart_data['class'].sum() / chart_data['class'].count()


    if entered_site == 'ALL':
        data = chart1.values
        labels = chart1.index

        fig = px.pie(values=data, 
        names=labels, 
        title='success rate for all launch site')
        return fig
    
    else:
        data = [chart2[entered_site], 1-chart2[entered_site]]
        labels = [1, 0]

        fig = px.pie(values=data, names=labels, title = 'success rate for specific launch site')
        return fig
        # return the outcomes piechart for a selected site
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            [Input(component_id='site-dropdown', component_property='value'),
            Input(component_id="payload-slider", component_property="value")]
            )

# add if else. to choose if all sites were selected or just a specific launch site was selected
def get_scatter_chart(entered_site, entered_payload):
    df = spacex_df
    low, high = entered_payload

    if entered_site == 'ALL':
        fig = px.scatter(df, 
            x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig

        #sns.scatterplot(data=df, x='Payload Mass (kg)', y='class', hue= 'Booster Version Category', legend='auto')
    
    else:
        #select data
        mask = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)'] < high) & (df['Launch Site']== entered_site)

        fig = px.scatter(df[mask], 
            x='Payload Mass (kg)', y='class', color= 'Booster Version Category')
        return fig
        
        #sns.scatterplot(data=df[df['Launch Site']=='CCAFS LC-40'], x='Payload Mass (kg)', y='class', hue= 'Booster Version Category', legend='auto')

# Run the app
if __name__ == '__main__':
    app.run_server()
