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

# Calculate group means
wt_mean = data.loc[data["Group"] == "Cln6_WT", "Expression"].mean()
mutant_mean = data.loc[data["Group"] == "Cln6_Mutant", "Expression"].mean()

# Fold change on the original expression scale
fold_change = 0.20056976742007995

# Statistical result from the exploratory analysis
p_value = 0.02677610935766152

st.subheader("Key Results")

col1, col2, col3, col4 = st.columns(4)

col1.metric("WT Mean", f"{wt_mean:.2f}")
col2.metric("Mutant Mean", f"{mutant_mean:.2f}")
col3.metric("Fold Change", f"{fold_change:.2f}")
col4.metric("Welch's p-value", f"{p_value:.4f}")

st.subheader("Expression Data")

st.dataframe(data, use_container_width=True)
