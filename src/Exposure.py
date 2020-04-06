import pandas as pd
import openpyxl as opxl
import os

# ---- This script calculates exposure from Streetlight data. ----

# for each "before" project...
os.chdir("streetlight_Data/before")
for folder in os.listdir():

    # open csv
    os.chdir(folder)


    # add Peak AM and Peak PM entries to a dictionary


    # for each destination...
    # get the total DMF traffic by adding up each DMF volume for a destination

    # calculate exposure: ExpIndex = MF_i/DMF_i
# do the same for the "After" condition

# for each MF in each destination in each project, subtract each "After" exposure index from each "Before" exposure index to get the change in exposure
# average the exposure differences, ignoring rows with missing exposures because only a before or after exposure value without its "twin" can't be compared

# write results to an excel file