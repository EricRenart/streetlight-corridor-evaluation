import pandas as pd
import numpy as np
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

# Return DMF traffic
def getDMFs(df):
    return df[df[HEADER_MF].str.contains("DMF")]

# Get total DMF traffic by destination
def sumDMF(df):
    dmfs = getDMFs(df)
    sumdmf = dmfs.groupby(HEADER_MF).sum()
    return sumdmf

def fillDMFTraffic(merged_df, dmf_df):
    for row in range(0,len(merged_df)):
        cur_destination = merged_df.iloc[row,0]
        cur_dmf = cur_destination + " DMF"
        print(dmf_df)
        if merged_df.iloc[row,1].__eq__(cur_dmf):
            cur_dmf_traffic = dmf_df.loc[cur_dmf,HEADER_OMD]
            for row1 in range(0,len(merged_df)):
                if merged_df.iloc[row1,0].__eq__(cur_destination):
                    merged_df.iloc[row1,5] = cur_dmf_traffic
            #merged_df.iloc[row,5] = cur_dmf_traffic
    return merged_df

# --- for each "before" project... ---
# ---open a file chooser to pick the before csv ---
before_path = askopenfilename(title='Choose before csv:')
print('CSV selected: '+before_path)

# --- open a file chooser again to pick the corresponding "after" csv ---
after_path = askopenfilename(title='Choose after csv:')
print('CSV selected: '+after_path)

# --- open csv's ---
before_dataframe = pd.read_csv(before_path)
after_dataframe = pd.read_csv(after_path)

# --- filter out "All Days: and "All Day" day types/day parts ---
before_dataframe_weekday = before_dataframe[before_dataframe[HEADER_DAY_TYPE] == "1: Weekday (Tu-Th)"]
after_dataframe_weekday = after_dataframe[after_dataframe[HEADER_DAY_TYPE] == "1: Weekday (Tu-Th)"]

# --- get the weekday AM and PM OMD traffic ---
OMD_traffic_weekday = before_dataframe_weekday[[HEADER_DEST,HEADER_MF,HEADER_DAY_PART,HEADER_DAY_TYPE,HEADER_OMD]]
OMD_traffic_weekday_after = after_dataframe_weekday[[HEADER_DEST,HEADER_MF,HEADER_DAY_PART,HEADER_DAY_TYPE,HEADER_OMD]]
OMD_traffic_AM = OMD_traffic_weekday[OMD_traffic_weekday[HEADER_DAY_PART] == "1: Peak AM (7am-10am)"]
OMD_traffic_PM = OMD_traffic_weekday[OMD_traffic_weekday[HEADER_DAY_PART] == "2: Peak PM (4pm-7pm)"]
OMD_traffic_AM_after = OMD_traffic_weekday_after[OMD_traffic_weekday_after[HEADER_DAY_PART] == "1: Peak AM (7am-10am)"]
OMD_traffic_PM_after = OMD_traffic_weekday_after[OMD_traffic_weekday_after[HEADER_DAY_PART] == "2: Peak PM (4pm-7pm)"]
# --- sum the DMF traffic for each destination ---

# get all rows which contain DMF and sum
print('TOTAL AM DMF TRAFFIC - BEFORE')
am_dmf_sum = sumDMF(OMD_traffic_AM)
print('TOTAL PM DMF TRAFFIC - BEFORE')
pm_dmf_sum = sumDMF(OMD_traffic_PM)
print('TOTAL AM DMF TRAFFIC - AFTER')
am_dmf_sum_after = sumDMF(OMD_traffic_AM_after)
print('TOTAL PM DMF TRAFFIC - AFTER')
pm_dmf_sum_after = sumDMF(OMD_traffic_PM_after)

# --- calculate exposure: ExpIndex = MF_i/DMF_i ---
# associate each DMF with its destination

merged_dmf_am = OMD_traffic_AM.merge(am_dmf_sum,on=HEADER_MF,how="outer")
merged_dmf_pm = OMD_traffic_PM.merge(pm_dmf_sum,on=HEADER_MF,how="outer")
merged_dmf_am_after = OMD_traffic_AM_after.merge(am_dmf_sum_after,on=HEADER_MF,how="outer")
merged_dmf_pm_after = OMD_traffic_PM_after.merge(pm_dmf_sum_after,on=HEADER_MF,how="outer")

# now assign sumDMF to all rows based on destination
filled_dmf_am = fillDMFTraffic(merged_dmf_am, am_dmf_sum)
filled_dmf_pm = fillDMFTraffic(merged_dmf_pm, pm_dmf_sum)
filled_dmf_am_after = fillDMFTraffic(merged_dmf_am_after, am_dmf_sum_after)
filled_dmf_pm_after = fillDMFTraffic(merged_dmf_pm_after, pm_dmf_sum_after)

# add a new column and calculate exposure index
filled_dmf_am["Exposure Index (AM Before)"] = (filled_dmf_am["Average Daily O-M-D Traffic (StL Index)_x"] / filled_dmf_am["Average Daily O-M-D Traffic (StL Index)_y"]) * 100
filled_dmf_pm["Exposure Index (PM Before)"] = (filled_dmf_pm["Average Daily O-M-D Traffic (StL Index)_x"] / filled_dmf_pm["Average Daily O-M-D Traffic (StL Index)_y"]) * 100
filled_dmf_am_after["Exposure Index (AM After)"] = (filled_dmf_am_after["Average Daily O-M-D Traffic (StL Index)_x"] / filled_dmf_am_after["Average Daily O-M-D Traffic (StL Index)_y"]) * 100
filled_dmf_pm_after["Exposure Index (PM After)"] = (filled_dmf_pm_after["Average Daily O-M-D Traffic (StL Index)_x"] / filled_dmf_pm_after["Average Daily O-M-D Traffic (StL Index)_y"]) * 100


# for each MF in each destination in each project, subtract each "After" exposure index from each "Before" exposure index to get the change in exposure
# average the exposure differences, ignoring rows with missing exposures because only a before or after exposure value without its "twin" can't be compared (inner join?)
exposure_am = pd.merge(filled_dmf_am,filled_dmf_am_after,how="inner",on=[HEADER_DEST,HEADER_MF,HEADER_DAY_PART])
exposure_pm = pd.merge(filled_dmf_pm,filled_dmf_pm_after,how="inner",on=[HEADER_DEST,HEADER_MF,HEADER_DAY_PART])

exposure_am["% Exposure Change AM"] = exposure_am["Exposure Index (AM After)"] - exposure_am["Exposure Index (AM Before)"]
exposure_pm["% Exposure Change PM"] = exposure_pm["Exposure Index (PM After)"] - exposure_pm["Exposure Index (PM Before)"]

# Create a summary table with the changes in exposure
summary_am = pd.DataFrame([exposure_am[HEADER_DEST],exposure_am[HEADER_MF],exposure_am["Exposure Index (AM Before)"],exposure_am["Exposure Index (AM After)"],exposure_am["% Exposure Change AM"]]).transpose()
summary_am_sorted = summary_am.sort_values(HEADER_DEST)
summary_pm = pd.DataFrame([exposure_pm[HEADER_DEST],exposure_pm[HEADER_MF],exposure_pm["Exposure Index (PM Before)"],exposure_pm["Exposure Index (PM After)"],exposure_pm["% Exposure Change PM"]]).transpose()
summary_pm_sorted = summary_pm.sort_values(HEADER_DEST)

# write out the results as a csv
proj_name = input("What is this project's name? :")
summary_am_sorted.to_csv(proj_name+"_exposure_am.csv")
summary_pm_sorted.to_csv(proj_name+"_exposure_pm.csv")
