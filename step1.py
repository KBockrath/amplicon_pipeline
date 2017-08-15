#!/usr/bin/python
# docker run -it -v /home/smccalla/:/home/smccalla/ -w /usr/ -i smccalla/amplicon_dockerfile /bin/bash
# python step1.py test*_R1.fastq.gz test*_R2.fastq.gz test_28 test test
# python step1.py GAIM_03*_R1_001.fastq.gz GAIM_03*_R2_001.fastq.gz GAIM_03 160408_NB501144_0002_AHMFMNBGXX Loons_Long_Tailed
#
#
#
# Assuming all the raw data is in /home/smccalla/working_docker_directory/raw_data
from __future__ import print_function
import sys, os, shutil, glob, zipfile

# read in command line variables
realnum1 = sys.argv[1]
realnum2 = sys.argv[2]
the_analysis_name = sys.argv[3]
machine_run = sys.argv[4]
sample_index_name = sys.argv[5]

# make a directory for output
if not os.path.exists(the_analysis_name):
    os.mkdir(the_analysis_name)

# then make a data directory
datadir = os.path.abspath(os.path.join(the_analysis_name,'data'))
if os.path.exists(datadir):
    shutil.rmtree(datadir) 
os.mkdir(datadir)

# copy over the forward and reverse raw data files
# find the raw data at: /home/smccalla/working_docker_directory/raw_data
# raw_datadir = os.path.abspath(os.path.join('/','home','smccalla','raw_data'))
raw_datadir = os.path.abspath(os.path.join('/','home','smccalla','working_docker_directory','raw_data'))

for file in glob.glob(os.path.join(raw_datadir,realnum1)):
    print ('copying from {0} to {1}'.format(file,os.path.join(datadir,os.path.basename(file))))
    shutil.copyfile(file,os.path.join(datadir,os.path.basename(file)))
    
for file in glob.glob(os.path.join(raw_datadir,realnum2)):
    print ('copying from {0} to {1}'.format(file,os.path.join(datadir,os.path.basename(file))))
    shutil.copyfile(file,os.path.join(datadir,os.path.basename(file)))

print ("Finished copying the forward and reverse files")


# unzip the raw data
for file in glob.glob(os.path.join(datadir,realnum1)):
    os.system('gunzip {0}'.format(file))
for file in glob.glob(os.path.join(datadir,realnum2)):
    os.system('gunzip {0}'.format(file))
print ("Finished unzipping the forward and reverse files")

# combining the raw data files
os.system('cat {0}/*R1*.fastq > {0}/all_R1.fastq'.format(datadir))
os.system('cat {0}/*R2*.fastq > {0}/all_R2.fastq'.format(datadir))

print ("Finished concatenating the forward and reverse files")

# Change file permissions
runstr='chmod -R 777 {0}'.format(
    os.path.join(datadir))

# make a fastQC folder
fastQCdir = os.path.join(datadir,'fastQC')
if not os.path.exists(fastQCdir):
    os.mkdir(fastQCdir)

os.system("export PATH=/usr/local/bin/FastQC:$PATH")
    
print ("moved in the fastQ data\n Now running fastQC")
#Test FastQC:
# /usr/local/bin/FastQC/fastqc --outdir /all_R1.fastq && fastqc /home/Applications/OBITools-1.2.5/bin/${the_analysis_name}/data/FastQC/all_R2.fastq && echo Finished FastQC
for i in [1,2]:
    print ('Running fastQC for all_R{0}.fastq'.format(i))
    runstr='fastqc {0} --outdir={1}'.format(
        os.path.join(datadir, 'all_R{0}.fastq'.format(i)),
        fastQCdir)
    os.system(runstr)

# Change file permissions
runstr='chmod -R 777 {0}'.format(
    os.path.join(datadir))    
    
print ("Finished fastQC")
# next run fastQvalidator

# make a fastQValidator folder
fastQvaldir = os.path.join(datadir,'fastQValidator')
if not os.path.exists(fastQvaldir):
    os.mkdir(fastQvaldir)

print ("Now running fastQValidator")
for i in [1,2]:
    print ('Running fastQValidator for all_R{0}.fastq'.format(i))
    runstr = '/usr/local/bin/fastQValidator/bin/fastQValidator --file {0} --minReadLen 70 --printableErrors 50' \
             ' --baseComposition --avgQual --maxErrors 50 > {1}'.format(
                os.path.join(datadir,'all_R{0}.fastq'.format(i)),
                os.path.join(fastQvaldir,'R{0}.fastQValidator'.format(i)))
    print ('running fasQValidator:\n{0}'.format(runstr))
    os.system(runstr)

print ("fastQValidator complete!")

# trimmomatic
print ("running Trimmomatic")
trimdatadir = os.path.join(datadir,'trimdata')
if not os.path.exists(trimdatadir):
    os.mkdir(trimdatadir)

# construct trimmomatic call
runstr = 'java -jar /usr/local/bin/trimmomatic-0.36.jar '  \
          'PE -phred33 -trimlog {0}trimlog.trim {1} {2} '  \
          '{3}/R1trimmed.fastq {3}/R1single.fastq {3}/R2trimmed.fastq {3}/R2single.fastq LEADING:3 ' \
          'TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:70'.format(
              os.path.join(trimdatadir,'{0}_trimlog.trim'.format(the_analysis_name)),
              os.path.join(datadir, 'all_R1.fastq'),
              os.path.join(datadir, 'all_R2.fastq'),
              trimdatadir
          )

print ('Running trimmomatic with system call:\n{0}'.format(runstr))

os.system(runstr)

# Join paired ends

# make a join_paired_ends folder
jpe_dir = os.path.join(datadir, 'join_paired_ends')
if not os.path.exists(jpe_dir):
    os.mkdir(jpe_dir)

# run join_paired_ends.py
runstr='join_paired_ends.py -m fastq-join ' \
    '-f {0}/R1trimmed.fastq -r {0}/R2trimmed.fastq -o {1}'.format(
    os.path.join(trimdatadir),
    jpe_dir)

print('Running join_paired_ends.py: \n'.format(runstr))
os.system(runstr)

# Change file permissions
runstr='chmod -R 777 {0}'.format(
    os.path.join(datadir))

print('Changing permissions: \n'.format(runstr))
os.system(runstr)

#with zipfile.ZipFile('{0}_step1_results.zip'.format(the_analysis_name), 'w', zipfile.ZIP_DEFLATED) as ifp:
#    for coutdir in [fastQCdir,fastQvaldir,trimdatadir,jpe_dir]:
#        for cf in os.listdir(coutdir):
#            ifp.write(os.path.join(coutdir,cf),cf)
