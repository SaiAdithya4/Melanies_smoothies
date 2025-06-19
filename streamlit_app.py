# Import python packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# Load secrets stored in Streamlit Cloud
sf_config = st.secrets["connection"]["snowflake"]

# Create Snowpark session manually
session = Session.builder.configs(sf_config).create()

# Write directly to the app
st.title("Customize Your SMOOTHIE🥤")
st.write("Choose the fruits you want in your custom SMOOTHIE🥤.")

# Input: name on order
name_on_order = st.text_input('Name on SMOOTHIE')
st.write('The name on SMOOTHIE will be:', name_on_order)

# Get fruit list from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
fruit_list = [row["FRUIT_NAME"] for row in my_dataframe.collect()]

# Select ingredients
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

# Handle form logic
if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)
    st.write(ingredients_string)

    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! ✅')
