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

if [[ ! -d "$package_dir" || "$(basename "$package_dir")" == "_template" ]]; then
  echo "A concrete project package is required: $package_dir" >&2
  exit 1
fi

required=(
  01_project_charter.md
  02_product_brief.md
  03_project_plan.md
  04_engineering_and_verification.md
  05_delivery_and_acceptance.md
)

failed=0
for file in "${required[@]}"; do
  if [[ ! -s "$package_dir/$file" ]]; then
    echo "MISSING: $file" >&2
    failed=1
  fi
done

check_value() {
  local file="$1"
  local label="$2"
  if rg -q -- "^- ${label}：.+$" "$package_dir/$file"; then
    echo "OK: $file contains ${label}"
  else
    echo "MISSING VALUE: $file -> ${label}" >&2
    failed=1
  fi
}

check_row() {
  local file="$1"
  local prefix="$2"
  if rg -q -- "^\\| ${prefix}[0-9]" "$package_dir/$file"; then
    echo "OK: $file contains ${prefix} entries"
  else
    echo "MISSING ENTRY: $file -> ${prefix}xx" >&2
    failed=1
  fi
}

check_value "01_project_charter.md" "项目编号与名称"
check_value "04_engineering_and_verification.md" "代码仓库、分支、提交/版本"
check_value "05_delivery_and_acceptance.md" "交付版本与构建标识"
check_row "02_product_brief.md" "R-"
check_row "03_project_plan.md" "M-"
check_row "03_project_plan.md" "T-"

if [[ "$failed" -ne 0 ]]; then
  echo "Project evidence check failed: $package_dir" >&2
  exit 1
fi

echo "Project evidence baseline is complete: $package_dir"
