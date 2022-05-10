import pandas as pd
import time
import streamlit as st
import plotly.express as px
@st.cache
def load_dataset(data_link):
    dataset = pd.read_csv(data_link)
    return dataset


titanic_link = 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv'
titanic_data = load_dataset(titanic_link)
#ЗАГОЛОВКИ #
st.title("Калькулятор Брэгговского зеркала")
st.markdown("Welcome to this in-depth introduction to [...].")
st.header("Customary quote")
st.markdown("> I just love to go home, no matter where I am [...]")
#ПРИКОЛЬНАЯ ШТУКА #
age_columns = st.beta_columns(2)
age_min = age_columns[0].number_input("Minimum Age", value=titanic_data['age'].min())
age_max = age_columns[1].number_input("Maximum Age", value=titanic_data['age'].max())
if age_max < age_min:
    st.error("The maximum age can't be smaller than the minimum age!")
else:
    st.success("Congratulations! Correct Parameters!")
    subset_age = titanic_data[(titanic_data['age'] <= age_max) & (age_min <= titanic_data['age'])]
    st.write(f"Number of Records With Age Between {age_min} and {age_max}: {subset_age.shape[0]}")