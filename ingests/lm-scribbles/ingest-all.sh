#!/usr/bin/env bash
# Ingest scribbles from all projects that need it

scribbles_base="/home/me/src/SCRIBBLES_WSL_2018"

# List of projects to ingest
projects=(
    "python-appcore"
    "python-classcore"
    "python-project-common"
    "rust-litrpg"
)

for project in "${projects[@]}"; do
    echo "================================================"
    echo "Ingesting: $project"
    echo "================================================"

    scribbles_path="$scribbles_base/$project/.auxiliary/scribbles"

    if [ ! -d "$scribbles_path" ]; then
        echo "ERROR: Scribbles directory not found: $scribbles_path"
        continue
    fi

    hatch run lmscribbles ingest \
        --project-name "$project" \
        --source-paths "$scribbles_path"

    echo ""
done

echo "================================================"
echo "All ingestions complete!"
echo "================================================"
