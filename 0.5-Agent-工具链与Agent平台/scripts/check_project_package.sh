#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <project_id-or-path>" >&2
  exit 2
fi

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
input="$1"
if [[ -d "$input" ]]; then
  package_dir="$(cd "$input" && pwd)"
else
  package_dir="$repo_root/1.1-项目事实与交付档案/$input"
fi

if [[ ! -d "$package_dir" ]]; then
  echo "Project package not found: $package_dir" >&2
  exit 1
fi

required=(
  01_project_charter.md
  02_product_brief.md
  03_project_plan.md
  04_engineering_and_verification.md
  05_delivery_and_acceptance.md
  06_retrospective.md
)

failed=0
for file in "${required[@]}"; do
  if [[ ! -s "$package_dir/$file" ]]; then
    echo "MISSING: $file" >&2
    failed=1
  else
    echo "OK: $file"
  fi
done

if [[ "$failed" -ne 0 ]]; then
  exit 1
fi

echo "Project package structure is complete: $package_dir"
