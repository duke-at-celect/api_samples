# api_samples
The purpose of this repository is share sample code with Celect customers to help enable them with using the Celect Fulfillment API.

## Prerequisites
_Language_
* Python3

_Libraries_
* pandas
* requests
* json
* pandas.io.json
* time
* argparse

_Security_
* Please update the 'client_id' and 'api_key' variables with your credentials

## capacity_state_prod.py
This script should be used to:
1. Save your store IDs and their current capacity settings to a CSV file. 
2. Reset your current store capacity settings back to the values found in the CSV

### Running the script
#### Get Current State
``` 
This command will output a new .CSV file to the working directory

$ python3 capacity_state_prod.py --state get --region us
```

#### Set Current State
``` 
This command will consume the file created from the --state get command

$ python3 capacity_state_prod.py --state set --file us_capacity_state.csv
```

#### Help
```
$ python3 capacity_state_prod.py --help
 Usage: capacity_state_prod.py [-h] [--state {get,set}] [--region {ca,us}]
                              [--file FILE]

optional arguments:
 -h, --help         show this help message and exit
 --state {get,set}  Either get current state or set state to a previous get.
 --region {ca,us}   Required with --state get Must be either 'ca' for Canada
                    or 'us' for United States
 --file FILE        Required with --state set. The file to process - include
                     path if necessary
```
