#!/usr/bin/python
#
#
# python step4.py test_28
# python step4.py GAIM_15
# python step4.py GAIM_05
# 
from __future__ import print_function
import sys, os, shutil, glob, zipfile

# install biopython
runstr='pip install biopython '

#runnum = int(sys.argv[1])
the_analysis_name = sys.argv[1]

# /home/smccalla/working_docker_directory/GAIM_15/data
datadir = os.path.abspath(os.path.join(the_analysis_name,'data'))

# /home/smccalla/working_docker_directory/GAIM_15/data/fasta_files
fastafilesdir = os.path.join(datadir, 'fasta_files')

# /home/smccalla/working_docker_directory/GAIM_15/data/join_paired_ends
jpe_dir = os.path.join(datadir, 'join_paired_ends')

# /home/smccalla/working_docker_directory/GAIM_15/data/fasta_files/fastqjoin.join.fna
fppath =  os.path.join(fastafilesdir, 'fastqjoin.join.fna')

# /home/smccalla/qiime_mapping_file_corrected.txt
mappingpath = os.path.join('/','home','smccalla','qiime_mapping_file_corrected.txt')

# /home/smccalla/working_docker_directory/GAIM_15/data/fasta_files/fastqjoin.join.fna.formatted/
formattednamesdir = os.path.join(fastafilesdir, 'fastqjoin.join.fna.formatted')

# /home/smccalla/working_docker_directory/GAIM_15/data/fasta_files/fastqjoin.join.fna.formatted/combined_seqs.fna
# Qiime name-formatted fasta file. Use this file for all subsequent analyses
combinedseqspath = os.path.join(fastafilesdir, 'fastqjoin.join.fna.formatted', 'combined_seqs.fna')

# /home/smccalla/working_docker_directory/GAIM_05/data/fasta_files/fastqjoin.join.fna.formatted/saved_files
savedfilesdir = os.path.join(fastafilesdir, 'fastqjoin.join.fna.formatted', 'saved_files')

#currdir = os.path.abspath(os.getcwd())

newotupath = os.path.join(savedfilesdir, 'otu_seqs.fasta')

# Concatenate BLAST
runstr = 'cat {1}/group_*.out > {1}/{0}_blast.out'.format(os.path.join(the_analysis_name),
            os.path.join(formattednamesdir))
            
print ('Concatenating BLAST results:\n{0}'.format(runstr))

os.system(runstr)

print('\n')

# Assign taxonomy #2
# https://github.com/Joseph7e/Assign-Taxonomy-with-BLAST
# Run the script with the new blast file AND the otus.txt file generated in Assign taxonomy #1.
# python taxonomy_assignment_BLAST.py --blast_file test_28_blast.out --cutoff_species 99 --cutoff_family 95 --cutoff_phylum 90 --length_percentage 0.8 --length_cutoff 70 --hits_to_consider 10 --percent_sway 0.5 --blast_evalue 1e-1 --make_biom --ncbi_nt combined_seqs.fna NONE ncbi_taxonomy_expanded.tsv -v --otu_file saved_files/combined_seqs_otus.txt
# python taxonomy_assignment_BLAST.py --blast_file GAIM_15_blast.out --cutoff_species 99 --cutoff_family 90 --cutoff_phylum 85 --length_percentage 0.8 --length_cutoff 70 --hits_to_consider 10 --percent_sway 0.5 --blast_evalue 1e-1 --make_biom --ncbi_nt combined_seqs.fna NONE ncbi_taxonomy_expanded.tsv -v --otu_file saved_files/combined_seqs_otus.txt

runstr = 'python taxonomy_assignment_BLAST_V1.1.py ' \
         '--blast_file {1}/{0}_blast.out --cutoff_species 98 --cutoff_family 98 --cutoff_phylum 98 --length_percentage 0.8 ' \
         '--length_cutoff 70 --hits_to_consider 20 --percent_sway 0.50 --blast_evalue 1e-11 --make_biom --ncbi_nt {1}/combined_seqs.fna NONE {1}/ncbi_taxonomy_expanded.tsv -v ' \
         '--otu_file {1}/saved_files/combined_seqs_otus.txt --output_dir {1}/{0}_OTU/'.format(os.path.join(the_analysis_name),
         os.path.join(formattednamesdir))

print('\n')
         
print ('taxonomy_assignment_BLAST.py #2 underway:\n{0}'.format(runstr))
os.system(runstr)

print('\n')

# Change file permissions
runstr='chmod -R 777 {0}'.format(
    os.path.join(datadir))
print('Changed permissions \n'.format(runstr))
os.system(runstr)

# Start Qiime analyses
print ('Starting Qiime analyses\n')

# Parameter file background:
# https://groups.google.com/forum/#!searchin/qiime-forum/summarize_taxa_through_plots.py$20parameter$20file$20species|sort:relevance/qiime-forum/KFdHfJpywOk/Aaz6R2XdDQAJ
# https://groups.google.com/forum/#!searchin/qiime-forum/summarize_taxa_through_plots.py$20parameter$20file$20species%7Csort:relevance/qiime-forum/f6ZDmnvvQcs/Mq_DujaKbn0J
# http://fmgdata.kinja.com/using-docker-with-conda-environments-1790901398
# Copy taxa_params.txt to the formattednamesdir
# cp /home/smccalla/taxa_params.txt .
for file in glob.glob(os.path.join('/','home','smccalla','taxa_params.txt')):
    print ('copying from {0} to {1}'.format(file,os.path.join(formattednamesdir,os.path.basename(file))))
    shutil.copyfile(file,os.path.join(formattednamesdir,os.path.basename(file)))

print('\n')
    
# summarize_taxa_through_plots.py
# summarize_taxa_through_plots.py -i otu_table.biom -p /home/smccalla/taxa_params.txt -m qiime_mapping_file_corrected.txt -o GAIM_15_taxa_summary -f
# https://groups.google.com/forum/#!searchin/qiime-forum/summarize_taxa_through_plots.py$20parameter$20file$20species|sort:relevance/qiime-forum/878CfWG7v0k/30dzkpugDAAJ
runstr = 'summarize_taxa_through_plots.py -i {1}/{0}_OTU/otu_table.biom -m {2} ' \
     '-p {1}/taxa_params.txt -o {1}/{0}_taxa_summary -f -s #SampleID '.format(os.path.join(the_analysis_name),
     os.path.join(formattednamesdir),os.path.join(mappingpath))
            
print ('Summarizing the biom file in plots:\n{0}'.format(runstr))
os.system(runstr)
print('\n')

# Filter out "unknowns" taxa records:
# http://qiime.org/scripts/filter_taxa_from_otu_table.html
# filter_taxa_from_otu_table.py -i otu_table.biom -o otu_table_non_unknown.biom -n Unassigned
runstr = 'filter_taxa_from_otu_table.py -i {1}/{0}_OTU/otu_table.biom ' \
     '-o {1}/{0}_OTU/{0}_otu_table_unknown_removed.biom -n Unassigned '.format(os.path.join(the_analysis_name),
     os.path.join(formattednamesdir),os.path.join(mappingpath))
print ('Filtering out "unknowns" taxa records:\n{0}'.format(runstr))
os.system(runstr)
print('\n')

# Change file permissions
runstr='chmod -R 777 {0}'.format(
    os.path.join(datadir))
print('Changed permissions \n'.format(runstr))
os.system(runstr)  
print('\n')

# Summarize the species with the "unknowns" removed
# summarize_taxa.py -i otu_table_non_unknown.biom -L 15 -o 15
# http://qiime.org/scripts/summarize_taxa.html
runstr = 'summarize_taxa.py ' \
     '-i {1}/{0}_OTU/{0}_otu_table_unknown_removed.biom ' \
     '-L 15 -o {1}/{0}_OTU/{0}_otu_table_unknown_removed '.format(os.path.join(the_analysis_name),
     os.path.join(formattednamesdir),os.path.join(mappingpath))
     
print ('Summarizing the species with the "unknowns" removed:\n{0}'.format(runstr))
os.system(runstr)
print('\n')

# Filter out "unknowns" and loons:
# http://qiime.org/scripts/filter_taxa_from_otu_table.html
# filter_taxa_from_otu_table.py -i otu_table.biom -o otu_table_non_unknown.biom -n Unassigned
runstr = 'filter_taxa_from_otu_table.py -i {1}/{0}_OTU/{0}_otu_table_unknown_removed.biom ' \
     '-o {1}/{0}_OTU/{0}_otu_table_loons_removed.biom -n D_8__Gaviiformes '.format(os.path.join(the_analysis_name),
     os.path.join(formattednamesdir),os.path.join(mappingpath))
     
print ('Filtering out "unknowns" and loons:\n{0}'.format(runstr))
os.system(runstr)
print('\n')

# Change file permissions
runstr='chmod -R 777 {0}'.format(
    os.path.join(datadir))
print('Changed permissions \n'.format(runstr))
os.system(runstr)

# Summarizing the species with "unknowns" and loon results removed
# summarize_taxa.py -i otu_table_non_unknown.biom -L 15 -o 15
# http://qiime.org/scripts/summarize_taxa.html
runstr = 'summarize_taxa.py ' \
     '-i {1}/{0}_OTU/{0}_otu_table_loons_removed.biom ' \
     '-L 15 -o {1}/{0}_OTU/{0}_species_summary_15 '.format(os.path.join(the_analysis_name),
     os.path.join(formattednamesdir),os.path.join(mappingpath))
     
print ('Summarizing the species with loon results removed:\n{0}'.format(runstr))
os.system(runstr)
print('\n')

# Change file permissions
runstr='chmod -R 777 {0}'.format(
    os.path.join(datadir))
print('Changed permissions \n'.format(runstr))
os.system(runstr)

print('\n')
print ('This is the end.')
print('\n')