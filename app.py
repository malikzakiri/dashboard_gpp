# 1. Import Dash
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import pandas as pd
from statistics import mode
import plotly.express as px

print('BERHASIL')

# 2. Create a Dash app instance, THEME
app = dash.Dash(
    external_stylesheets=[dbc.themes.LITERA],
    name='Global Power Plant'
)

# -- Navbar & Title Tab --
app.title='Power Plant Dashboard Analytics'
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="#")),
    ],
    brand="Global Power Plant",
    brand_href="#",
    color="primary",
    dark=True,
)

# -- IMPORT DATASET GPP --
gpp=pd.read_csv('power_plant.csv')

# -- CARD CONTENT --
total_country = [
    dbc.CardHeader('Number of Country'),
    dbc.CardBody([
        html.H1(gpp['country_long'].nunique())
    ]),
]

total_power_plant = [
    dbc.CardHeader('Number of Power Plant'),
    dbc.CardBody([
        html.H1(gpp['name of powerplant'].nunique())
    ]),
]

total_fuel = [
    dbc.CardHeader('Most Used Fuel', style={"color":"black"}),
    dbc.CardBody([
        html.H1(f"{mode(gpp['primary_fuel'])} = {len(gpp[gpp['primary_fuel']==(gpp.describe(include='object')).loc['top','primary_fuel']])}")
    ])
]

# ----------- CHOROPLETH MAP ----------
# Data aggregation
agg1 = pd.crosstab(
    index=[gpp['country code'], gpp['start_year']],
    columns='No of Power Plant'
).reset_index()

# Visualization
plot_map= px.choropleth(agg1,
    locations='country code',
    color_continuous_scale='tealgrn',
    color='No of Power Plant',
    animation_frame='start_year',
    template='ggplot2')


#-- BAR PLOT CONTENT --
# Data aggregation
gpp_indo = gpp[gpp['country_long'] == 'Indonesia']
top_indo = gpp_indo.sort_values('capacity in MW').tail(10)

# Visualize
plot_ranking = px.bar(
    top_indo,
    x = 'capacity in MW',
    y = 'name of powerplant',
    color_discrete_sequence=px.colors.qualitative.Light24,
    #template = 'ggplot2',
    title = 'Rangking of Overall Power Plants in Indonesia'
)

# -- BOX-PLOT CONTENT --
plot_distribution = px.box(
    gpp_indo,
    color='primary_fuel',
    x='capacity in MW',
    color_discrete_sequence=px.colors.qualitative.Light24,
    #template='ggplot2',
    title='Distribution of capacity in MW in each fuel',
    labels={
        'primary_fuel': 'Type of Fuel'
    }
).update_xaxes(visible=False)

# --------- PLOT PIE CONTENT ------------
# aggregation
agg2=pd.crosstab(
    index=gpp_indo['primary_fuel'],
    columns='No of Power Plant'
).reset_index()

# visualize
plot_pie = px.pie(
    agg2,
    values='No of Power Plant',
    names='primary_fuel',
    color_discrete_sequence=px.colors.qualitative.Light24,
    #template='ggplot2',
    hole=0.4,
    labels={
        'primary_fuel': 'Type of Fuel'
    }
)

# -- LAYOUT --
app.layout = html.Div(children=[
    navbar,

    html.Br(),
    
    # --Component Main Page--
    html.Div([

        #--ROW 1--
        dbc.Row([

            # COLUMN 1
            dbc.Col(
                [
                    dbc.Card(total_country, color='info'),
                    html.Br(),
                    dbc.Card(total_power_plant, color='primary'),
                    html.Br(),
                    dbc.Card(total_fuel, color='secondary'),
                ],
                width=3
                ),

            # COLUMN 2
            dbc.Col([
                dcc.Graph(figure=plot_map)
            ],
            width=9),
        ]),

        html.Hr(),

        #--ROW 2--
        dbc.Row([
           
            # COLUMN 1
            dbc.Col([
                html.H1('Analysis by Contry'),
                html.Br(),
                dbc.Tabs([
                    #-- TAB 1: RANKING --
                    dbc.Tab(
                        dcc.Graph(
                            id='plot_ranking',
                            figure=plot_ranking
                        ),
                        label='Ranking'),
                    
                    #-- TAB 2: DISTRIBUTION
                    dbc.Tab(
                        dcc.Graph(
                            id='plot_distribution',
                            figure=plot_distribution,
                        ),
                        label='Distribution'),
                ]),
            ],
            width=8),

            # COLUMN 2
            dbc.Col([
                dbc.Card([
                        dbc.CardHeader('Select Country'),
                        dbc.CardBody(
                            dcc.Dropdown(
                                id='choose_country',
                                options=gpp['country_long'].unique(),
                                value='Indonesia'
                            )
                        ),
                ]),
                dcc.Graph(
                    id='plot_pie',
                    figure=plot_pie
                ),
            ],width=4),

        ]),
    ],
    style={
        'paddingRight':'25px',
        'paddingLeft':'25px'
    })
])

# ---- CALLBACK PLOT RANKING ----
@app.callback(
    Output(component_id='plot_ranking',component_property='figure'),
    Input(component_id='choose_country', component_property='value')
)

def update_plot1(country_name):
    # Data aggregation
    gpp_indo = gpp[gpp['country_long'] == country_name]

    top_indo = gpp_indo.sort_values('capacity in MW').tail(10)

    # Visualize
    plot_ranking = px.bar(
        top_indo,
        x = 'capacity in MW',
        y = 'name of powerplant',
        color_discrete_sequence=px.colors.qualitative.Light24,
        #template = 'ggplot2',
        title = f'Rangking of Overall Power Plants in {str(country_name)}'
    )

    return plot_ranking

# ---- CALLBACK PLOT DISTRIBUTION ----
@app.callback(
    Output(component_id='plot_distribution',component_property='figure'),
    Input(component_id='choose_country', component_property='value')
)

def update_plot1(country_name):
    
    gpp_indo = gpp[gpp['country_long'] == country_name]

    plot_distribution = px.box(
        gpp_indo,
        color='primary_fuel',
        x='capacity in MW',
        color_discrete_sequence=px.colors.qualitative.Light24,
        #template='ggplot2',
        title='Distribution of capacity in MW in each fuel',
        labels={
            'primary_fuel': 'Type of Fuel'
        }
    ).update_xaxes(visible=False)

    return plot_distribution

# ---- CALLBACK PLOT PIE ----
@app.callback(
    Output(component_id='plot_pie',component_property='figure'),
    Input(component_id='choose_country', component_property='value')
)

def update_plot1(country_name):
    
    gpp_indo = gpp[gpp['country_long'] == country_name]

    agg2=pd.crosstab(
        index=gpp_indo['primary_fuel'],
        columns='No of Power Plant'
    ).reset_index()

    plot_pie = px.pie(
        agg2,
        values='No of Power Plant',
        names='primary_fuel',
        color_discrete_sequence=['aquamarine', 'salmon', 'plum', 'grey', 'slateblue'],
        template='ggplot2',
        hole=0.4,
        labels={
            'primary_fuel': 'Type of Fuel'
        }
    )

    return plot_pie

# 3. Start the Dash server
if __name__ == "__main__":
    app.run_server()
