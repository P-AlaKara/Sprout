#TOD: Add Icon to Customer Segment - goals
#change colours on the goals container
import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import dash_mantine_components as dmc
from datetime import datetime, timedelta
import plotly.graph_objs as go

#stylesheets
font_import = html.Link(
    rel='stylesheet',
    href='https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap'
)
external_stylesheets = ['assets/goals_styles.css', dbc.themes.DARKLY]

# Initialize the Dash app
app2 = Dash(__name__, external_stylesheets=external_stylesheets)

goals_dic = dict()
goals_dic_cust = dict()
#get goal details - sales
df_target = pd.read_csv('sales_goals.csv')
df_target.drop(columns=['Unnamed: 0'], inplace=True)
targetscope = df_target._get_value(0,'targetscope')
salestype = df_target._get_value(0,'salestype')
targetvalue = df_target._get_value(0,'targetvalue')
deadline = df_target._get_value(0,'deadline')
targetval = '1,200'
#get goal details - customers
df_target_cust = pd.read_csv('cust_goals.csv')
df_target_cust.drop(columns=['Unnamed: 0'], inplace=True)
targetscope_cust = df_target_cust._get_value(0,'targetscope')
type_cust = df_target_cust._get_value(0,'type')
targetvalue_cust = df_target_cust._get_value(0,'targetvalue')
deadline_cust = df_target_cust._get_value(0,'deadline')
#prepare sales dataset
df = pd.read_csv('modified_sales.csv')
df.drop(columns=['saleID', 'time', 'staff_no', 'staff_name', 'customerID',
                'age', 'productID', 'product_name', 'payment_method', 'discount', 'stock'], inplace=True)
#prepare customers dataset
df_cust = pd.read_csv('customers.csv')
df_cust['Date Joined'] = pd.to_datetime(df_cust['Date Joined'], dayfirst=True)
#create the sales form element
form = html.Div([
    html.H3(className='sales-form-text', children=["Select Target Scope"]),
    dcc.Dropdown(
        id='target-scope',
        options=[
            {'label': 'Global', 'value': 'global'},
            {'label': 'Specific Location', 'value': 'location'},
            {'label': 'Specific Category', 'value': 'category'},
            {'label': 'Customer Segment', 'value': 'segment'}
        ],
        value='global',
        style={'margin': '5px auto', 'color':'black'}
    ),
        
    # Input for location
    dcc.Input(
        id='location-input',
        className='location-input',
        type='text',
        placeholder='Enter location...',
        style={'margin-bottom': '10px', 'display': 'none', 'width':'10rem'}
    ),
        
    # Input for category
    html.Div([
        dcc.Input(
            id='category-input',
            className='category-input',
            type='text',
            placeholder='Enter category...',
            style={'margin-bottom': '10px', 'display': 'none'}
        )
    ], id='category-container'),
        
    # Input for customer segment
    html.Div([
        dcc.Input(
            id='segment-input',
            type='text',
            placeholder='Enter customer segment...',
            style={'margin-bottom': '10px', 'display': 'none'}
        )
    ], id='segment-container'),

    # Input for sales type
    html.Div([
        html.H3(className='sales-form-text', children=["Select Goal Type"]),
        dcc.Dropdown(
            id='sales-type',
            options=[
                {'label': 'Sales Volume', 'value': 'volume'},
                {'label': 'Revenue', 'value': 'revenue'},
                {'label': 'Profit', 'value': 'profit'}
            ],
            value='volume',
            style={'margin-bottom': '20px', 'display': 'none'}
        )
    ], id='sales-type-container'),

    # Input for actual value
    html.Div([
        html.H3(className="form-label", children=['Enter value']),
        dcc.Input(
            id='actual-value',
            type='number',
            placeholder='Enter actual value...',
            style={'margin-bottom': '10px', 'display': 'none'}
        )
    ], id='actual-value-container'),
        
    html.H3(className='form-label-tf', children=["Time Frame"]),
    dcc.DatePickerSingle(
        id='time-frame',
        placeholder='Enter deadline...',
        min_date_allowed = datetime.today() + timedelta(days=7),
        style={'margin-bottom': '10px', 'width':'50rem'}
    ),
    html.Button('Set Goal', id='submit-button', style={'display':'block'}, n_clicks=0)
], id='goal-form', style={'display': 'none', 'position': 'fixed', 'top': 0, 'left': 0, 'width': '100vw', 'height': '100vh', 'backgroundColor': 'rgba(0,0,0,0.5)', 'zIndex': 9999})

#create the customers form
form_cust = html.Div([
    html.H3(className='cust-form-text', children=["Select Goal Type"]),
    dcc.Dropdown(
        id='target-scope-cust',
        options=[
            {'label': 'Global', 'value': 'global'},
            {'label': 'Specific Location', 'value': 'location'},
            {'label': 'Specific Segment', 'value': 'segment'}
        ],
        value='global',
        style={'width': '30rem', 'margin-bottom': '10px'}
    ),
        
    # Input for location
    dcc.Input(
        id='location-input-cust',
        type='text',
        placeholder='Enter location...',
        style={'margin-bottom': '10px', 'display': 'none'}
    ),
        
    # Input for customer segment
    html.Div([
        dcc.Input(
            id='segment-input-cust',
            type='text',
            placeholder='Enter the segment...',
            style={'margin-bottom': '10px', 'display': 'none'}
        )
    ], id='segment-container-cust'),

    # Input for actual value
    html.Div([
        html.H3(className="form-label-cust-value", children=['Enter value']),
        dcc.Input(
            id='actual-value-cust',
            type='number',
            placeholder='Enter actual value...',
            style={'margin-bottom': '10px', 'display': 'none'}
        )
    ], id='actual-value-cust-container'),
        
    html.H3(className='label-cust-tf', children=["Time Frame"]),
    dcc.Dropdown(
        id='time-frame-cust',
        options=[
            {'label': 'Monthly', 'value': 'monthly'},
            {'label': 'Quarterly', 'value': 'quarterly'},
            {'label': 'Yearly', 'value': 'yearly'}
        ],
        value='global',
        style={'width': '30rem', 'margin-bottom': '10px'}
    ),
    html.Button('Set Goal', id='submit-button-cust', style={'display':'block'}, n_clicks=0)
], id='cust-goal-form', style={'display': 'none', 'position': 'fixed', 'top': 0, 'left': 0, 'width': '100vw', 'height': '100vh', 'backgroundColor': 'rgba(0,0,0,0.5)', 'zIndex': 9999})

#create plot sales
if salestype == 'volume':
    if targetscope == 'location':
        grouped = df.groupby(['county','date']).agg(value=('quantity','sum')).reset_index()
        if df_target._get_value(0,'location') == 'Nairobi':
            # Using get_group to access the group for 'Nairobi'
            sales_volume = grouped.groupby('county').get_group('Nairobi')
        if df_target._get_value(0,'location') == 'Kisumu':
            sales_volume = grouped.groupby('county').get_group('Nairobi')
        if df_target._get_value(0,'location') == 'Nakuru':
            sales_volume = grouped.groupby('county').get_group('Nairobi')
    if targetscope == 'category':
        grouped = df.groupby(['category','date']).agg(value=('quantity','sum')).reset_index()
        if df_target._get_value(0,'category') == 'Technology':
            sales_volume = grouped.groupby('category').get_group('Technology')
        if df_target._get_value(0,'category') == 'Furniture':
            sales_volume = grouped.groupby('category').get_group('Furniture')
        if df_target._get_value(0,'category') == 'Office Supplies':
            sales_volume = grouped.groupby('category').get_group('Technology')
    if targetscope == 'segment':
        grouped = df.groupby(['segment','date']).agg(value=('quantity','sum')).reset_index()
        if df_target._get_value(0,'segment') == 'Consumer':
            sales_volume = grouped.groupby('segment').get_group('Consumer')
        if df_target._get_value(0,'segment') == 'Corporate':
            sales_volume = grouped.groupby('segment').get_group('Corporate')
        if df_target._get_value(0,'segment') == 'Home Office':
            sales_volume = grouped.groupby('segment').get_group('Home Office')
    if targetscope == 'global':
        sales_volume = df.groupby('date').agg(value = ('quantity','sum')).reset_index()
elif salestype == 'profit':
    if targetscope == 'location':
        grouped = df.groupby(['county','date']).agg(value=('quantity','sum')).reset_index()
        if df_target._get_value(0,'location') == 'Nairobi':
            # Using get_group to access the group for 'Nairobi'
            sales_volume = grouped.groupby('county').get_group('Nairobi')
        if df_target._get_value(0,'location') == 'Kisumu':
            sales_volume = grouped.groupby('county').get_group('Nairobi')
        if df_target._get_value(0,'location') == 'Nakuru':
            sales_volume = grouped.groupby('county').get_group('Nairobi')
    if targetscope == 'category':
        grouped = df.groupby(['category','date']).agg(value=('quantity','sum')).reset_index()
        if df_target._get_value(0,'category') == 'Technology':
            sales_volume = grouped.groupby('category').get_group('Technology')
        if df_target._get_value(0,'category') == 'Furniture':
            sales_volume = grouped.groupby('category').get_group('Furniture')
        if df_target._get_value(0,'category') == 'Office Supplies':
            sales_volume = grouped.groupby('category').get_group('Technology')
    if targetscope == 'segment':
        grouped = df.groupby(['segment','date']).agg(value=('quantity','sum')).reset_index()
        if df_target._get_value(0,'segment') == 'Consumer':
            sales_volume = grouped.groupby('segment').get_group('Consumer')
        if df_target._get_value(0,'segment') == 'Corporate':
            sales_volume = grouped.groupby('segment').get_group('Corporate')
        if df_target._get_value(0,'segment') == 'Home Office':
            sales_volume = grouped.groupby('segment').get_group('Home Office')
    if targetscope == 'global':
        sales_volume = df.groupby('date').agg(value = ('profit','average')).reset_index()
else:
    if targetscope == 'location':
        grouped = df.groupby(['county','date']).agg(value=('quantity','sum')).reset_index()
        if df_target._get_value(0,'location') == 'Nairobi':
            # Using get_group to access the group for 'Nairobi'
            sales_volume = grouped.groupby('county').get_group('Nairobi')
        if df_target._get_value(0,'location') == 'Kisumu':
            sales_volume = grouped.groupby('county').get_group('Nairobi')
        if df_target._get_value(0,'location') == 'Nakuru':
            sales_volume = grouped.groupby('county').get_group('Nairobi')
    if targetscope == 'category':
        grouped = df.groupby(['category','date']).agg(value=('quantity','sum')).reset_index()
        if df_target._get_value(0,'category') == 'Technology':
            sales_volume = grouped.groupby('category').get_group('Technology')
        if df_target._get_value(0,'category') == 'Furniture':
            sales_volume = grouped.groupby('category').get_group('Furniture')
        if df_target._get_value(0,'category') == 'Office Supplies':
            sales_volume = grouped.groupby('category').get_group('Technology')
    if targetscope == 'segment':
        grouped = df.groupby(['segment','date']).agg(value=('quantity','sum')).reset_index()
        if df_target._get_value(0,'segment') == 'Consumer':
            sales_volume = grouped.groupby('segment').get_group('Consumer')
        if df_target._get_value(0,'segment') == 'Corporate':
            sales_volume = grouped.groupby('segment').get_group('Corporate')
        if df_target._get_value(0,'segment') == 'Home Office':
            sales_volume = grouped.groupby('segment').get_group('Home Office')
    if targetscope == 'global':
        sales_volume = df.groupby('date').agg(value = ('revenue','sum')).reset_index()

trace1 = go.Scatter(
    x=sales_volume['date'], y=sales_volume['value'],
    #mode='markers+lines',
    mode='lines',
    name='Actual Sales',
    line=dict(
        shape='spline',
        smoothing=1.3,
        width=2,
        color='red'
    )
)
trace2 = go.Scatter(
    x=sales_volume['date'],
    y=[targetvalue] * len(sales_volume['date']),  # Create a list of the target value with the same length as the date range
    mode='lines',
    name='Target Sales',
    line=dict(
        color='red',
        width=2,
        dash='dashdot'  # Set the dash pattern to create a dotted line
    )
)
data = [trace1, trace2]
# Create a layout
layout = go.Layout(
    title='Actual vs Target Sales',
    xaxis=dict(title='Date', tickmode='auto', nticks=7),
    yaxis=dict(title='Sales Volume')
)
# Create a figure(sales goal tracking)
fig_sales = go.Figure(data=data, layout=layout)
fig_sales.update_layout(
        plot_bgcolor='rgb(40, 37, 37)',
        paper_bgcolor='rgb(40, 37, 37)',
        font_color='white',
        width=500,
        height=320,
        margin=dict(l=0, r=5, t=80, b=5),
        title=dict(text='Target Sales Volume', font=dict(family='Arial', color='#f0e8e7')),
        title_x = 0.5,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left",  x=0)
)
fig_sales.update_xaxes(showgrid=True, gridcolor='dimgray')
fig_sales.update_yaxes(showgrid=True, gridcolor='dimgray')

#create plot customers
#create plot
if targetscope == 'location':
    grouped = df.groupby(['county','date']).agg(value=('customer_name','count')).reset_index()
    if df_target_cust._get_value(0,'location') == 'Nairobi':
        # Using get_group to access the group for 'Nairobi'
        cust_volume = grouped.groupby('county').get_group('Nairobi')
    if df_target_cust._get_value(0,'location') == 'Nakuru':
        cust_volume = grouped.groupby('county').get_group('Nakuru')
    if df_target_cust._get_value(0,'location') == 'Kisumu':
        cust_volume = grouped.groupby('county').get_group('Kisumu')
if targetscope == 'segment':
    grouped_cust = df_cust.groupby(['segment','Date Joined']).agg(value=('customer_ID','count')).reset_index()
    cust_volume = grouped_cust.groupby(pd.Grouper(key='Date Joined', freq='2QE'))['value'].sum().reset_index()
    #if df_target_cust._get_value(0,'segment') == 'consumer':
        #cust_volume = grouped_cust.groupby('segment').get_group('consumer')
    #if df_target_cust._get_value(0,'segment') == 'corporate':
        #cust_volume = grouped_cust.groupby('segment').get_group('corporate')
    #if df_target_cust._get_value(0,'segment') == 'Home office':
        #cust_volume = grouped_cust.groupby('segment').get_group('Home office')
if targetscope == 'global':
    cust_volume = df_cust.groupby('Date Joined').agg(value = ('customer_ID','count')).reset_index()

grouped_cust = df_cust.groupby(['segment','Date Joined']).agg(value=('customer_ID','count')).reset_index()
grouped_customers = grouped_cust.groupby(pd.Grouper(key='Date Joined', freq='2QE'))['value'].sum().reset_index()
fig_cust = px.line(grouped_customers, x='Date Joined', y='value', line_shape='spline')
fig_cust.add_trace(go.Scatter(
    x=fig_cust.data[0].x,  # Use the same x-values as the original line
    y=[100] * len(fig_cust.data[0].x),  #target values
    mode='lines',
    line=dict(color='red', dash='dash'),  
    name='Target'  #legend name
))
fig_cust.update_layout(
        plot_bgcolor='rgb(40, 37, 37)',
        paper_bgcolor='rgb(40, 37, 37)',
        font_color='white',
        width=500,
        height=320,
        margin=dict(l=0, r=5, t=80, b=5),
        title=dict(text='Target Customer Numbers', font=dict(family='Arial', color='#f0e8e7')),
        title_x = 0.5,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left",  x=0)
)
fig_cust.update_traces(line_color='red')
fig_cust.update_xaxes(showgrid=True, gridcolor='dimgray')
fig_cust.update_yaxes(showgrid=True, gridcolor='dimgray')
#define sidebar and content
sidebar = html.Div(
    [
        html.Img(src='assets/logo2.png', className='logo-img'),
        html.Hr(style={'margin':0}),
        html.Nav([
        html.Ul([
            html.Li(html.A(children=[DashIconify(icon="ant-design:home-outlined", className='icon'),'Home'], href='http://127.0.0.1:5000/', style={'display':'block'})),
            html.Li(html.A(children=[DashIconify(icon="ant-design:tags-outlined", className='icon'),'Sales Dashboard'], href='http://127.0.0.1:8050/')),
            html.Li(html.A(children=[DashIconify(icon="ant-design:database-outlined", className='icon'),'Products Dashboard'], href='http://127.0.0.1:8052/')),
            html.Li(html.A(children=[DashIconify(icon="ant-design:team-outlined", className='icon'),'Customers Dashboard'], href='http://127.0.0.1:8051/')),
            html.Li(html.A(children=[DashIconify(icon="ant-design:aim-outlined", className='icon'),'Goals'], href='http://127.0.0.1:8053/')),
            html.Li(html.A(children=[DashIconify(icon="ant-design:stock-outlined", className='icon'),'Analysis'], href='http://127.0.0.1:8054/')),
            html.Li(html.A(children=[DashIconify(icon="ant-design:search-outlined", className='icon'),'Queries'], href='http://127.0.0.1:8055/'))
        ], className='nav'),
    ], className='navbar')],
)
content = html.Div([
    html.H1(id='header-prod', children=['GOALS DASHBOARD']),
        html.Div( 
            className='header-icons-prod',
            children=[
                dbc.NavLink(children=[DashIconify(icon="mdi:home", className='icon-header-prod'),], href="http://127.0.0.1:5000/"),  
                dbc.NavLink(children=[DashIconify(icon="mdi:account", className='icon-header-prod'),], href="/"),  
            ],
        ),
    dmc.Divider(label = 'Set Goals',  labelPosition='center', size=2),
    # Form for setting sales goals
    html.Div([
        html.Button('Set Sales Goal', id='toggle-form', n_clicks=0, className='goal-button sales-button'),
        html.Button('Set Customers Goal', id='toggle-form-cust', n_clicks=0, className='goal-button cust-button'),
    ], className='goals-buttons'),
    form,
    form_cust,
    # Output for displaying confirmation message
    html.Div(id='output-message', style={'margin-top': '20px'}),
    html.Div(id='output-message-cust', style={'margin-top': '20px'}),
    dmc.Divider(label = 'Track Goal',  labelPosition='center', size=2),
    dbc.Row([
        dbc.Col([
            #display the goal
            dmc.Group(
                            #position='center',
                            className='goal',
                            spacing='xs',
                            style={'flex-direction':'column', 'jusfity-content':'center'},
                            children=[
                                dmc.Group(children=[DashIconify(icon="clarity:date-line", id='globe-icon', color="orange", width=24, style={"margin-top": "3rem"}),
                                                    dmc.Text('Daily Sales Target', id='target-text', size='lg', style={'font-family':'IntegralCF-ExtraBold', 'margin-top':'3rem'})]),
                                dmc.Text(f'{targetval}', size='xl', color='red', style={'font-family':'IntegralCF-RegularOblique', 'font-size':'2rem', 'color':'red'}),
                                dmc.Group(children=[DashIconify(icon="mdi:globe", color="orange", width=24),
                                                    dmc.Text('Scope: Global', id='target-text-two', size='lg', style={'font-family':'IntegralCF-ExtraBold'})]),
                                dmc.Group(children=[DashIconify(icon="mdi:counter", color="orange", width=24),
                                                    dmc.Text('Type: Volume', id='target-text-three', size='lg', style={'font-family':'IntegralCF-ExtraBold'})])
                            ]
                        )
            ], id='goals-container'),
        dbc.Col([
            #graph showing actual vs target
            html.Div(id='sales-goal-chart', className='chart', children=[dcc.Graph(figure=fig_sales, 
                                                                                   config={"displaylogo": False,'modeBarButtonsToRemove': ['pan2d','lasso2d','autoScale2d','resetScale2d','select2d']},)])
        ])
    ], className='goal-one-row'),
    dbc.Row(
        [
            dbc.Col(
                [
                    dmc.Group(
                        #position='center',
                        className='goal goal_one',
                        spacing='xs',
                        style={'flex-direction':'column', 'jusfity-content':'center'},
                        children=[
                            dmc.Group(children=[DashIconify(icon="clarity:date-line", id='globe-icon-cust', color="orange", width=24, style={"margin-top": "3rem"}),
                                                dmc.Text('Quarterly Customers Target', id='target-text-cust', size='lg', style={'font-family':'IntegralCF-ExtraBold', 'margin-top':'3rem'})]),
                            dmc.Text(f'{targetvalue_cust}', size='xl', color='red', style={'font-family':'IntegralCF-RegularOblique', 'font-size':'2rem', 'color':'red'}),
                            dmc.Group(children=[DashIconify(icon="mdi:office-building", color="orange", width=24),
                                                dmc.Text('Scope: Corporate Segment', id='target-text-two-cust', size='lg', style={'font-family':'IntegralCF-ExtraBold'})]),
                            dmc.Group(children=[DashIconify(icon="mdi:counter", color="orange", width=24),
                                                dmc.Text('Type: Volume', id='target-text-three-cust', size='lg', style={'font-family':'IntegralCF-ExtraBold'})])
                        ]
                    )
                ]
            ),
            dbc.Col(
                [
                    html.Div(id='cust-goal-chart', className='chart', children=[dcc.Graph(figure=fig_cust, 
                                                                                          config={"displaylogo": False,'modeBarButtonsToRemove': ['pan2d','lasso2d','autoScale2d','resetScale2d','select2d']},)])
                ]
            )
        ], className='goal-two-col'
    )
], className='content-goals') 
# Define the layout of the app
app2.layout = dbc.Container([
    dbc.Row(
        [
            dbc.Col(sidebar, width=3, className='sidebar'),
            dbc.Col(content, width=9),
        ],
        style={"height": "100vh"}
    ),
], fluid=True)

######################################CALLBACKS#######################################
#show or hide form
@app2.callback(
    Output('goal-form', 'style'),
    Input('toggle-form', 'n_clicks'),
)
def toggle_form(n_clicks):
    if n_clicks % 2 == 0:
        return {'display': 'none'}
    else:
        return {'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center', 'alignItems': 'center'}
#show or hide customers form
@app2.callback(
    Output('cust-goal-form', 'style'),
    Input('toggle-form-cust', 'n_clicks'),
)
def toggle_form(n_clicks):
    if n_clicks % 2 == 0:
        return {'display': 'none'}
    else:
        return {'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center', 'alignItems': 'center'}

# Define callback to show/hide scope-specific input based on user selection
@app2.callback(
    Output('location-input', 'style'),
    Output('category-input', 'style'),
    Output('segment-input', 'style'),
    Output('sales-type', 'style'),
    Output('actual-value', 'style'),
    [Input('target-scope', 'value')]
)
def show_hide_scope_specific_input(value):
    location_style = {'margin-bottom': '10px', 'display': 'none'}
    category_style = {'margin-bottom': '10px', 'display': 'none'}
    segment_style = {'margin-bottom': '10px', 'display': 'none'}
    sales_type_style = {'margin-bottom': '20px', 'display': 'none'}
    actual_value_style = {'margin-bottom': '10px', 'display': 'none'}
    
    if value == 'location':
        location_style['display'] = 'block'
    elif value == 'category':
        category_style['display'] = 'block'
    elif value == 'segment':
        segment_style['display'] = 'block'
    
    sales_type_style['display'] = 'block'
    actual_value_style['display'] = 'block'
    
    return location_style, category_style, segment_style, sales_type_style, actual_value_style
#customers form
@app2.callback(
    Output('location-input-cust', 'style'),
    Output('segment-input-cust', 'style'),
    Output('actual-value-cust', 'style'),
    [Input('target-scope-cust', 'value')]
)
def show_hide_scope_specific_input(value):
    location_style = {'margin-bottom': '10px', 'display': 'none'}
    segment_style = {'margin-bottom': '10px', 'display': 'none'}
    actual_value_style = {'margin-bottom': '10px', 'display': 'none'}
    
    if value == 'location':
        location_style['display'] = 'block'
    elif value == 'segment':
        segment_style['display'] = 'block'  
    actual_value_style['display'] = 'block'
    
    return location_style, segment_style, actual_value_style

# Define callback to handle form submission
@app2.callback(
    Output('output-message', 'children'),
    [Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('target-scope', 'value'),
     dash.dependencies.State('location-input', 'value'),
     dash.dependencies.State('category-input', 'value'),
     dash.dependencies.State('segment-input', 'value'),
     dash.dependencies.State('sales-type', 'value'),
     dash.dependencies.State('actual-value', 'value'),
     dash.dependencies.State('time-frame', 'date')])
def update_output(n_clicks, target_scope, location, category, segment, sales_type, actual_value, time_frame):
    if n_clicks > 0:
        message = "Sales goals set for the following:\n"
        if target_scope == 'global':
            message += "- Global:\n"
        elif target_scope == 'location':
            if location:
                message += f"- Location: {location}\n"
                goals_dic['location']=location
            else:
                return "Please enter a location."
        elif target_scope == 'category':
            if category:
                message += f"- Category: {category}\n"
                goals_dic['category']=category
            else:
                return "Please enter a category."
        elif target_scope == 'segment':
            if segment:
                message += f"- Customer Segment: {segment}\n"
                goals_dic['segment']=segment
            else:
                return "Please enter a customer segment."
                
        if not sales_type:
            return "Please select a sales type."
        if not actual_value:
            return "Please enter the actual value."
        
        if sales_type == 'volume':
            message += f"- Goal: Increase sales volume to {actual_value} before {time_frame}\n"
            new_data = {'salestype':'volume', 'targetscope':target_scope, 'targetvalue':actual_value, 'deadline':time_frame}
        elif sales_type == 'revenue':
            message += f"- Goal: Increase sales revenue to ${actual_value} before {time_frame}\n"
            new_data = {'salestype':'revenue', 'targetscope':target_scope, 'targetvalue':actual_value, 'deadline':time_frame}
        elif sales_type == 'profit':
            message += f"- Goal: Increase sales profit by {actual_value} percent before {time_frame}\n"
            new_data = {'salestype':'profit', 'targetscope':target_scope, 'targetvalue':actual_value, 'deadline':time_frame}
        goals_dic.update(new_data)
        df_sales = pd.DataFrame(goals_dic, index=[0])
        df_sales.to_csv('sales_goals.csv', mode='w')
        return message
    else:
        return ""   #change this code to avoid program crashing

#customers form
@app2.callback(
    Output('output-message-cust', 'children'),
    [Input('submit-button-cust', 'n_clicks')],
    [dash.dependencies.State('target-scope-cust', 'value'),
     dash.dependencies.State('location-input-cust', 'value'),
     dash.dependencies.State('segment-input-cust', 'value'),
     dash.dependencies.State('actual-value-cust', 'value'),
     dash.dependencies.State('time-frame-cust', 'value')])
def update_output(n_clicks, target_scope, location, segment, actual_value, time_frame_cust):
    if n_clicks > 0:
        message = "Customer goals set for the following:\n"
        if target_scope == 'global':
            message += "- Global:\n"
        elif target_scope == 'location':
            if location:
                message += f"- Location: {location}\n"
                goals_dic_cust['location']=location
            else:
                return "Please enter a location."
        elif target_scope == 'segment':
            if segment:
                message += f"- Customer Segment: {segment}\n"
                goals_dic_cust['segment']=segment
            else:
                return "Please enter a customer segment."
                
        if not actual_value:
            return "Please enter the actual value."
        
        message += f"- Goal: Increase customer numbers to {actual_value} {time_frame_cust}\n"
        new_data = {'type':'volume', 'targetscope':target_scope, 'targetvalue':actual_value, 'period':time_frame_cust}
        
        goals_dic_cust.update(new_data)
        df_sales = pd.DataFrame(goals_dic_cust, index=[0])
        df_sales.to_csv('cust_goals.csv', mode='w')
        return message
    else:
        return ""   #change this code to avoid program crashing

# Run the app
if __name__ == '__main__':
    app2.run(debug=False, port=8053)