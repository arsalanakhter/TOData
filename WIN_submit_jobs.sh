#!/usr/bin/env bash
#SBATCH -J toptw
#SBATCH -n 12
#SBATCH -N 1
#SBATCH -p short
#SBATCH --mem 2G

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
MYDIR='C:\Users\Arsala~1\Documents\GitHub\TOData\'

# Folder where you want your data to be stored (my cluster environment)
DATADIR=$MYDIR/data
SOLDIR=$MYDIR/sol

# Change as per experiment
# THISJOB=$MYDIR

########################################
#
# Job-related variables
#
########################################

# Job working directory
# (Don't change this)
#WORKDIR=$LOCALDIR/$MYUSER/$THISJOB



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
#trap cleanup EXIT SIGINT SIGTERM



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
# Make DIRS for data and sol
mkdir -p $DATADIR
mkdir -p $SOLDIR
for NO_OF_ROBOTS in 2 3
do
    for NO_OF_DEPOTS in 2 3
    do
        for NO_OF_TASKS in 5 10
        do 
            for FUEL in 50 75 150
            do
                for T_MAX in 150 300 600
                do
                    # Create Instance name
                    INSTANCE_STRING="R${NO_OF_ROBOTS}D${NO_OF_DEPOTS}T${NO_OF_TASKS}F${FUEL}Tmax${T_MAX}"
                    # submit job
                    sh cluster_single_job.sh ${INSTANCE_STRING}
                    # Sleep for 1 sec so that the machine is not overloaded
                    sleep 1
                done
            done
        done
    done
done
# Transfer generated *.dat files into home directory
# Create the two folders (my cluster environment)
# Make sure they ARE NOT already present
# mkdir $DATADIR
# mkdir $DATADIR/csv && mkdir $DATADIR/img
# mv *.csv $DATADIR/csv
# mv *.html $DATADIR/img
