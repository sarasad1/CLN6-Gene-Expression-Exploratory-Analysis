import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="CLN6 Gene Expression Explorer",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 CLN6 Gene Expression Explorer")

st.write(
    "An exploratory analysis of CLN6 gene expression "
    "in wild-type and mutant mouse cerebellar cells."
)

data = pd.read_csv("CLN6_expression.csv")

st.subheader("Expression Data")

st.dataframe(data, use_container_width=True)
