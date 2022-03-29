######### Import your libraries #######
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly as py
import plotly.graph_objs as go

###### Define your variables #####
tabtitle = 'Drinking By Continent!'
sourceurl = 'https://raw.githubusercontent.com/psgrewal42/304-titanic-dropdown/main/assets/drinks.csv'
githublink = 'https://github.com/psgrewal42/304-titanic-dropdown'

###### Import a dataframe #######
df = pd.read_csv("./assets/drinks.csv", keep_default_na=False)
df['cont_fname'] = df['continent'].map(
    {'EU': 'Europe', 'AF': 'Africa', 'NA': 'North America', 'SA': 'South America', 'AS': 'Asia',
     'OC': 'Oceania'})
variables_list = ['mean', 'median', 'max', 'min']
continent_list = ['Asia', 'Africa', 'Europe', 'North America', 'Oceania', 'South America']

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = tabtitle

####### Layout of the app ########
app.layout = html.Div([
    html.H3('Drinking Habits Analysis'),
    html.Br(),
    html.H4('Choose an aggregation function:'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in variables_list],
        value=variables_list[0]
    ),
    html.Br(),
    html.H4('Choose continents:'),
    dcc.Dropdown(
        id='dropdown2',
        options=[{'label': i, 'value': i} for i in continent_list],
        value=continent_list,
        multi=True
    ),
    html.Br(),
    dcc.Graph(id='display-value'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])


def get_results_after_aggregation(df_param: pd.DataFrame, agg: str, continents: []):
    if agg == 'mean':
        return pd.DataFrame(
            df_param[df['cont_fname'].isin(continents)].groupby('cont_fname', as_index=True)[['beer_servings', 'spirit_servings', 'wine_servings']].mean())
    if agg == 'median':
        return pd.DataFrame(
            df_param[df['cont_fname'].isin(continents)].groupby('cont_fname', as_index=True)[['beer_servings', 'spirit_servings', 'wine_servings']].median())
    if agg == 'max':
        return pd.DataFrame(
            df_param[df['cont_fname'].isin(continents)].groupby('cont_fname', as_index=True)[['beer_servings', 'spirit_servings', 'wine_servings']].max())
    if agg == 'min':
        return pd.DataFrame(
            df_param[df['cont_fname'].isin(continents)].groupby('cont_fname', as_index=True)[['beer_servings', 'spirit_servings', 'wine_servings']].min())


######### Interactive callbacks go here #########
@app.callback(Output('display-value', 'figure'),
              [Input('dropdown', 'value'), Input('dropdown2', 'value')])
def display_value(agg, continents):
    results = get_results_after_aggregation(df, agg, continents)
    # Create a grouped bar chart
    beer_data = go.Bar(x=results.index,
                       y=results['beer_servings'],
                       name='Beer',
                       marker=dict(color='brown'))

    wine_data = go.Bar(x=results.index,
                       y=results['wine_servings'],
                       name='Wine',
                       marker=dict(color='purple'))

    spirit_data = go.Bar(x=results.index,
                         y=results['spirit_servings'],
                         name='Spirit',
                         marker=dict(color='blue'))

    mylayout = go.Layout(
        title='Alcohol Consumption (' + agg + ')',
        xaxis=dict(title='Continent'),  # x-axis label
        yaxis=dict(title=str('Servings')),  # y-axis label

    )
    fig = go.Figure(data=[beer_data, wine_data, spirit_data], layout=mylayout)
    return fig


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
