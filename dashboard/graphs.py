import plotly.express as px
from dashboard.data_handling import *


figure_sales_segment = px.pie(df_segments,
                              values='Sales',
                              names='Segment',
                              title='Sales by Segment',
                              hole=0.5,
                              height=380)

figure_orders = px.bar(df_orders_amount,
                       x='Segment',
                       y='Amount',
                       color='Segment',
                       text='Amount',
                       title='Orders by Segment',
                       height=380)

figure_sales_by_date = px.line(df_time, title='Sales by Date', height=380)

figure_sales_by_subcategory = px.bar(df_category,
                                     x='Sub-Category',
                                     y='Sales',
                                     title='Sales by Sub-Category',
                                     height=380)

figure_shipping = px.histogram(df, x=df['Shipping Time'].dt.days, title='Shipping Time', height=380)

figure_subcategories = px.scatter(df_subcategories,
                                  x='Average_Deal_Size',
                                  y='Customers',
                                  color='Category',
                                  size='Sales_sum',
                                  title='Average Sales and Customers by Sub-Category',
                                  height=380)
