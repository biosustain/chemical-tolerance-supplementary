# Gene-set Enrichment Analysis

Gene-set Enrichment analysis was done using the GSEA software (http://software.broadinstitute.org/gsea/index.jsp).
The subdirectory GSEA contains the input files and results of these analyses.

For each toxic chemical (coumaric acid, hexanoic acid, HMDA, isobutyric acid, octanoic acid and putrescine), 4 samples were subjected to RNA-Seq (in triplicates, 12 samples in total):
 - MG1655 in M9
 - MG1655 in M9 + chemical
 - Evolved strain in M9
 - Evolved strain in M9 + chemical
 
For each chemical four contrasts between conditions were tested using GSEA:
 - Evolved in M9+chemical vs. evolved in M9
 - MG1655 in M9+chemical vs. MG1655 in M9
 - Evolved in M9 vs. MG1655 in M9
 - Evolved in M9+chemical vs. MG1655 in M9+chemical
 
 The GSEA analyses were run with 1000 permutations, without collapsing gene sets, and with a lower limit on gene set size of 2.
