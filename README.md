# streetlight-corridor-evaluation
Calculate exposure metrics from StreetLight Data for the NYCDOT RIS Corridor Evaluation Project

This script takes the CSV files that are generated when an O-M-D analysis is run and calculates the exposure indices and changes in exposure.

Note that the destination middle filter (DMF) zones and destination zones must be properly named in order for the script to run properly:

If the destination zone is named `<destination>`:

DMF Name = `<destination> DMF`
