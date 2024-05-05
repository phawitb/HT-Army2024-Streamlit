import streamlit as st
import pandas as pd
import streamlit as st
# import hydralit_components as hc
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


st.write('Wellcome to HT-Army')

id = st.text_input("Enter your ID", )

if not os.path.exists('data.csv'):
    df = pd.DataFrame()
else:
    df = pd.read_csv('data.csv')

# st.write(df)
# st.write(df['id'].unique())

IDS = get_all_id()

if id:

    # if id in df['id'].unique(): 
    if id in IDS: 
        if id in df['id'].unique():
            st.write('Last')
            df2 = df[df['id']==id]
            

            # chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

            df2.set_index('time', inplace=True)
            df2.drop(columns=['id'], inplace=True)

        
            st.write(df2.iloc[-1])

            
            st.write('History')
            st.write(df2)
            st.line_chart(df2)

        else:
            st.write('No history data!')

        st.write('Setup')
        
        L = [None,None,None]
        if not os.path.exists('config.json'):
            config_data = {}
            
        else:
            with open('config.json') as json_file:
                config_data = json.load(json_file)

            if id in config_data.keys():
                for i in range(3):
                    try:
                        L[i] = config_data[id][f'line{i+1}']
                    except:
                        pass
        
        line1 = st.text_input("Enter line1 Token", L[0])
        line2 = st.text_input("Enter line2 Token", L[1])
        line3 = st.text_input("Enter line3 Token", L[2])

        config_data[id] = {
            'line1' : line1,
            'line2' : line2,
            'line3' : line3,
        }

        if st.button("update"):
        
            with open('config.json', 'w') as json_file:
                json.dump(config_data, json_file)

            # st.write('config_data:',config_data)
            st.write('update complete!')

        


            




        
     

    else:
        st.write('id not exist!')


else:
    st.write('please input ID')

