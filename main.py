import pandas as pd
import time
import streamlit as st
import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from urllib.request import urlopen
import json

@st.cache
def load_dataset(data_link):
    dataset = pd.read_csv(data_link)
    return dataset


titanic_link = 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv'
titanic_data = load_dataset(titanic_link)
#ЗАГОЛОВКИ #
st.title("Калькулятор Брэгговского зеркала")
st.markdown("Welcome to this in-depth introduction to [...].")
#код для вводимых данных
st.number_input('Длина волны', min_value = 0, max_value = 1000, step = 1)
st.number_input('Значение угла', min_value = 0, max_value = 180, step = 1)
st.selectbox(
     'Тип поляризации',
     ('TE', 'TM',))
