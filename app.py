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


# Convert expression values to numeric
data["Expression"] = pd.to_numeric(
    data["Expression"],
    errors="coerce"
)

# Check for missing values
if data["Expression"].isna().any():
    st.error(
        "Some expression values are missing or are not numeric."
    )
    st.stop()


# ============================================================
# Prepare Cln6 Groups
# ============================================================

wt_data = data.loc[
    data["Group"] == "Cln6_WT",
    "Expression"
].astype(float)

mutant_data = data.loc[
    data["Group"] == "Cln6_Mutant",
    "Expression"
].astype(float)


# Check that both groups are available
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

# Expression values are on a log2 scale.
# Therefore, the difference between group means
# represents the log2 fold change.

log2_fold_change = mutant_mean - wt_mean

# Back-transform the log2 fold change
# to obtain the mutant-to-WT fold change.

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
        +
        (len(mutant_data) - 1) * mutant_data.var(ddof=1)
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

The analysis focuses on one research question:

> **Does Cln6 expression differ between wild-type and Cln6 mutant cells?**

The workflow includes dataset inspection, CLN6 probe-based expression
analysis, statistical comparison, and biological interpretation.

The results are presented through an interactive Streamlit dashboard
as an exploratory re-analysis of publicly available data.
"""
)


# ============================================================
# Sidebar
# ============================================================

st.sidebar.header("🔎 Explore the Data")

group_option = st.sidebar.selectbox(
    "Select group",
    ["All", "WT", "Mutant"]
)


# ============================================================
# Filter Data
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
    "Samples in dataset",
    n_samples
)

col2.metric(
    "Groups in dataset",
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


# ============================================================
# CLN6 Expression
# ============================================================

st.subheader("🧬 CLN6 Expression")

st.markdown(
    """
The plot below shows the individual Cln6 expression values for
the selected samples. Displaying individual observations makes
the variation between biological replicates visible.
"""
)

expression_data = filtered_data.copy()

expression_data["Display Group"] = (
    expression_data["Group"].replace(
        {
            "Cln6_WT": "WT",
            "Cln6_Mutant": "Mutant"
        }
    )
)


# ============================================================
# Expression Plot
# ============================================================

st.scatter_chart(
    expression_data,
    x="Display Group",
    y="Expression"
)


# ============================================================
# Expression Values
# ============================================================

st.markdown("### Expression Values")

st.dataframe(
    expression_data[
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

Therefore:

- The difference between the group means represents the
  **log2 fold change**.
- The log2 fold change is back-transformed to obtain the
  **mutant-to-WT fold change**.
- Welch's t-test compares the two groups without assuming
  equal variances.
- Cohen's d describes the standardized magnitude of the
  observed difference.
"""
)


# ============================================================
# Main Statistics
# ============================================================

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
    "Log2 Fold Change",
    f"{log2_fold_change:.2f}"
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Fold Change",
    f"{fold_change:.2f}"
)

col2.metric(
    "Welch's p-value",
    f"{p_value:.4f}"
)

col3.metric(
    "Cohen's d",
    f"{cohens_d:.2f}"
)


# ============================================================
# Detailed Statistical Results
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

st.markdown("### Detailed Results")

st.dataframe(
    stats_table,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# Statistical Interpretation
# ============================================================

st.info(
    """
**Interpretation:** The mutant group shows lower mean Cln6
expression than the wild-type group.

The log2 fold change is approximately **-2.32**, corresponding
to a mutant-to-WT fold change of approximately **0.20** after
back-transformation.

Welch's t-test gives a p-value of approximately **0.0268**.

Because only three biological replicates were available in each
Cln6 group, this result should be interpreted as an **exploratory
finding** rather than definitive evidence of a biological effect.
"""
)


# ============================================================
# Biological Interpretation
# ============================================================

st.subheader("🧠 Biological Interpretation")

st.markdown(
    """
Cln6 expression was lower in the mutant group than in the
wild-type group.

The mean expression was approximately **7.45** in the wild-type
samples and **5.13** in the mutant samples.

This corresponds to a difference of approximately **-2.32 on the
log2 expression scale** and a mutant-to-WT fold change of
approximately **0.20**.

The observation is consistent with the experimental context of the
dataset, which includes Cln6 mutant cerebellar cells.

However, this analysis identifies an **association** between the
Cln6 mutant condition and lower measured Cln6 expression. It does
not establish causality or explain the molecular mechanism responsible
for the observed difference.
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
- Additional datasets and experimental validation would be needed
  to confirm and extend these findings.
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

- **Pathway and functional analysis** to investigate cellular
  processes affected by broader gene-expression changes.

- **Integration of transcriptomic and proteomic data** to compare
  molecular changes at the RNA and protein levels.

- **Experimental validation** using appropriate CLN6 models and
  independent biological experiments.
"""
)


# ============================================================
# Relevance to CLN6 Research
# ============================================================

st.subheader("🔗 Relevance to Future CLN6 Research")

st.markdown(
    """
This exploratory analysis provides a computational starting point
for investigating the molecular consequences of CLN6 deficiency.

The same general approach can be extended from a single-gene
expression analysis toward broader transcriptomic and multi-omics
investigations.

These computational analyses can complement experimental approaches
such as CLN6-deficient cellular models, patient-derived models,
and organelle-focused studies.
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
