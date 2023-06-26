import streamlit as st
from PIL import Image
import pandas as pd
import altair as alt
from datetime import datetime

st.set_page_config(page_title="KPI Tracker", layout="wide")

# Define function to create the line chart using Altair
def create_line_chart(df, title):
    # Convert Dates column to datetime type for plotting purposes
    df['Dates'] = pd.to_datetime(df['Dates'], format='%d/%m/%Y')

    # Define the line chart using Altair
    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('Dates:T', axis=alt.Axis(title='Date', format=("%d/%m/%Y"), tickCount=len(df.index))),
        y=alt.Y('Actual', sort=None, title='Targets'),
        tooltip=[alt.Tooltip('Dates', title='Date'), alt.Tooltip('Actual', title='Target')]
    ).properties(
        width=900  # Set the chart width to 900 pixels
    )

    # Add target line to chart
    target_line = alt.Chart(df).mark_line(strokeDash=[5, 5], stroke='red').encode(
        x='Dates',
        y=alt.Y('Target', sort=alt.EncodingSortField(field='Target', order='ascending')),
    )

    # Combine the two charts
    final_chart = chart + target_line

    # Set the subtitle of the chart
    st.subheader(title)

    st.altair_chart(final_chart)

    # Define the header of the table
    st.header(title)
    # Display the table
    st.write(df)


# Open image
image = Image.open('MJMEDICAL.png')

# Display image
st.image(image)

# Load data from Excel file
excel_file = 'data.xlsx'
xls = pd.ExcelFile(excel_file)

# Read sheets from Excel file
total_progress = pd.read_excel(xls, 'total_progress')
total_progress_with_specs_and_cost = pd.read_excel(xls, 'total_progress_with_specs_and_cost')
dataentry_progress = pd.read_excel(xls, 'dataentry_progress')
roomloading_progress = pd.read_excel(xls, 'roomloading_progress')
activity_progress = pd.read_excel(xls, 'activity_progress')
cost_progress = pd.read_excel(xls, 'cost_progress')
activity_room_progress = pd.read_excel(xls, 'activity_room_progress')

# Other sheets
costs = pd.read_excel(xls, 'costs')
cost_total = pd.read_excel(xls, 'cost_progress_total')
costs_to_do = pd.read_excel(xls, 'costs_to_do')
specs = pd.read_excel(xls, 'specs')
spec_progress = pd.read_excel(xls, 'spec_progress')
spec_room_progress = pd.read_excel(xls, 'spec_room_progress')
overall = pd.read_excel(xls, 'overall')
overall_audit = pd.read_excel(xls, 'overall_audit')
Priority_Rooms = pd.read_excel(xls, 'priority')

spec_audit = pd.read_excel(xls, 'spec_audit_progress')
data_audit = pd.read_excel(xls, 'dataentry_audit_progress')
activities_audit = pd.read_excel(xls, 'activities_audit_progress')
room_loading_audit = pd.read_excel(xls, 'room_loading_audit_progress')

# Sidebar options
option = st.sidebar.selectbox('Select an option', ['Room Progress', 'Progress', 'Audit'])

if option == 'Room Progress':
    charts = {
        'Total Room Progress (Equipment, Room loading, Activities & Costs)': total_progress,
        'Rooms with all equipment planning done': dataentry_progress,
        'Rooms with all room loading done': roomloading_progress,
        'Rooms with all activities done': activity_room_progress,
        'Rooms with all costs done': cost_total,
    }

    chart_choice = st.sidebar.selectbox('Choose chart', list(charts.keys()))
    selected_chart = charts[chart_choice]
    create_line_chart(selected_chart, chart_choice)

elif option == 'Progress':
    charts = {
        'Equipment Planning Progress': dataentry_progress,
        'Room Loading Progress': roomloading_progress,
        'Activity Progress': activity_progress,
        'Cost': cost_progress,
    }

    chart_choice = st.sidebar.selectbox('Choose chart', list(charts.keys()))
    selected_chart = charts[chart_choice]
    create_line_chart(selected_chart, chart_choice)

elif option == 'Audit':
    charts = {
        'Equipment planning': data_audit,
        'Activities': activities_audit,
        'Room Loading': room_loading_audit,
    }

    chart_choice = st.sidebar.selectbox('Choose chart', list(charts.keys()))
    selected_chart = charts[chart_choice]
    create_line_chart(selected_chart, chart_choice)

# CSS styling and other Streamlit configurations
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

style_css = """
<link rel="stylesheet" href="static\style.css">
"""
st.markdown(style_css, unsafe_allow_html=True)
