#first-row row --whole of row 1
#col --all the columns
# add 2 more graphs related to store locations and profits,revenue etc.
import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import dash_mantine_components as dmc

df = pd.read_csv('modified_sales.csv')
df.drop(columns=['staff_no', 'staff_name', 'customer_name', 'age', 'productID', 
                 'age'], inplace=True)
top_products_df = df.drop(columns=['product_name', 'customerID', 'date', 'time', 'saleID', 'payment_method', 'county'])
grouped_category = top_products_df.groupby('sub_category').agg(quantity=('quantity', 'sum'),
                                                               profit=('profit', 'mean')).reset_index()
county_profit_df = df.groupby('county').agg(profit=('profit', 'mean')).reset_index()
#new column names for the data table
new_columns = ['SUBCATEGORY', 'QUANTITY', 'PROFIT']
#linked stylesheets
external_stylesheets = ['assets/sales_styles.css', dbc.themes.DARKLY]

#functionss
def get_top_products(df, n=10):
    df_sorted = df.sort_values(by='quantity', ascending=False)
    top_products = df_sorted.head(n)
    return top_products
#figures
figure2=px.pie(county_profit_df, names='county', values='profit', hole=0.2)
figure2.update_layout(margin=dict(l=40, r=40, t=40, b=0), 
                      paper_bgcolor='rgb(40, 37, 37)', width=340, height=250, 
                      title=dict(text='Profit by Location', font=dict(family='Arial', color='#f0e8e7')),
                      legend=dict(
                        font=dict(
                            color="white"  
                        ))
                    )

fig_bubble = px.scatter(df, x='category', y='county', color='segment')
fig_bubble.update_layout(
        plot_bgcolor='rgb(40, 37, 37)',
        paper_bgcolor='rgb(40, 37, 37)',
        font_color='white',
        width=870,
        height=338,
        margin=dict(l=5, r=5, t=80, b=5),
        title=dict(text="Profit by County and Category", font=dict(family='Arial', color='#f0e8e7')),
        title_x = 0.5
)
fig_bubble.update_xaxes(showgrid=True, gridcolor='dimgray')
fig_bubble.update_yaxes(showgrid=True, gridcolor='dimgray')
app = Dash(__name__, external_stylesheets=external_stylesheets)

sidebar = html.Div(
    [
        html.Img(src='assets/logo2.png', className='logo-img'),
        html.Hr(style={'margin-bottom':0}),
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
    ], className='navbar')], className='sidebar'
)
content = html.Div(
    [
        html.H1(id='header-sales', children=['SALES DASHBOARD']),
        html.Div( 
            className='header-icons',
            children=[
                dbc.NavLink(children=[DashIconify(icon="mdi:home", className='icon-header'),], href="http://127.0.0.1:5000/"),  
                dbc.NavLink(children=[DashIconify(icon="mdi:account", className='icon-header'),], href="/"),  
            ],
        ),
        #dmc.Divider(className='divider', label = 'Stats',  labelPosition='center', size=4),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row([
                            dbc.Col([
                                dmc.Group(
                                    #position='center',
                                    className='stats',
                                    spacing='xs',
                                    style={'margin-top':10, 'flex-direction':'column', 'background-color': 'rgb(227, 66, 52)',
                                            'border': '2px solid rgb(40, 37, 37)', 'border-radius': '25px'},
                                    children=[
                                        html.Div(id='dummy-input', style={'display':'none'}),
                                        dmc.Text('Customers', size='xs', color='white', style={'font-family':'IntegralCF-RegularOblique'}),
                                        dmc.Text(id='totalcust', size='xl', style={'font-family':'IntegralCF-ExtraBold'}),
                                        dmc.Text('Total Customers', id = 'churn_rate', size='xs', color='white', style={'font-family':'IntegralCF-RegularOblique'})
                                    ]
                                )
                            ], className='stats-col'),
                            dbc.Col([
                                dmc.Group(
                                    #position='center',
                                    className='stats',
                                    spacing='xs',
                                    style={'margin-top':10, 'flex-direction':'column', 'background-color': 'rgb(70, 130, 180)',
                                            'border': '2px solid rgb(40, 37, 37)', 'border-radius': '25px'},
                                    children=[
                                        html.Div(id='dummy-input_two', style={'display':'none'}),
                                        dmc.Text('Sales', size='xs', color='white', style={'font-family':'IntegralCF-RegularOblique'}),
                                        dmc.Text(id='totalsales', size='xl', style={'font-family':'IntegralCF-ExtraBold'}),
                                        dmc.Text('December Sales', size='xs', color='white', style={'font-family':'IntegralCF-RegularOblique'})
                                    ]
                                )
                            ], className='stats-col')
                        ], className='stats-row-1'),
                        #dmc.Divider(label = 'Income',  labelPosition='center', size='xl'),
                        dbc.Row([
                            dbc.Col([
                                dmc.Group(
                                    #position='center',
                                    className='stats',
                                    spacing='xs',
                                    style={'margin-top':10, 'flex-direction':'column', 'background-color': 'rgb(80, 200, 120)',
                                            'border': '2px solid rgb(40, 37, 37)', 'border-radius': '25px'},
                                    children=[
                                        html.Div(id='dummy-input_three', style={'display':'none'}),
                                        dmc.Text('Revenue', size='xs', color='white', style={'font-family':'IntegralCF-RegularOblique'}),
                                        dmc.Text(id='totalrevenue', size='xl', style={'font-family':'IntegralCF-ExtraBold'}),
                                        dmc.Text('December Revenue', size='xs', color='white', style={'font-family':'IntegralCF-RegularOblique'})
                                    ]
                                )
                            ], className='stats-col'),
                            dbc.Col([
                                dmc.Group(
                                    #position='center',
                                    className='stats',
                                    spacing='xs',
                                    style={'margin-top':10, 'flex-direction':'column', 'background-color': 'rgb(192, 132, 20)',
                                            'border': '2px solid rgb(40, 37, 37)', 'border-radius': '25px'},
                                    children=[
                                        html.Div(id='dummy-input_four', style={'display':'none'}),
                                        dmc.Text('Profit', size='xs', color='white', style={'font-family':'IntegralCF-RegularOblique'}),
                                        dmc.Text(id='averageprofit', size='xl', style={'font-family':'IntegralCF-ExtraBold'}),
                                        dmc.Text('December Profit', size='xs', color='white', style={'font-family':'IntegralCF-RegularOblique'})
                                    ]
                                )
                            ], class_name='stats-col')
                        ], className='stats-row-2')
                    ], className='stats-cont'
                ),
                dbc.Col(
                    [
                        html.Div(className='btn btn-outline-light bar-radio', children=[dcc.RadioItems(options=['profit', 'price', 'quantity'], 
                                                                                                               value='price', labelStyle={'margin-right': '40px'},
                                                                                                               id='controls-and-radio-item', inline=True)]),
                        html.Div(className='six-columns plot-container', children=[dcc.Graph(figure={}, id='controls-and-graph', config={"displaylogo": False,'modeBarButtonsToRemove': ['pan2d','lasso2d','autoScale2d','resetScale2d','select2d']},)]),
                    ], class_name='hist-cont'
                )
            ], className='first-row', style={'height': '50vh',
                   'margin-top': '1px', 
                   'margin-bottom': '20px'}
        ),
        dmc.Divider(className='divider', label = 'Profits',  labelPosition='center', size='4'),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            id='data-table', className='six-columns', 
                                children=[dash_table.DataTable(data=get_top_products(grouped_category).to_dict('records'),
                                                               columns=[{'name': column.replace('_', ' ').upper(), 'id':column} for column in grouped_category.columns], 
                                                               page_size=10, style_data={ 'border': '0px'},
                                                               style_data_conditional=[{'if': {'row_index': 'odd'},'backgroundColor': 'rgb(40, 37, 37)',}])],
                            title='Top Selling Products', style={'margin-top': '10px'}
                        )
                    ]
                ),
                dbc.Col(
                    [
                        html.Div(
                            id='pie-chart-sales', className='six-columns', children=[dcc.Graph(figure=figure2, config={"displaylogo": False,},)]
                        )
                    ]
                )
            ],  className='second-row', style={'margin-top': '10px'}
        ), 
    ], className='content'
)

# App layout
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, width=3, className='sidebar'),
                dbc.Col(content, width=9),
            ],
            style={"height": "100vh"}
        ),
    ],
    fluid=True
)

#figure2.update_layout(margin=dict(l=40, r=25, t=45, b=20), height=300,  width=340 )
#update customer numbers
@callback(
        Output('totalcust','children'),
        Input('dummy-input', 'children')
)
def update_customers(dummy_input):
    unique_customers = df['customerID'].nunique()
    return "{:,}".format(unique_customers)
#update sales numbers
@callback(
        Output('totalsales','children'),
        Input('dummy-input_two', 'children')
)
def update_customers(dummy_input_two):
    total_sales = df['saleID'].count()
    return "{:,}".format(total_sales)
#update revenue numbers
@callback(
        Output('totalrevenue','children'),
        Input('dummy-input_three', 'children')
)
def update_customers(dummy_input_three):
    total_revenue = df['price'].sum()
    return "{:,.2f}".format(total_revenue)
#update average profit
@callback(
        Output('averageprofit','children'),
        Input('dummy-input_four', 'children')
)
def update_customers(dummy_input_four):
    avg_profit = df['profit'].mean()
    return "{:,.3f}".format(avg_profit)
#update the bar graph according to use input
@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='category', y=col_chosen, histfunc='avg')
    fig.update_layout(
        plot_bgcolor='rgb(40, 37, 37)',
        #paper_bgcolor='#212121',
        paper_bgcolor='rgb(40, 37, 37)',
        font_color='white',
        width=450,
        height=250,
        margin=dict(l=5, r=5, t=30, b=5),
        yaxis = dict(showgrid=False),
        title=dict(text='Categories Characteristics', font=dict(family='Arial', color='#f0e8e7'))
    )
    fig.update_traces(marker_color='#be3144')
    return fig

if __name__ == '__main__':
    app.run(debug=False, port=8050)
