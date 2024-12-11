#!/bin/bash
set -e

# Activate conda environment
source /opt/conda/etc/profile.d/conda.sh
conda activate catpred

# Run prediction script with passed arguments
cd /app/catpred
exec python demo_run.py "$@"