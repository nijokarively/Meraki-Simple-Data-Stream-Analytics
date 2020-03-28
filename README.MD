This script uses built-in python3 libraries (i.e. math, json, sqlite3, time, argparse), thus it does NOT require the user to install additional modules.

Please ensure to have python3.x installed given that it will not run properly with python2.x.

How to use:

In order to make this script as simple and flexible as possible, I decided to utilise command line parameters.
This approach enables us to reuse this service in complex pipelines without having to readapt the code.

To run this script type the following in your cmd, bash or cli => python main.py -i <input_data_source> -d <database_location> or python3 main.py -i <input_data_source> -d <database_location>

e.g. python main.py -i data_10k.json -d mytest1.db

NB: Please replace <input_data_source> with the input source and <database_location> with the database path.

A brief help guide can be displayed by running => python main.py -h or python3 main.py -h


### TESTING

I used a functional programming TDD approach using pytest.

Please make sure to install pytest either via pip install -r requirements.txt or pip install pytest

To run the test use the following command: pytest test_main.py -v

For more information please read the 'Notes' file in the root directory.

