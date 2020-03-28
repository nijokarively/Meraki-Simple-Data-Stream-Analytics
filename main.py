import sqlite3, argparse, json, time
from sqlite3 import Error
from math import trunc

def load_data(data_source):
    try:
        with open(data_source, 'r') as json_data:
            data = json_data.read()

        return json.loads(data)
    except Exception as e:
        print(e)

def convert_epoch_to_minutes(timestamp):
    try:
        # assuming that the time is a standard epoch timestamp seconds, if we divide it 
        # by 60(seconds) we can convert the epoch time to minutes
        epoch_minutes = timestamp / ( 60)
        return trunc(epoch_minutes)
    except Exception as e:
        print(e)

def calculate_moving_average(current_average, new_value, num_samples):
    try:
        return round((current_average * (num_samples - 1) + new_value) / num_samples, 2)
    except Exception as e:
        print(e)

def store_results_to_db(results, db_name):
    try: 
        conn = sqlite3.connect(db_name)

        conn.execute('''CREATE TABLE IF NOT EXISTS nodes(
         node_id INT NOT NULL,
         timestamp INT NOT NULL,
         max_value INT NOT NULL,
         min_value INT NOT NULL,
         average REAL NOT NULL,
         PRIMARY KEY (node_id, timestamp));''')
        
        for key, value in results.items():

            node_id = key

            for sub_key in value: 

                timestamp = sub_key
                max_value = value[sub_key]['max_value']
                min_value = value[sub_key]['min_value']
                average = value[sub_key]['average']
            
                conn.execute("""INSERT INTO nodes (node_id, timestamp, max_value, min_value, average)
                                VALUES (?, ?, ?, ?, ?)""",
                                (node_id, timestamp, max_value, min_value, average))

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.commit()
            conn.close()

def parse_input():
    parser = argparse.ArgumentParser(
        description='Meraki Code Challenge - Simple Data Stream Analytics')
    parser.add_argument('-i',
                        action='store',
                        default=None,
                        dest='data_source',
                        help='location of input data source (e.g. data.json)')
    parser.add_argument('-d',
                        action='store',
                        default=None,
                        dest='db_name',
                        help='location of database for storing analytics (e.g. test.db)')
  
    return parser.parse_args()

def main():
    # get data source and db locations
    param = parse_input()
    data_source = param.data_source
    db_name = param.db_name

    if data_source and db_name:      
        start_time = int(round(time.time() * 1000))

        results = {} # e.g. results = {node_id:{timestamp:{'num_samples', 'max_value', 'min_value', 'average'}}}

        data = load_data(data_source)

        for node in data:

            node_id = str(node['node_id'])
            timestamp = str(convert_epoch_to_minutes(node['timestamp']))

            # in python try-except performs faster than explicit if-else statements, so rather than checking if key exists we try to access it directly. (EAFP)
            try:
                current_max = results[node_id][timestamp]['max_value']
                current_min = results[node_id][timestamp]['min_value']
                current_average = results[node_id][timestamp]['average']
                num_samples = results[node_id][timestamp]['num_samples'] + 1

                results[node_id][timestamp]['num_samples'] = num_samples
                results[node_id][timestamp]['max_value'] = max(current_max, node['value'])
                results[node_id][timestamp]['min_value'] = min(current_min, node['value'])
                results[node_id][timestamp]['average'] = calculate_moving_average(current_average, node['value'], num_samples)
            except KeyError:
                try: 
                    results[node_id][timestamp] = {'num_samples': 1, 'max_value': node['value'], 'min_value': node['value'], 'average': node['value'] }
                except KeyError:
                    results[node_id] = { timestamp : {'num_samples': 1, 'max_value': node['value'], 'min_value': node['value'], 'average': node['value'] }}

        store_results_to_db(results, db_name)

        elapsed_time = int(round(time.time() * 1000)) - start_time
        print('Elapsed time: %s ms' % elapsed_time)
    else:
        print('Missing parameters! Please use the -h or --help to find out more!')

if __name__ == '__main__':
    main()