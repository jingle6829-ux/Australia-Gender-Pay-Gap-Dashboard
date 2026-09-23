import dash
from dash import dcc, html, Input, Output,State
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import requests
import plotly.express as px

# ===========================
# Loading Data
# ============================
file_path = '/Users/jingle/Downloads/QBUS5010_PROJECT_GROUP_011/raw data.xlsx'

sheet_names = ['state(Weekly Cash earning)', 'population&working hours']

df_state = pd.read_excel(file_path, sheet_name='state(Weekly Cash earning)')
df_population = pd.read_excel(file_path, sheet_name='population&working hours')

num_cols = [
    'Year',
    'Male_Earnings', 'Female_Earnings',
    'Male_Participation_Rate', 'Female_Participation_Rate',
    'Male_Employees', 'Female_Employees'
]
df_state[num_cols] = df_state[num_cols].apply(pd.to_numeric, errors='coerce')

# ===========================
# Data processing
# ============================

year_list = sorted(df_state['Year'].unique().tolist())
state_list = sorted(df_state['State'].unique().tolist())
industry_list = sorted(df_state['Industry'].unique().tolist())
df_state['pay_gap'] = (df_state['Male_Earnings']- df_state['Female_Earnings'])
df_state['num_gap'] = (df_state['Male_Employees'] - df_state['Female_Employees'])
occupation_list = sorted(df_population['Occupation'].unique().tolist())

GEO_URL = "https://raw.githubusercontent.com/codeforgermany/click_that_hood/master/public/data/australia.geojson"
AUS_GEOJSON = requests.get(GEO_URL).json() 

def get_state_center(state_name):
    centers = {
        'New South Wales': {'lon': 147.5, 'lat': -33.5},
        'Victoria': {'lon': 145.0, 'lat': -37.0},
        'Queensland': {'lon': 143.0, 'lat': -21.0},
        'South Australia': {'lon': 135.0, 'lat': -30.0},
        'Western Australia': {'lon': 121.0, 'lat': -25.0},
        'Tasmania': {'lon': 147.0, 'lat': -42.0},
        'Northern Territory': {'lon': 133.0, 'lat': -19.0},
        'Australian Capital Territory': {'lon': 149.0, 'lat': -35.5},
    }
    return centers.get(state_name, {'lon': 133.0, 'lat': -25.0})

# ===========================
# Dashboard
# ============================
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

# Sidebar
sidebar = html.Div([
    html.H3("Home", style={'textAlign': 'center', 'marginTop': '20px', 'fontWeight': 'bold'}),
    html.Hr(),
    dbc.Nav([
        dbc.NavLink("Data Overview", id="page-1-link", href="/page-1", active="exact"),
        dbc.NavLink("Comparison", id="page-2-link", href="/page-2", active="exact"),
    ], vertical=True, pills=True),
], style={
    'position': 'fixed', 'top': 0, 'left': 0, 'bottom': 0, 'width': '250px',
    'padding': '20px', 'backgroundColor': '#ECF0F1'
})

# Header and dropdowns
content = html.Div([
    html.Div([
        html.H1("Australia Gender Equality Analysis",
                style={'textAlign': 'center', 'padding': '20px',
                       'backgroundColor': '#2171b5', 'color': 'white', 'margin': '0'}),
        html.Br()
    ])
])

# App layout
app.layout = html.Div([
    dcc.Location(id='url'),
    sidebar,
    html.Div(id='page-content', style={'marginLeft': '270px', 'padding': '20px'})
])

# Page 1
page_1_layout = html.Div([
    dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5('▼ Time: 2010–2025'),
                    dcc.Dropdown(
                        options= year_list,
                        value=int(max(year_list)),
                        id='year_dropdown',
                        style={'width': '200px'}
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    html.H5('▼ States:'),
                    dcc.Dropdown(
                        options= state_list,
                        value= None,
                        id='state_dropdown',
                        style={'width': '200px'}
                    )
                ])
            ])
        ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4("Average Gender Pay Gap", style={'fontWeight': 'bold'}),
                html.H6("Weakly Earning", style={'color':'grey','fontWeight': 'bold'}),
                html.Div(id='pay_gap',style={'color': 'red', 'textAlign': 'center', 'fontWeight': 'bold','fontSize': '32px' }),
                html.Div(id='gap_show',style={'textAlign': 'center','fontSize': '12px' })
            ], id='metric-card-1', style={
                'padding': '20px', 'border': '2px solid #ddd', 'borderRadius': '10px',
                'backgroundColor': 'white', 'height': '180px',
                'cursor': 'pointer', 'transition': 'all 0.3s'
            })
        ], width=4),
        dbc.Col([
            html.Div([
                html.H4("Participation Rate Gap", style={'fontWeight': 'bold'}),
                html.Br(),
                html.Div(id='rate_gap',style={'color': 'red', 'textAlign': 'center', 'fontWeight': 'bold','fontSize': '32px' }),
                html.Div(id='rate_show',style={'textAlign': 'center','fontSize': '12px' })
            ], id='metric-card-2', style={
                'padding': '20px', 'border': '2px solid #ddd', 'borderRadius': '10px',
                'backgroundColor': 'white', 'height': '180px',
                'cursor': 'pointer', 'transition': 'all 0.3s'
            })
        ], width= 4),
        dbc.Col([
             html.Div([
                html.H4("Employee Number Gap", style={'fontWeight': 'bold'}),
                html.H6("unit: '000 ", style={'color':'grey','fontWeight': 'bold'}),
                html.Div(id='number_gap',style={'color': 'red', 'textAlign': 'center', 'fontWeight': 'bold','fontSize': '32px' }),
                html.Div(id='number_show',style={'textAlign': 'center','fontSize': '12px' })
            ], id='metric-card-3', style={
                'padding': '20px', 'border': '2px solid #ddd', 'borderRadius': '10px',
                'backgroundColor': 'white', 'height': '180px',
                'cursor': 'pointer', 'transition': 'all 0.3s'
            })
        ], width=4)
    ]),
    ## model
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Average Gender Pay Gap")),
        dbc.ModalBody(id="modal-body-1"),
    ], id="modal-1", size="lg", is_open=False),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Participation Rate Gap")),
        dbc.ModalBody(id="modal-body-2"),
    ], id="modal-2", size="lg", is_open=False),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Employee Number Gap")),
        dbc.ModalBody(id="modal-body-3"),
    ], id="modal-3", size="lg", is_open=False),
    dcc.Graph(id = "trend_graphic")
])

# Page 2
page_2_layout = html.Div([
    html.H3("Comparison income in Industry"),
    html.Hr(),
    html.Div([
                    html.H5('▼ Industry:'),
                    dcc.Dropdown(
                        options = industry_list,
                        value= [],
                        id='industry_dropdown',
                        multi=True,
                        clearable=False,  
                        closeOnSelect=False
                    )
                ]),
    html.H5('▼ Time silder (2010 - 2015)'),
    dcc.Slider(df_state['Year'].min(),
               df_state['Year'].max(),
               step = None,
               id = 'year_dropdown1',
               value=df_state['Year'].max(),
               marks={str(year): str(year) for year in df_state['Year'].unique()}),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = 'State_filter')
        ],width = 5),
        dbc.Col([
            dcc.Graph(id = 'industry')
        ],width = 7)
    ]),
    html.Br(),
    html.Br(),
    html.Br(),
    html.H3("Comparison in Occupations"),
    html.Hr(),
    html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5('▼ Time: 2010–2025'),
                    dcc.Dropdown(
                        options= year_list,
                        value=int(max(year_list)),
                        id='occupation_year_dropdown',
                        style={'width': '200px'}
                    )
                ])
            ],width="auto"),
            dbc.Col([
                html.Div([
                    html.H5('▼ Occupation:'),
                    dcc.Dropdown(
                        options= occupation_list,
                        value= ['Accountants','Managers nfd'],
                        id='occupation_dropdown',
                        multi=True,
                        clearable=False,
                        closeOnSelect=False
                    )
                ])
            ])
        ],justify='start', align='center', className='g-0', style={'gap': '40px'}),
    ]),
    html.Div([
        dbc.Row([
            dbc.Col([
                html.H5("▼ State 1:"),
                dcc.Dropdown(
                    options=state_list,
                    value='New South Wales',
                    id='occupation_state1_dropdown'
                )
            ]),
            dbc.Col([
                html.H5("▼ State 2:"),
                dcc.Dropdown(
                    options=state_list,
                    value='Victoria',
                    id='occupation_state2_dropdown'
                )
            ])
        ]),
        html.Br(),
        dcc.Graph(id='occupation_compare_graph_population'),
        dcc.Graph(id='occupation_compare_graph_hour'),
    ])
], style={'padding': '20px'})

# Routing callback
@app.callback(Output('page-content', 'children'),
        Input('url', 'pathname'))
def render_page(pathname):
    if pathname in ("/", "/page-1"):
        return html.Div([content, page_1_layout])
    elif pathname == "/page-2":
        return html.Div([content, page_2_layout])
    else:
        return html.Div([html.H3("404 Page not found")])

# Pay gap calculation
@app.callback(
    Output('pay_gap', 'children'),
    Output('gap_show','children'),
    Output('rate_gap', 'children'),
    Output('rate_show', 'children'),
    Output('number_gap', 'children'),
    Output('number_show','children'),
    Output('trend_graphic','figure'),
    Input('year_dropdown', 'value'),
    Input('state_dropdown', 'value'))
def cal_pay_gap(year_value, state_value):
    if state_value == None:
        fresh_data = df_state[(df_state['Year'] == year_value)]
    else:
        fresh_data = df_state[(df_state['Year'] == year_value) & (df_state['State'] == state_value)]
    
    avg_gap = fresh_data['pay_gap'].mean()

    male_wage = fresh_data['Male_Earnings'].mean()
    female_wage = fresh_data['Female_Earnings'].mean()

    male_rate = fresh_data['Male_Participation_Rate'].mean()
    female_rate = fresh_data['Female_Participation_Rate'].mean()
    avg_rate = male_rate - female_rate

    male_num = fresh_data['Male_Employees'].mean()
    female_num = fresh_data['Female_Employees'].mean()
    avg_num = male_num - female_num

    # graph
    if state_value == None:
        line_data = df_state
    else:
        line_data = df_state[df_state['State'] == state_value]
    
    total_earning = line_data.groupby('Year')[['Male_Earnings','Female_Earnings']].mean().reset_index()

    #  gender pay gap (%)
    total_earning['Gap_Percent'] = (
        (total_earning['Male_Earnings'] - total_earning['Female_Earnings'])
        / total_earning['Male_Earnings'] * 100
    )

    gap_text = [f"{y:.1f}%" if x == year_value else "" 
            for x, y in zip(total_earning['Year'], total_earning['Gap_Percent'])]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=total_earning['Year'],
        y=total_earning['Male_Earnings'],
        mode='lines+markers',
        name='Male Earnings'
    ))

    fig.add_trace(go.Scatter(
        x=total_earning['Year'],
        y=total_earning['Female_Earnings'],
        mode='lines+markers',
        name='Female Earnings',
        line_color='#19D3F3'
    ))

    fig.add_trace(go.Scatter(
        x=total_earning['Year'],
        y=total_earning['Gap_Percent'],
        mode='lines+markers+text',
        name='Gender Pay Gap (%)',
        line=dict(dash='dash'),
        yaxis='y2',
        text=gap_text,
        textposition='top center'
    ))

    # fig.add_trace(go.Scatter(
    #     x=total_earning['Year'],
    #     y=total_earning['Male_Earnings'],
    #     mode='lines',
    #     line=dict(width=0),
    #     showlegend=False,
    #     hoverinfo='skip'
    # ))
    # fig.add_trace(go.Scatter(
    #     x=total_earning['Year'],
    #     y=total_earning['Female_Earnings'],
    #     mode='lines',
    #     fill='tonexty',  # 这一句就是填充
    #     fillcolor='rgba(150,150,150,0.2)',
    #     line=dict(width=0),
    #     name='Gap area'
    # ))

    fig.update_layout(
        title='Gender Pay Gap Trend Over Time',
        xaxis_title='Year',
        yaxis_title='Average Weekly Earnings ($AUD)',
        yaxis2=dict(
            title='Gender Pay Gap (%)',
            overlaying='y',
            side='right',
            showgrid=False,
            range=[0, 25],
            autorange=False
        )
    )

    return f"{avg_gap:,.1f}",f"Males:{male_wage:,.1f} | Females {female_wage:,.1f}", f"{avg_rate:,.1f}",f"Males:{male_rate:,.1f} | Females {female_rate:,.1f}",f"{avg_num:,.1f}",f"Males:{male_num:,.1f} | Females {female_num:,.1f}",fig

@app.callback(
    [Output("modal-1", "is_open"), Output("modal-body-1", "children")],
    [Input("metric-card-1", "n_clicks")],
    [State('year_dropdown', 'value'),
     State('state_dropdown', 'value'),
     State("modal-1", "is_open")]
)
def toggle_modal_1(n,year_value, state_value, is_open):
    if state_value == None:
        fresh_data = df_state[(df_state['Year'] == year_value)]
        state = 'Asutralia'
    else:
        fresh_data = df_state[(df_state['Year'] == year_value) & (df_state['State'] == state_value)]
        state = state_value
    
    avg_gap = fresh_data['pay_gap'].mean()
    male_wage = fresh_data['Male_Earnings'].mean()
    female_wage = fresh_data['Female_Earnings'].mean()

    if n:
        content = html.Div([
            html.P("Shown is the difference in average weekly earnings between men and women over the same time period."),
            html.Br(),
            html.P([
                "In ",
                html.Span(year_value, style={"color": "red", "fontWeight": "bold"}),
                ", the average gender pay gap in ",
                html.Span(state, style={"color": "red", "fontWeight": "bold"}),
                " is ",
                html.Span(f"${avg_gap:,.1f}", style={"color": "red", "fontWeight": "bold"}),
                " per week."
            ]),
            html.Br(),
            html.P([
                "The figures show men earn an average of ",
                html.Span(f"${male_wage:,.1f}", style={"color": "red", "fontWeight": "bold"}),
                " a week, while women earn just ",
                html.Span(f"${female_wage:,.1f}", style={"color": "red", "fontWeight": "bold"}),
                "."
            ]),
            html.Br(),
            html.P("This difference reflects whether there is a significant gender inequality in pay.")
        ])
        return not is_open, content
    return is_open, dash.no_update

@app.callback(
    [Output("modal-2", "is_open"), Output("modal-body-2", "children")],
    [Input("metric-card-2", "n_clicks")],
    [State('year_dropdown', 'value'),
     State('state_dropdown', 'value'),
     State("modal-2", "is_open")]
)
def toggle_modal_2(n,year_value, state_value, is_open):
    if state_value == None:
        fresh_data = df_state[(df_state['Year'] == year_value)]
        state = 'Asutralia'
    else:
        fresh_data = df_state[(df_state['Year'] == year_value) & (df_state['State'] == state_value)]
        state = state_value

    male_rate = fresh_data['Male_Participation_Rate'].mean()
    female_rate = fresh_data['Female_Participation_Rate'].mean()
    avg_rate = male_rate - female_rate

    if n:
        content = html.Div([
            html.P("Shown is the difference in labour force participation rates between men and women over the same time period."),
            html.Br(),
            html.P([
                "Labour force participation data for ",
                html.Span(year_value, style={"color": "red", "fontWeight": "bold"}),
                " shows that the participation rate in ",
                html.Span(state, style={"color": "red", "fontWeight": "bold"}),
                " for men is ",
                html.Span(f"{male_rate:,.1f}%", style={"color": "red", "fontWeight": "bold"}),
                " compared to ",
                html.Span(f"{female_rate:,.1f}%", style={"color": "red", "fontWeight": "bold"}),
                " for women, a difference of ",
                html.Span(f"{avg_rate:,.1f} percentage points", style={"color": "red", "fontWeight": "bold"}),
                "."
            ]),
            html.Br(),
            html.P("This difference reflects gender imbalance at the level of labour force participation.")
        ])
        return not is_open, content
    return is_open, dash.no_update

@app.callback(
    [Output("modal-3", "is_open"), Output("modal-body-3", "children")],
    [Input("metric-card-3", "n_clicks")],
    [State('year_dropdown', 'value'),
     State('state_dropdown', 'value'),
     State("modal-3", "is_open")]
)
def toggle_modal_3(n,year_value, state_value, is_open):
    if state_value == None:
        fresh_data = df_state[(df_state['Year'] == year_value)]
        state = 'Asutralia'
    else:
        fresh_data = df_state[(df_state['Year'] == year_value) & (df_state['State'] == state_value)]
        state = state_value

    male_num = fresh_data['Male_Employees'].mean()
    female_num = fresh_data['Female_Employees'].mean()
    avg_num = male_num - female_num

    if n:
        content = html.Div([
            html.P("Shown is the difference in the number of employed men and women over the same time period."),
            html.Br(),
            html.P([
                "In terms of employment numbers, the data shows that in ",
                html.Span(year_value, style={"color": "red", "fontWeight": "bold"}),
                ", ",
                html.Span(f"{male_num:,.1f} thousand", style={"color": "red", "fontWeight": "bold"}),
                " men and ",
                html.Span(f"{female_num:,.1f} thousand", style={"color": "red", "fontWeight": "bold"}),
                " women will be employed in ",
                html.Span(state, style={"color": "red", "fontWeight": "bold"}),
                ", a gap of ",
                html.Span(f"{avg_num:,.1f} thousand", style={"color": "red", "fontWeight": "bold"}),
                "."
            ]),
            html.Br(),
            html.P("The results reflect whether the gender distribution of employment opportunities is balanced.")
        ])
        return not is_open, content

    return is_open, dash.no_update

@app.callback(Output('State_filter','figure'),
                Output('industry','figure'),
                Input('year_dropdown1', 'value'),
                Input('industry_dropdown', 'value'),
                Input('State_filter', 'clickData'))
def interactive(year_value,industry_selected,clickData):
    # ===================
    #        map 
    # ===================
    year_select = df_state[(df_state['Year'] == year_value)]
    if industry_selected and len(industry_selected) > 0:
        year_select = year_select[year_select['Industry'].isin(industry_selected)]

    selected_state = None
    if clickData and 'points' in clickData and len(clickData['points']) > 0:
        selected_state = clickData['points'][0].get('location')

    year_select['AvgEarnings'] = (year_select['Male_Earnings'] + year_select['Female_Earnings']) / 2.0
    map_df = year_select.groupby('State')['AvgEarnings'].mean().reset_index()

    map = px.choropleth(
        map_df,
        geojson=AUS_GEOJSON,
        locations='State',               
        featureidkey='properties.name',       
        color='AvgEarnings',
        color_continuous_scale='Blues',
        labels={'AvgEarnings': 'Weekly $'},
        title='Average weekly total cash earnings - state'
    )

    if selected_state:
        map.update_geos(
            visible=False,
            fitbounds='locations',
            domain=dict(x=[0, 1], y=[0.1, 0.9]),
            projection_scale=8.0,
            center=get_state_center(selected_state) 
        )
        map.update_layout(title=f'Zoomed to {selected_state}')
    else:
        map.update_geos(fitbounds='locations', visible=False)

    map.update_layout( 
        margin=dict(l=0, r=0, t=40, b=0),
        coloraxis_colorbar=dict(title='Weekly $')
    )

    # groupby industry
    if selected_state is not None:
        df_bar_source = year_select[year_select['State'] == selected_state]
    else:
        df_bar_source = year_select
    df_bar = (df_bar_source.groupby('Industry')[['Male_Earnings', 'Female_Earnings']].mean())
    # sorted by the value
    df_bar['max_val'] = df_bar[['Male_Earnings', 'Female_Earnings']].max(axis=1)
    df_bar = df_bar.sort_values('max_val', ascending=True) 
    male_vals  = df_bar['Male_Earnings'].tolist()
    fem_vals   = df_bar['Female_Earnings'].tolist()

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        y=industry_list, x=male_vals,
        name='Male', orientation='h'
    ))
    fig2.add_trace(go.Bar(
        y=industry_list, x=fem_vals,
        name='Female', orientation='h',
        marker_color='#19D3F3'
    ))

    fig2.update_layout(
        barmode='group',                                 
        title='Average weekly earnings by industry and gender',
        xaxis_title='Average Weekly Earnings ($)',
        yaxis_title='',
        margin=dict(l=10, r=10, t=40, b=10),
        height=500, 
        legend=dict(orientation='v', yanchor='bottom', y=1, xanchor='right', x=1)
    )
    fig2.update_yaxes(automargin=True, tickfont=dict(size=11))


    return map,fig2

@app.callback(
    Output('occupation_compare_graph_population', 'figure'),
    Output('occupation_compare_graph_hour', 'figure'),
    Input('occupation_year_dropdown', 'value'),
    Input('occupation_dropdown', 'value'),
    Input('occupation_state1_dropdown', 'value'),
    Input('occupation_state2_dropdown', 'value')
)
def update_occupation_chart(year_select, occ_list, state1, state2):
    if not occ_list:
        return go.Figure(), go.Figure()

    df_sub = df_population[
        (df_population['Year'] == year_select) &
        (df_population['Occupation'].isin(occ_list)) &
        (df_population['State'].isin([state1, state2]))
    ].copy()

    # =========================
    # A. population
    # =========================
    df_pivot = df_sub.pivot_table(
        index=['Year', 'Occupation', 'State'],
        columns='Sex',
        values="Employed total ('000)",
        aggfunc='sum',
        fill_value=0
    ).reset_index()

    for col in ['Males', 'Females']:
        if col not in df_pivot.columns:
            df_pivot[col] = 0

    df_s1 = df_pivot[df_pivot['State'] == state1].copy()
    df_s2 = df_pivot[df_pivot['State'] == state2].copy()

    for df_ in (df_s1, df_s2):
        df_['Total'] = df_['Males'] + df_['Females']
        df_['female_pct'] = np.where(df_['Total'] > 0, df_['Females'] / df_['Total'] * 100, 0)
        df_['male_pct'] = np.where(df_['Total'] > 0, df_['Males'] / df_['Total'] * 100, 0)
        df_['Occupation'] = pd.Categorical(df_['Occupation'], categories=occ_list, ordered=True)
        df_.sort_values('Occupation', inplace=True)

    # population 
    fig_pop = make_subplots(
        rows=1,
        cols=2,
        horizontal_spacing=0.08,
        subplot_titles=(f"{state1}", f"{state2}")
    )

    # left（state1）
    fig_pop.add_trace(
        go.Bar(
            y=df_s1['Occupation'],
            x=df_s1['female_pct'],
            name='Female',
            orientation='h',
            marker_color='#19D3F3',
            text=[f"{v:.0f}%" for v in df_s1['female_pct']],
            textposition='inside'
        ),
        row=1, col=1
    )
    fig_pop.add_trace(
        go.Bar(
            y=df_s1['Occupation'],
            x=df_s1['male_pct'],
            name='Male',
            orientation='h',
            marker_color='#636EFA',
            text=[f"{v:.0f}%" for v in df_s1['male_pct']],
            textposition='inside'
        ),
        row=1, col=1
    )

    # right（state2）
    fig_pop.add_trace(
        go.Bar(
            y=df_s2['Occupation'],
            x=df_s2['female_pct'],
            name='Female',
            orientation='h',
            marker_color='#19D3F3',
            text=[f"{v:.0f}%" for v in df_s2['female_pct']],
            textposition='inside',
            showlegend=False
        ),
        row=1, col=2
    )
    fig_pop.add_trace(
        go.Bar(
            y=df_s2['Occupation'],
            x=df_s2['male_pct'],
            name='Male',
            orientation='h',
            marker_color='#636EFA',
            text=[f"{v:.0f}%" for v in df_s2['male_pct']],
            textposition='inside',
            showlegend=False
        ),
        row=1, col=2
    )

    # x / y scaling
    fig_pop.update_xaxes(range=[0, 100], row=1, col=1)
    fig_pop.update_xaxes(range=[0, 100], row=1, col=2)
    fig_pop.update_yaxes(autorange='reversed', row=1, col=1)
    fig_pop.update_yaxes(autorange='reversed', row=1, col=2, showticklabels=False)

    fig_pop.update_layout(
        barmode='stack',
        title=f'Population – {year_select}',
        height=80 * max(len(df_s1), len(df_s2)) + 150,
        legend=dict(orientation='h', yanchor='bottom', y=1, xanchor='right', x=0.6)
    )

    # =========================
    # B. hours
    # =========================
    pivot_hours = df_sub.pivot_table(
        index=['Year', 'State', 'Occupation'],
        columns='Sex',
        values="Number of hours actually worked in all jobs ('000 Hours)",
        aggfunc='sum',
        fill_value=0
    ).reset_index()

    for col in ['Males', 'Females']:
        if col not in pivot_hours.columns:
            pivot_hours[col] = 0

    dfh_s1 = pivot_hours[pivot_hours['State'] == state1].copy()
    dfh_s2 = pivot_hours[pivot_hours['State'] == state2].copy()

    for df_ in (dfh_s1, dfh_s2):
        df_['Total'] = df_['Males'] + df_['Females']
        df_['female_pct'] = np.where(df_['Total'] > 0, df_['Females'] / df_['Total'] * 100, 0)
        df_['male_pct'] = np.where(df_['Total'] > 0, df_['Males'] / df_['Total'] * 100, 0)
        df_['Occupation'] = pd.Categorical(df_['Occupation'], categories=occ_list, ordered=True)
        df_.sort_values('Occupation', inplace=True)

    fig_hour = make_subplots(
        rows=1,
        cols=2,
        horizontal_spacing=0.08,
        subplot_titles=(f"{state1}", f"{state2}")
    )

    # left hours
    fig_hour.add_trace(
        go.Bar(
            y=dfh_s1['Occupation'],
            x=dfh_s1['female_pct'],
            name='Female',
            orientation='h',
            marker_color='#19D3F3',
            text=[f"{v:.0f}%" for v in dfh_s1['female_pct']],
            textposition='inside'
        ),
        row=1, col=1
    )
    fig_hour.add_trace(
        go.Bar(
            y=dfh_s1['Occupation'],
            x=dfh_s1['male_pct'],
            name='Male',
            orientation='h',
            marker_color='#636EFA',
            text=[f"{v:.0f}%" for v in dfh_s1['male_pct']],
            textposition='inside'
        ),
        row=1, col=1
    )

    # right hours
    fig_hour.add_trace(
        go.Bar(
            y=dfh_s2['Occupation'],
            x=dfh_s2['female_pct'],
            name='Female',
            orientation='h',
            marker_color='#19D3F3',
            text=[f"{v:.0f}%" for v in dfh_s2['female_pct']],
            textposition='inside',
            showlegend=False
        ),
        row=1, col=2
    )
    fig_hour.add_trace(
        go.Bar(
            y=dfh_s2['Occupation'],
            x=dfh_s2['male_pct'],
            name='Male',
            orientation='h',
            marker_color='#636EFA',
            text=[f"{v:.0f}%" for v in dfh_s2['male_pct']],
            textposition='inside',
            showlegend=False
        ),
        row=1, col=2
    )

    fig_hour.update_xaxes(range=[0, 100], row=1, col=1)
    fig_hour.update_xaxes(range=[0, 100], row=1, col=2)
    fig_hour.update_yaxes(autorange='reversed', row=1, col=1)
    fig_hour.update_yaxes(autorange='reversed', row=1, col=2, showticklabels=False)

    fig_hour.update_layout(
        barmode='stack',
        title=dict(text = f'Working Hours – {year_select}'),
        height=80 * max(len(dfh_s1), len(dfh_s2)) + 150,
        legend=dict(orientation='h', yanchor='bottom', y=1, xanchor='right', x=0.6)
    )

    return fig_pop, fig_hour

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
