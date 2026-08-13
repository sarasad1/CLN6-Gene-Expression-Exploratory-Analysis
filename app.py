import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="CLN6 Gene Expression Explorer",
    page_icon="🧬",
    layout="wide"
)


# ============================================================
# Load Data
# ============================================================

try:
    data = pd.read_csv("CLN6_expression.csv")

except FileNotFoundError:
    st.error(
        "CLN6_expression.csv was not found. "
        "Please make sure the file is included in the project."
    )
    st.stop()


# ============================================================
# Basic Data Validation
# ============================================================

required_columns = ["Sample", "Group", "Expression"]

missing_columns = [
    column for column in required_columns
    if column not in data.columns
]

if missing_columns:
    st.error(
        f"Missing required columns: {', '.join(missing_columns)}"
    )
    st.stop()


data["Expression"] = pd.to_numeric(
    data["Expression"],
    errors="coerce"
)

if data["Expression"].isna().any():
    st.error(
        "Some expression values are missing or are not numeric."
    )
    st.stop()


# ============================================================
# Prepare CLN6 Groups
# ============================================================

wt_data = data.loc[
    data["Group"] == "Cln6_WT",
    "Expression"
].astype(float)

mutant_data = data.loc[
    data["Group"] == "Cln6_Mutant",
    "Expression"
].astype(float)

if len(wt_data) < 2 or len(mutant_data) < 2:
    st.error(
        "At least two observations are required in each "
        "Cln6 group for statistical analysis."
    )
    st.stop()


# ============================================================
# Descriptive Statistics
# ============================================================

wt_mean = wt_data.mean()
mutant_mean = mutant_data.mean()

wt_sd = wt_data.std(ddof=1)
mutant_sd = mutant_data.std(ddof=1)


# ============================================================
# Log2 Fold Change and Fold Change
# ============================================================

# Expression values are reported on a log2 scale.
# Therefore, the difference between group means represents
# the log2 fold change.

log2_fold_change = mutant_mean - wt_mean

# Back-transform the log2 fold change to obtain
# the mutant-to-WT fold change.

fold_change = 2 ** log2_fold_change


# ============================================================
# Welch's t-test
# ============================================================

t_statistic, p_value = ttest_ind(
    mutant_data,
    wt_data,
    equal_var=False
)


# ============================================================
# Cohen's d
# ============================================================

pooled_sd = np.sqrt(
    (
        (len(wt_data) - 1) * wt_data.var(ddof=1)
        + (len(mutant_data) - 1) * mutant_data.var(ddof=1)
    )
    /
    (
        len(wt_data) + len(mutant_data) - 2
    )
)

# Negative value indicates lower expression
# in the mutant group relative to WT.

cohens_d = (
    (mutant_mean - wt_mean)
    / pooled_sd
)


# ============================================================
# Title and Project Overview
# ============================================================

st.title("🧬 CLN6 Gene Expression Explorer")

st.markdown(
    """
### Project Overview

This project explores **Cln6 gene expression** in wild-type and
Cln6 mutant mouse cerebellar cells using publicly available
microarray data from the **NCBI Gene Expression Omnibus (GEO)**.

The analysis addresses one focused research question:

> **Does Cln6 expression differ between wild-type and Cln6 mutant cells?**

The workflow includes dataset inspection, CLN6 probe-based expression
analysis, statistical comparison, effect-size estimation, and
biological interpretation.

The results are presented through an interactive Streamlit dashboard
as an **exploratory re-analysis of publicly available data**.
"""
)


# ============================================================
# Sidebar
# ============================================================

st.sidebar.header("🔎 Explore the Data")

group_option = st.sidebar.selectbox(
    "Select samples to display",
    ["All", "WT", "Mutant"]
)

st.sidebar.caption(
    "The selection changes the displayed observations and table. "
    "Statistical results are calculated using all CLN6 WT and "
    "CLN6 mutant samples."
)


# ============================================================
# Filter Data for Visualization
# ============================================================

if group_option == "WT":

    filtered_data = data[
        data["Group"] == "Cln6_WT"
    ].copy()

elif group_option == "Mutant":

    filtered_data = data[
        data["Group"] == "Cln6_Mutant"
    ].copy()

else:

    filtered_data = data.copy()


filtered_data["Display Group"] = (
    filtered_data["Group"].replace(
        {
            "Cln6_WT": "WT",
            "Cln6_Mutant": "Mutant"
        }
    )
)


# ============================================================
# Dataset & Samples
# ============================================================

st.subheader("📂 Dataset & Samples")

st.markdown(
    """
The original GEO study includes wild-type and mutant cerebellar
cell groups for both Cln3 and Cln6.

For this project, the analysis focuses specifically on the
**Cln6 wild-type and Cln6 mutant groups**.
"""
)

n_samples = len(data)
n_groups = data["Group"].nunique()

wt_count = (
    data["Group"] == "Cln6_WT"
).sum()

mutant_count = (
    data["Group"] == "Cln6_Mutant"
).sum()


# ============================================================
# Dataset Metrics
# ============================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Samples",
    n_samples
)

col2.metric(
    "Groups",
    n_groups
)

col3.metric(
    "Cln6 WT",
    wt_count
)

col4.metric(
    "Cln6 Mutant",
    mutant_count
)

st.markdown(
    """
**Dataset:** GSE24368  
**Organism:** *Mus musculus*  
**Platform:** Affymetrix Mouse Genome 430 2.0 Array  
**Data type:** Microarray gene expression  
**Normalization:** gcRMA  
**CLN6 probe:** 1454837_at
"""
)


# ============================================================
# Key Results
# ============================================================

st.subheader("📌 Key Results")

st.caption(
    "Summary statistics calculated from all three biological "
    "replicates in each CLN6 group."
)

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
    "Exploratory p-value",
    f"{p_value:.4f}"
)


# ============================================================
# CLN6 Expression
# ============================================================

st.subheader("🧬 CLN6 Expression")

st.markdown(
    """
Individual observations are shown to make variation between
biological replicates visible rather than displaying only group
means.
"""
)


# ============================================================
# Expression Plot
# ============================================================

st.scatter_chart(
    filtered_data,
    x="Display Group",
    y="Expression"
)


# ============================================================
# Expression Values
# ============================================================

st.markdown("### Expression Values")

st.dataframe(
    filtered_data[
        ["Sample", "Display Group", "Expression"]
    ],
    use_container_width=True,
    hide_index=True
)


# ============================================================
# Statistical Analysis
# ============================================================

st.subheader("📊 Statistical Analysis")

st.markdown(
    """
The expression values are reported on a **log2 scale**.

The difference between the group means therefore represents the
**log2 fold change**. This value is back-transformed to obtain the
**mutant-to-WT fold change**.

A **Welch's t-test** was used to compare the two groups without
assuming equal variances. **Cohen's d** was calculated to describe
the standardized magnitude of the observed difference.
"""
)


# ============================================================
# Statistical Results
# ============================================================

stats_table = pd.DataFrame(
    {
        "Measure": [
            "WT mean",
            "Mutant mean",
            "WT standard deviation",
            "Mutant standard deviation",
            "Log2 fold change",
            "Fold change (Mutant / WT)",
            "Welch's t-statistic",
            "Welch's t-test p-value",
            "Cohen's d"
        ],
        "Value": [
            wt_mean,
            mutant_mean,
            wt_sd,
            mutant_sd,
            log2_fold_change,
            fold_change,
            t_statistic,
            p_value,
            cohens_d
        ]
    }
)

st.dataframe(
    stats_table,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# Statistical Interpretation
# ============================================================

st.info(
    f"""
**Statistical interpretation**

The mutant group shows lower mean Cln6 expression than the
wild-type group.

The difference between group means is approximately
**{log2_fold_change:.2f} on the log2 scale**, corresponding to a
mutant-to-WT fold change of approximately **{fold_change:.2f}**
after back-transformation.

Welch's t-test gives an **exploratory p-value of {p_value:.4f}**.

The estimated Cohen's d is **{cohens_d:.2f}**, indicating a large
standardized difference between the two groups.

Because only three biological replicates were available per group,
these statistical results should be interpreted as **exploratory**
rather than definitive evidence of a biological effect.
"""
)


# ============================================================
# Biological Interpretation
# ============================================================

st.subheader("🧠 Biological Interpretation")

st.markdown(
    """
The analysis shows lower measured Cln6 expression in the mutant
group compared with the wild-type group.

This observation is consistent with the experimental context of
the dataset, which contains cerebellar cells carrying the Cln6
mutant condition.

However, this analysis identifies an **association** between the
Cln6 mutant condition and lower measured Cln6 expression. It does
not establish causality or determine the molecular mechanism
responsible for the observed difference.

Therefore, the result is best considered a **computationally
observed expression difference that requires further investigation
and experimental validation**.
"""
)


# ============================================================
# Limitations
# ============================================================

st.subheader("⚠️ Limitations")

st.markdown(
    """
- Only three biological replicates were available in each Cln6 group.
- The analysis focuses on a single gene/probe rather than
  genome-wide differential expression.
- The analysis uses one CLN6 probe from an Affymetrix microarray.
- The data are derived from a processed public dataset.
- The statistical result should be considered exploratory because
  of the small sample size.
- The observed association does not establish causality.
- Additional datasets and independent experimental validation
  would be needed to confirm and extend these observations.
"""
)


# ============================================================
# Future Directions
# ============================================================

st.subheader("🚀 Future Directions")

st.markdown(
    """
This analysis provides a starting point for moving from a
single-gene observation toward a broader investigation of
CLN6 deficiency.

Possible next steps include:

- **Genome-wide transcriptomic analysis** to identify broader
  molecular changes associated with CLN6 deficiency.

- **Pathway and functional analysis** to investigate biological
  processes associated with broader gene-expression changes.

- **Integration of transcriptomic and proteomic data** to compare
  molecular changes at the RNA and protein levels.

- **Experimental validation** using appropriate CLN6 models and
  independent biological experiments.
"""
)


# ============================================================
# Relevance to Future CLN6 Research
# ============================================================

st.subheader("🔗 Relevance to Future CLN6 Research")

st.markdown(
    """
This exploratory analysis provides a computational starting point
for investigating the molecular consequences associated with CLN6
deficiency.

The same general approach can be extended from a single-gene
expression analysis toward broader transcriptomic and multi-omics
investigations.

Computational analyses of this type can complement experimental
approaches involving CLN6-deficient cellular models, patient-derived
models, and organelle-focused studies.
"""
)


# ============================================================
# What This Project Demonstrates
# ============================================================

st.subheader("🧪 What This Project Demonstrates")

st.markdown(
    """
This project demonstrates an independent workflow for working with
public biological data, from dataset exploration to statistical
analysis and scientific interpretation.

**Skills demonstrated:**

- Public dataset exploration and interpretation
- GEO-based microarray data analysis
- Probe-based gene expression analysis
- Python and Pandas
- Statistical analysis using SciPy
- Welch's t-test
- Effect-size estimation using Cohen's d
- Biological data visualization
- Scientific interpretation and limitation assessment
- Reproducible computational workflow
- Interactive dashboard development with Streamlit
"""
)


# ============================================================
# References & Reproducibility
# ============================================================

st.subheader("📚 References & Reproducibility")

st.markdown(
    """
### Data Source

**GEO accession:** GSE24368

**Platform:** Affymetrix Mouse Genome 430 2.0 Array

**Organism:** *Mus musculus*

**CLN6 probe:** 1454837_at


### Original Study

Cao et al. (2011), *Distinct Early Molecular Responses to
Mutations Causing vLINCL and JNCL Presage ATP Synthase Subunit C
Accumulation in Cerebellar Cells.*

The original study used three biological samples per genotype
for the gene-expression experiments. The microarray data were
background-corrected and normalized using gcRMA.


### Reproducibility

The analysis was performed using Python.

The workflow included:

1. Dataset inspection
2. CLN6 probe identification
3. CLN6 expression extraction
4. Descriptive statistics
5. Welch's t-test
6. Effect-size estimation
7. Biological interpretation
8. Interactive Streamlit visualization
"""
)


# ============================================================
# Footer
# ============================================================

st.divider()

st.markdown(
    """
### CLN6 Gene Expression Analysis Dashboard

**Developed by Sara Saad AlJuhani**

Bachelor of Chemistry | Bioinformatics Enthusiast

**Data Source:** NCBI Gene Expression Omnibus (GEO)

**Built using:** Python • Streamlit • Pandas • NumPy • SciPy
"""
)
