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
query = 'SELECT * FROM [panndetekt].[dbo].[DB2] WHERE TagName = \'10HCC40CP001\';'
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

post_list = [[sublist[0], sublist[2]] for sublist in epoch_results]

url = "http://13.68.199.3/kairosapi/api/v1/datapoints"
col = "UMEA_10HCC40CP001"
def post(url,store_vals,col):
    body = [{
            "name": str(col),
            # "datapoints": [toDatapointsFormat(x) for x in store_vals],
            "datapoints": store_vals,
            "tags": {
            "type": "eqp_state"
            }}]
    # print(body)
#    print(url, col)
    res = requests.post(url=url,json = body,stream=True)
    print(res.content)
    print(res.status_code)
    if res.status_code == 204:
       
        print ('Data Posted Successfully!')
    else:
        print("Post data fail")

post(url, post_list, col)


cursor.close()
conn.close()
