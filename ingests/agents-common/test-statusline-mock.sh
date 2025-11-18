#!/bin/bash
# Test statusline script with mock input

# Create mock input JSON
cat <<EOF | /home/me/.config/claude/statusline.py
{
  "hook_event_name": "Status",
  "session_id": "test-session",
  "transcript_path": "$HOME/.config/claude/projects/-home-me-src-agents-common/72687e8f-409b-4c1d-81e2-8bedbfa401f3.jsonl",
  "cwd": "/home/me/src/agents-common",
  "gitBranch": "master",
  "model": {
    "id": "claude-sonnet-4-5-20250929",
    "display_name": "Sonnet 4.5"
  },
  "workspace": {
    "current_dir": "/home/me/src/agents-common",
    "project_dir": "/home/me/src/agents-common"
  },
  "version": "2.0.0"
}
EOF

echo ""