import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import requests
import requests
import json
import os

def get_all_id():
    url = "https://raw.githubusercontent.com/phawitb/adjustHT4/main/config_htarmy2024.txt"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text
        IDS = [x.split(',')[0] for x in data.split()]
        return IDS
    else:
        # print("Failed to retrieve data. Status code:", response.status_code)
        return None

def send_line_notify(message, token):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer ' + token}
    data = {'message': message}
    r = requests.post(url, headers=headers, data=data)
    if r.status_code == 200:
        print('Message sent successfully!')
    else:
        print('Failed to send message. Status code:', r.status_code)




st.write('?id=S002&temperature=34&humidity=44&hic=40&flag=red&pm25=40')

token = 'i4dIQOPNh6slv6gG9h5SoQdiq5SD2btX35Vg5IDl0Qm'


utc_now = datetime.utcnow()
time = utc_now + timedelta(hours=7)



# Get URL parameters
# params = st.experimental_get_query_params()
params = st.query_params



# Get temperature and humidity parameters
id = params.get('id',None)
temperature = params.get('temperature',None)
humidity = params.get('humidity', None)
hic = params.get('hic', None)
flag = params.get('flag', None)
pm25 = params.get('pm25', None)

# Display temperature and humidity
st.write(f"id: {id}")
st.write(f"Temperature: {temperature}")
st.write(f"Humidity: {humidity}")
st.write(f"hic: {hic}")
st.write(f"flag: {flag}")
st.write(f"pm25: {pm25}")
st.write("time", time)

if id in get_all_id():
    if id and temperature:

        try:
            df = pd.read_csv('data.csv')
        except:
            df = pd.DataFrame()


        new_row = {'time': [time],
                'id': [id],
                'temperature': [temperature],
                'humidity': [humidity],
                'hic': [hic],
                'flag': [flag],
                'pm25': [pm25]
                }

        df2 = pd.DataFrame(new_row)

        # new_row = {'Column1': value1, 'Column2': value2, ...}  # Replace 'Column1', 'Column2', etc. with your column names and 'value1', 'value2', etc. with your values
        df = pd.concat([df, df2], ignore_index=True)
        df.to_csv('data.csv', index=False)  # Set index=False to not include the index in the CSV file

        with open('config.json') as json_file:
            config_data = json.load(json_file)

        line_list = [config_data[id][x] for x in config_data[id].keys()]
        line_list = [x for x in line_list if x]

        # st.write(line_list)

        msg = "Unit : "
        msg += f"id: {id}"
        msg += f"temperature: {temperature}"
        msg += f"humidity: {humidity}"
        msg += f"hic: {hic}"
        msg += f"flag: {flag}"
        if pm25:
            msg += f"pm25: {pm25}"
        msg += f"time: {time}"

        for l in line_list:
            send_line_notify(msg, token)

        
        # message = 'tessssst'
        # send_line_notify(message, token)

        st.write(df)


else:
    st.write('id does not exist')

    # data = {'time': [time],
    #         'id': [id],
    #         'temperature': [temperature],
    #         'humidity': [humidity],
    #         'hic': [hic],
    #         'pm25': [pm25]
    #         }

    # df = pd.DataFrame(data)
    # st.write(df)

    # df.to_csv('data.csv', index=False)



