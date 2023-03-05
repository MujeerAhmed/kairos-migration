import pyodbc
import time
from datetime import datetime
import requests

session  = requests.Session()

# Connection string for SQL Server
conn_string = 'Driver={SQL Server};Server=MUJEERPC\MSSQLSERVER01;Database=panndetekt;Trusted_Connection=yes;'

# Connect to the database
conn = pyodbc.connect(conn_string)

# Create a cursor
cursor = conn.cursor()

# Execute a SQL query
query = 'SELECT * FROM [panndetekt].[dbo].[DB2] WHERE TagName = \'10HCC01CF001\';'
cursor.execute(query)

# Fetch the results
results = cursor.fetchall()

# Convert timestamp to epoch format
epoch_results = []
for row in results:
    dt = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f0')  # Convert string to datetime object
    epoch_time = int(time.mktime(dt.timetuple()))
    epoch_time = epoch_time*1000
    epoch_row = [epoch_time] + list(row[1:])
    epoch_results.append(epoch_row)

# Define the chunk size
chunk_size = 20000

# Post data in chunks
for i in range(0, len(epoch_results), chunk_size):
    post_list = [[sublist[0], sublist[2]] for sublist in epoch_results[i:i+chunk_size]]
    url = "http://13.68.199.3/kairosapi/api/v1/datapoints"
    col = "UMEA_10HCC01CF001"
    body = [{
            "name": str(col),
            "datapoints": post_list,
            "tags": {
            "type": "eqp_state"
            }}]
    res = requests.post(url=url, json=body, stream=True)
    print(res.content)
    print(res.status_code)
    if res.status_code == 204:
        print('Data Posted Successfully!')
    else:
        print("Post data fail")

cursor.close()
conn.close()
