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
import sys

# checking for filename 
if(len(sys.argv) > 1):
    filename = sys.argv[1] 
    output_filename = filename[0:-4] + '_edit.csv'
else:
    filename = 'summary.csv'
    output_filename = 'summary_edit.csv'

unique_arr = [[]]

with open(filename, 'r') as f, open(output_filename, 'w') as nf:
    reader = csv.reader(f)
    writer = csv.writer(nf)
    for row in reader:
        if (row[1], row[3]) not in unique_arr:
            unique_arr.append((row[1], row[3]))
            writer.writerow(row)

# print(unique_arr)
