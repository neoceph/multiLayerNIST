#!/bin/sh

# Set some input variables to determine input files to run
inputNames="inputfile_MultiLayer.k"
logString="Log_MultiLayer"
export OMP_NUM_THREADS=18

# Provide appropiate paths
execDirec="./"
execFile="./AM-CFD"
inputDirec="./"

# Define the name of the logfile
logAppend=".log"

# Set up the full file names/paths
fileI=$inputNames
printf "Running %s file\n" $fileI
logFileName="$logString$logAppend"
inputI=$inputDirec$fileI

# delete last analysis files
rm -R Trial_MultiLayer/
rm -R Trial_MultiLayer.pvd Log_MultiLayer.log *.txt
pkill -9 execFile

# run the simulation
cmd="$execDirec$execFile $inputI > $logFileName &"
eval $cmd

echo "Starting the simulation in 5 seconds..."
sleep 5

# start Log_MultiLayer.log tailing
tail -f Log_MultiLayer.log
