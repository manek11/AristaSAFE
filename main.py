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

import csv

unique_arr = [[]]

with open('summary.csv', 'r') as f, open('summary_edit.csv', 'w') as nf:
    reader = csv.reader(f)
    writer = csv.writer(nf)
    for row in reader:
        print(row)
        if (row[1], row[3]) not in unique_arr:
            unique_arr.append((row[1], row[3]))
            writer.writerow(row)

# print(unique_arr)
