#!/bin/bash
#
#
#sed -i 's/\r//' step1_GAIM01_14jul2016.sh
#chmod -R 777 .
#cd /home/smccalla/htcondor/$(the_analysis_name)/condor_out/results/
#sed 's/:/_/g' -i /home/smccalla/htcondor/$(the_analysis_name)/data/fasta_files/group_*.out
#cat group*.out > $(the_analysis_name).blastout
#cd ..
#mkdir blast_summary && cp -r /home/smccalla/htcondor/$(the_analysis_name)/data/fasta_files/$(the_analysis_name).blastout .

#while read -r f; do mv "$f" "${f//:/_}"; done <files.txt

#rename 's/:/_/g' *

#Run outside of condor:
cd /home/smccalla/htcondor/GAIM_12/condor_out/results/
sed 's/:/_/g' -i /home/smccalla/htcondor/GAIM_12/data/fasta_files/group_*.out
cat group*.out > GAIM_12.blastout
cd ..
mkdir blast_summary && cp -r /home/smccalla/htcondor/GAIM_12/data/fasta_files/GAIM_12.blastout .