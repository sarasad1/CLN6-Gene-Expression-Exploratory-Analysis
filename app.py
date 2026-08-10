import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="CLN6 Gene Expression Explorer",
    page_icon="🧬",
    layout="wide"
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------

data = pd.read_csv("CLN6_expression.csv")

# --------------------------------------------------
# Basic Data Check
# --------------------------------------------------

required_columns = ["Sample", "Group", "Expression"]

missing_columns = [
    col for col in required_columns
    if col not in data.columns
]

if missing_columns:
    st.error(
        f"Missing required columns: {', '.join(missing_columns)}"
    )
    st.stop()

# --------------------------------------------------
# Prepare Groups
# --------------------------------------------------

wt_data = data.loc[
    data["Group"] == "Cln6_WT",
    "Expression"
].astype(float)

mutant_data = data.loc[
    data["Group"] == "Cln6_Mutant",
    "Expression"
].astype(float
)

# --------------------------------------------------
# Descriptive Statistics
# --------------------------------------------------

wt_mean = wt_data.mean()
mutant_mean = mutant_data.mean()

wt_sd = wt_data.std()
mutant_sd = mutant_data.std()

# Difference on the log2 expression scale
log2_fold_change = mutant_mean - wt_mean

# Back-transform log2 difference to fold change
fold_change = 2 ** log2_fold_change

# --------------------------------------------------
# Welch's t-test
# --------------------------------------------------

t_statistic, p_value = ttest_ind(
    wt_data,
    mutant_data,
    equal_var=False
)

# --------------------------------------------------
# Cohen's d
# --------------------------------------------------

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

cohens_d = (wt_mean - mutant_mean) / pooled_sd

# --------------------------------------------------
# Title and Project Overview
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

st.sidebar.header("🔎 Explore the Data")

group_option = st.sidebar.selectbox(
    "Select group",
    ["All", "WT", "Mutant"]
)

# --------------------------------------------------
# Filter Data
# --------------------------------------------------

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

# Number of samples
n_samples = len(data)

# Number of experimental groups
groups = data["Group"].unique()
n_groups = len(groups)

# Group counts
wt_count = (
    data["Group"] == "Cln6_WT"
).sum()

mutant_count = (
    data["Group"] == "Cln6_Mutant"
).sum()

# --------------------------------------------------
# Dataset Metrics
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Samples analyzed",
    n_samples
)

col2.metric(
    "Experimental groups",
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

st.markdown("""
**Dataset:** GSE24368  
**Organism:** *Mus musculus*  
**Platform:** Affymetrix Mouse Genome 430 2.0 Array (GPL1261)  
**CLN6 probe:** 1454837_at
""")

# --------------------------------------------------
# Key Results
# --------------------------------------------------

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

# --------------------------------------------------
# CLN6 Expression
# --------------------------------------------------

st.subheader("🧬 CLN6 Expression")

st.markdown("""
The plot below shows the individual Cln6 expression values for the
selected samples. Displaying individual biological replicates helps
make the variation within each group visible.
""")

# Prepare expression data
expression_data = filtered_data.copy()

expression_data["Display Group"] = expression_data[
    "Group"
].replace({
    "Cln6_WT": "WT",
    "Cln6_Mutant": "Mutant"
})

# --------------------------------------------------
# Expression Plot
# --------------------------------------------------

st.scatter_chart(
    expression_data,
    x="Display Group",
    y="Expression"
)

# --------------------------------------------------
# Expression Values
# --------------------------------------------------

st.markdown("### Expression Values")

st.dataframe(
    expression_data[
        ["Sample", "Display Group", "Expression"]
    ],
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# Selected Samples
# --------------------------------------------------

st.subheader("📋 Selected Samples")

st.markdown(
    f"Showing samples selected from the sidebar: **{group_option}**"
)

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

Because the expression values are on a log2 scale, the difference
between the group means represents the log2 fold change. The fold
change is then obtained by back-transforming this difference.
""")

# --------------------------------------------------
# Display Main Statistics
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
# Detailed Statistical Results
# --------------------------------------------------

stats_table = pd.DataFrame({
    "Measure": [
        "WT mean",
        "Mutant mean",
        "WT standard deviation",
        "Mutant standard deviation",
        "Mean difference (Mutant - WT)",
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
        log2_fold_change,
        fold_change,
        t_statistic,
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
# Statistical Interpretation
# --------------------------------------------------

st.info("""
**Interpretation:** The mutant group shows lower mean Cln6 expression
than the wild-type group.

The difference between the group means is approximately -2.32 on the
log2 expression scale. After back-transformation, this corresponds to
a mutant-to-wild-type fold change of approximately 0.20.

Welch's t-test gives a p-value of approximately 0.0268. Since only
three biological replicates were available in each group, this result
should be treated as an exploratory finding rather than definitive
evidence of a biological effect.
""")

# --------------------------------------------------
# Exploratory Interpretation
# --------------------------------------------------

st.subheader("🔬 Exploratory Interpretation")

st.markdown("""
Cln6 expression appears higher in the wild-type group than in the
mutant group.

The mutant samples showed lower measured Cln6 expression, with a
mutant-to-wild-type fold change of approximately 0.20 on the linear
scale.

The statistical comparison also provides nominal evidence of a
difference between the two groups. However, the small number of
biological replicates limits the strength of this conclusion.

Therefore, the result is best viewed as an exploratory observation
that may help generate questions for further investigation.
""")

# --------------------------------------------------
# Dataset Information
# --------------------------------------------------

st.subheader("📚 Dataset Information")

st.markdown("""
**Dataset:** GSE24368

**Organism:** *Mus musculus*

**Platform:** Affymetrix Mouse Genome 430 2.0 Array (GPL1261)

**Data type:** Microarray gene expression

**Preprocessing:** GC-RMA normalized log2 expression values

**CLN6 probe:** 1454837_at

**Groups analyzed:**
- 3 Cln6 WT samples
- 3 Cln6 Mutant samples
""")

# --------------------------------------------------
# Biological Interpretation
# --------------------------------------------------

st.subheader("🧠 Biological Interpretation")

st.markdown("""
The analysis showed lower Cln6 expression in the mutant group compared
with the wild-type group.

The mean expression was approximately 7.45 in the wild-type samples
and 5.13 in the mutant samples. The difference was approximately -2.32
on the log2 expression scale.

This observation is consistent with the biological context of the
experiment, which includes Cln6 mutant cerebellar cells.

However, the analysis is based on only three biological replicates per
group. The result should therefore be considered exploratory rather
than definitive evidence of a biological mechanism.

Importantly, this analysis identifies an association between the
Cln6 mutant condition and lower measured Cln6 expression. It does not
establish causality or explain the molecular mechanism responsible for
the observed difference.
""")

st.info("""
**In simple terms:** Cln6 expression was lower in the mutant samples
than in the wild-type samples. The finding is interesting and provides
a starting point for asking broader questions about what happens to
cellular pathways when CLN6 is deficient.
""")

# --------------------------------------------------
# Limitations
# --------------------------------------------------

st.subheader("⚠️ Limitations")

st.markdown("""
- Only three biological replicates were available for each group.
- The analysis focuses on a single gene rather than genome-wide
  differential expression.
- The analysis uses one CLN6 probe from an Affymetrix microarray.
- The data are derived from a processed public dataset.
- The statistical result is exploratory because of the small sample
  size.
- The observed association does not establish causality.
- Additional datasets and experimental validation would be needed
  to confirm and extend these findings.
""")

# --------------------------------------------------
# Future Directions
# --------------------------------------------------

st.subheader("🚀 Future Directions")

st.markdown("""
This project provides a small gene-level view of CLN6 expression.
A natural next step would be to move from a single-gene observation
toward a broader investigation of the molecular consequences of
CLN6 deficiency.

Possible directions include:

### 1. Genome-wide transcriptomic analysis

Instead of focusing only on CLN6, differential expression analysis
could be extended across the transcriptome to identify broader
molecular changes associated with CLN6 deficiency.

### 2. Pathway and functional analysis

Genes showing consistent changes could be investigated using
functional enrichment approaches such as Gene Ontology and pathway
analysis to identify cellular processes that may be affected.

### 3. ER and lysosomal biology

Because CLN6 is associated with the endoplasmic reticulum while
CLN6 deficiency is linked to lysosomal storage disease, future
analysis could investigate molecular changes related to ER and
lysosomal function.

### 4. Transcriptomics and proteomics integration

Combining transcriptomic and proteomic data could provide a broader
view of the molecular consequences of CLN6 deficiency and help
determine whether changes observed at the RNA level are also reflected
at the protein level.

### 5. CLN6 knockout models

Future work could compare molecular profiles from CLN6 knockout
cellular models with the observations from the public dataset used
here.

### 6. Patient-derived iPSCs

Patient-derived iPSCs carrying pathogenic CLN6 mutations could provide
a human cellular model for investigating disease-associated molecular
changes.

### 7. Pathogenic CLN6 mutations

Different pathogenic CLN6 variants could be investigated to examine
their effects on CLN6 protein function and subcellular localization,
which may help clarify genotype-phenotype relationships.

### 8. Organelle-specific studies

Future experiments could investigate ER and lysosomal compartments
more directly and examine molecular changes associated with CLN6
deficiency.

### 9. TurboID proximity labeling

TurboID-based proximity labeling could be used in future experimental
work to investigate proteins and molecular interactions associated
with CLN6 and its cellular environment.

### 10. Experimental validation

Computational findings could ultimately be followed by independent
laboratory experiments to determine whether observed molecular
changes are reproducible and biologically relevant.
""")

# --------------------------------------------------
# Project Relevance
# --------------------------------------------------

st.subheader("🔗 Relevance to Future CLN6 Research")

st.markdown("""
This exploratory analysis provides a computational starting point for
a broader investigation of CLN6 disease mechanisms.

The same general workflow can be extended from a single-gene
expression question toward transcriptomic, proteomic, and
organelle-specific analyses.

This creates a useful connection between public-data analysis and
experimental approaches such as CLN6 knockout models, patient-derived
iPSCs, multi-omics analysis, and TurboID-based proximity labeling.
""")

# --------------------------------------------------
# References & Reproducibility
# --------------------------------------------------

st.subheader("📚 References & Reproducibility")

st.markdown("""
### Data Source

The expression data used in this project were obtained from the
NCBI Gene Expression Omnibus (GEO).

- **GEO accession:** GSE24368
- **Platform:** GPL1261 — Affymetrix Mouse Genome 430 2.0 Array
- **CLN6 probe:** 1454837_at

### Original Study

The dataset is associated with the study:

*Distinct Early Molecular Responses to Mutations Causing vLINCL
and JNCL Presage ATP Synthase Subunit c Accumulation in
Cerebellar Cells.*

### Reproducibility

The analysis was performed using Python in Google Colab.

The workflow included:

1. Dataset inspection
2. Probe annotation
3. CLN6 probe identification
4. CLN6 expression extraction
5. Descriptive statistics
6. Welch's t-test
7. Effect-size estimation
8. Biological interpretation

The final results were presented through an interactive Streamlit
dashboard.
""")

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.markdown("""
**Tools used:** Python • pandas • NumPy • SciPy • Streamlit

**Data source:** NCBI Gene Expression Omnibus (GEO)

**Project:** CLN6 Gene Expression Exploratory Analysis
""")
