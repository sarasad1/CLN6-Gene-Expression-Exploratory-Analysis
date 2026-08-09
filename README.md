# CLN6 Gene Expression: Exploratory Analysis

Exploratory analysis of CLN6 gene expression in wild-type and mutant
mouse cerebellar cells using publicly available GEO data.

## Project Overview

This project explores the expression of the Cln6 gene in wild-type
and Cln6 mutant mouse cerebellar cells using publicly available
microarray data from the NCBI Gene Expression Omnibus (GEO).

The analysis follows a simple and reproducible exploratory
bioinformatics workflow, starting from data inspection and probe
annotation and progressing to gene-level expression comparison,
statistical analysis, visualization, and biological interpretation.

## Dataset

- GEO accession: GSE24368
- Organism: Mus musculus
- Platform: GPL1261 — Affymetrix Mouse Genome 430 2.0 Array
- Experiment type: Expression profiling by array
- Total samples: 12
- CLN6 comparison: 6 samples
  - 3 Cln6 wild-type
  - 3 Cln6 mutant

The dataset was generated to investigate molecular responses
associated with mutations causing neuronal ceroid lipofuscinosis.

The original study compared wild-type and mutant cerebellar cells
associated with Cln6 and Cln3 mutations.
### Data Source

The expression data and sample information were obtained from the
NCBI Gene Expression Omnibus (GEO):

- [GSE24368](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE24368)
- [GPL1261](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GPL1261)

- ## Research Question

Does Cln6 expression differ between wild-type and Cln6 mutant
mouse cerebellar cells in the GSE24368 dataset?

## Objective

The objective of this project is to explore the expression of Cln6
between wild-type and mutant cells, quantify the observed difference,
and evaluate the statistical evidence for this difference using a
simple and reproducible exploratory analysis workflow.


## Analysis Workflow

The analysis followed the following exploratory workflow:

1. Dataset inspection
   - Examined the structure, dimensions, data types, missing values, and duplicate probe IDs.

2. Platform annotation
   - Used the GPL1261 annotation file to connect Affymetrix probe IDs with gene symbols and Entrez Gene IDs.

3. Probe-to-gene mapping
   - Evaluated probe-to-gene relationships and identified the probe corresponding to Cln6.

4. CLN6 expression extraction
   - Extracted Cln6 expression values for the six Cln6-related samples:
     - 3 wild-type samples
     - 3 mutant samples

5. Exploratory comparison
   - Compared Cln6 expression between wild-type and mutant groups using descriptive statistics and visualization.

6. Statistical analysis
   - Used Welch's t-test to evaluate the difference between the two groups.
   - Calculated the fold change and Cohen's d as measures of the magnitude of the observed difference.

7. Biological interpretation
   - Interpreted the observed expression difference in the context of the original GSE24368 study.

8. Limitations
   - Considered the small sample size and other limitations when interpreting the results.
  
   -
## Tools & Technologies

- Python — primary programming language
- Google Colab — analysis environment
- pandas — data manipulation and exploration
- NumPy — numerical calculations
- SciPy — statistical testing
- matplotlib / seaborn — data visualization
- NCBI GEO — public gene-expression dataset
- GPL1261 annotation — probe and gene annotation
