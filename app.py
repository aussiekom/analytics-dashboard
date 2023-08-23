import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard", layout="wide")
st.subheader("Analytics Dashboard")
st.markdown("##")

# Load the new dataset
df = pd.read_csv('superstore.csv')

# Sidebar filters
st.sidebar.header("Please filter")
category = st.sidebar.selectbox("Select Category", options=df["Category"].unique())

# Dynamically populate sub-category options based on selected category
sub_category_options = df[df["Category"] == category]["Sub-Category"].unique()
sub_category = st.sidebar.selectbox("Select Sub-Category", options=sub_category_options)

df_selection = df.query("Category == @category & `Sub-Category` == @sub_category")

def Home():
    # Display data in an expander
    with st.expander("Dataset Overview"):
        show_data = st.multiselect('Filter: ', df_selection.columns, default=["Category", "Sub-Category", "Sales", "Profit"])
        st.dataframe(df_selection[show_data], use_container_width=True)

    # Compute top analytics
    total_sales = float(df_selection['Sales'].sum())
    total_profit = float(df_selection['Profit'].sum())

    total1, total2 = st.columns(2, gap='large')
    with total1:
        st.info('Total Sales')
        st.metric(label="Total Sales", value=f"${total_sales:,.2f}")

    with total2:
        st.info('Total Profit')
        st.metric(label="Total Profit", value=f"${total_profit:,.2f}")

    st.markdown("""---""")

    # Line chart for sales and profit over time
    time_series_data = df_selection.groupby("Order Date").sum()[["Sales", "Profit"]]
    time_series_data.reset_index(inplace=True)

    fig_time_series = px.line(
        time_series_data,
        x="Order Date",
        y=["Sales", "Profit"],
        title="<b>Sales and Profit Over Time</b>",
        labels={"value": "Amount", "Order Date": "Date"},
        template="plotly_white"
    )

    fig_time_series.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False)
    )

    # Render the time series line chart
    st.plotly_chart(fig_time_series, use_container_width=True)

# Forecast


# sidebar menu
def sideBar():
    with st.sidebar:
        selected = st.selectbox(
            "Main Menu",
            options=["Home", "Forecast"],
            format_func=lambda x: "Home" if x == "Home" else "Forecast"
        )

    if selected == "Home":
        Home()
    elif selected == "Forecast":
        forecast()

sideBar()

# Theme
hide_st_style = """
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""
