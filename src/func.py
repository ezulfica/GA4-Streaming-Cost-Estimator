import streamlit as st
from datetime import timedelta
import pandas as pd
from src.hypothesis import DW_hypothesis

def initialize_app():
    st.title('GA4 Cost Estimators')
    provider = st.selectbox(
        label="Select your Datawarehouse solution",
        options=["BigQuery", "Snowflake"],
        placeholder="Choose an option"
    )
    return provider

def display_hypothesis(provider):
    value_hypothesis = DW_hypothesis(choice=provider)
    hypothesis_dt = pd.DataFrame.from_dict(value_hypothesis[1], orient='index', columns=['Hypothesis'])
    hypothesis_dt['Hypothesis'] = hypothesis_dt['Hypothesis'].str.replace("\n", "<br>")
    st.markdown(
        """
        <style>
            .dataframe th, .dataframe td {
                white-space: pre-line !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown(hypothesis_dt.to_html(escape=False), unsafe_allow_html=True)
    return value_hypothesis[0]

def get_user_inputs():
    col1, col2, col3 = st.columns(3)
    with col1:
        num_events = st.number_input(label="Daily events (AVG)", min_value=0, step=1, key="num_event")
    with col2:
        start_date = st.date_input(label="Date", format="YYYY-MM-DD")
    with col3:
        retention = st.number_input(label="Data retention (year)", min_value=0, step=1)
    return num_events, start_date, retention

def calculate_costs(num_events, start_date, retention, params):
    daily_cost = num_events * params['GB_cost'] / params['GB_events']
    daily_gb = num_events / params['GB_events']
    retention_days = retention * 365
    
    date_index = [start_date + timedelta(days=i) for i in range(retention_days + 1)]
    storage_gb = [daily_gb * i for i in range(retention_days + 1)]
    ingestion_cost = [round(daily_cost, 2) for _ in range(retention_days + 1)]
    storage_cost_gb = [params['storage_cost'](gb) for gb in storage_gb]

    df = pd.DataFrame({
        "date": date_index,
        "Storage (GB)": storage_gb,
        "Ingestion Cost ($)": ingestion_cost,
        "Storage Cost ($)": storage_cost_gb,
    })
    df["Compute Cost ($)"] = df.apply(lambda x: params['compute_cost'](x["Storage (GB)"], date=x["date"]), axis=1)
    df["Period"] = df["date"].astype(str).str[:7]
    df["year"] = df["date"].astype(str).str[:4]
    return df

def display_results(df, retention):
    monthly_cost = df.groupby(["year", "Period"]).agg({
        "Storage (GB)": "max", 
        "Storage Cost ($)": "max", 
        "Ingestion Cost ($)": "sum", 
        "Compute Cost ($)": "max"
    })
    monthly_cost["Total $"] = monthly_cost["Storage Cost ($)"] + monthly_cost["Ingestion Cost ($)"] + monthly_cost["Compute Cost ($)"]

    yearly_cost = monthly_cost.groupby("year").agg({
        "Storage (GB)": "max", 
        "Storage Cost ($)": "sum", 
        "Ingestion Cost ($)": "sum", 
        "Compute Cost ($)": "sum", 
        "Total $": "sum"
    })

    last_value = df.tail(1)
    total_cost = (
        last_value["Compute Cost ($)"].iloc[0] * 12 +
        last_value["Ingestion Cost ($)"].iloc[0] * 365 +
        last_value["Compute Cost ($)"].iloc[0] * 365
    )
    st.write(f"After {retention} years, your annual cost will be {round(total_cost, 2)}$")
    st.write("Yearly Cost in $")
    st.write(yearly_cost)
    st.write("Monthly Cost in $")
    st.write(monthly_cost)
    


