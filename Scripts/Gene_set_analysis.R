library("piano")

directory <- "~/Documents/Assistant/Cross-tolerance/chemical-tolerance-supplementary/Data/RNA-Seq/"

gene_sets <- loadGSC(paste(directory, "GSEA/Combined_genesets_pathway_regulon.gmt", sep=""))

for (compound in c("COUM", "IBUA", "PUTR", "HMDA", "OCTA", "HEXA")) {
  print(compound)

  path <- paste(directory, "ANOVA_results_", compound, ".tsv", sep="")
  
  df = read.csv(path, sep="\t")
  rownames(df) <- df$GENE
  
  gsa_res_medium <- runGSA(df["MEDIUM"] * df["medium_direction"], geneSetStat = "gsea", gsc=gene_sets, gsSizeLim = c(2, Inf))
  
  gsa_res_strain <- runGSA(df["STRAIN"] * df["strain_direction"], geneSetStat = "gsea", gsc=gene_sets, gsSizeLim = c(2, Inf))
  
  gsa_res_interaction <- runGSA(df["STRAIN.MEDIUM"] * df["interaction_direction"], geneSetStat = "gsea", gsc=gene_sets, gsSizeLim = c(2, Inf))
  
  out_res <- data.frame(
    gsa_res_medium$statDistinctDir,
    gsa_res_medium$pAdjDistinctDirUp,
    gsa_res_medium$pAdjDistinctDirDn,
    gsa_res_strain$statDistinctDir,
    gsa_res_strain$pAdjDistinctDirUp,
    gsa_res_strain$pAdjDistinctDirDn,
    gsa_res_interaction$statDistinctDir,
    gsa_res_interaction$pAdjDistinctDirUp,
    gsa_res_interaction$pAdjDistinctDirDn,
    
    row.names=names(gsa_res_medium$gsc)
  )
  names(out_res) <- c("Medium_ES", "Medium_p_UP", "Medium_p_DN", "Strain_ES", "Strain_p_UP", "Strain_p_DN", "Interaction_ES", "Interaction_p_UP", "Interaction_p_DN")
  
  write.table(x = out_res, file = paste(directory, "gsa_result_", compound, ".tsv", sep=""), sep="\t")
}
