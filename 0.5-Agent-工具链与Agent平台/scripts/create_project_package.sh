#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <project_id>" >&2
  exit 2
fi

project_id="$1"
if [[ ! "$project_id" =~ ^[a-z0-9][a-z0-9_-]{2,63}$ ]]; then
  echo "project_id must match: [a-z0-9][a-z0-9_-]{2,63}" >&2
  exit 2
fi

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
archive_root="$repo_root/1.1-项目事实与交付档案"
template="$archive_root/_template"
target="$archive_root/$project_id"

if [[ ! -d "$template" ]]; then
  echo "Project template not found: $template" >&2
  exit 1
fi

if [[ -e "$target" ]]; then
  echo "Project package already exists: $target" >&2
  exit 1
fi

cp -a "$template" "$target"
echo "Created project package: $target"
echo "Complete 01_project_charter.md and 02_product_brief.md before implementation."
