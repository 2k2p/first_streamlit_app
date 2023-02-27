import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My parents new healthy diner')

streamlit.header('🥣Breakfast Menu')
streamlit.text('🥗Omega 3 & Blueberry Oatmeal')
streamlit.text('🐔Kale, Spinach & Rocket Smoothie')
streamlit.text('🥑🍞Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')

my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

def get_fruitvice_data(choice1):
  fruityvice_responce = requests.get("https://fruityvice.com/api/fruit/"+choice1)
  fruityvice_normalized = pandas.json_normalize(fruityvice_responce.json())
  return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
     streamlit.error('Please select fruit to to get info.')
  else :   
    value = get_fruitvice_data(fruit_choice)
    streamlit.dataframe(value)

except URLError as e:
  streamlit.error()
  
#streamlit.stop()

streamlit.header("View Our Fruit List OR Add New Fruit")

def get_fruit_list():
  with my_cnx.cursor() as my_cur:
       my_cur.execute("select * from FRUIT_LOAD_LIST")
       return my_cur.fetchall()

if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows=get_fruit_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)

  
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
       my_cur.execute("insert into FRUIT_LOAD_LIST values ('" +new_fruit+"')")
       return 'Thanks for adding ', add_my_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
msg = insert_row_snowflake(add_my_fruit)
my_cnx.close()
streamlit.text(msg)
      
#my_cur.execute("insert into FRUIT_LOAD_LIST values ('from streamlit')")
