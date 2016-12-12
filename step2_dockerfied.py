#!/usr/bin/python
##python step2_docker3.py GAIM_12
from __future__ import print_function
import sys, os, shutil, glob
import zipfile
import os
from Bio import SeqIO
import glob

exfile = 'fastqjoin.join.fna'

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
runstr = 'add_qiime_labels.py -i /home/smccalla/{0}/data/fasta_files/ ' \
                '-m /home/smccalla/loon_qiime_mapping_file_trainer_file_3_corrected.txt ' \
                '-c InputFileName -n 1 -o {1}'.format(
                os.path.join(the_analysis_name), os.path.join(fastafilesdir))
os.system(runstr)

runstr = 'pwd'
os.system(runstr)

#Split the data into many files
fasta_many_dir = os.path.join(datadir, 'fasta_manyfiles')
if os.path.exists(fasta_many_dir):
    shutil.rmtree(fasta_many_dir)
os.mkdir(fasta_many_dir)

# get yer split on!
currdir = os.path.abspath(os.getcwd())

print ('navigating into: {0}'.format(fasta_many_dir))
os.chdir(fasta_many_dir)

#os.runstr = 'python /home/smccalla/split_fasta.py'
#runstr = 'python split_fasta.py'
#print ('splitting the data using:\n{0}'.format(runstr))
#os.system(runstr)

fppath =  os.path.join(fastafilesdir, 'combined_seqs.fna')

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
			
record_iter = SeqIO.parse(open(fppath),"fasta")
for i, batch in enumerate(batch_iterator(record_iter, 10000)):
    filename = "group_%i.fasta" % (i)
    handle = open(filename, "w")
    count = SeqIO.write(batch, handle, "fasta")
    handle.close()
    print("Wrote %i records to %s" % (count, filename))


print ('returning to the main directory: {0}'.format(currdir))
os.chdir(currdir)

print ('Finished splittng the fasta data into many files.\n\nfin')

#with zipfile.ZipFile('{0}_step2_results.zip'.format(the_analysis_name), 'w') as zf:
#    with open(exfile, 'wb') as ofp:
#        ofp.write(zf.read(exfile))
        
with zipfile.ZipFile('{0}_step2_results.zip'.format(the_analysis_name), 'w', zipfile.ZIP_DEFLATED) as ifp:
    for coutdir in [fastafilesdir,fasta_many_dir]:
        for cf in os.listdir(coutdir):
            ifp.write(os.path.join(coutdir,cf),cf)