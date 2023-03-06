import pyodbc
import time
from datetime import datetime
import requests

tag_names = ['1LBA99EA011']
conn_string = 'Driver={SQL Server};Server=MUJEERPC\MSSQLSERVER01;Database=panndetekt;Trusted_Connection=yes;'

conn = pyodbc.connect(conn_string)

cursor = conn.cursor()

for tag_name in tag_names:
    query = f"SELECT * FROM [panndetekt].[dbo].[DB2] WHERE TagName = '{tag_name}'"
    cursor.execute(query)

    results = cursor.fetchall()

    epoch_results = []
    for row in results:
        dt = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f0')  # Convert string to datetime object
        epoch_time = int(time.mktime(dt.timetuple()))
        epoch_time = epoch_time*1000
        epoch_row = [epoch_time] + list(row[1:])
        epoch_results.append(epoch_row)

    post_list = [[sublist[0], sublist[2]] for sublist in epoch_results]

    url = "http://13.68.199.3/kairosapi/api/v1/datapoints"
    col = f"UMEA_{tag_name}"
    
    def post_with_delay(url,store_vals,col):
        body = [{
                "name": str(col),
                "datapoints": store_vals,
                "tags": {
                "type": "eqp_state"
                }}]
        res = requests.post(url=url,json = body,stream=True)
        print(res.content)
        print(res.status_code)
        if res.status_code == 204:
            print ('Data Posted Successfully! -', tag_name)
        else:
            print("Post data fail")
    
    while post_list:
        post_chunk = post_list[:20000]
        post_list = post_list[20000:]
        post_with_delay(url, post_chunk, col)
        time.sleep(3)
        results.clear()
        
cursor.close()
conn.close()
