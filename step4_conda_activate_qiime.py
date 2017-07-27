#!/usr/bin/python
#
#
#
# python step4_conda_activate_qiime.py GAIM_15
import sys, os

# http://fmgdata.kinja.com/using-docker-with-conda-environments-1790901398
os.system('/bin/bash -c "source activate qiime1 && exec python /home/smccalla/step4.py GAIM_15"')