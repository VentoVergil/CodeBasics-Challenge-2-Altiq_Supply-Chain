import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import metrics

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

merged_frame = order_lines.reset_index().merge(customer_target[['customer_id','customer_name','city']],how = 'left')
merged_frame = merged_frame.merge(product,how = 'left')
merged_frame.set_index('order_id',inplace = True)

merged_frame['duration'] = merged_frame['actual_delivery_date'] - merged_frame['order_placement_date']
merged_frame['week'] = merged_frame['order_placement_date'].dt.isocalendar().week
merged_frame['month'] = merged_frame['order_placement_date'].dt.month_name()

# print(merged_frame.pivot_table(index = 'category',values = 'order_qty',columns = 'city',aggfunc = 'sum'))

# merged_frame.to_csv('merged.csv')

# check for duplicated data == Nil, CHeck for NA == Nil

# Order Lines 1st March 2022 to 30th August 2022
merged_frame.sort_index(key = lambda x: x.str.extract(r'[a-zA-Z]{3,}(\d+)',expand = False),inplace = True)

lifr = metrics.livo(merged_frame)[0]  # line fill rate 66

vofr = metrics.livo(merged_frame)[1]  # volume fill rate 97

ot = metrics.ifotif(merged_frame)[0]  # on time delivery

ifu = metrics.ifotif(merged_frame)[1]  # in full delivery

otif = metrics.ifotif(merged_frame)[2]  # on time in full delivery

'''cv = {'target':customer_target.describe().loc['mean'][['ontime_target%','infull_target%','otif_target%']].tolist(),
      'ours':[ot,ifu,otif]}
tr = pd.DataFrame(cv,index = ['ot','ifu','otif'])'''

'''for group, data in merged_frame.groupby('city'):
    print(f'LIFR% of {group} = {round(metrics.livo(data)[0])}')
    print(f'VOFR% of {group} = {round(metrics.livo(data)[1])}')
    print(f'OT% of {group} = {round(metrics.ifotif(data)[0])}')
    print(f'IF% of {group} = {round(metrics.ifotif(data)[1])}')
    print(f'OTIF% of {group} = {round(metrics.ifotif(data)[2])}')
    print()

for group, data in merged_frame.groupby('customer_name'):
    print(f'LIFR% of {group} = {round(metrics.livo(data)[0])}')
    print(f'VOFR% of {group} = {round(metrics.livo(data)[1])}')
    print(f'OT% of {group} = {round(metrics.ifotif(data)[0])}')
    print(f'IF% of {group} = {round(metrics.ifotif(data)[1])}')
    print(f'OTIF% of {group} = {round(metrics.ifotif(data)[2])}')
    print()'''

'''for group, data in merged_frame.groupby('city'):
    # print(f'LIFR% of {group} = {round(metrics.livo(data)[0])}')
    # print(f'VOFR% of {group} = {round(metrics.livo(data)[1])}')
    print(f'OT% of {group} = {round(metrics.ifotif(data)[0])}')
    print(f'IF% of {group} = {round(metrics.ifotif(data)[1])}')
    print(f'OTIF% of {group} = {round(metrics.ifotif(data)[2])}')
    print()'''


'''tr.plot(kind='bar')
plt.show()
'''

'''variables = ['lifr', 'vofr', 'ot', 'ifu', 'otif']
for i in variables:
    print(f'{i} = {eval(i)}')'''

'''v = merged_frame['On Time In Full'].value_counts(normalize = True)
plt.pie(v,labels = v.index,autopct = '%.0f%%')
plt.show()'''

acc = merged_frame[merged_frame['city'] == 'Surat']

print(metrics.ifotif(acc)[0])
