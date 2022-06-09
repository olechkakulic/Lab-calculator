import streamlit as st
import pandas as pd
from count import *
import os
from count import calc_TE_pol
from bokeh.plotting import figure



def interpol(mat, wl):
    with open('DataFiles/' + mat + '.csv', 'r') as f:
        lines = f.readlines()
        for i in range(2, len(lines)):
            line_prev = lines[i - 1].split(',')
            line_cur = lines[i].split(',')
            if float(line_prev[0]) <= wl <= float(line_cur[0]):
                return (float(line_cur[1]) - float(line_prev[1])) / (float(line_cur[0]) - float(line_prev[0])) * (
                            wl - float(line_prev[0])) + float(line_prev[1])
    return 1


def update_n(a, inp_wl):
    n = []
    for mat in a:
        # n.append(get_coefficent(str(mat), float(inp_wl)))
        n.append(interpol(str(mat), float(inp_wl)))
    return n


# работа с файлами
@st.cache
def load_dataset(data_link):
    dataset = pd.read_csv(data_link)
    return dataset


directory = 'DataFiles'
files = os.listdir(directory)
filenames = []
for i in range(len(files)):
    filenames.append(str(files[i][:-4]))

# ЗАГОЛОВКИ
st.title("Калькулятор Брэгговского зеркала")
# код для вводимых данных
angle_input = st.sidebar.number_input('Значение угла', min_value=0, max_value=90, step=5)
angle_input = angle_input * 2 * pi / 360
polarisation = st.sidebar.selectbox(
    'Тип поляризации',
    ('TE', 'TM',))
n_pod = 1.00
n_air = 1.00
input_wl = st.sidebar.number_input(f"Длина волны,мкм", min_value=0.4, max_value=0.8, step=0.05)
container = st.container()
ncol = st.sidebar.number_input("Введите количество слоев", min_value=0, step=1)
nal = []
h = []
layers_name = []

for i in range(ncol):
    a = st.sidebar.selectbox(f"Материал слоя # {i + 1}", (filenames), key=i)
    layers_name.append(a)
    if a:
        tolсhina = st.sidebar.number_input(f"Толщина {i + 1} слоя,мкм", min_value=0.03, max_value=0.4, step=0.01)
        h.append(tolсhina * 10 ** (-6))
        enable_wave_lenght = st.sidebar.checkbox(f'Коэф-т преломления слоя {i + 1} постоянен')
        if enable_wave_lenght:
            n = st.sidebar.number_input(f'Введите коэффициент преломления {i + 1} слоя', min_value=0.001,
                                        max_value=5.00, step=0.01)
            nal.append(n)
        else:
            # na = get_coefficent(str(a), float(input_wl))
            na = interpol(str(a), float(input_wl))
            n = st.sidebar.write(f' n({i + 1}) = {na}')
            nal.append(na)
            #nal.append(f"{na:.2}")
if st.button('Рассчитать') and ncol > 0:
    r_coef1, t_coef1 = calc_TE_pol(ncol - 1, nal, angle_input, h, input_wl, n_pod, n_air, str(polarisation))
    Result = f"Коэффициент отражения: {r_coef1}",f" Коэффициент пропускания: {t_coef1}"
    st.info(Result)
    angles = []
    # powers00=[]
    powersnn = []
    # T_0N=[]
    T_N0_angle = []
    for i in range(0, 90, 1):
        i = i * 2 * pi / 360
        angles.append(i)
        # powers00.append(calc_TE_pol(ncol - 1, nal, i, h, input_wl, n_pod, n_air)[0])
        powersnn.append(round(calc_TE_pol(ncol - 1, nal, i, h, input_wl, n_pod, n_air, str(polarisation))[0], 3))
        T_N0_angle.append(round(calc_TE_pol(ncol - 1, nal, i, h, input_wl, n_pod, n_air, str(polarisation))[1], 3))
    # fig1=figure(
    #     title='R00(angle)',
    #     x_axis_label='angle, grad',
    #     y_axis_label='R00'
    # )
    # fig1.line(angles, powers00, legend_label='Olya1', line_width=2)
    # st.bokeh_chart(fig1, use_container_width=True)

    fig2 = figure(
        title='RNN(angle)',
        x_axis_label='angle, grad',
        y_axis_label='Power reflection'
    )
    fig2.line(angles, powersnn, line_width=2)
    st.bokeh_chart(fig2, use_container_width=True)

    fig3 = figure(
        title='TNN(angle)',
        x_axis_label='angle, rad',
        y_axis_label='Transmission coefficient'
    )
    fig3.line(angles, T_N0_angle, line_width=2)
    st.bokeh_chart(fig3, use_container_width=True)

    powersnn_wave = []
    T_N0_wave = []
    wawes = []
    for waw in numpy.arange(0.4, 0.8, 0.001):
        wawes.append(waw)
        p = calc_TE_pol(ncol - 1, update_n(layers_name, waw), angle_input, h, waw, n_pod, n_air, str(polarisation))[0]
        if p<=0:
            powersnn_wave.append(0)
        elif p>0 and p<1:
            powersnn_wave.append(round(p, 5))
        elif p>=1:
            powersnn_wave.append(1)
        #powersnn_wave.append(round(p, 5))
        print(p)
        s=calc_TE_pol(ncol - 1, update_n(layers_name, waw), angle_input, h, waw, n_pod, n_air, str(polarisation))[1]
        if s <= 0:
            T_N0_wave.append(0)
        elif s > 0 and s < 1:
            T_N0_wave.append(round(s, 5))
        elif s >= 1:
            T_N0_wave.append(1)
            # powersnn_wave.append(round(p, 5))
        print(s)

    st.write(powersnn_wave, T_N0_wave)
    fig3 = figure(
        title='RNN(wave)',
        x_axis_label='wave, µm',
        y_axis_label='RNN'
    )
    fig3.line(wawes, powersnn_wave, line_width=2)
    st.bokeh_chart(fig3, use_container_width=True)

    fig4 = figure(
        title='TNN(wave)',
        x_axis_label='wave, нм',
        y_axis_label='TNN'
    )
    fig4.line(wawes, T_N0_wave, line_width=2)
    st.bokeh_chart(fig4, use_container_width=True)
