# pip install streamlit-echarts


import streamlit as st
import pandas as pd
import requests
import datetime
from streamlit_echarts import st_echarts

st.set_page_config(layout="wide")

def create_gaung(value,name,color):
    option = {
        "tooltip": {
            "formatter": '{a} <br/>{b} : {c}%'
        },
        "series": [{
            "name": '进度',
            "type": 'gauge',
            "startAngle": 180,
            "endAngle": 0,
            "progress": {
                "show": "true"
            },
            "radius":'100%', 

            "itemStyle": {
                "color": color,
                "shadowColor": 'rgba(0,138,255,0.45)',
                "shadowBlur": 10,
                "shadowOffsetX": 2,
                "shadowOffsetY": 2,
                "radius": '55%',
            },
            "progress": {
                "show": "true",
                "roundCap": "true",
                "width": 15
            },
            "pointer": {
                "length": '60%',
                "width": 8,
                "offsetCenter": [0, '5%']
            },
            "detail": {
                "valueAnimation": "true",
                "formatter": '{value}%',
                "backgroundColor": color, #'#58D9F9',
                "borderColor": '#999',
                "borderWidth": 4,
                "width": '60%',
                "lineHeight": 20,
                "height": 20,
                "borderRadius": 188,
                "offsetCenter": [0, '40%'],
                "valueAnimation": "true",
            },
            "data": [{
                "value": value,
                "name": name
            }]
        }]
    };

    return option

st.header('Welcome to HT-Army App!')

url = "https://raw.githubusercontent.com/phawitb/HT-Army2024/main/config.txt"
df = pd.read_csv(url,header=None)
df.columns = ['id', 'adj_temp', 'adj_humid', 'adj_pm25', 'line1', 'line2', 'unit']
user_input = st.text_input('#### Enter ID:')

if user_input and user_input in list(df['id']):

    df_id = df[df['id']==user_input]
    st.write('#### Unit:', df_id['unit'].iloc[0])

    with st.spinner('Wait for it...'):
    
        url = f"https://script.google.com/macros/s/AKfycbx1nHCA01C2U0NdpsnPdO0Oc5xEjLgfOZWIOwu1f0DX72OGHOHHBRdRqwZyNO-EENF1xg/exec?id={user_input}"
        response = requests.get(url)

    if response.status_code == 200:
        try:
            data = response.json()
            isdata = True
        except:
            isdata = False


        if isdata:

            df_history = pd.DataFrame(data)
            df_history['datetime'] = [datetime.datetime.fromtimestamp(x) for x in df_history['date']]
            last_date = df_history[df_history['date'] == df_history['date'].max()]

            st.write(f"#### Lastseen {last_date['datetime'].iloc[0]}")

            col1, col2, col3=st.columns([1,1,1])
            with col1:
                value,name,color = last_date['hic'].iloc[0],'Heat Index',last_date['flag'].iloc[0]
                option = create_gaung(value,name,color)
                st_echarts(options=option, key="1")

            with col2:
                
                value,name,color = last_date['temp'].iloc[0],'Temperature',last_date['flag'].iloc[0]
                option = create_gaung(value,name,color)
                st_echarts(options=option, key="2")

            with col3:
                
                value,name,color = last_date['humid'].iloc[0],'Temperature','#58D9F9'
                option = create_gaung(value,name,color)
                st_echarts(options=option, key="3")

            st.write('### Historys')

            df_history = df_history.drop(columns=['date'])
            
            st.line_chart(
            df_history, x="datetime", y=["temp", "humid"], color=["#FF0000", "#0000FF"]  # Optional
            )

            df_history.set_index('datetime', inplace=True)
            st.write(df_history)

        else:

            st.write('No history data')

    else:
        st.write(f"Failed to retrieve data: {response.status_code}")

    
    st.markdown("[Setting](https://ht-army2024-f4e56.web.app/)")
        

else:
    st.write('user ID not exist!')
        



