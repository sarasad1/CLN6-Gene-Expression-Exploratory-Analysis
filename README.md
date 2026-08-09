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
- 

## Data Inspection and Quality Checks

The expression dataset contained 45,101 probe sets and 12 samples.

Initial quality checks showed:

- Rows: 45,101
- Columns: 13
- Missing expression values: 0
- Duplicate probe IDs: 0
- Unique probe IDs: 45,101

The expression values were numeric, while probe identifiers were stored as text.

The GPL1261 annotation file contained 45,101 probe annotations and was used to map probe IDs to gene symbols and Entrez Gene IDs.

## Cln6 Probe Identification

The GPL1261 annotation was used to identify the probe corresponding
to the Cln6 gene.

Only one probe was mapped to Cln6:

| Probe ID | Gene Symbol | Entrez Gene ID |
|---|---|---:|
| 1454837_at | Cln6 | 76524 |

This probe was therefore used for the subsequent Cln6 expression analysis.

## Cln6 Expression Analysis

The expression values for the Cln6 probe (1454837_at) were extracted
for the six Cln6-related samples in GSE24368.

| Group | n | Mean | SD |
|---|---:|---:|---:|
| Cln6 WT | 3 | 7.45 | 0.59 |
| Cln6 Mutant | 3 | 5.13 | 0.90 |

The mean expression was lower in the Cln6 mutant group compared with
the wild-type group.

### Exploratory Visualization

The expression values were visualized by group to examine the
distribution and magnitude of the difference between wild-type and
mutant samples.

The visualization showed consistently lower Cln6 expression values
in the mutant samples compared with the wild-type samples.

## Statistical Analysis

Because the two groups contained only three biological replicates
each, Welch's t-test was used as an exploratory comparison without
assuming equal variances between the groups.

The results were:

- Welch's t-statistic: 3.73
- p-value: 0.0268

The p-value provides nominal statistical evidence of a difference
between the two groups. However, the small sample size limits the
strength and generalizability of this finding.

### Effect Size and Fold Change

The mean difference between mutant and wild-type expression was:

−2.32 log2 expression units

The estimated fold change was:

Mutant / WT = 0.20

This indicates that the measured Cln6 expression in the mutant group
was approximately 20% of the wild-type mean on the corresponding
expression scale.

## Biological Interpretation

The exploratory analysis showed substantially lower Cln6 expression
in the mutant group compared with wild-type cells.

The observed difference is biologically consistent with the
experimental design of GSE24368, which includes CbCln6 mutant cells
used to investigate molecular responses associated with CLN6-related
neuronal ceroid lipofuscinosis.

The original study also investigated Cln6 expression experimentally
and reported reduced Cln6 mRNA in the mutant cells using qRT-PCR.
However, the original Affymetrix analysis did not identify Cln6 as
significantly altered according to the study's genome-wide analysis
criteria.

Therefore, the present result should be interpreted as an exploratory
observation rather than independent evidence of a causal effect of
the mutation on Cln6 expression.

## Limitations

Several limitations should be considered when interpreting this
analysis:

- The analysis included only three biological replicates per group,
  resulting in limited statistical power.
- The analysis focused on a single gene rather than genome-wide
  differential expression.
- The expression data were generated using an Affymetrix microarray
  platform and processed using gcRMA.
- The analysis used a single Cln6 probe and therefore does not assess
  all possible transcript-level changes.
- The observed association between genotype and Cln6 expression does
  not establish causality.
- Additional experimental validation would be required to confirm
  the observed expression difference.

## Conclusion

This exploratory analysis identified lower Cln6 expression in
CbCln6 mutant mouse cerebellar cells compared with wild-type cells.

The mutant group showed a lower mean expression level, with a
mutant-to-wild-type fold change of approximately 0.20. Welch's
t-test provided nominal statistical evidence for a difference
between the groups.

However, the small sample size and the exploratory nature of the
analysis limit the strength of the conclusion.

Overall, this project demonstrates a reproducible workflow for
exploring a publicly available gene-expression dataset, from probe
annotation and gene-level extraction to statistical comparison and
biological interpretation.

## References

1. NCBI Gene Expression Omnibus (GEO). GSE24368.
   https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE24368

2. NCBI Gene Expression Omnibus (GEO). GPL1261.
   https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GPL1261

3. Original study associated with GSE24368.
   PubMed: https://pubmed.ncbi.nlm.nih.gov/21359198/

