# Import python packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# Snowflake connection config (replace with real credentials or use st.secrets)
connection_parameters = {
    "account": "YRDDECB-KTB35239",
    "user": "SaiAdithya",
    "password": "SaiAdithya@4804",
    "role": "ACCOUNTADMIN",
    "warehouse": "COMPUTE_WH",
    "database": "smoothies",
    "schema": "public"
}

# Create and use Snowpark session directly (no get_active_session)
session = Session.builder.configs(connection_parameters).create()

# Streamlit UI
st.title("Customize Your SMOOTHIE🥤")
st.write("Choose the fruits you want in your custom SMOOTHIE🥤.")

name_on_order = st.text_input('Name on SMOOTHIE')
st.write('The name on SMOOTHIE will be:', name_on_order)

# Fetch fruit names from Snowflake
fruit_df = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
fruit_list = [row["FRUIT_NAME"] for row in fruit_df.collect()]  # Convert to list

# Ingredient selector
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

# Handle order submission
if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)
    st.write("Ingredients selected:", ingredients_string)

    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    if st.button("Submit Order"):
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
