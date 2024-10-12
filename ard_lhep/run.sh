#!/bin/bash
rm  *.jpg
rm  *.png
python shot_by_signal.py -v --preview-width 1280 -f /home/ubuntu/ard_lhep/1.cfg
