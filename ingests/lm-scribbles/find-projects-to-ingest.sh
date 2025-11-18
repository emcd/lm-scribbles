#!/usr/bin/env bash
# Find projects in SCRIBBLES_WSL_2018 that have scribbles and need ingestion

scribbles_base="/home/me/src/SCRIBBLES_WSL_2018"
ingests_dir="/home/me/src/lm-scribbles/ingests"

echo "Projects with scribbles (excluding .gitignore):"
echo "================================================"

for project_dir in "$scribbles_base"/*; do
    if [ ! -d "$project_dir" ]; then
        continue
    fi

    project_name=$(basename "$project_dir")
    scribbles_path="$project_dir/.auxiliary/scribbles"

    if [ ! -d "$scribbles_path" ]; then
        continue
    fi

    # Count files excluding .gitignore
    file_count=$(find "$scribbles_path" -type f -not -name '.gitignore' 2>/dev/null | wc -l)

    if [ "$file_count" -eq 0 ]; then
        continue
    fi

    # Check if already ingested
    if [ -d "$ingests_dir/$project_name" ]; then
        status="[ALREADY INGESTED]"
    else
        status="[NEEDS INGESTION]"
    fi

    echo "$status $project_name: $file_count files"
done
