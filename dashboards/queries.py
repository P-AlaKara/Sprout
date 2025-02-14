import dash_ag_grid as dag
from dash import Dash, html, dcc, Input, Output
import pandas as pd
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv(
    "data/customers.csv"
)
df_sales = pd.read_csv('data/modified_sales.csv')
df_sales.drop(columns=['staff_no', 'staff_name', 'customer_name', 'age', 'segment', 
               'product_name', 'stock', 'profit', 'discount', 'productID'], inplace=True)
df_products = pd.read_csv('data/modified_sales.csv')
df_products.drop(columns=['staff_no', 'staff_name', 'customer_name', 'age', 'segment',
                   'profit', 'discount','saleID','date', 'time', 'customerID', 'county',
                   'payment_method', 'quantity'], inplace=True)
columnDefs = [
    {"field": "customer_ID"},
    {"field": "customer_name"},
    {"field": "age"},
    {"field": "segment"},
    {"field": "Date Joined"},
]
#payment_method, ID, time
columnDefsSales = [
    {"field": "date"},
    {"field": "county"},
    {"field": "price"},
    {"field": "quantity"},
    {"field": "category"},
    {"field": "sub_category"},
]
columnDefsProducts = [
    {"field": "productID"},
    {"field": "category"},
    {"field": "stock"},
    {"field": "price"},
    {"field": "sub_category"},
    {"field": 'product_name',},
]

def generate_column_defs(data):
    return [{"headerName": i, "field": i, "flex": 1} for i in data.columns]
navbar = html.Div(
    className="navbar navbar-expand-lg navbar-light",
    children=[
        html.Div(
            className="navbar-header",
            children=[
                html.P(className='heading-text', children=['QUERIES DASHBOARD'])
            ],
            style={"flex": "1"}
        ),
        html.Div(
            className="navbar-nav ml-auto",
            children=[
                html.Div(
                    html.A(
                        DashIconify(icon="mdi:view-dashboard", className='icon-header-quer'),
                        className="nav-item nav-link",
                        href="http://127.0.0.1:8050/",
                        title="Dashboard"
                    ),
                    style={"padding": "0 10px"}
                ),
                html.Div(
                    html.A(
                        DashIconify(icon="mdi:home", className='icon-header-quer'),
                        className="nav-item nav-link",
                        href="http://127.0.0.1:5000/",
                        title="Home"
                    ),
                    style={"padding": "0 10px"}
                ),
                html.Div(
                    html.A(
                        DashIconify(icon="mdi:account", className='icon-header-quer'),
                        className="nav-item nav-link",
                        href="#",
                        title="Account",
                        id="account-icon"
                    ),
                    style={"padding": "0 10px"}
                )
            ],
            style={"display": "flex", "gap": "10px"}
        )
    ],
    style={"display": "flex", "justify-content": "space-between", "padding": "10px"}
)

app.layout = html.Div(
    [
        navbar,
        # Placeholder for account details
        html.Div(id='account-details', style={'position': 'absolute', 'top': 0, 'left': 0, 'width': '100vw', 'height': '100vh', 'backgroundColor': 'rgba(0, 0, 0, 0.5)', 'zIndex': 9999, 'display': 'none', 'alignItems': 'center', 'justifyContent': 'center'}),
        html.Div([
        dcc.Tabs(id='tabs-example', value='tab-1', children=[
            dcc.Tab(label='CUSTOMERS', value='tab-1', className='cust-tab'),
            dcc.Tab(label='SALES', value='tab-2', className='sales-tab'),
            dcc.Tab(label='PRODUCTS', value='tab-3', className='prod-tab'),
        ]),
        html.Div(id='tabs-content-example')
    ]),
    ]
)
@app.callback(Output('tabs-content-example', 'children'),
              Input('tabs-example', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return dag.AgGrid(
            id="styling-inputs-text-inputs",
            className='ag-theme-alpine',
            rowData=df.to_dict("records"),
            columnDefs=generate_column_defs(df),
            defaultColDef={'filter': True, "floatingFilter": True, 'editable': True},
            dashGridOptions={'suppressMenuHide': True, "animateRows": False},
            columnSize="sizeToFit",
            style={"width": "99vw"}
        )
    elif tab == 'tab-2':
        return dag.AgGrid(
            id="styling-inputs-text-inputs",
            rowData=df_sales.to_dict("records"),
            columnDefs=columnDefsSales,
            defaultColDef={'filter': True, "floatingFilter": True, 'editable': True},
            dashGridOptions={'suppressMenuHide': True, "animateRows": False},
            columnSize="sizeToFit",
            style={"width": "99vw"}
        )
    elif tab == 'tab-3':
        return dag.AgGrid(
            id="styling-inputs-text-inputs",
            rowData=df_products.to_dict("records"),
            columnDefs=columnDefsProducts,
            defaultColDef={'filter': True, "floatingFilter": True, 'editable': True, "resizable": True},
            dashGridOptions={'suppressMenuHide': True, "animateRows": False},
            columnSize="sizeToFit",
            style={"width": "99vw"}
        )

'''# Callback to update account details
@app.callback(
    Output('account-details', 'style'),
    Output('account-details', 'children'),
    Input('account-icon', 'n_clicks')
)
def display_account_details(n_clicks):
    if n_clicks is None:
        return {'display': 'none'}, ""

    return {'display': 'flex', 'position': 'absolute', 'top': 0, 'right': 0, 'width': '30vw', 'height': '40vh', 'zIndex': 9999, 'margin-top':'40px', 'justifyContent': 'center', 'background-color':'white'}, dbc.Card(
        dbc.CardBody([
            html.H4(user_data["username"], style={'color': 'black'}),
            html.P(f"Email: {user_data['email']}", style={'color': 'black'}),
            html.P("Password: " + "*" * len(user_data["password"]), style={'color': 'black'}),
        ]),
        style={"width": "18rem", "margin": "auto"}
    )'''

if __name__ == "__main__":
    app.run(debug=False, port=8055)
