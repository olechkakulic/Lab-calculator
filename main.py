#import time
import streamlit as st
import pandas as pd
import numpy as np
#from urllib.request import urlopen
#import json
import os
#from openpyxl import load_workbook


#функция для посчитать
# def count_math()
# epsilon = n^2
# k_i_matrix = transpose([epsilon, k_zi])
# k_zi = (epsilon - k_x)**0.5


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

#ЗАГОЛОВКИ #
st.title("Калькулятор Брэгговского зеркала")
st.markdown("Люблю Дашеньку Салтыкову")
#код для вводимых данных
lol =st.sidebar.number_input('Значение угла', min_value = 0, max_value = 180, step = 1)
cock = st.sidebar.selectbox(
     'Тип поляризации',
     ('TE', 'TM',))
# material=st.sidebar.selectbox(
#      'Материал',
#      (filenames))
# if material:
#     input_wl=st.sidebar.number_input('Длина волны ', min_value=get_step(str(material), 1), max_value=get_step(str(material), 2), step=0.001)
# # st.sidebar.number_input('n', value = get_koef)
#     if input_wl:
#         n=st.sidebar.write('n', get_coefficent(str(material),float(input_wl)))

# функция для посчитать
container = st.container()
ncol = st.sidebar.number_input("Введите количество слоев",  min_value = 0, step = 1)
# cols = container.columns(ncol)

for i in range(ncol):
    # col1 = cols[i%1]
    a = st.sidebar.selectbox(f"Номер слоя # {i}", (filenames), key=i)
    if a:
        # col2 = cols[i%1]
        input_wl = st.sidebar.number_input(f"Длина волны,м {i}", min_value=get_step(str(a), 1), max_value=get_step(str(a), 2), step=0.001, key=str(a))
        tolshina = st.sidebar.number_input(f"Толщина,м {i}", min_value=0.0, max_value=0.01, step=0.001)
        enable_wave_lenght = st.sidebar.checkbox(f'Коэф-т приломления слоя {i} постоянен')
        if input_wl and enable_wave_lenght:
            n = st.sidebar.write('ТУТ БУДЕТ ЧОТО')
        else:
            na = get_coefficent(str(a), float(input_wl))
            n = st.sidebar.write(f':sunglasses: n({i}) = {na}')


#функция посчитать
# materials = {'ag':,
# 'ar':,
# 'au':,
# 'be':,
# 'bi':,
# 'ca':,
# 'ce':,
# 'co':,
# 'cr':,
# 'cs':,
# 'cu':,
# 'er':,
# 'eu':,
# 'he':,
# 'hf':,
# 'hg':,
# 'ho':,
# 'in':,
# 'ir':,
# 'k':,
# 'kr':,
#
