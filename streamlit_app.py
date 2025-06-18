# Import python packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your SMOOTHIE🥤")
st.write(
    """Choose the fruits you want in your custom SMOOTHIE🥤."""
)

# Create Snowflake session config (replace with your values)
connection_parameters = {
    "account": "YRDDECB-KTB35239",
    "user": "SaiAdithya",
    "password": "SaiAdithya@4804",
    "role": "ACCOUNTADMIN",  # optional, change if needed
    "warehouse": "COMPUTE_WH",
    "database": "smoothies",
    "schema": "public"
}

# Create and set active session
session = Session.builder.configs(connection_parameters).create()
Session._set_active_session(session)  # This is necessary for get_active_session()

# Streamlit UI
name_on_order = st.text_input('Name on SMOOTHIE')
st.write('The name on SMOOTHIE will be:', name_on_order)

# Get fruit options from Snowflake table
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
fruit_names = [row["FRUIT_NAME"] for row in my_dataframe.collect()]  # Convert to list of strings

# Ingredient selection
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_names,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)

    st.write("You selected:", ingredients_string)

    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
