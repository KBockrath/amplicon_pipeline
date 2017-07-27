#!/usr/bin/python
#
#
#
import sys, os

# http://fmgdata.kinja.com/using-docker-with-conda-environments-1790901398
os.system('/bin/bash -c "source activate qiime1 && exec python /home/smccalla/step2.py GAIM_15"')