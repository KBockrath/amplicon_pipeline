# amplicon_pipeline
Get rid of line endings: sed -i 's/\r//' step1.py

Example submit for step1:
> step1.py GAIM_01*_R1_001.fastq.gz GAIM_01*_R2_001.fastq.gz GAIM_01 160408_NB501144_0002_AHMFMNBGXX Loons_Long_Tailed

Example submit for step2:
> step2.py GAIM_01

Example submit for step3:
> step3.py
______________________________________________________________________________________________________________________________
Example HTCondor submit for step1:
> condor_submit step1.sub

Example HTCondor submit for step2:
> condor_submit step2.sub

Example HTCondor submit for step3:
> condor_submit step3.sub
______________________________________________________________________________________________________________________________
Example HTCondor submit for DAG:
> condor_submit_dag DAGabc.dag
