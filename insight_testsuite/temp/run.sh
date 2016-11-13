#!/usr/bin/env bash

# run script for running the fraud detection algorithm with a python file
# second arg is the degree of friendship

# I'll execute my programs, with the input directory paymo_input and output the files in the directory paymo_output
python ./src/payMo_feature.py 1 ./paymo_input/batch_payment.txt ./paymo_input/stream_payment.txt ./paymo_output/output1.txt
python ./src/payMo_feature.py 2 ./paymo_input/batch_payment.txt ./paymo_input/stream_payment.txt ./paymo_output/output2.txt
python ./src/payMo_feature.py 4 ./paymo_input/batch_payment.txt ./paymo_input/stream_payment.txt ./paymo_output/output3.txt
