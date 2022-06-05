#import time
import streamlit as st
import pandas as pd
from numpy import pi
import numpy as np
#from urllib.request import urlopen
#import json
import os
#from openpyxl import load_workbook
from plot import calc_TE_pol
from bokeh.plotting import figure

def get_step(material_name, types):
    if types == 1:
        return float(globals()[material_name]['wl'].values[0])
    elif types == 2:
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
lol =st.sidebar.number_input('Значение угла', min_value=0, max_value=90, step=1)
lol=lol*2*pi/360
cock = st.sidebar.selectbox(
     'Тип поляризации',
     ('TE', 'TM',))
n_air=st.sidebar.number_input('Коэф-т преломления среды', min_value=0.01, max_value=3.00, step=0.01)
n_pod =st.sidebar.number_input('Коэф-т преломления подложки', min_value=0.01, max_value=3.00, step=0.01)


# функция для посчитать
container = st.container()
ncol = st.sidebar.number_input("Введите количество слоев",  min_value=0, step=1)
# cols = container.columns(ncol)
nal=[]
wl=[]
h=[]


for i in range(ncol):
    a = st.sidebar.selectbox(f"Номер слоя # {i+1}", (filenames), key=i)
    if a:
        input_wl = st.sidebar.number_input(f"Длина волны,м {i+1} слоя", min_value=get_step(str(a), 1), max_value=get_step(str(a), 2), step=0.01, key=str(a))
        wl.append(input_wl)
        tolshina = st.sidebar.number_input(f"Толщина,м {i+1} слоя", min_value=0.000, max_value=0.010, step=0.001, format="%f")
        h.append(tolshina)
        enable_wave_lenght = st.sidebar.checkbox(f'Коэф-т приломления слоя {i+1} постоянен')
        if input_wl and enable_wave_lenght:
            n = st.sidebar.number_input(f'Введите коэффициент преломления {i+1} слоя', min_value=0.001, max_value=5.00, step=0.01)
            nal.append(n)
        else:
            na = get_coefficent(str(a), float(input_wl))
            n = st.sidebar.write(f' n({i}) = {na}')
            nal.append(na)
if st.button('Люблю сему') and cock=='TE':
    BOba = calc_TE_pol(ncol-1, nal, lol, h, wl, n_pod, n_air)
    st.write(BOba)
    angles=[]
    powers00=[]
    powersnn=[]
    for i in range(0,90):
        i=i*2*pi/360
        angles.append(i)
        powers00.append(calc_TE_pol(ncol - 1, nal, i, h, wl, n_pod, n_air)[0])
        powersnn.append(calc_TE_pol(ncol - 1, nal, i, h, wl, n_pod, n_air)[1])
    fig1=figure(
        title='R00(angle)',
        x_axis_label='angle, grad',
        y_axis_label='R00'
    )
    fig1.line(angles, powers00, legend_label='Olya1', line_width=2)
    st.bokeh_chart(fig1, use_container_width=True)
    fig2 = figure(
        title='R00(angle)',
        x_axis_label='angle, grad',
        y_axis_label='RNN'
    )
    fig2.line(angles, powersnn, legend_label='Olya2', line_width=2)
    st.bokeh_chart(fig2, use_container_width=True)
