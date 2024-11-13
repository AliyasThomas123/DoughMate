import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os , pickle


def get_pizza_sales_data(start_date ,end_date):
    train_df = pd.read_excel("./dataset.xlsx",parse_dates=True)
    ingredients = pd.read_excel("./Data/Pizza_ingredients.xlsx")
    ingredients['Total_Quantity'] = 0
    count_list =[]
    for family in train_df['pizza_name_id'].unique():
            pizza_count ={}
            train =   train_df.loc[train_df['pizza_name_id'] == family]
            train_ = train.groupby(['order_date', 'pizza_name_id']).agg({'quantity': 'sum'}).reset_index()
            train_ = train_[['order_date', 'quantity']]
            train_['order_date'] = pd.to_datetime(train_['order_date'])
            file_path = f"./Arima_models/"
            file_name = f"Arima_{family}.pkl" 
         
            full_path = os.path.join(file_path, file_name)

          
            with open(full_path, 'rb') as f:
                model = pickle.load(f)

            print(f"Model loaded from {full_path}")

           
            #start_date_obj = datetime.strptime(start_date, '%Y/%m/%d')
            #end_date_obj =datetime.strptime(end_date, '%Y/%m/%d')
            formatted_start_date = start_date.strftime('%Y-%m-%d')
            formatted_end_date = end_date.strftime('%Y-%m-%d')


            date_range = pd.date_range(start=formatted_start_date, end=formatted_end_date, freq='D')

           
            df_dates = pd.DataFrame(date_range, columns=['Date'])
           
            pred = model.predict(start=len(train_), end=len(train_) + len(df_dates) -1, typ='levels').rename('ARIMA predictions')

       
            #print(pred)
            p=list(pred)
            res=sum(p)
            piz_count = round(res,0)
            pizza_count[family] = round(res,0)
            count_list.append(pizza_count)
            print("ROUNDED----",round(res,0))
            

            ingredients.loc[ingredients['pizza_name_id'] == family, 'Total_Quantity'] = ingredients['Total_Quantity']+ingredients['Items_Qty_In_Grams'] * piz_count
    
    print("PIZZA---COUNT",count_list)
    return ingredients,count_list

# Sidebar Period Picker

st.markdown("""
    <style>        
 .glow-img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 50%;
        box-shadow: 0 0 15px red, 0 0 30px red, 0 0 45px red;
        border-radius: 10px;
    }
          </style>
            """
            ,unsafe_allow_html=True)
with st.sidebar:
    image_path = "https://img.freepik.com/premium-vector/slice-pizza-cartoon-character-ilustraion-funny-pose-fast-food-ilustration_1289230-15.jpg?ga=GA1.1.293997524.1725359861"
    st.markdown(f'<img src="{image_path}" style="width:100%; height:auto;" class ="glow-img">'
                ,unsafe_allow_html=True)
    st.header("Select Period")
    
    # Form for date selection and submission
    with st.form(key='date_form'):
        period = st.selectbox(
            'Duration',
            ('Next 7 Days', 'Next 14 Days', 'Next 30 Days','Custom'),
            index=1
        )
        
        # Convert selected period to days
        days_map = {'Next 7 Days': 7, 'Next 14 Days': 14, 'Next 30 Days': 30,'Custom':0}
        selected_days = days_map[period]
        
        # Calculate default start and end dates
        start_date = datetime.today()
        end_date = start_date + timedelta(days=selected_days)
        
        # Display the start and end date in date picker
        selected_start_date = st.date_input("Start Date", start_date)
        selected_end_date = st.date_input("End Date", end_date)
        
        # Submit button
        submit_button = st.form_submit_button(label='Submit')
st.title(f"DoughMate")
if submit_button:
    pizza_sales_df,count_list = get_pizza_sales_data(start_date , end_date)
    sales = pd.DataFrame([{'pizza_type': k, 'quantity': v} for item in count_list for k, v in item.items()])
    res=pizza_sales_df.groupby('pizza_ingredients')['Total_Quantity'].aggregate('sum').reindex()
    # Main Panel
    

    # 1. Display total number of pizza sales
    total_sales = 10
    #st.metric(label="Total Pizza Sales", value=total_sales)

    with st.expander("Purchase Order"):
        st.subheader("Purchase Order")
        st.markdown(f"<h6>{selected_start_date} - {selected_end_date}</h6>", unsafe_allow_html=True)
     
        
        st.dataframe(res,height=600, width=800)

    # 3. Insight button simulation using expander (acts like a modal)
    with st.expander("Show Insights"):
        st.write("Here are the insights based on pizza sales:")
        st.dataframe(sales,height=600, width=800)
        # Generate a bar plot for pizza sales by type
        fig, ax = plt.subplots()
        plt.figure(figsize=(5,56))
        sales.groupby('pizza_type')['quantity'].sum().plot(kind='bar', ax=ax)
        plt.title('Pizza Sales by Type')
        plt.xlabel('Pizza Type')
        plt.ylabel('Sales Expecting')
        st.pyplot(fig)

    # Save the selected start and end dates for future use
    st.session_state['start_date'] = selected_start_date
    st.session_state['end_date'] = selected_end_date
