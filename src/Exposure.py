import pandas as pd
import os
from tabulate import tabulate
from tkinter.filedialog import askopenfilename, askdirectory, asksaveasfile

# ---- This script calculates exposure from Streetlight data. ----
HEADER_MF = "Middle Filter Zone Name"
HEADER_DEST = "Destination Zone Name"
HEADER_OMD = "Average Daily O-M-D Traffic (StL Index)"
HEADER_DAY_PART = "Day Part"
HEADER_DAY_TYPE = "Day Type"

# pretty-prints a dataframe with StreetLight Data with the help of tabulate
def prettyprint(stl_dataframe):
    tabulate_header = ['ID', 'DESTINATION', 'MIDDLE FILTER', 'DAY PART', 'OMD TRAFFIC']
    print(tabulate(stl_dataframe, headers=tabulate_header, tablefmt='psql'))

def isDMF(string):
    if string.__contains__("DMF"): return True
    else: return False

# for each "before" project...
# open a file chooser to pick the before csv
before_path = askopenfilename(title='Choose before csv:')
print('CSV selected: '+before_path)

# open a file chooser again to pick the corresponding "after" csv
after_path = askopenfilename(title='Choose after csv:')
print('CSV selected: '+after_path)

# open csv's
before_dataframe = pd.read_csv(before_path)
after_dataframe = pd.read_csv(after_path)

# filter out "All Days: and "All Day" day types/day parts
before_dataframe_weekday = before_dataframe[before_dataframe[HEADER_DAY_TYPE] == "1: Weekday (Tu-Th)"]

# get the weekday AM and PM OMD traffic
OMD_traffic_weekday = before_dataframe_weekday[[HEADER_DEST,HEADER_MF,HEADER_DAY_PART,HEADER_DAY_TYPE,HEADER_OMD]]
OMD_traffic_AM = OMD_traffic_weekday[OMD_traffic_weekday[HEADER_DAY_PART] == "1: Peak AM (7am-10am)"]
OMD_traffic_PM = OMD_traffic_weekday[OMD_traffic_weekday[HEADER_DAY_PART] == "2: Peak PM (4pm-7pm)"]
print('AM OMD TRAFFIC')
print(tabulate(OMD_traffic_AM))
print('PM OMD TRAFFIC')
print(tabulate(OMD_traffic_PM))

# sum the DMF traffic for each destination
# get all rows which contain DMF
am_dmfs = OMD_traffic_AM[OMD_traffic_AM[HEADER_MF].str.contains("DMF")]
pm_dmfs = OMD_traffic_PM[OMD_traffic_PM[HEADER_MF].str.contains("DMF")]

print(tabulate(am_dmfs))
print(tabulate(pm_dmfs))

am_dmf_sum = am_dmfs.groupby(HEADER_MF).sum()
print(tabulate(am_dmf_sum))

# calculate exposure: ExpIndex = MF_i/DMF_i
# do the same for the "After" condition

# for each MF in each destination in each project, subtract each "After" exposure index from each "Before" exposure index to get the change in exposure
# average the exposure differences, ignoring rows with missing exposures because only a before or after exposure value without its "twin" can't be compared

# write results to an excel file