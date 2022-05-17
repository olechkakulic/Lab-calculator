#import time
#import streamlit as st
import streamlit as st
import pandas as pd
#import numpy as np
#from urllib.request import urlopen
#import json
import os
#from openpyxl import load_workbook

def get_step(material_name, type):
    if type==1:
        return float(globals()[material_name]['wl'].values[0])
    elif type==2:
        return float(globals()[material_name]['wl'].values[-1])
@st.cache
def load_dataset(data_link):
    dataset = pd.read_csv(data_link)
    return dataset
# работа с файлами
directory = 'DataFiles'
files = os.listdir(directory)
filenames=[]
for i in range(len(files)):
        globals()[(files[i][:-4])] = pd.read_csv('DataFiles/'+files[i])
        filenames.append(str(files[i][:-4]))

titanic_link = 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv'
titanic_data = load_dataset(titanic_link)
#ЗАГОЛОВКИ #
st.title("Калькулятор Брэгговского зеркала")
st.markdown("Люблю Дашеньку Салтыкову")
#код для вводимых данных
st.sidebar.number_input('Значение угла', min_value = 0, max_value = 180, step = 1)
st.sidebar.selectbox(
     'Тип поляризации',
     ('TE', 'TM',))
material=st.sidebar.selectbox(
     'Материал',
     (filenames))
if material:
    st.sidebar.number_input('Длина волны ', min_value=get_step(str(material), 1), max_value=get_step(str(material), 2))





