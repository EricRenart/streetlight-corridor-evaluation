This folder contains metrics for the Segment Analysis trips passing through the road segment zones of the named analysis.

The trips that are analyzed for each line segment zone are determined by the zone's start gate and end gate. The analysis is done for all trips that pass through the start gate and then pass through the end gate. The pass-through gates may include a defined direction on the start gate and end gate. If the zone is bi-directional, the analysis includes trips that pass through the start and end gate going in opposite directions.

TERMS
=====
Gate Direction: A start gate or end gate may optionally have a direction which limits the trips analyzed for the gate-- only trips that pass through the gate within -20/+20 degrees of the direction will be analyzed for the gate. Values are provided in degrees from 0 to 359, where 0 is due north, 90 is east, 180 is due south, etc. A value of "Null" refers to no direction filter and therefore all trips that pass through the gate will be used. However, unless the zone is bi-directional, the analysis will use only trips that pass through the start gate before they pass through the end gate. Gate directions are applied both ways for bi-directional zones.


OUTPUT UNIT TERMS
=================
StreetLight Volume: The estimated trip counts as calculated by StreetLight Data's machine learning algorithm.

StreetLight Index: The relative trip activity. The StreetLight Index does not indicate the actual number of trips or vehicles. Trip Index values for different vehicle types, weight classes, and countries are based on different sample populations and therefore cannot be compared with each other.

StreetLight Sample Trip Counts: The total StreetLight sample trip counts for the zone (or set of zones) for all days in the entire data period.

*Note that, while most output units are represented as an average day per its day type definition, Trip Counts are not converted to an average day but rather represent the total Trip Counts. For example, a Trip Count value of 100 for an O-D pair, on an average weekday in March 2017, represents the sum of all trips used from the StreetLight data set for all the weekdays in March 2017.

*More information of the output unit methodology can be found in StreetLight Data's Support Center (https://support.streetlightdata.com).


FILES
=====
Analysis.txt
===========
This file lists information about the analysis as a whole, including the full analysis name, organization and user that created the analysis, and the analysis options configuration

sa_*.csv
========
This files contains the Segment Analysis metrics.

The fields are:
- Type of Travel: Type of mode analyzed.
- Zone ID: Numeric ID for the zone as provided by the user.
- Zone Name: Name for the zone as provided by the user.
- Zone Is Pass-Through: Indicates if the zone is pass-through or not as described above in the Terms.
- Zone Direction (degrees): This refers to the direction in which trips pass through the zone as described above in the Terms.
- Zone is Bi-Direction: Indicates if the zones are bi-directional. Values are "Yes" or "No".
- Day Type: All Days (traffic from Monday through Sunday), and other day type traffic segmentation as defined by user.
- Day Part: Segments of the day defined by the user in intervals of hours to analyze traffic (All Day is always included as entire 24 hours). The day parts reflect the local time at the start gate.
- Segment Traffic: The volume of trips passing from the start gate to the end gate based on the Output Type (as descibed above in the Output Unit Terms). Bi-directional zones also include trips passing from the end gate to the start gate.
- Avg Segment Speed (mph): The average speed, in miles per hour, for low network factor* trip segments passing from the start gate to the end gate.
- Avg All Segment Speed (mph): The average speed, in miles per hour, for all trip segments passing from the start gate to the end gate.
- Avg Segment Duration (sec): The average duration, in seconds, for low network factor* trip segments passing from the start gate to the end gate.
- Avg All Segment Duration (sec): The average duration, in seconds, for all trip segments passing from the start gate to the end gate.
- Free Flow Factor: a measure of congestion, is the "Average Trip Speed" divided by the "Free Flow Trip Speed". The Free Flow Trip Speed is the the Maximum Average Trip Speed in any one of the 24 hours of the day, averaged over all the days in the data period. The Free Flow Factor is a percentage value, between 0 and 1, to 3 digits of precision.
  Congestion: 1 minus the Free Flow Factor for a given segment.
- Segment Speed X-Y mph (percent): The percent of all trip segments passing from the start gate to the end gate for which the speed is in the bin from X to Y mph.**
- Segment Duration X-Y min (percent): The percent of all trip segments passing from the start gate to the end gate for which the segment duration is in the bin from X to Y minutes.**

*Network factor is defined as unlocked trip length / distance ( trip point in origin zone, trip point in destination zone). Low network is less than 4. This is different from circuity in that it is always calculated using the unlocked (or connect the points) trip length, not the Locked to Route trip length.
**Each distribution bin is inclusive of the start value X and exclusive of the end value Y. For example, the bin (5-10) contains values greater than or equal to 5.0 and less than 10.0.

sample_size.csv
===============
This file contains information about the size of the data sample that was analyzed for this analysis and its data period.

The fields are:
- Data Source: Type of data source analyzed.
- Sample Type: Type of mode analyzed.
- Vehicle Weight: Type of commercial vehicle analyzed.
- Approximate Device Count: Calculated as the number of unique devices in the analysis, rounded to nearest 10 (if below 100), and to nearest 100 (if above 100). N/A for analysis run with Navigaton-GPS data source.
- Approximate Trip Count: An estimated value (calculated during processing) of the number of unique device trips in the StreetLight Data database that were analyzed for this analysis and its Data Period.

zones.csv
=========
This file contains information about the zones used in this analysis.

The fields are:
- Zone Type: Indicates if the zone for this is an origin or destination zone.
- Zone ID: Numeric ID for the zone as provided by the user.
- Zone Name: Name for the zone as provided by the user.
- Zone is Pass-Through: Indicates if the zone is marked as pass-through or not as described above under Terms. Is either makred as “Yes” or “No."
- Zone Direction (degrees): This refers to the direction in which trips pass through the zone as described above under Terms.
- Zone is Bi-Direction: Indicates if the zones are bi-directional. Is either marked as "Yes" or "No".
- Fingerprint1: A 64-bit signed integer assigned by StreetLight based on key spatial characteristics of the zone. Combination of Fingerprint1 and Fingerprint2 make up the fingerprint of the zone and indicate if two zones are the same or unique.
- Fingerprint2: A 64-bit signed integer assigned by StreetLight based on key spatial characteristics of the zone. Combination of Fingerprint1 and Fingerprint2 make up the fingerprint of the zone and indicate if two zones are the same or unique.

*.(dbf|prj|shp|shx|cpg)
=======================
These files comprise the shapefiles for the analysis's zone sets.

A shapefile consists of the following several files:
.shp file contains the feature geometries and can be viewed in a geographic information systems application such as QGIS.
.dbf file contains the attributes in dBase format and can be opened in Microsoft Excel.
.shx file contains the data index.
.prj file contains the projection information.
.cpg file contains the encoding applied to create the shapefile.

These shapefiles have the following attributes/columns:
- id: Numeric ID for the zone as provided by the user. This may be null as the field is optional.
- name: Name for the zone as provided by the user.
- direction (degrees): This refers to the direction in which trips pass through the zone as described above under Terms.
- is_pass: Indicates if the zone is pass-through or not as described above under Terms. 1 = “Yes” and 0 = “No”.
- geom: Polygon of the zone.
- is_bidi: A value of 1 indicates traffic measured in two opposite directions for a single set of Metric values. 0 value indicates traffic is in single direction specified by users.

*_line.(dbf|prj|shp|shx|cpg)
============================
These shapefiles have the following attributes/columns:
- id: Numeric ID for the zone as provided by the user. This may be null as the field is optional.
- name: Name for the zone as provided by the user.
- geom: LineString of the zone.
- road_type: Type of the road that is represented by the LineString, as entered upon creation of the zone.
- gate_lat: The latitude for the location of the gate on the line segment, as entered upon creation of the zone.
- gate_lon: The longitude for the location of the gate on the line segment, as entered upon creation of the zone.
- gate_width: The total width of the gate, in meters, as entered upon creation of the zone.


NOTES
=====
Day Part Calculations
=====================
The Day Part calculations are done in relation to the zones used in the analysis. The Day Part is determined by when trips pass through the zone's start gate.


Copyright © 2011 - 2020, StreetLight Data, Inc. All rights reserved.
