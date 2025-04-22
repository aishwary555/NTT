import streamlit as st
import pandas as pd
from oeee_calculator import calculate_oee
from query_parser import extract_filters_from_query

st.set_page_config(page_title="GenAI OEE Assistant", layout="centered")
st.title("🤖 GenAI OEE Assistant")
st.markdown("Ask a question like: **Show me the OEE of device D100 in Mumbai in March**")

uploaded_file = st.file_uploader("Upload IoT sensor Excel file", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    query = st.text_input("💬 Enter your query:")

    if query:
        with st.spinner("Analyzing your query..."):
            filters = extract_filters_from_query(query)
            if None in filters.values():
                st.error("Could not extract all filters from the query.")
            else:
                oee = calculate_oee(df, filters["device_id"], filters["location"], filters["month"])
                if oee is None:
                    st.warning("No matching data found.")
                else:
                    st.success(f"OEE for Device **{filters['device_id']}** at **{filters['location']}** in **Month {filters['month']}** is **{oee}%**")
