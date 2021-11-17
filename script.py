import pandas as pd
import time
import sys
import os

# function to extract data center city name
def datacenter_city_name(device):
    datacenter = ''
    for char in device[0:4]:
        if not char == '-' and not char.isdigit():
            datacenter += char
    return datacenter

if(len(sys.argv) > 1):
    if(sys.argv[1] != '-h' and os.path.exists(sys.argv[1])):
        fname = sys.argv[1]
    else:   
        print()
        print('usage: python3 script.py <filename.csv>')
        print()
        exit()
else:
    print()
    print('usage: python3 script.py <filename.csv>')
    print()
    exit()

# start time for runtime calculation
t0 = time.time()

# read input filename
df = pd.read_csv(fname)

# sort values before analysis
df.sort_values(['TIMESTAMP', 'DeviceName', 'Event'], inplace=True)
df.reset_index(drop=True, inplace=True)

# make count column and initialize to 1
df['Count'] = 1

# obtain a new dataframe with duplicate count column
count_df = df.groupby(['DeviceName', 'Event']).count()['Count'].to_frame()

# sort values in ascending order to obtain first occurence
df.sort_values(['DeviceName', 'Event', 'TIMESTAMP'], ascending=[1, 1, 1], inplace=True)
df['First Occurence'] = df['TIMESTAMP']
df_1 = df.copy(deep=True)
df.drop(columns=['First Occurence'], inplace=True)

# sort values in descending order to obtain last occurence
df.sort_values(['DeviceName', 'Event', 'TIMESTAMP'], ascending=[1, 1, 0], inplace=True)
df['Last Occurence'] = df['TIMESTAMP']   
df_2 = df.copy(deep=True)
df.drop(columns=['Last Occurence'], inplace=True)

# merge new columns with df
df['First Occurence'] = df_1['First Occurence'].to_numpy()
df['Last Occurence'] = df_2['Last Occurence'].to_numpy()

# drop duplicate entries
df.drop_duplicates(subset={'DeviceName', 'Event'}, inplace=True)
df.reset_index(drop=True, inplace=True)

# make count column in df
for index, row in count_df.iterrows():
    curr_device_name = index[0]
    curr_event = index[1]
    curr_count = row[0]
    curr_idx = df.loc[(df['DeviceName'] == curr_device_name) & (df['Event'] == curr_event)].index
    df.iloc[curr_idx, 4] = curr_count

# sort values before saving
df.sort_values(['DeviceName'], inplace=True)
df.reset_index(drop=True, inplace=True)

output_fname = pd.ExcelWriter(fname[0:-4]+'_output.xlsx', engine='xlsxwriter')

# save data 
df.to_excel(output_fname, sheet_name = 'duplicates_removed', index=False)

# for duplicate flag
duplicates_df = df.loc[df['Count'] > 1].copy(deep=True)
duplicates_df.reset_index(drop=True, inplace=True)

# save duplicate_df in file
duplicates_df.to_excel(output_fname, sheet_name = 'multiple_counts', index=False)

# for sorted flag
sorted_df = df.copy(deep=True)
sorted_df.sort_values(['Event', 'DeviceName'], inplace=True)
sorted_df.reset_index(drop=True, inplace=True) 

# save sorted_df in file
sorted_df.to_excel(output_fname, sheet_name = 'events_sorted', index=False)

# provide data center analysis
dc_analysis_df = sorted_df.copy(deep=True)
dc_analysis_df.drop(columns=['TIMESTAMP', 'Message', 'Count', 'First Occurence', 'Last Occurence'], inplace=True)

dc_analysis_df['DataCenter City Name'] = dc_analysis_df['DeviceName'].apply(datacenter_city_name)

column_names = ['DataCenter City Name', 'DeviceName', 'Event']
dc_analysis_df = dc_analysis_df.reindex(columns=column_names)

duplicateRowsDF = dc_analysis_df[dc_analysis_df.duplicated(['DataCenter City Name', 'Event'], keep=False)]
duplicateRowsDF.reset_index(drop=True, inplace=True)

# save duplicateRowsDF in file
duplicateRowsDF.to_excel(output_fname, sheet_name = 'dc_analysis', index=False)

# save the entire file with multiple sheets
output_fname.save()

# runtime analysis
t1 = time.time()
total = t1-t0

print()
print(fname[0:-4]+'_output.xlsx generated')
print()
print('Total Runtime: ' + str(round(total, 2)) + ' s')
print()