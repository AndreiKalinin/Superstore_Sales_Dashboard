from dash import dcc
from datetime import date
from dashboard.data_handling import df


region_selector = dcc.Dropdown(df.Region.unique(),
                               id='region_selector',
                               multi=True,
                               value=df.Region.unique(),
                               style={'color': 'black'})

category_selector = dcc.Dropdown(df.Category.unique(),
                                 id='category_selector',
                                 multi=True,
                                 value=df.Category.unique())

date_picker = dcc.DatePickerRange(id='date_picker',
                                  min_date_allowed=df['Order Date'].min(),
                                  max_date_allowed=df['Order Date'].max(),
                                  start_date=date(2016, 6, 1),
                                  end_date=date(2016, 8, 31),
                                  display_format='YYYY-MM-DD'
                                  )
