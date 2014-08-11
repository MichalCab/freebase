#!/bin/bash
# devide big file to smaller ones

# Configuration stuff

fspec=$1
num_files=3

# Work out lines per file.

total_lines=$(cat ${fspec} | wc -l)
((lines_per_file = (total_lines + num_files - 1) / num_files))

# Split the actual file, maintaining lines.
split --lines=${lines_per_file} ${fspec} ${fspec}.parts.

# Debug information

echo "Total lines     = ${total_lines}"
echo "Lines  per file = ${lines_per_file}"    
wc -l ${fspec}.*
