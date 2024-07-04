from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import dash_mantine_components as dmc
from datetime import datetime, timedelta

df = pd.read_csv('modified_sales.csv')
df.drop(columns=['saleID', 'time', 'staff_no', 'staff_name',
                 'productID', 'product_name', 'stock', 'discount'], inplace=True)
df_customers = pd.read_csv('customers.csv')

#create grouped bar chart and date range picker
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
min_date = df['date'].min()
# Set the start_date to the minimum date
start_date = min_date
# Set the end_date to the minimum date plus 7 days
end_date = min_date + timedelta(days=5)
date_range_picker = dcc.DatePickerRange(
    id='date-range-picker',
    className= 'date-range-picker',
    start_date=start_date,
    #end_date=df['date'].max(),
    end_date = end_date,
    display_format='DD/MM/YYYY',
    style={'font-size':'small', 'background-color': 'rgb(40, 37, 37)', 'color':'white'}
)

# Create the groupted bar chart
bar_chart = dcc.Graph(id='bar-chart', config={"displaylogo": False,'modeBarButtonsToRemove': ['pan2d','lasso2d','autoScale2d','resetScale2d','select2d']},)
#create the data table
top_customers = df.groupby('customer_name').agg(revenue=('price','sum')).reset_index().round(2)
def get_top_customers(df, n=10):
    df_sorted = df.sort_values(by='revenue', ascending=False)
    top_products = df_sorted.head(n)
    return top_products

#create the pie chart
corporate_consumer = df.groupby('segment').agg(revenue=('price','sum')).reset_index()
fig_pie = px.pie(corporate_consumer, names='segment', values='revenue',
                 color_discrete_map={'Consumer' : 'rgb(3, 3, 182)', 'Corporate' : 'rgb(1, 156, 1)', 'Home Office':'rgb(178, 8, 8)'})
fig_pie.update_layout(margin=dict(l=10, r=0, t=40, b=0), 
                      paper_bgcolor='rgb(40,37,37)', width=269, height=245,
                      title=dict(text='Revenue by Segment', font=dict(family='Arial', color='#f0e8e7')))
#create the bar chart
age_bins = [0, 18, 25, 35, 45, 55, 65, 100]
age_labels = ['0-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']
df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels, include_lowest=True)
revenue_by_age_group = df.groupby('age_group').agg(revenue=('price','sum')).reset_index()
fig_bar = px.bar(revenue_by_age_group, x='age_group', y='revenue')
fig_bar.update_layout(
        plot_bgcolor='rgb(40, 37, 37)',
        paper_bgcolor='rgb(40, 37, 37)',
        font_color='white',
        width=300,
        height=250,
        margin=dict(l=0, r=5, t=80, b=5),
        title=dict(text='Total Revenue by Age Group', font=dict(family='Arial', color='#f0e8e7')),
        title_x = 0.5,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left",  x=0)
)
fig_bar.update_xaxes(showgrid=True, gridcolor='dimgray')
fig_bar.update_yaxes(showgrid=True, gridcolor='dimgray')
fig_bar.update_traces(marker_color='#be3144')
#create the line chart
df_customers['Date Joined'] = pd.to_datetime(df_customers['Date Joined'])
data = df_customers.groupby(pd.Grouper(key='Date Joined', freq='2Q'))['customer_ID'].count().reset_index()
data.columns = ['date', 'customers']
fig_line = px.line(data, x='date', y='customers', markers=True)
fig_line.update_traces(line_color='red')
fig_line.update_layout(
        plot_bgcolor='rgb(40, 37, 37)',
        paper_bgcolor='rgb(40, 37, 37)',
        font_color='white',
        width=300,
        height=250,
        margin=dict(l=5, r=5, t=80, b=5),
        title=dict(text='Customer Numbers', font=dict(family='Arial', color='#f0e8e7')),
        title_x = 0.5
)
fig_line.update_xaxes(showgrid=True, gridcolor='dimgray')
fig_line.update_yaxes(showgrid=True, gridcolor='dimgray')

#custom css styles
custom_styles = {
    'row': {
        'display': 'grid',
        'grid-template-columns': 'repeat(3, 1fr)',
        'grid-gap': '5px',
    }
}
external_stylesheets = ['static/css/customers_styles.css', dbc.themes.DARKLY]

app = Dash(__name__, external_stylesheets=external_stylesheets)
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

content = html.Div(
    [
        html.H1(id='header-prod', children=['CUSTOMERS DASHBOARD']),
        html.Div( 
            className='header-icons-prod',
            children=[
                dbc.NavLink(children=[DashIconify(icon="mdi:home", className='icon-header-prod'),], href="http://127.0.0.1:5000/"),  
                dbc.NavLink(children=[DashIconify(icon="mdi:account", className='icon-header-prod'),], href="/"),  
            ],
        ),
        dmc.Divider(className='prod-divider', label = 'Stats',  labelPosition='center', size=2),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dmc.Group(
                            #position='center',
                            className='stats-cust stats_one',
                            spacing='xs',
                            style={'flex-direction':'column'},
                            children=[
                                html.Div(id='dummy-input', style={'display':'none'}),
                                dmc.Text('TOTAL CUSTOMERS', size='xs', color='white', style={'font-family':'IntegralCF-RegularOblique'}),
                                dmc.Text(id='totalcust', size='xl', style={'font-family':'IntegralCF-ExtraBold'}),
                            ]
                        )
                    ], className='cust-stats-col'
                ),
                dbc.Col(
                    [
                        dmc.Group(
                            #position='center',
                            className='stats-cust stats_two',
                            spacing='xs',
                            style={'flex-direction':'column'},
                            children=[
                                html.Div(id='dummy-input_two', style={'display':'none'}),
                                dmc.Text('AVERAGE AGE', size='xs', color='white', style={'font-family':'IntegralCF-RegularOblique'}),
                                dmc.Text(id='avgage', size='xl', style={'font-family':'IntegralCF-ExtraBold'}),
                            ]
                        )
                    ], className='cust-stats-col'
                ),
                dbc.Col(
                    [
                        dmc.Group(
                            #position='center',
                            className='stats-cust stats_three',
                            spacing='xs',
                            style={'flex-direction':'column'},
                            children=[
                                html.Div(id='dummy-input_three', style={'display':'none'}),
                                dmc.Text('AVERAGE SPEND', size='xs', color='white', style={'font-family':'IntegralCF-RegularOblique'}),
                                dmc.Text(id='avgspend', size='xl', style={'font-family':'IntegralCF-ExtraBold'}),
                            ]
                        )
                    ], className='cust-stats-col'
                ),
                dbc.Col(
                    [
                        dmc.Group(
                            #position='center',
                            className='stats-cust stats_four',
                            spacing='xs',
                            style={'flex-direction':'column'},
                            children=[
                                html.Div(id='dummy-input_four', style={'display':'none'}),
                                dmc.Text('RETENTION IN MONTHS', size='xs', color='white', style={'font-family':'IntegralCF-RegularOblique'}),
                                dmc.Text(id='retention', size='xl', style={'font-family':'IntegralCF-ExtraBold'}),
                            ]
                        )
                    ], className='cust-stats-col'
                )
            ], className='cust-stats-row'
        ),
        dmc.Divider(className='prod-divider', label = 'Graphs',  labelPosition='center', size=2),
        dbc.Row(
            [
                html.Div(className='grouped-bar-container', children=[
                    html.Label('Select Date Range:'),
                    date_range_picker
                ]),
                bar_chart
            ], className='cust-row-two'
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            id='bar-chart-two', className='chart-cust', children=[dcc.Graph(figure=fig_bar, config={"displaylogo": False,'modeBarButtonsToRemove': ['pan2d','lasso2d','autoScale2d','resetScale2d','select2d']},)]
                        )
                    ]
                ),
                dbc.Col(
                    [
                        html.Div(
                           id='line-chart', className='chart-cust', children=[dcc.Graph(figure=fig_line, config={"displaylogo": False,'modeBarButtonsToRemove': ['pan2d','lasso2d','autoScale2d','resetScale2d','select2d']},)]
                        )
                    ]
                ),
                html.Div(
                            id='pie-chart', className='chart-cust', children=[dcc.Graph(figure=fig_pie)]
                        )
            ], className="cust-row-three"
        )
    ], className='content'
)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, width=3, className='sidebar'),
                dbc.Col(content, width=9),
            ],
            style={"height": "100vh"}
        ),
    ], fluid=True
)

#callbacks
# Define the callback function for date picker bar chart
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('date-range-picker', 'start_date'),
     Input('date-range-picker', 'end_date')]
)
def update_bar_chart(start_date, end_date):
    # Filter the DataFrame for the selected date range
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    # Group the data by segment and calculate the revenue
    segment_revenue = filtered_df.groupby(['date', 'segment'])['price'].sum().reset_index()
    # Create the bar chart
    fig = px.bar(segment_revenue, x='date', y='price', color='segment', 
                 barmode='group', title='Revenue by Segment', 
                 labels={
                     "date": "date",
                     "price": "revenue",
                 },
                 color_discrete_map={'Consumer' : 'rgb(3, 3, 182)', 'Corporate' : 'rgb(1, 156, 1)', 'Home Office':'rgb(178, 8, 8)'})
    #fig.update_layout(xaxis_tickangle=-45)
    fig.update_layout(
        plot_bgcolor='rgb(40, 37, 37)',
        paper_bgcolor='rgb(40, 37, 37)',
        font_color='white',
        #width=440,
        height=340,
        margin=dict(l=5, r=5, t=80, b=5),
        title_x = 0.5,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left",  x=0)    
    )
    fig.update_xaxes(showgrid=True, gridcolor='dimgray')
    fig.update_yaxes(showgrid=True, gridcolor='dimgray')
    return fig

#update total customers
@callback(
        Output('totalcust','children'),
        Input('dummy-input', 'children')
)
def update_products(dummy_input):
    total_customers = df['customerID'].nunique()
    return "{:,}".format(total_customers)

#update total stock
@callback(
        Output('avgage','children'),
        Input('dummy-input_two', 'children')
)
def update_stock(dummy_input_two):
    avg_age = round(df['age'].mean())
    return "{:,}".format(avg_age)

#update avgspend
#update total price
@callback(
        Output('avgspend','children'),
        Input('dummy-input_three', 'children')
)
def update_stock(dummy_input_three):
    df['total_amount'] = df['price'] * df['quantity']
    customer_totals = df.groupby('customerID')['total_amount'].sum()
    average_spend = round(customer_totals.mean())
    return "{:,}".format(average_spend)

#update customer retention
@callback(
        Output('retention','children'),
        Input('dummy-input_four', 'children')
)
def update_stock(dummy_input_four):
    df_customers['join_date'] = pd.to_datetime(df_customers['Date Joined'], dayfirst=True)
    today = pd.Timestamp(datetime.now().date())
    df_customers['age_in_days'] = (today - df_customers['join_date']) / pd.Timedelta(days=1)
    df_customers['age_in_months'] = (df_customers['age_in_days'] / 30.4375).apply(lambda x: int(x))
    average_customer_age_months = round(df_customers['age_in_months'].mean())
    return "{:,}".format(average_customer_age_months)
if __name__ == '__main__':
    app.run(debug=False, port=8051)
