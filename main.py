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

def get_coefficent(mat, inp_wl):
    wl_list = globals()[mat]['wl'].tolist()
    nearest_wl = min(wl_list, key=lambda x: abs(x - inp_wl))
    number = wl_list.index(nearest_wl)
    return float(globals()[mat]['n'].values[number])

#def get_koef(koefficient):
        #return float(globals()[koefficient]['n'].values[])
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
    input_wl=st.sidebar.number_input('Длина волны ', min_value=get_step(str(material), 1), max_value=get_step(str(material), 2))
# st.sidebar.number_input('n', value = get_koef)
    if input_wl:
        st.sidebar.write('n', get_coefficent(str(material),float(input_wl)))






