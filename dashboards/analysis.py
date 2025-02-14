from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash_iconify import DashIconify
import dash_mantine_components as dmc
from datetime import datetime, timedelta
import numpy as np
from prophet import Prophet
from statsmodels.tsa.stattools import adfuller
import dash_bootstrap_components as dbc
import flask

df_one = pd.read_csv('data/modified_sales.csv')
df_two = pd.read_csv('data/synthetic.csv')
df_one.drop(columns=['saleID', 'staff_no', 'staff_name', 'customerID','age','county','payment_method','profit',
                 'productID', 'product_name', 'discount'], inplace=True)
df_cust = pd.read_csv('data/customers.csv')

##########################PREDICTION USING TIME SERIES ANALYSIS#######################
#PREPROCESSING
df_two['Date'] = pd.to_datetime(df_two['Date'], dayfirst=False)
tech_data = df_two
# Check stationarity and apply differencing if needed
result = adfuller(tech_data['Quantity'])
if result[1] > 0.05:
    tech_data['Quantity'] = tech_data['Quantity'].diff()
tech_data
# Prepare the data for Prophet
tech_data = tech_data[['Date', 'Quantity']]
tech_data.columns = ['ds', 'y']
tech_data['ds'] = pd.to_datetime(tech_data['ds'], dayfirst=True)

# Create and fit the Prophet model
model = Prophet()
model.fit(tech_data)
# Define the future date range
future = model.make_future_dataframe(periods=60)  # Forecast for next 60 days
# Generate the forecasts
forecast = model.predict(future)
# Filter the forecast data to include only the month of January
january_forecast = forecast[(forecast['ds'].dt.month == 1)]
# Add the forecast for January as a trace
fig_line_weekly = px.line(x=january_forecast['ds'], y=january_forecast['yhat'])
fig_line_weekly.update_layout(
        plot_bgcolor='rgb(40, 37, 37)',
        paper_bgcolor='rgb(40, 37, 37)',
        font_color='white',
        width=870,
        height=450,
        margin=dict(l=5, r=5, t=80, b=5),
        title=dict(text='Daily Forecast', font=dict(family='Arial', color='#f0e8e7')),
        title_x = 0.5
)
fig_line_weekly.update_xaxes(showgrid=True, gridcolor='dimgray')
fig_line_weekly.update_yaxes(showgrid=True, gridcolor='dimgray')
fig_line_weekly.update_traces(line_color='red', line=dict(shape='spline'))
# Calculate the cumulative sum of the forecasted values for January
january_forecast['cumulative_forecast'] = january_forecast['yhat'].cumsum()
# Plot the cumulative line graph
fig_cumulative_line = px.line(x=january_forecast['ds'], y=january_forecast['cumulative_forecast'])
fig_cumulative_line.update_layout(
        plot_bgcolor='rgb(40, 37, 37)',
        paper_bgcolor='rgb(40, 37, 37)',
        font_color='white',
        width=900,
        height=450,
        margin=dict(l=5, r=5, t=80, b=5),
        title=dict(text='Cumulative Forecast', font=dict(family='Arial', color='#f0e8e7')),
        title_x = 0.5
)
fig_cumulative_line.update_xaxes(showgrid=True, gridcolor='dimgray')
fig_cumulative_line.update_yaxes(showgrid=True, gridcolor='dimgray')
# Update line properties
fig_cumulative_line.update_traces(line_color='red', line_shape='spline')

#STOCK OUT RISK ANALYSIS
highest_price = df_one.groupby(['sub_category', 'date']).agg(quantity=('quantity', 'sum')).reset_index()
# Group by subcategory and date, sum the quantities sold
grouped_data = highest_price.groupby(['sub_category', 'date'])['quantity'].sum().reset_index()
# Calculate the total number of days in the period
total_days = grouped_data['date'].nunique()
# Calculate average daily sales for each subcategory
average_daily_sales = grouped_data.groupby('sub_category')['quantity'].sum() / total_days
#goods_stock = df_one.groupby('sub_category')['stock'].sum().reset_index().round({'stock': 0})
goods_stock = df_one.groupby('sub_category')['stock'].sum().reset_index()
# Create a new DataFrame with subcategories and their average daily sales
average_daily_sales_df = pd.DataFrame({'sub_category_one': average_daily_sales.index, 'average_daily_sales': average_daily_sales.values})
result = pd.concat([goods_stock, average_daily_sales_df], axis=1, join='inner')
#result = result.rename(columns={'quantity': 'average_daily_sales'})
result.drop(columns=['sub_category_one'], inplace=True)
result['days'] = (result['stock'] / result['average_daily_sales']).round().astype(int)
fig_stock_out = px.scatter(result, x='stock', y='days',
                 title='Product Stock vs Price',
                 labels={'stock': 'Stock Quantity', 'days': 'Days to Stock Out'},
                 color='sub_category',  # Color-code points by category
                 hover_data=['average_daily_sales'])  
fig_stock_out.update_layout(
        plot_bgcolor='rgb(40, 37, 37)',
        paper_bgcolor='rgb(40, 37, 37)',
        font_color='white',
        width=910,
        height=450,
        margin=dict(l=5, r=5, t=80, b=5),
        title=dict(text='Stock Out Risk', font=dict(family='Arial', color='#f0e8e7')),
        title_x = 0.5
)
fig_stock_out.update_xaxes(showgrid=True, gridcolor='dimgray')
fig_stock_out.update_yaxes(showgrid=True, gridcolor='dimgray')
#CUSTOMER LIFETIME VALUE ANALYSIS
#customer value = avg purchase value * avg number of purchases
#CLV = customer value * avg customer lifespan
customer_value = df_one[['customer_name', 'quantity', 'price', 'segment']]
customer_value['total'] = customer_value['quantity'] * customer_value['price']
customer_value = customer_value.groupby(['customer_name', 'segment']).agg(purchase_value=('total', 'sum')).reset_index()
customer_counts = df_one['customer_name'].value_counts().to_dict()
customer_value['number_purchases'] = customer_value['customer_name'].map(customer_counts)
customer_age = df_cust['age'].to_dict()
customer_value['age'] = customer_value.index.map(customer_age)
customer_value['clv'] = customer_value['purchase_value'] * customer_value['number_purchases']
fig_clv = px.scatter(customer_value, x='age', y='clv',
                 title='Product Stock vs Price',
                 color='segment',  
                 hover_data=['customer_name'])  
fig_clv.update_layout(
        plot_bgcolor='rgb(40, 37, 37)',
        paper_bgcolor='rgb(40, 37, 37)',
        font_color='white',
        width=910,
        height=450,
        margin=dict(l=5, r=5, t=80, b=5),
        title=dict(text='Lifetime Values', font=dict(family='Arial', color='#f0e8e7')),
        title_x = 0.5
)
fig_clv.update_xaxes(showgrid=True, gridcolor='dimgray')
fig_clv.update_yaxes(showgrid=True, gridcolor='dimgray')
#PRODUCT AFFINITY ANALYSIS
product_data = df_one[['sub_category', 'date']]
# Create a dictionary to store dates and corresponding unique items
date_items_dict = {}
# Iterate over the rows of the DataFrame
for _, row in df_one.iterrows():
    # Get the date and sub_category from the current row
    date = row['date']
    sub_category = row['sub_category']
    
    # If the date is not in the dictionary, initialize it with an empty set
    if date not in date_items_dict:
        date_items_dict[date] = set()
    
    # Add the sub_category to the set for the corresponding date
    date_items_dict[date].add(sub_category)
from collections import defaultdict
# Create a dictionary to store item co-occurrences
item_cooccurrences = defaultdict(int)
# Iterate over the dates in date_items_dict
for date, items in date_items_dict.items():
    # Create a set of unique item pairs for the current date
    item_pairs = set((item1, item2) for item1 in items for item2 in items if item1 != item2)    
    # Increment the count for each item pair
    for item_pair in item_pairs:
        item_cooccurrences[item_pair] += 1
# Sort the item co-occurrences by their count in descending order
sorted_cooccurrences = sorted(item_cooccurrences.items(), key=lambda x: x[1], reverse=True)
N = 10
top_cooccurrences = sorted_cooccurrences[:N]
# Create the data for the Dash table
table_data = [
    {"Item Pair": f"{item_pair}", "Co-occurrence Count": count}
    for item_pair, count in top_cooccurrences
]

#link external stylesheets
external_stylesheets = ['assets/analysis.css', dbc.themes.DARKLY]
#initialize dash
app1 = Dash(__name__, external_stylesheets=external_stylesheets)
sidebar = html.Div(
    [
        html.Img(src='assets/logo2.png', className='logo-img'),
        html.Hr(className='hr-analysis', style={'margin':0}),
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
        html.Div(id='header-analysis', children=['ANALYSIS DASHBOARD']),
        html.Div( 
            className='header-icons-prod',
            children=[
                dbc.NavLink(children=[DashIconify(icon="mdi:home", className='icon-header-prod'),], href="http://127.0.0.1:5000/"),  
                dbc.NavLink(children=[DashIconify(icon="mdi:account", className='icon-header-prod'),], href="/"),  
            ],
        ),
        dmc.Divider(className='analysis-divider', label = 'Analysis',  labelPosition='center', size=2),
        dcc.Tabs(parent_className='custom-tabs', className='custom-tabs-container', children=[
            dcc.Tab(label='Demand Prediction', className='custom-tab prediction-tab', selected_className='custom-tab--selected', children=[
                html.Div([
                    dcc.Graph(
                        figure=fig_cumulative_line,
                        config={"displaylogo": False,'modeBarButtonsToRemove': ['pan2d','lasso2d','autoScale2d','resetScale2d','select2d']}
                    ),
                    html.Hr(className='prod-divider'),
                    dcc.Graph(
                        figure=fig_line_weekly, 
                        config={"displaylogo": False,'modeBarButtonsToRemove': ['pan2d','lasso2d','autoScale2d','resetScale2d','select2d']}
                    )
                ])
            ]),
            dcc.Tab(label='Stock Out Risk', className='custom-tab stock-tab', selected_className='custom-tab--selected', children=[
                html.Div([
                    dcc.Graph(
                        figure=fig_stock_out,
                        config={"displaylogo": False,'modeBarButtonsToRemove': ['pan2d','lasso2d','autoScale2d','resetScale2d','select2d']}
                    ),
                    html.Hr(className='graph-bottom')
                ]
                )
            ]),
            dcc.Tab(label='CLV analysis', className='custom-tab clv-tab', selected_className='custom-tab--selected', children=[
                dcc.Graph(
                    figure=fig_clv,
                    config={"displaylogo": False,'modeBarButtonsToRemove': ['pan2d','lasso2d','autoScale2d','resetScale2d','select2d']}
                )
            ]),
            dcc.Tab(label='Product Affinity', className='custom-tab affinity-tab', selected_className='custom-tab--selected', children=[
                 html.Div(
    id='affinity-table', 
    className='affinity', 
    children=[
        dash_table.DataTable(
            data=table_data,
            columns=[
                {"name": "Item Pair", "id": "Item Pair"},
                {"name": "Co-occurrence Count", "id": "Co-occurrence Count"}
            ],
            style_data={'border': '0px', 'fontSize': '16px', 'color': 'white'},
            style_data_conditional=[
                {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(40, 37, 37)'},
                {'if': {'row_index': 'even'}, 'backgroundColor': 'rgb(50, 50, 50)'}
            ],
            style_header={
                'backgroundColor': 'darkred',
                'fontWeight': 'bold',
                'color': 'white',
                'fontSize': '18px'
            },
            style_table={'margin-top': '10px'},
            style_cell={'textAlign': 'left', 'padding': '10px'}
        )
    ],
    title='Product Affinities'
)
            ]),
            
        ])
    ], className='content'
)
app1.layout = dbc.Container(
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

if __name__ == '__main__':
    app1.run(debug=True, port=8054)
