#!/usr/bin/python
# python step2.py GAIM_15
# python step2.py GAIM_01
# python step2.py test_28
from __future__ import print_function
import sys, os, shutil, glob
import zipfile
import os
import glob

# install biopython
runstr='pip install biopython '

print('Installing biopython: {0} \n'.format(runstr))
os.system(runstr)
from Bio import SeqIO

exfile = 'fastqjoin.join.fna'

the_analysis_name=sys.argv[1]

# /home/smccalla/working_docker_directory/GAIM_15/data
datadir = os.path.abspath(os.path.join(the_analysis_name,'data'))

# /home/smccalla/working_docker_directory/GAIM_15/data/fasta_files
fastafilesdir = os.path.join(datadir, 'fasta_files')

# /home/smccalla/working_docker_directory/GAIM_15/data/join_paired_ends
jpe_dir = os.path.join(datadir, 'join_paired_ends')

# /home/smccalla/working_docker_directory/GAIM_15/data/fasta_files/fastqjoin.join.fna
fppath =  os.path.join(fastafilesdir, 'fastqjoin.join.fna')

# /home/smccalla/loon_qiime_mapping_file_trainer_file_3_corrected.txt
mappingpath = os.path.join('/','home','smccalla','loon_qiime_mapping_file_trainer_file_3_corrected.txt')

# /home/smccalla/working_docker_directory/GAIM_15/data/fasta_files/fastqjoin.join.fna.formatted/
formattednamesdir = os.path.join(fastafilesdir, 'fastqjoin.join.fna.formatted')

# /home/smccalla/working_docker_directory/GAIM_15/data/fasta_files/fastqjoin.join.fna.formatted/combined_seqs.fna
# Qiime name-formatted fasta file. Use this file for all subsequent analyses
combinedseqspath = os.path.join(fastafilesdir, 'fastqjoin.join.fna.formatted', 'combined_seqs.fna')

# /home/smccalla/working_docker_directory/GAIM_05/data/fasta_files/fastqjoin.join.fna.formatted/saved_files
savedfilesdir = os.path.join(fastafilesdir, 'fastqjoin.join.fna.formatted', 'saved_files')

# /home/smccalla/working_docker_directory/GAIM_05/data/fasta_files/fastqjoin.join.fna.formatted/otu_picking_output
otupickdir = os.path.join(fastafilesdir, 'fastqjoin.join.fna.formatted', 'otu_picking_output')

currdir = os.path.abspath(os.getcwd())

# Convert fasta to fastq:
# make a directory for the output

if os.path.exists(fastafilesdir):
    shutil.rmtree(fastafilesdir)
os.mkdir(fastafilesdir)

# convert fastq to fasta
runstr = 'convert_fastaqual_fastq.py -f ' \
         '{0} -c fastq_to_fastaqual' \
         ' -o {1}'.format(os.path.join(jpe_dir,'fastqjoin.join.fastq'),
                                        fastafilesdir)
print ('fasta to fastq conversion:\n{0}'.format(runstr))

#convert_fastaqual_fastq.py -f fastqjoin.join.fastq -c fastq_to_fastaqual -o /home/smccalla/htcondor/GAIM_15/data/fasta_files

os.system(runstr)
print ('Finished converting fastq to fasta --- Huzzah!')

#SED out the 'N'
runstr = "sed -i 's/N//g' {0}/fastqjoin.join.fna".format(
                os.path.join(fastafilesdir))
os.system(runstr)

#SED out the ':'
runstr = "sed -i 's/://g'  {0}/fastqjoin.join.fna".format(
                os.path.join(fastafilesdir))
os.system(runstr)

#SED out the sequencing string
runstr = "sed -i 's/NB5011442HMFMNBGXX//g'  {0}/fastqjoin.join.fna".format(
                os.path.join(fastafilesdir))
os.system(runstr)

#####Change the location of the files

#Add Qiime labels to the sequences names
#add_qiime_labels.py -i {0} -m loon_qiime_mapping_file_trainer_file_3_corrected.txt -c InputFileName -n 1 -o combined_fasta
runstr = 'add_qiime_labels.py -i {1} ' \
                '-m {3} ' \
                '-c InputFileName ' \
                '-n 1 ' \
                '-o {2}.formatted'.format(
                os.path.join(the_analysis_name), 
                os.path.join(fastafilesdir),
                os.path.join(fppath),
                os.path.join(mappingpath))
os.system(runstr)

runstr = 'pwd'
os.system(runstr)

#SED out the sequencing string
runstr = "sed -i 's/ .*//' {0}".format(
                os.path.join(combinedseqspath))
os.system(runstr)

# cp /home/smccalla/working_docker_directory/ncbi_taxonomy_expanded.tsv .
for file in glob.glob(os.path.join('/','home','smccalla','ncbi_taxonomy_expanded.tsv')):
    print ('copying from {0} to {1}'.format(file,os.path.join(formattednamesdir,os.path.basename(file))))
    shutil.copyfile(file,os.path.join(formattednamesdir,os.path.basename(file)))

# /home/smccalla/
homedir = os.path.abspath(os.path.join('/','home','smccalla'))
# cp /home/smccalla/working_docker_directory/usage/Assign-Taxonomy-with-BLAST-master/Assign-Taxonomy-with-BLAST-master/taxonomy_assignment_BLAST_V1.1.py .
for file in glob.glob(os.path.join('/','home','smccalla','taxonomy_assignment_BLAST_V1.1.py')):
    print ('copying from {0} to {1}'.format(file,os.path.join(formattednamesdir,os.path.basename(file))))
    shutil.copyfile(file,os.path.join(formattednamesdir,os.path.basename(file)))

os.chdir(formattednamesdir)
print ('navigating into: {0}'.format(formattednamesdir))

# Assign taxonomy #1
# https://github.com/Joseph7e/Assign-Taxonomy-with-BLAST
# nohup python taxonomy_assignment_BLAST.py combined_seqs.fna NONE NONE
runstr = 'python taxonomy_assignment_BLAST_V1.1.py ' \
         '{0} NONE NONE'.format(os.path.join(formattednamesdir,'combined_seqs.fna'))
print ('taxonomy_assignment_BLAST.py going on:\n{0}'.format(runstr))
os.system(runstr)

# copy the otu_seqs.fasta and otus.txt to a saved_files directory
# make a directory for the output
if os.path.exists(savedfilesdir):
    shutil.rmtree(savedfilesdir)
os.mkdir(savedfilesdir)

# cp otu_seqs.fasta to savedfilesdir
for file in glob.glob(os.path.join(formattednamesdir,'Assigned_Taxonomy','otu_seqs.fasta')):
    print ('copying from {0} to {1}'.format(file,os.path.join(formattednamesdir,os.path.basename(file))))
    shutil.copyfile(file,os.path.join(savedfilesdir,os.path.basename(file)))

# cp otus.txt to otupickdir
for file in glob.glob(os.path.join(formattednamesdir,otupickdir,'combined_seqs_otus.txt')):
    print ('copying otus.txt #1 from {0} to {1} \n \n \n'.format(file,os.path.join(formattednamesdir,os.path.basename(file))))
    shutil.copyfile(file,os.path.join(savedfilesdir,os.path.basename(file)))

currdir = os.path.abspath(os.getcwd())

newotupath = os.path.join(savedfilesdir, 'otu_seqs.fasta')

#Split the data into many files
def batch_iterator(iterator, batch_size):
    """Returns lists of length batch_size.

    This can be used on any iterator, for example to batch up
    SeqRecord objects from Bio.SeqIO.parse(...), or to batch
    Alignment objects from Bio.AlignIO.parse(...), or simply
    lines from a file handle.

    This is a generator function, and it returns lists of the
    entries from the supplied iterator.  Each list will have
    batch_size entries, although the final list may be shorter.
    """
    entry = True  # Make sure we loop once
    while entry:
        batch = []
        while len(batch) < batch_size:
            try:
                entry = iterator.next()
            except StopIteration:
                entry = None
            if entry is None:
                # End of file
                break
            batch.append(entry)
        if batch:
            yield batch
			
record_iter = SeqIO.parse(open(newotupath),"fasta")
for i, batch in enumerate(batch_iterator(record_iter, 3000)):
    filename = "group_%i.fasta" % (i)
    handle = open(filename, "w")
    count = SeqIO.write(batch, handle, "fasta")
    handle.close()
    print("Wrote %i records to %s" % (count, filename))

print ('returning to the main directory: {0}'.format(currdir))
os.chdir(currdir)

print ('Finished splittng the fasta data into many files.\n\nfin')

# Change file permissions
runstr='chmod -R 777 {0}'.format(
    os.path.join(datadir))

print('Changing permissions: \n'.format(runstr))
os.system(runstr)

#with zipfile.ZipFile('{0}_step2_results.zip'.format(the_analysis_name), 'w') as zf:
#    with open(exfile, 'wb') as ofp:
#        ofp.write(zf.read(exfile))
        
#with zipfile.ZipFile('{0}_step2_results.zip'.format(the_analysis_name), 'w', zipfile.ZIP_DEFLATED) as ifp:
#    for coutdir in [fastafilesdir,fasta_many_dir]:
#        for cf in os.listdir(coutdir):
#            ifp.write(os.path.join(coutdir,cf),cf)
