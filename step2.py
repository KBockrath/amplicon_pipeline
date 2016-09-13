#!/usr/bin/python
from __future__ import print_function
import sys, os, shutil, glob

the_analysis_name=sys.argv[1]
datadir = os.path.abspath(os.path.join(the_analysis_name,'data'))
jpe_dir = os.path.join(datadir, 'join_paired_ends')

#Convert fasta to fastq:
# make a directory for the output
fastafilesdir = os.path.join(datadir, 'fasta_files')
if os.path.exists(fastafilesdir):
    shutil.rmtree(fastafilesdir)
os.mkdir(fastafilesdir)


# convert fastq to fasta
runstr = 'convert_fastaqual_fastq.py -f ' \
         '{0} -c fastq_to_fastaqual' \
         ' -o {1}'.format(os.path.join(jpe_dir,'fastqjoin.join.fastq'),
                                        fastafilesdir)
print ('fasta to fastq conversion:\n{0}'.format(runstr))

#convert_fastaqual_fastq.py -f fastqjoin.join.fastq -c fastq_to_fastaqual -o /home/smccalla/htcondor/GAIM_12/data/fasta_files

os.system(runstr)
print ('Finished converting fastq to fasta --- Huzzah!')

#Split the data into many files
fasta_many_dir = os.path.join(datadir, 'fasta_manyfiles')
if os.path.exists(fasta_many_dir):
    os.rmtree(fasta_many_dir)
os.mkdir(fasta_many_dir)

# get yer split on!
currdir = os.path.abspath(os.getcwd())

print ('navigating into: {0}'.format(fasta_many_dir))
os.chdir(fasta_many_dir)

os.runstr = 'python /home/Applications/OBITools-1.2.5/bin/split_fasta.py'
print ('splitting the data using:\n{0}'.format(runstr))
os.system(runstr)

print ('returning to the main directory: {0}'.format(currdir))
os.chdir(currdir)

print ('Finished splittng the fasta data into many files.\n\nfin')



