# amplicon_pipeline

## 3 different ways to analyze data with these files
_____________________________________________________________________________________________________________________________
If not using HTCondor

Example submit for step1:
> step1.py GAIM_01*_R1_001.fastq.gz GAIM_01*_R2_001.fastq.gz GAIM_01 160408_NB501144_0002_AHMFMNBGXX Loons_Long_Tailed

Example submit for step2:
> step2.py GAIM_01

Example submit for step3:
> condor_submit step3.sub

Example submit for step3:
> step4.py GAIM_01
______________________________________________________________________________________________________________________________
If using HTCondor

Example submit for step1:
> condor submit step1.sub

Example submit for step2:
> condor submit step2.sub

Example submit for step3:
> condor submit step3.sub

Example submit for step3:
> condor submit step4.sub
______________________________________________________________________________________________________________________________
If using HTCondor and DAG

Example HTCondor submit for DAG:
> condor_submit_dag DAGabc.dag
