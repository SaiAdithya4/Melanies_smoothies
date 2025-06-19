# ✅ Do NOT import get_active_session
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# ✅ Get Snowflake credentials from Streamlit Cloud Secrets
sf_config = st.secrets["connection"]["snowflake"]

# ✅ Create Snowpark session manually
session = Session.builder.configs(sf_config).create()

# 🧃 UI
st.title("Customize Your SMOOTHIE 🥤")
st.write("Choose the fruits you want in your custom SMOOTHIE.")

# 👤 Name input
name_on_order = st.text_input("Name on SMOOTHIE")
st.write("The name on SMOOTHIE will be:", name_on_order)

# 🍓 Load fruit list from Snowflake table
fruit_df = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
fruit_list = [row["FRUIT_NAME"] for row in fruit_df.collect()]

# 🍍 Ingredient selection
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

# ✅ Submit button
if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)
    st.write("Ingredients:", ingredients_string)

    insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    if st.button("Submit Order"):
        session.sql(insert_stmt).collect()
        st.success("✅ Your Smoothie is ordered!")
