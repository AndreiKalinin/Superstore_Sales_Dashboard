import pandas as pd


df = pd.read_excel('data.xls').sort_values(by='Ship Mode', key=lambda x: x.str.len())
df['Shipping Time'] = df['Ship Date'] - df['Order Date']

df_segments = df.groupby('Segment', as_index=False).agg({'Sales': 'sum'})
df_orders_amount = df.groupby('Segment', as_index=False).agg({'Order ID': 'count'}) \
                     .rename(columns={'Order ID': 'Amount'})
df_time = df.groupby('Order Date').agg({'Sales': 'sum'})
df_category = df.groupby('Sub-Category', as_index=False).agg({'Sales': 'sum'})

df_subcategories = df.groupby(['Category', 'Sub-Category'], as_index=False) \
                     .agg({'Sales': ['mean', 'sum'], 'Customer ID': pd.Series.nunique})
df_subcategories.columns = ['Category', 'Sub-Category', 'Average_Deal_Size', 'Sales_sum', 'Customers']
