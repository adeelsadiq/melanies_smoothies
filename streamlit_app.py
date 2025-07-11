# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw: ")
st.write(
  """Choose the fruit you want in your custom smoothie
  """
)
st.write(
  """Choose up to five ingredients
  """
)

cnx= st.connection("snowflake")
session = cnx.session()
name_on_order = st.text_input("Name on Smoothie:", "")
st.write("the name on your smoothie will be: ", name_on_order)
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width= True)
st.stop()
ingredients_list = st.multiselect(
    "What are your favourite fruits?",
    my_dataframe,
    max_selections=5
)
if ingredients_list: 
    st.write("""Your selection is: """)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen+' '
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width = True)

    st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)values 
    ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    st.write(my_insert_stmt)
    # st.stop()
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+name_on_order+'! ', icon="✅") 
# st.text(smoothiefroot_response.json())

# st.dataframe(data=my_dataframe, use_container_width=True)
