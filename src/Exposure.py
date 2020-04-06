import pandas as pd
import openpyxl as opxl
import os

# ---- This script calculates exposure from Streetlight data. ----
os.chdir("src/streetlight_Data") # change to directory with streetlight data


# for each "before" project...
os.chdir("before")
for file in os.listdir():

    # open csv
    sip_data = pd.read_csv(file)

    # add Peak AM and Peak PM entries to a dictionary


    # for each destination...
    # get the total DMF traffic by adding up each DMF volume for a destination

    # calculate exposure: ExpIndex = MF_i/DMF_i
# do the same for the "After" condition

# for each MF in each destination in each project, subtract each "After" exposure index from each "Before" exposure index to get the change in exposure
# average the exposure differences, ignoring rows with missing exposures because only a before or after exposure value without its "twin" can't be compared

# write results to an excel file