#!/usr/bin/env bash
#SBATCH -n 1
#SBATCH -N 10
#SBATCH -p short
#SBATCH --mem 32G

# Stop execution after any error
set -e

# Cleanup function to be executed upon exit, for any reason
function cleanup() {
    rm -rf $WORKDIR
}



########################################
#
# Useful variables
#
########################################

# Your user name
# (Don't change this)
MYUSER=$(whoami)

# Path of the local storage on a node
# Use this to avoid sending data streams over the network
# (Don't change this)
#LOCALDIR=/local
# To be changed as per experiment (my cluster environment)
MYDIR='/home/aakhter/work/TOData'

# Folder where you want your data to be stored (my cluster environment)
DATADIR=$MYDIR/data
SOLDIR=$MYDIR/sol

# Change as per experiment
THISJOB=$MYDIR

########################################
#
# Job-related variables
#
########################################

# Job working directory
# (Don't change this)
WORKDIR=$LOCALDIR/$MYUSER/$THISJOB



########################################
#
# Job directory
#
########################################

# Create work dir from scratch, enter it
# (Don't change this)
#rm -rf $WORKDIR && mkdir -p $WORKDIR && cd $WORKDIR

# Make sure you cleanup upon exit
# (Don't change this)
trap cleanup EXIT SIGINT SIGTERM



########################################
#
# Actual job logic
#
########################################

# Execute job
# Commands
#module load gurobi # Comment this if running heuristic
#python3 -m pip install plotly --user
#mkdir C-mdvrp # comment this if running random input
#cp $MYDIR/C-mdvrp/* $WORKDIR/C-mdvrp/  # comment this if running random input
#for i in {1..10}
#do
INSTANCE_STRING=$1 
echo $INSTANCE_STRING
#SBATCH -J ${INSTANCE_STRING}
python $MYDIR/main.py ${INSTANCE_STRING}
#done
#rm -rf $DATADIR
#mkdir $DATADIR
#mkdir $DATADIR/csv && mkdir $DATADIR/img
#mv *.csv $DATADIR/csv
#mv *.html $DATADIR/img
