#!/usr/bin/python
#python step4_docker3.py GAIM_12
#Assuming all the raw data is in the front folder
from __future__ import print_function
import sys, os, shutil, glob, zipfile
from subprocess import call

# read in command line variables
the_analysis_name = sys.argv[1]

condor_results_dir = os.path.abspath(os.path.join(the_analysis_name, 'results'))

datadir = os.path.abspath(os.path.join(the_analysis_name,'data'))
fastafilesdir = os.path.join(datadir, 'fasta_files')
fppath =  os.path.join(fastafilesdir, 'combined_seqs.fna')

#Concatenate the BLAST output
runstr='cat {0}/group*.out > {0}/{1}.blastout'.format(os.path.join(condor_results_dir), the_analysis_name)
print('Concatenating the BLAST results into one ginormous file: \n'.format(runstr))
os.system(runstr)

#Format the data with BROCC so it can be used in Qiime
#PYTHONHOME=/usr/
#brocc.py -i /home/smccalla/working_docker_directory/GAIM_12/data/fasta_files/combined_seqs.fna -b /home/smccalla/working_docker_directory/GAIM_12/results/GAIM_12.blastout -o /home/smccalla/htcondor/GAIM_12/data/GAIM_12_BROCC_blast_summary/ --min_species_id 90 --min_genus_id 85

runstr='brocc.py -i {0} ' \
                '-b {1}/{2}.blastout ' \
                '-o {1}/{2}_BROCC_summary ' \
                '--min_species_id 100 ' \
                '--min_genus_id 99'.format(os.path.join(fppath),os.path.join(condor_results_dir), 
                os.path.join(the_analysis_name))
print('Running brocc.py: \n{0}'.format(runstr))
os.system(runstr)
