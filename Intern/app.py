#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import os
import base64 

st.sidebar.image("main.jpg", use_column_width=False)
st.sidebar.markdown("""> Created by: [Team 6]""")

user_color = "#FFFFF"
title_webapp = "Certificate Verification"
html_temp = f"""
            <div style="background-color:{user_color};padding:12px">
            <h1 style="yellow:blue;text-align:center;">{title_webapp}
            </div>
            """
st.markdown(html_temp, unsafe_allow_html=True)

def load_data(excel_file):
    return pd.read_excel(excel_file)

def get_info_by_certification_id(df,cert_id):
    info = df[df["Certification ID "] == cert_id]
    return info

def get_info_by_intern_id(df,intern_id):
    info = df[df["Intern ID "] == intern_id]
    return info

def add_intern_info(df,intern_info):
    return df.append(intern_info, ignore_index=True)

def delete_intern_info(df,intern_id):
    return df[df["Intern ID "] != intern_id]

def save_data(df,excel_file):
    df.to_excel(excel_file, index=False)

data = load_data("Intern_data.xlsx")

use_case = st.sidebar.selectbox("Select Use Case:",("Verified by Certification Id","Verified by Intern Id",
                                                "Add/Delete Intern Info"))

if use_case == "Verified by Certification Id":
    cert_id = st.sidebar.text_input("Enter Certification ID:")
    if st.sidebar.button("Show"):
        info = get_info_by_certification_id(data,cert_id)
        if not info.empty:
            st.success("Verified ✔️")
            st.write(info[["Intern ID ","Name","Join date","Department","Email_ID"]])
        else:
            st.write("No information found for the given Certification ID.")

elif use_case == 'Verified by Intern Id':
    intern_id = st.sidebar.text_input("Enter Intern ID:")
    if st.sidebar.button("Show"):
        info = get_info_by_intern_id(data,intern_id)
        if not info.empty:
            st.success("Verified ✔️")
            st.write(info[["Name","Join date","Department","Email_ID"]])
        else:
            st.write("No information found for the given Intern ID.")

else:
    st.sidebar.header("Add Intern Info")
    certification_id = st.sidebar.text_input("Certification ID ")
    intern_id = st.sidebar.text_input("Intern ID ")
    name = st.sidebar.text_input("Name")
    join_date = st.sidebar.text_input("Join Date")
    department = st.sidebar.text_input("Department")
    email_id = st.sidebar.text_input("Email ID")

    if st.sidebar.button("Add"):
        new_intern_info = {"Certification ID ": certification_id,"Intern ID ": intern_id,"Name": name,"Join date": join_date,
                           "Department": department,"Email_ID": email_id}
        data = add_intern_info(data, new_intern_info)
        st.success("Intern information added successfully!")
        st.write("Verifying added intern information:")
        info = get_info_by_intern_id(data,intern_id)
        if not info.empty:
            st.success("Verified ✔️")
            st.write(info[["Name","Join date","Department","Email_ID"]])
            save_data(data,"Intern_data.xlsx")
        else:
            st.write("No information found for the added Intern ID.")

    st.sidebar.header("Delete Intern Info")
    delete_id = st.sidebar.text_input("Intern ID to delete")

    if st.sidebar.button("Delete"):
        data = delete_intern_info(data,delete_id)
        st.success("Intern information deleted successfully!")
        st.write("Verifying deleted intern information:")
        info = get_info_by_intern_id(data,delete_id)
        if info.empty:
            st.write("Intern information deleted successfully!")
            save_data(data,"Intern_data.xlsx")
        else:
            st.write("Intern information still exists for the deleted Intern ID.")


if st.sidebar.button("Download Updated CSV"):
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode() 
    href = f'<a href="data:file/csv;base64,{b64}" download="updated_data.csv">Download Updated CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)


# In[ ]:




