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
# Dataset & Samples
# --------------------------------------------------

st.subheader("📂 Dataset & Samples")

st.markdown("""
The analysis uses publicly available gene expression data from the
NCBI Gene Expression Omnibus (GEO).

The original dataset contains 12 samples representing different
experimental groups. For this analysis, we focused specifically on
the samples associated with the Cln6 genotype.
""")

# Number of samples and groups from the loaded data
n_samples = len(data)
groups = data["Group"].unique()
n_groups = len(groups)

wt_count = (data["Group"] == "Cln6_WT").sum()
mutant_count = (data["Group"] == "Cln6_Mutant").sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Samples analyzed", n_samples)
col2.metric("Experimental groups", n_groups)
col3.metric("Cln6 WT", wt_count)
col4.metric("Cln6 Mutant", mutant_count)

st.markdown("""
**Dataset:** GSE24368  
**Organism:** *Mus musculus*  
**Platform:** Affymetrix Mouse Genome 430 2.0 Array  
**CLN6 probe:** 1454837_at
""")
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
# CLN6 Expression
# --------------------------------------------------

st.subheader("🧬 CLN6 Expression")

st.markdown("""
Explore the measured Cln6 expression values for the analyzed samples.
The values are shown individually to make the variation between
biological replicates visible.
""")

# Group selection
group_option = st.radio(
    "Select samples to display:",
    ["All samples", "WT", "Mutant"],
    horizontal=True
)

# Prepare display data
expression_data = data.copy()

expression_data["Display Group"] = expression_data["Group"].replace({
    "Cln6_WT": "WT",
    "Cln6_Mutant": "Mutant"
})

# Apply selection
if group_option == "WT":
    expression_data = expression_data[
        expression_data["Display Group"] == "WT"
    ]

elif group_option == "Mutant":
    expression_data = expression_data[
        expression_data["Display Group"] == "Mutant"
    ]

# Expression plot
st.scatter_chart(
    expression_data,
    x="Display Group",
    y="Expression"
)

# Show selected values
st.markdown("### Expression Values")

st.dataframe(
    expression_data[
        ["Sample", "Display Group", "Expression"]
    ],
    use_container_width=True,
    hide_index=True
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
# Statistical Analysis
# --------------------------------------------------

st.subheader("📊 Statistical Analysis")

st.markdown("""
The following statistics summarize the difference in Cln6 expression
between the wild-type and mutant groups.
""")

# --------------------------------------------------
# Calculate descriptive statistics
# --------------------------------------------------

wt_mean = wt_data.mean()
mutant_mean = mutant_data.mean()

# Difference between group means on the log2 expression scale
log2_fold_change = mutant_mean - wt_mean

# Convert log2 fold change to fold change on the original scale
fold_change = 2 ** log2_fold_change

# --------------------------------------------------
# Statistical results
# --------------------------------------------------

# Results from the exploratory Welch's t-test
p_value = 0.02677610935766152

# Cohen's d from the accompanying analysis
cohens_d = 3.042470743854891

# --------------------------------------------------
# Display key statistics
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "WT Mean",
    f"{wt_mean:.2f}"
)

col2.metric(
    "Mutant Mean",
    f"{mutant_mean:.2f}"
)

col3.metric(
    "Mean Difference",
    f"{log2_fold_change:.2f}"
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Log2 Fold Change",
    f"{log2_fold_change:.2f}"
)

col2.metric(
    "Fold Change",
    f"{fold_change:.2f}"
)

col3.metric(
    "Welch's p-value",
    f"{p_value:.4f}"
)

st.metric(
    "Cohen's d",
    f"{cohens_d:.2f}"
)

# --------------------------------------------------
# Detailed statistical results
# --------------------------------------------------

stats_table = pd.DataFrame({
    "Measure": [
        "WT mean",
        "Mutant mean",
        "Mean difference (Mutant - WT)",
        "Log2 fold change",
        "Fold change (Mutant / WT)",
        "Welch's t-test p-value",
        "Cohen's d"
    ],
    "Value": [
        wt_mean,
        mutant_mean,
        log2_fold_change,
        log2_fold_change,
        fold_change,
        p_value,
        cohens_d
    ]
})

st.markdown("### Detailed Results")

st.dataframe(
    stats_table,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# Interpretation
# --------------------------------------------------

st.info("""
**Interpretation:** The mutant group shows lower mean Cln6 expression
than the wild-type group. The difference between the group means was
approximately -2.32 on the log2 expression scale, corresponding to a
mutant-to-wild-type fold change of approximately 0.20 on the original
expression scale.

Welch's t-test produced a p-value of approximately 0.0268. Because only
three biological replicates were available in each group, this result
should be interpreted as an exploratory finding rather than definitive
evidence of a biological effect.
""")

# --------------------------------------------------

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
# Biological Interpretation
# --------------------------------------------------

st.subheader("🧠 Biological Interpretation")

st.markdown("""
The analysis showed lower Cln6 expression in the mutant group compared
with the wild-type group.

The mean expression was approximately 7.45 in the wild-type samples
and 5.13 in the mutant samples. The difference was about -2.32 on the
log2 expression scale, corresponding to a mutant-to-wild-type fold
change of approximately 0.20.

This means that the mutant samples showed substantially lower measured
Cln6 expression than the wild-type samples in this dataset.

This observation is consistent with the biological context of the
experiment, which included Cln6 mutant cerebellar cells. However, the
analysis is based on only three biological replicates per group, so the
result should be viewed as an exploratory observation rather than
definitive evidence of a biological effect.

Importantly, this analysis shows an association between the Cln6 mutant
condition and lower Cln6 expression. It does not establish that the
mutation directly caused the observed expression change.
""")

st.info("""
**In simple terms:** Cln6 expression was lower in the mutant samples
than in the wild-type samples. The result is interesting and consistent
with the experimental context, but additional data and experimental
validation would be needed to determine how this change relates to
CLN6 disease mechanisms.
""")
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
