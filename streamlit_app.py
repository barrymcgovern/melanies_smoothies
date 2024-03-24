# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Soothie Order Form Test :cup_with_straw:")
st.write(
    """Choose the fruits you want
    """
)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your Smoothie order is ' + name_on_order)

ingredients_list = st.multiselect (
    'Choose up to 5 ingredients',
    my_dataframe,
     max_selections=5
)

ingredients_string = ''

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    st.write(my_insert_stmt);
    
    if ingredients_string:
        if name_on_order:
            time_to_insert = st.button('Submit Order')
            if time_to_insert:
                session.sql(my_insert_stmt).collect()
                st.success('Your Smoothie is ordered!', icon="✅")




