import pandas as pd
import openpyxl as opxl
import os
from tkinter.filedialog import askopenfilename, askdirectory, asksaveasfile

# ---- This script calculates exposure from Streetlight data. ----

# for each "before" project...
# open a file chooser to pick the before csv
before_path = askopenfilename(title='Choose before csv:')
print('CSV selected: '+before_path)

# open a file chooser again to pick the corresponding "after" csv
after_path = askopenfilename(title='Choose after csv:')

# open csv's
before_dataframe = pd.read_csv(before_path)
after_dataframe = pd.read_csv(after_path)

# filter out "All Days: and "All Day" day types/day parts
before_dataframe_weekday = before_dataframe[before_dataframe["Day Type"] == "1: Weekday (Tu-Th)"]

# get the weekday AM and PM OMD traffic
OMD_traffic_weekday = before_dataframe_weekday[["Destination Zone Name","Middle Filter Zone Name","Day Part","Average Daily O-M-D Traffic (StL Index)"]]
OMD_traffic_AM = OMD_traffic_weekday[OMD_traffic_weekday["Day Part"] == "1: Peak AM (7am-10am)"]
OMD_traffic_PM = OMD_traffic_weekday[OMD_traffic_weekday["Day Part"] == "2: Peak PM (4pm-7pm)"]
print(OMD_traffic_AM)
print(OMD_traffic_PM)

# calculate exposure: ExpIndex = MF_i/DMF_i
# do the same for the "After" condition

# for each MF in each destination in each project, subtract each "After" exposure index from each "Before" exposure index to get the change in exposure
# average the exposure differences, ignoring rows with missing exposures because only a before or after exposure value without its "twin" can't be compared

# write results to an excel file