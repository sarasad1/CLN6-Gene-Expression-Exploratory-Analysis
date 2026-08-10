# CLN6 Gene Expression: Exploratory Analysis

An exploratory analysis of **Cln6 gene expression** in wild-type and mutant mouse cerebellar cells using publicly available microarray data from the NCBI Gene Expression Omnibus (GEO).

## Project Overview

This project started with a simple question: does Cln6 expression differ between wild-type and Cln6 mutant mouse cerebellar cells?

To explore this question, I re-analyzed part of the public dataset GSE24368. The analysis focused on the six samples related to Cln6 and followed the data from the original microarray measurements to gene-level expression analysis.

The workflow includes data inspection, probe annotation, Cln6 expression extraction, descriptive statistics, statistical testing, visualization, and biological interpretation.

The analysis was performed in Python using Google Colab, and the final results were presented in an interactive Streamlit dashboard.

## Research Question

**Does Cln6 expression differ between wild-type and Cln6 mutant mouse cerebellar cells in the GSE24368 dataset?**

## Dataset

- **GEO accession:** GSE24368
- **Organism:** *Mus musculus*
- **Platform:** GPL1261 — Affymetrix Mouse Genome 430 2.0 Array
- **Experiment type:** Expression profiling by array
- **Total samples:** 12
- **Samples used for this analysis:** 6

The six samples used in this project were the Cln6 wild-type and Cln6 mutant samples:

- 3 Cln6 wild-type samples
- 3 Cln6 mutant samples

The remaining six samples belong to the Cln3 comparison and were not included in the Cln6 analysis.

### Data Sources

- [GSE24368 — NCBI GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE24368)
- [GPL1261 — NCBI GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GPL1261)

## Analysis Workflow

The analysis was carried out in several steps:

1. **Data inspection**
   - Checked the dataset dimensions, column names, data types, missing values, and duplicate probe IDs.

2. **Platform annotation**
   - Used the GPL1261 annotation file to connect Affymetrix probe IDs with gene information.

3. **Probe identification**
   - Searched the annotation for the Cln6 gene and identified the corresponding probe.

4. **Expression extraction**
   - Extracted the Cln6 expression values from the six Cln6-related samples.

5. **Exploratory analysis**
   - Compared expression values between the wild-type and mutant groups using group means, standard deviations, and individual sample values.

6. **Statistical analysis**
   - Used Welch's t-test as an exploratory comparison between the two groups.
   - Calculated fold change and Cohen's d to describe the observed difference.

7. **Biological interpretation**
   - Compared the result with findings reported in the original study.

8. **Dashboard**
   - Built an interactive Streamlit dashboard to present the main results and expression data.

## Data Inspection and Quality Checks

The original expression dataset contained:

- **45,101 probe sets**
- **12 samples**
- **0 missing expression values**
- **0 duplicate probe IDs**
- **45,101 unique probe IDs**

The expression values were stored as numeric values, while probe IDs were stored as text.

The GPL1261 annotation was then used to connect the probe IDs with gene information.

## Cln6 Probe Identification

The GPL1261 annotation was searched to identify the probe corresponding to the mouse **Cln6** gene.

The analysis identified one probe:

| Probe ID | Gene Symbol | Entrez Gene ID |
|---|---|---:|
| 1454837_at | Cln6 | 76524 |

This probe was used for the Cln6 expression analysis.

## Cln6 Expression Analysis

The expression values for probe `1454837_at` were extracted from the six Cln6-related samples.

| Group | n | Mean | SD |
|---|---:|---:|---:|
| Cln6 WT | 3 | 7.45 | 0.59 |
| Cln6 Mutant | 3 | 5.13 | 0.90 |

The mutant group had a lower mean expression value than the wild-type group.

### Individual Expression Values

| Sample | Group | Expression |
|---|---|---:|
| GSM600922 | Cln6 WT | 6.7894 |
| GSM600923 | Cln6 WT | 7.6558 |
| GSM600924 | Cln6 WT | 7.9045 |
| GSM600925 | Cln6 Mutant | 6.1341 |
| GSM600926 | Cln6 Mutant | 4.3760 |
| GSM600927 | Cln6 Mutant | 4.8862 |

## Visualization

The individual Cln6 expression values were plotted by group so that the six biological replicates could be viewed directly.

The plot shows lower expression values in the mutant samples compared with the wild-type samples.

The purpose of the visualization was mainly to show the individual observations rather than only comparing the two group means.

## Statistical Analysis

There were only three biological replicates in each group, so the statistical analysis was treated as exploratory.

Welch's t-test was used because it does not require the two groups to have equal variances.

The test gave:

- **Welch's t-statistic:** 3.73
- **p-value:** 0.0268

This p-value suggests a difference between the two groups under the test used. However, the sample size is very small, so the result should be treated as exploratory rather than as definitive evidence of differential expression.

### Effect Size and Fold Change

The difference between the group means was:

**Mutant − WT = −2.32 log2 expression units**

Because the expression values are on a log2 scale, the mutant-to-wild-type fold change was calculated by back-transforming the difference between the group means.

**Mutant / WT fold change ≈ 0.20**

This means that the mutant group had approximately 20% of the wild-type mean on the back-transformed linear scale.

The calculated Cohen's d was:

**Cohen's d = 3.04**

This indicates a large standardized difference in this small sample, but the effect size should also be interpreted cautiously because there were only three replicates per group.

## Biological Interpretation

The analysis showed lower measured Cln6 expression in the mutant group compared with the wild-type group.

This direction is consistent with the original study, which later reported reduced Cln6 mRNA in the CbCln6 mutant cells using qRT-PCR.

At the same time, the original Affymetrix analysis did not identify Cln6 as significantly altered according to its genome-wide analysis criteria. The authors subsequently used qRT-PCR and reported reduced Cln6 mRNA in the mutant cells.

This difference between the microarray analysis and the qRT-PCR result is an important part of the interpretation of this project.

The result presented here should therefore be considered an exploratory re-analysis of the available microarray measurements, not independent experimental validation.

The analysis shows an association between the Cln6 mutant group and lower measured Cln6 expression, but it does not establish that the mutation directly caused the observed change.

## Limitations

There are several limitations to this analysis:

- Only three biological replicates were available for each group.
- The analysis focuses on one gene rather than performing genome-wide differential expression analysis.
- Only one Cln6 probe was identified and used.
- The data were generated using an Affymetrix microarray platform.
- The small sample size limits statistical power and generalizability.
- The p-value is based on an exploratory single-gene comparison and should not be interpreted as definitive evidence.
- The analysis shows an association and cannot establish causality.
- Additional experimental validation would be needed to confirm the biological significance of the observed difference.

## Conclusion

In this exploratory analysis, Cln6 expression was lower in the CbCln6 mutant samples than in the wild-type samples.

The mutant-to-wild-type fold change was approximately **0.20**, and Welch's t-test gave a p-value of **0.0268**.

The result is consistent with the direction of the reduced Cln6 mRNA reported by the original study using qRT-PCR, but the small number of samples and the differences between microarray and qRT-PCR measurements limit the conclusions that can be drawn.

Overall, this project provided a practical workflow for working with public gene expression data, starting with data inspection and probe annotation and ending with statistical analysis, biological interpretation, and an interactive dashboard.

## Reproducibility

The analysis was performed using:

- Python
- Google Colab
- pandas
- NumPy
- SciPy
- matplotlib / seaborn
- NCBI GEO data
- GPL1261 annotation

The Google Colab notebook contains the analysis steps, while the Streamlit application presents the main results interactively.

## Interactive Dashboard

An interactive Streamlit dashboard was created to explore the Cln6 expression data and summarize the main findings.

**Dashboard:** Add Streamlit URL here


## Tools

Python — data analysis
Google Colab — analysis environment
pandas — data manipulation
NumPy — numerical calculations
SciPy — statistical testing
matplotlib / seaborn — visualization
Streamlit — interactive dashboard
GitHub — project documentation and version control
NCBI GEO — public gene expression data

## References

NCBI Gene Expression Omnibus (GEO). GSE24368.
https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE24368
NCBI Gene Expression Omnibus (GEO). GPL1261 — Affymetrix Mouse Genome 430 2.0 Array.
https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GPL1261
Original study associated with GSE24368.
PubMed: https://pubmed.ncbi.nlm.nih.gov/21359198/
Original study full text.
https://pmc.ncbi.nlm.nih.gov/articles/PMC3040763/

