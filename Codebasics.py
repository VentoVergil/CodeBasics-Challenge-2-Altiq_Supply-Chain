import pandas as pd
import numpy as np
import re


pd.options.display.max_colwidth = 100
pd.options.display.width = 1000
pd.options.display.max_rows = 1000
pd.options.display.max_columns = 100

order_lines = pd.read_csv(r'C:\Users\Te.TE\Documents\Serpent\Data\Code BAsics\C2 Input for '
                          r'participants\fact_order_lines.csv',
                          parse_dates = ['agreed_delivery_date','actual_delivery_date','order_placement_date'],
                          index_col = 'order_id')

customer_target = pd.read_csv(r'C:\Users\Te.TE\Documents\Serpent\Data\Code BAsics\C2 Input for '
                              r'participants\dim_targets_orders_merge.csv')  # customer details and targets

product = pd.read_csv(r'C:\Users\Te.TE\Documents\Serpent\Data\Code BAsics\C2 Input for participants\dim_products.csv')

# check for duplicated data == Nil, CHeck for NA == Nil

merged_frame = order_lines.reset_index().merge(customer_target[['customer_id','customer_name','city']],how = 'left')
merged_frame = merged_frame.merge(product,how = 'left')
merged_frame.set_index('order_id',inplace = True)

merged_frame['duration'] = merged_frame['actual_delivery_date'] - merged_frame['order_placement_date']
merged_frame['week'] = merged_frame['order_placement_date'].dt.isocalendar().week
merged_frame['month'] = merged_frame['order_placement_date'].dt.month_name()

# Order Lines 1st March 2022 to 30th August 2022
merged_frame.sort_index(key = lambda x: x.str.extract(r'[a-zA-Z]{3,}(\d+)',expand = False),inplace = True)

merged_frame.to_csv('merged.csv')






