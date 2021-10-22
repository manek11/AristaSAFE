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

# usage: python3 main.py <filename.csv> -duplicate or -sorted
# default assumes file called summary.csv : python3 main.py

import csv
import os
from os import dup, read
import sys
from alive_progress import alive_bar
from time import sleep


def datacenter_name(device):
    datacenter = ''
    for char in device[0:5]:
        if not char.isdigit():
            datacenter += char
    return datacenter

# checking for filename 
if(len(sys.argv) > 2):
    filename = sys.argv[1] 
    output_filename = filename[0:-4] + '_edit.csv'
    duplicate_events_filename = filename[0:-4] + '_duplicate_events.csv'
    sorted_events_filename = filename[0:-4] + '_sorted_events.csv'
    flag = sys.argv[2]

elif(len(sys.argv) > 1):
    filename = sys.argv[1] 
    output_filename = filename[0:-4] + '_edit.csv'
    duplicate_events_filename = filename[0:-4] + '_duplicate_events.csv'
    sorted_events_filename = filename[0:-4] + '_sorted_events.csv'
    flag = '-none'

else:
    filename = 'summary.csv'
    output_filename = 'summary_edit.csv'
    duplicate_events_filename = 'summary_duplicate_events.csv'
    sorted_events_filename = filename[0:-4] + 'summary_sorted_events.csv'
    flag = '-none'

# initialize needed lists 
unique_arr = []
counter_arr = []
new_file_data = []
duplicates_data = []
sorted_events = []
event_analyzer = []


# initialize new columns
column_count = "Number of Occurences"
column_start = "First Occurence"
column_end = "Last Occurence"

total_rows = 0

with open(filename, 'r') as f:
    reader = csv.reader(f)
    total_rows = len(list(reader))

print()
print('-----Duplicates being removed-----')
print()
# duplicate check
with open(filename, 'r') as f, open(output_filename, 'w') as nf:
    reader = csv.reader(f)
    writer = csv.writer(nf)

    with alive_bar(total_rows) as bar:  

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
                    
            sleep(0.00000000001)        
            bar()

    writer.writerows(new_file_data)

print()
print('-----Duplicates removed-----')
print()

sum = 0
for i in range(len(new_file_data)):
    if (i != 0):
        sum+=int(new_file_data[i][4])
print("Total entries: " + str(sum))    
print()
'''
Changes:
1) Make a new excel sheet for duplicate cases only
2) Make a new excel sheet where rows are sorted such that same eventes are bundled together
'''

if flag == '-duplicate':
    # make a new exceel file for duplicate events only
    # for i in range(len(new_file_data)):
    #     if (i != 0):
    #         if (int(new_file_data[i][4]) > 1):
    #             duplicates_data.append(new_file_data[i])
    print('-----Duplicates being written-----')
    print()
    with alive_bar(len(new_file_data)) as bar:  
        for i in range(len(new_file_data)):
            if (i != 0):
                if (int(new_file_data[i][4]) > 1):
                    duplicates_data.append(new_file_data[i])
            sleep(0.01)        
            bar()     
    print()        

    with open(duplicate_events_filename, 'w') as nf:
        writer = csv.writer(nf)
        writer.writerows(duplicates_data)

    dup_sum = 0
    for i in range(len(duplicates_data)):
        if (i != 0):
            dup_sum+=int(duplicates_data[i][4])

    print("Total duplicates entries: " + str(dup_sum))  
    print("Total single entries: " + str(int(sum - dup_sum)))  
    print()

elif flag == '-sorted':

    print('-----Sorting based on events-----')
    print()
    with alive_bar(len(new_file_data)) as bar:  
        for i in range(len(new_file_data)):
            if new_file_data[i] not in sorted_events:
                sorted_events.append(new_file_data[i])
            for j in range(len(new_file_data)):
                if i!=j and i!=0 and j!=0:
                    if new_file_data[i][3] == new_file_data[j][3]:
                        if new_file_data[j] not in sorted_events:
                            sorted_events.append(new_file_data[j])
            sleep(0.01)        
            bar()     
    print()  

    with open(sorted_events_filename, 'w') as nf:
        writer = csv.writer(nf)
        writer.writerows(sorted_events)         

    print("--------Analyzing Data Centers with errors--------")
    print()

    multiple_cases_flag = False

    for i in range(len(sorted_events)):
        if i!=0:
            dc_1 =  datacenter_name((sorted_events[i][1]))
            event_1 = sorted_events[i][3]
            for j in range(len(sorted_events)):
                if i!=0 and j!=0 and i!=j:
                    dc_2 =  datacenter_name(sorted_events[j][1])
                    event_2 = sorted_events[j][3]
                    if dc_1 == dc_2 and event_1 == event_2 and (dc_2, event_2) not in event_analyzer :
                        event_analyzer.append((dc_2, event_2))
                        print("Multiple devices encountering same error observed in datacenter: " + dc_2 + " starting at row " + str(j) + " in the file " + sorted_events_filename)
                        break
    
    print()
    print("--------Analysis Complete--------")
    print()

else:
    if os.path.exists(duplicate_events_filename):
        os.remove(duplicate_events_filename)

    if os.path.exists(sorted_events_filename):
        os.remove(sorted_events_filename)        

