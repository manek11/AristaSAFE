'''

Author: Manek Gujral 
Created: 19 Oct, 2021

Steps:
1) Import needed libs
2) open excel file to analyze
3) 4 columns: Timestamp, DeviceName, Message, Event
4) iterate through device column while collecting in a dictionary and check if it already exists
5) if it does not exist -> add device and corresponding event
6) if it exists -> check if event already exists 
7)              -> if NO: log
8)              -> if YES: delete row

'''

# usage: python3 main.py <filename.csv>
# default assumes file called summary.csv : python3 main.py

import csv
import os
from os import read
import sys

# checking for filename 
if(len(sys.argv) > 1):
    filename = sys.argv[1] 
    output_filename = filename[0:-4] + '_edit.csv'
else:
    filename = 'summary.csv'
    output_filename = 'summary_edit.csv'

# initialize needed lists 
unique_arr = []
counter_arr = []
new_file_data = []

# initialize new columns
column_count = "Number of Occurences"
column_start = "First Occurence"
column_end = "Last Occurence"

# duplicate check
with open(filename, 'r') as f, open(output_filename, 'w') as nf:
    reader = csv.reader(f)
    writer = csv.writer(nf)

    for row in reader:

        if (row[1], row[3]) not in unique_arr:
            unique_arr.append((row[1], row[3]))
            counter_arr.append(1)

            if(reader.line_num == 1):
                row.append(column_count)
                row.append(column_start)
                row.append(column_end)

            else:
                row.append(str(1))
                row.append(row[0])
                row.append(row[0])
          
            new_file_data.append(row)    

        else:
            idx = [index for index in range(len(unique_arr)) if unique_arr[index] == (row[1], row[3])]
            counter_arr[idx[0]] += 1
            curr_row_timestamp = row[0]
            old_row_first_timestamp = new_file_data[idx[0]][5]
            old_row_last_timestamp = new_file_data[idx[0]][6]
            new_file_data[idx[0]][4] = str(counter_arr[idx[0]])

            if curr_row_timestamp > old_row_last_timestamp:
                new_file_data[idx[0]][6] = curr_row_timestamp
                
            elif curr_row_timestamp < old_row_first_timestamp:
                new_file_data[idx[0]][5] = curr_row_timestamp
            
    writer.writerows(new_file_data)

    sum = 0
    for i in range(len(new_file_data)):
        if (i != 0):
            sum+=int(new_file_data[i][4])

    print("Total entrires: " + str(sum))    


