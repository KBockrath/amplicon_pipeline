#!/bin/bash
#
#
#sed -i 's/\r//' step1_GAIM01_14jul2016.sh
#chmod -R 777 .
#cd /home/smccalla/htcondor/$(the_analysis_name)/condor_out/results/
#sed 's/:/_/g' -i /home/smccalla/htcondor/$(the_analysis_name)/data/fasta_files/group_*.out
#cat group*.out > $(the_analysis_name).blastout
#cd ..
#mkdir blast_summary && chmod -R 777 . && cp -r /home/smccalla/htcondor/$(the_analysis_name)/data/fasta_files/$(the_analysis_name).blastout .


#Concatenate the BLAST output
cd /home/smccalla/htcondor/GAIM_12/condor_out/results/
sed 's/:/_/g' -i /home/smccalla/htcondor/GAIM_12/condor_out/results/group_*.out
cat group*.out > GAIM_12.blastout
cd /home/smccalla/htcondor/GAIM_12/data/
mkdir blast_summary && chmod -R 777 . && cp -r /home/smccalla/htcondor/GAIM_12/data/fasta_files/GAIM_12.blastout /home/smccalla/htcondor/GAIM_12/data/blast_summary/GAIM_12.blastout
cat /home/smccalla/htcondor/GAIM_12/data/fasta_files/group_*.fasta > /home/smccalla/htcondor/GAIM_12/data/blast_summary/GAIM_12.blastin


#Format the data so it can be used in Qiime
#PYTHONHOME=/usr/
brocc.py -i /home/smccalla/htcondor/GAIM_12/data/blast_summary/GAIM_12.blastin -b /home/smccalla/htcondor/GAIM_12/data/blast_summary/GAIM_12.blastout -o /home/smccalla/htcondor/GAIM_12/data/blast_summary/ --min_species_id 90 --min_genus_id 85


#Use Qiime
make_otu_table.py -i /home/smccalla/htcondor/GAIM_12/data/blast_summary/Standard_Taxonomy.txt -t /home/smccalla/htcondor/GAIM_12/data/blast_summary/Standard_Taxonomy.txt -o /home/smccalla/htcondor/GAIM_12/data/blast_summary/otu_table.biom
#summarize_taxa.py -i /home/smccalla/htcondor/GAIM_12/data/blast_summary/otu_table.biom -o /home/smccalla/htcondor/GAIM_12/data/blast_summary/
#make_otu_heatmap.py -i /home/smccalla/htcondor/GAIM_12/data/blast_summary/otu_table.biom -o /home/smccalla/htcondor/GAIM_12/data/blast_summary/otuheatmap.table 
#filter_taxa_from_otu_table.py -i /home/smccalla/htcondor/GAIM_12/data/blast_summary/otu_table.biom -o /home/smccalla/htcondor/GAIM_12/data/blast_summary/otutable.filtered
#summarize_taxa_through_plots.py -i /home/smccalla/htcondor/GAIM_12/data/blast_summary/otu_table.biom -o /home/smccalla/htcondor/GAIM_12/data/blast_summary/plot_summary
#compute_taxonomy_ratios.py -i /home/smccalla/htcondor/GAIM_12/data/blast_summary/otu_table.biom -o /home/smccalla/htcondor/GAIM_12/data/blast_summary/compute_taxonomy_ratios.txt --increased p__Firmicutes
#single_rarefaction.py -i /home/smccalla/htcondor/GAIM_12/data/blast_summary/otu_table.biom -o /home/smccalla/htcondor/GAIM_12/data/blast_summary/single_rarefaction.out -d 1
#summarize_taxa.py -i /home/smccalla/htcondor/GAIM_12/data/blast_summary/Standard_Taxonomy.txt -o /home/smccalla/htcondor/GAIM_12/data/blast_summary/summarize_taxa.txt




