#!/bin/bash
#
#

runnumber=$1

#run outformat 6 BLAST
blastn -query /home/smccalla/test_28/data/fasta_files/fastqjoin.join.fna.formatted/group_${runnumber}.fasta -db /home/Applications/ncbi-blast-2.4.0+/bin/nt00thru36 -evalue 1e-1 -out /home/smccalla/test_28/data/fasta_files/fastqjoin.join.fna.formatted/group_${runnumber}.out -outfmt '6 qseqid qlen sseqid pident length qstart qend sstart send evalue bitscore staxids' && echo Yes BLAST is finished
# blastn -query /home/smccalla/test_28/data/fasta_files/fastqjoin.join.fna.formatted/group_${runnumber}.fasta -db /home/Applications/ncbi-blast-2.4.0+/bin/nt00thru36 -evalue 1e-1 -out /home/smccalla/test_28/data/fasta_files/fastqjoin.join.fna.formatted/group_${runnumber}.out -outfmt '6 qseqid qlen sseqid pident length qstart qend sstart send evalue bitscore staxids' && echo Yes BLAST is finished
