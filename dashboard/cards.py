import dash_bootstrap_components as dbc
from dash import html


card_sales_sum = [
    dbc.CardHeader('Total Revenue', style={'text-align': 'center'}),
    dbc.CardBody(
        [
            html.H3(className='card-title', id='sales_sum_primary',
                    style={'text-align': 'center', 'font-size': 36, 'display': 'inline'}),
            html.P(className='card-text',
                   id='sales_sum_secondary',
                   style={'text-align': 'center', 'font-size': 20, 'display': 'inline'}),
        ]
    ),
]

card_avg_check = [
    dbc.CardHeader('Average Deal Size', style={'text-align': 'center'}),
    dbc.CardBody(
        [
            html.H3(className='card-title', id='avg_check_primary',
                    style={'text-align': 'center', 'font-size': 36, 'display': 'inline'}),
            html.P(className='card-text',
                   id='avg_check_secondary',
                   style={'text-align': 'center', 'font-size': 20, 'display': 'inline'}),
        ]
    ),
]

card_customers = [
    dbc.CardHeader('Customers', style={'text-align': 'center'}),
    dbc.CardBody(
        [
            html.H3(className='card-title', id='customers_primary',
                    style={'text-align': 'center', 'font-size': 36, 'display': 'inline'}),
            html.P(className='card-text',
                   id='customers_secondary',
                   style={'text-align': 'center', 'font-size': 20, 'display': 'inline'}),
        ]
    ),
]

card_avg_per_user = [
    dbc.CardHeader('Average Revenue Per Customer', style={'text-align': 'center'}),
    dbc.CardBody(
        [
            html.H3(className='card-title', id='avg_per_user_primary',
                    style={'text-align': 'center', 'font-size': 36, 'display': 'inline'}),
            html.P(className='card-text',
                   id='avg_per_user_secondary',
                   style={'text-align': 'center', 'font-size': 20, 'display': 'inline'}),
        ]
    ),
]
