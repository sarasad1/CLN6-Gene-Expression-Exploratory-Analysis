import streamlit as st
import pandas as pd


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="CLN6 Gene Expression Explorer",
    page_icon="🧬",
    layout="wide"
)


# --------------------------------------------------
# Load data
# --------------------------------------------------

data = pd.read_csv("CLN6_expression.csv")


# --------------------------------------------------
# Calculate summary statistics
# --------------------------------------------------

wt_data = data.loc[data["Group"] == "Cln6_WT", "Expression"]
mutant_data = data.loc[data["Group"] == "Cln6_Mutant", "Expression"]

wt_mean = wt_data.mean()
mutant_mean = mutant_data.mean()

mean_difference = mutant_mean - wt_mean

# Statistical results obtained from the accompanying
# Google Colab analysis.

fold_change = 0.20056976742007995
p_value = 0.02677610935766152
cohens_d = 3.042470743854891


# --------------------------------------------------
# Title and project description
# --------------------------------------------------

st.title("🧬 CLN6 Gene Expression Explorer")

st.markdown("""
### Project Overview

This project explores Cln6 gene expression in wild-type and
Cln6 mutant mouse cerebellar cells using publicly available
microarray data from the NCBI Gene Expression Omnibus (GEO).

The analysis focuses on a simple research question:

> Does Cln6 expression differ between wild-type and Cln6 mutant cells?

The workflow starts with dataset inspection and probe annotation,
followed by gene-level expression comparison, statistical analysis,
and biological interpretation.

The results are presented through an interactive dashboard to make
the analysis easier to explore and understand.
""")


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.header("Explore the Data")

group_option = st.sidebar.selectbox(
    "Select group",
    ["All", "WT", "Mutant"]
)


# --------------------------------------------------
# Filter data
# --------------------------------------------------

if group_option == "WT":

    filtered_data = data[data["Group"] == "Cln6_WT"].copy()

elif group_option == "Mutant":

    filtered_data = data[data["Group"] == "Cln6_Mutant"].copy()

else:

    filtered_data = data.copy()


# --------------------------------------------------
# Key results
# --------------------------------------------------

st.subheader("Key Results")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "WT Mean",
    f"{wt_mean:.2f}"
)

col2.metric(
    "Mutant Mean",
    f"{mutant_mean:.2f}"
)

col3.metric(
    "Mutant / WT Fold Change",
    f"{fold_change:.2f}"
)

col4.metric(
    "Welch's p-value",
    f"{p_value:.4f}"
)


# --------------------------------------------------
# Expression visualization
# --------------------------------------------------

st.subheader("CLN6 Expression by Sample")

plot_data = filtered_data.copy()

plot_data["Group"] = plot_data["Group"].replace({
    "Cln6_WT": "WT",
    "Cln6_Mutant": "Mutant"
})

st.scatter_chart(
    plot_data,
    x="Sample",
    y="Expression",
    color="Group"
)


# --------------------------------------------------
# Selected samples
# --------------------------------------------------

st.subheader("Selected Samples")

st.dataframe(
    filtered_data,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# Statistical summary
# --------------------------------------------------

st.subheader("Statistical Summary")

stats_table = pd.DataFrame({
    "Measure": [
        "WT mean (log2 expression)",
        "Mutant mean (log2 expression)",
        "Mean difference (Mutant - WT)",
        "Fold change (Mutant / WT)",
        "Welch's t-test p-value",
        "Cohen's d"
    ],
    "Value": [
        wt_mean,
        mutant_mean,
        mean_difference,
        fold_change,
        p_value,
        cohens_d
    ]
})

st.dataframe(
    stats_table,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# Interpretation
# --------------------------------------------------

st.subheader("Exploratory Interpretation")

st.write(
    """
    CLN6 expression appears higher in the wild-type group
    than in the mutant group.

    The mutant-to-wild-type fold change was approximately
    0.20 after back-transformation from the log2 expression
    scale. This corresponds to approximately 20% of the
    wild-type expression level on the linear scale.

    Welch's t-test produced a p-value of approximately 0.0268.
    However, only three biological replicates were available
    per group. Therefore, this result should be interpreted
    as exploratory evidence of a difference rather than
    definitive evidence of a biological effect.
    """
)


# --------------------------------------------------
# Dataset information
# --------------------------------------------------

st.subheader("Dataset Information")

st.write(
    """
    **Dataset:** GSE24368

    **Organism:** Mus musculus

    **Platform:** Affymetrix Mouse Genome 430 2.0 Array (GPL1261)

    **Data type:** Microarray gene expression

    **Preprocessing:** GC-RMA normalized log2 expression values

    **CLN6 probe:** 1454837_at

    **Groups analyzed:**
    - 3 Cln6_WT samples
    - 3 Cln6_Mutant samples
    """
)


# --------------------------------------------------
# Limitations
# --------------------------------------------------

st.subheader("Limitations")

st.write(
    """
    - Only three biological replicates were available for each group.
    - This is an exploratory single-gene analysis.
    - The analysis uses one CLN6 probe from an Affymetrix microarray.
    - The results indicate an association between genotype and
      CLN6 expression but do not establish causality.
    - Additional experimental validation would be required.
    """
)
