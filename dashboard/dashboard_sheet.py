from dash import Dash
from dash.dependencies import Input, Output

import plotly.io as io
from dashboard.formatting_functions import *
from dashboard.cards import *
from dashboard.graphs import *
from dashboard.filters import *
from dashboard.data_handling import *

io.templates.default = 'seaborn'

# app layout
app = Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ])
app.layout = html.Div([dbc.Row(html.H1('Superstore Sales')),
                       dbc.Row([
                           dbc.Col([html.Div('Region', style={'font-size': '20px', 'margin-bottom': '10px'}),
                                    html.Div(region_selector)], width={'size': 4}),
                           dbc.Col([html.Div('Category', style={'font-size': '20px', 'margin-bottom': '10px'}),
                                    html.Div(category_selector)], width={'size': 4}),
                           dbc.Col([html.Div('Date range', style={'font-size': '20px', 'margin-bottom': '10px'}),
                                    html.Div(date_picker)], width={'size': 4})
                       ], style={'margin-bottom': '20px'}),
                       dbc.Row([dbc.Col(dbc.Card(card_sales_sum, outline=True), width={'size': 3}),
                                dbc.Col(dbc.Card(card_avg_check, outline=True), width={'size': 3}),
                                dbc.Col(dbc.Card(card_customers, outline=True), width={'size': 3}),
                                dbc.Col(dbc.Card(card_avg_per_user, outline=True), width={'size': 3}),
                                ], style={'margin-bottom': '20px'}),
                       dbc.Row([dbc.Col(dcc.Graph(id='sales_by_segment', figure=figure_sales_segment),
                                        width={'size': 3}),
                                dbc.Col(dcc.Graph(id='orders_by_segment', figure=figure_orders),
                                        width={'size': 3}),
                                dbc.Col(dcc.Graph(id='shipping_time', figure=figure_shipping),
                                        width={'size': 3}),
                                dbc.Col(dcc.Graph(id='subcategories', figure=figure_subcategories),
                                        width={'size': 3})
                                ],
                               style={'margin-bottom': '20px'}),
                       dbc.Row([dbc.Col(dcc.Graph(id='daily_sales', figure=figure_sales_by_date),
                                        width={'size': 6}),
                                dbc.Col(dcc.Graph(id='sales_by_category', figure=figure_sales_by_subcategory),
                                        width={'size': 6})],
                               style={'margin-bottom': '20px'})], style={'margin-left': '40px', 'margin-right': '40px'})


# callback
@app.callback([Output(component_id='sales_sum_primary', component_property='children'),
               Output(component_id='sales_sum_secondary', component_property='children'),
               Output(component_id='sales_sum_secondary', component_property='style'),
               Output(component_id='avg_check_primary', component_property='children'),
               Output(component_id='avg_check_secondary', component_property='children'),
               Output(component_id='avg_check_secondary', component_property='style'),
               Output(component_id='customers_primary', component_property='children'),
               Output(component_id='customers_secondary', component_property='children'),
               Output(component_id='customers_secondary', component_property='style'),
               Output(component_id='avg_per_user_primary', component_property='children'),
               Output(component_id='avg_per_user_secondary', component_property='children'),
               Output(component_id='avg_per_user_secondary', component_property='style'),
               Output(component_id='sales_by_segment', component_property='figure'),
               Output(component_id='orders_by_segment', component_property='figure'),
               Output(component_id='shipping_time', component_property='figure'),
               Output(component_id='subcategories', component_property='figure'),
               Output(component_id='daily_sales', component_property='figure'),
               Output(component_id='sales_by_category', component_property='figure')],
              [Input(component_id='region_selector', component_property='value'),
               Input(component_id='category_selector', component_property='value'),
               Input(component_id='date_picker', component_property='start_date'),
               Input(component_id='date_picker', component_property='end_date')])
def update_charts_and_cards(reg, categ, start_date, end_date):
    """Update all dashboards elements according to selected values"""
    chart_data = df[(df['Region'].isin(reg)) & (df['Category'].isin(categ))
                    & (df['Order Date'] >= start_date) & (df['Order Date'] <= end_date)]
    start_ytd = pd.to_datetime(start_date) + pd.DateOffset(years=-1)
    end_ytd = pd.to_datetime(end_date) + pd.DateOffset(years=-1)
    chart_data_ytd = df[(df['Region'].isin(reg)) & (df['Category'].isin(categ))
                        & (df['Order Date'] >= start_ytd) & (df['Order Date'] <= end_ytd)]
    value_sales_primary = chart_data['Sales'].sum()
    value_sales_secondary = chart_data['Sales'].sum() / chart_data_ytd['Sales'].sum() - 1
    value_avg_check_primary = chart_data['Sales'].mean()
    value_avg_check_secondary = chart_data['Sales'].mean() / chart_data_ytd['Sales'].mean() - 1
    value_customers_primary = chart_data['Customer ID'].nunique()
    value_customers_secondary = chart_data['Customer ID'].nunique() / chart_data_ytd['Customer ID'].nunique() - 1
    value_sales_per_user_primary = value_sales_primary / value_customers_primary
    value_sales_per_user_secondary = value_sales_per_user_primary / chart_data_ytd['Sales'].sum() * chart_data_ytd[
        'Customer ID'].nunique() - 1
    figure_sales_by_segment = px.pie(chart_data, values='Sales', names='Segment', title='Sales by Segment', hole=0.5)
    figure_sales_by_segment.update_layout(margin=dict(t=50, b=50), title_x=0.05)
    figure_sales_by_segment.update_traces(hovertemplate='Segment: %{label} <br>Sales: %{value:,.0f}<extra></extra>')

    figure_orders_by_segment = px.bar(chart_data.groupby('Segment', as_index=False)
                                      .agg({'Order ID': 'count'})
                                      .rename(columns={'Order ID': 'Amount'}),
                                      x='Segment',
                                      y='Amount',
                                      color='Segment',
                                      text='Amount',
                                      title='Orders by Segment')
    figure_orders_by_segment.update_traces(hovertemplate='Segment: %{x} <br>Orders: %{y} <extra></extra>')
    figure_orders_by_segment.update_yaxes(title='Orders')
    figure_orders_by_segment.update_layout(showlegend=False, margin=dict(t=50, b=50), title_x=0.05)

    figure_shipping_time = px.histogram(chart_data,
                                        x=chart_data['Shipping Time'].dt.days,
                                        title='Shipping Time',
                                        height=380)
    figure_shipping_time.update_xaxes(title='Days')
    figure_shipping_time.update_yaxes(title='Orders')
    figure_shipping_time.update_layout(margin=dict(t=50, b=50), title_x=0.05)
    figure_shipping_time.update_traces(hovertemplate='Shipping time: %{x} <br>Orders: %{y:,.0f}<extra></extra>')

    chart_data_agg = chart_data.groupby(['Category', 'Sub-Category'], as_index=False) \
                               .agg({'Sales': ['mean', 'sum'], 'Customer ID': pd.Series.nunique})
    chart_data_agg.columns = ['Category', 'Sub-Category', 'Average_Deal_Size', 'Sales_sum', 'Customers']
    figure_sales_and_customers = px.scatter(chart_data_agg,
                                            x='Average_Deal_Size',
                                            y='Customers',
                                            color='Category',
                                            size='Sales_sum',
                                            title='Average Sales and Customers by Sub-Category',
                                            height=380)
    figure_sales_and_customers.update_layout(margin=dict(t=50, b=50), title_x=0.05)
    figure_sales_and_customers.update_traces(hovertemplate='Shipping time: %{x} <br>Orders: %{y:,.0f}<extra></extra>')

    figure_daily_sales = px.line(chart_data.groupby('Order Date').agg({'Sales': 'sum'}), title='Sales by Date')
    figure_daily_sales.update_yaxes(title='Sales')
    figure_daily_sales.update_layout(showlegend=False,
                                     xaxis={'rangeslider': {'visible': True}},
                                     margin=dict(t=50, b=50),
                                     title_x=0.05)
    figure_daily_sales.update_traces(hovertemplate='Date: %{x} <br>Sales: %{y:,.0f}<extra></extra>')

    figure_sales_by_category = px.bar(chart_data.groupby(['Sub-Category', 'Segment'], as_index=False)
                                      .agg({'Sales': 'sum'}),
                                      x='Sub-Category',
                                      y='Sales',
                                      color='Segment',
                                      title='Sales by Sub-Category')
    figure_sales_by_category.update_layout(margin=dict(t=50, b=50),
                                           title_x=0.05,
                                           xaxis={'categoryorder': 'total ascending'})
    figure_sales_by_category.update_xaxes(categoryorder='total descending')
    figure_sales_by_category.update_traces(hovertemplate='Sub-Category: %{x} <br>Sales: %{y:,.0f}<extra></extra>')

    return num_format(value_sales_primary), percent_format(value_sales_secondary), value_color(value_sales_secondary), \
        num_format(value_avg_check_primary), percent_format(value_avg_check_secondary), \
        value_color(value_avg_check_secondary), \
        num_format(value_customers_primary), percent_format(value_customers_secondary), \
        value_color(value_customers_secondary), \
        num_format(value_sales_per_user_primary), percent_format(value_sales_per_user_secondary), \
        value_color(value_sales_per_user_secondary), \
        figure_sales_by_segment, figure_orders_by_segment, figure_shipping_time, figure_sales_and_customers, \
        figure_daily_sales, figure_sales_by_category
