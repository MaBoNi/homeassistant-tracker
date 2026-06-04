#!/bin/bash

# === scripts/increment-version.sh ===
# Automatically increment patch version for semantic versioning (YY.MM.PATCH)
# Used by GitHub Actions on PR merge to main branch

set -euo pipefail

# Configuration
readonly CURRENT_YEAR=$(date +%y)
readonly CURRENT_MONTH=$(date +%-m)

# Function to get the current month version (e.g., 26.4)
get_current_month_version() {
    echo "${CURRENT_YEAR}.${CURRENT_MONTH}"
}

# Function to get the latest git tag matching the current month
get_latest_patch_version() {
    local month_prefix="$1"

    # Get all tags matching the current month pattern (e.g., 26.4.*)
    # Sort them by version number and get the latest one
    local latest_tag
    latest_tag=$(git tag -l "${month_prefix}.*" | sort -V | tail -n 1)

    if [[ -z "$latest_tag" ]]; then
        # No patch versions exist for this month, start with .0
        echo "${month_prefix}.0"
    else
        echo "$latest_tag"
    fi
}

# Function to increment the patch version
increment_patch() {
    local version="$1"

    # Extract patch number from version (e.g., "26.4.15" -> "15")
    local patch_number
    patch_number=$(echo "$version" | cut -d. -f3)

    # Increment patch number
    local new_patch=$((patch_number + 1))

    # Reconstruct version with incremented patch
    local month_version
    month_version=$(echo "$version" | cut -d. -f1-2)

    echo "${month_version}.${new_patch}"
}

# Main logic
main() {
    echo "🔧 Calculating next patch version..."

    # Get current month version prefix
    local month_version
    month_version=$(get_current_month_version)
    echo "📅 Current month version prefix: $month_version"

    # Get latest patch version for current month
    local current_version
    current_version=$(get_latest_patch_version "$month_version")
    echo "🏷️  Latest version: $current_version"

    # Check if we need to roll to new month
    local current_month_from_tag
    current_month_from_tag=$(echo "$current_version" | cut -d. -f2)

    if [[ "$current_month_from_tag" != "$CURRENT_MONTH" ]]; then
        # New month, start from .0
        local new_version="${month_version}.0"
        echo "🆕 New month detected, starting with: $new_version"
    else
        # Same month, increment patch
        local new_version
        new_version=$(increment_patch "$current_version")
        echo "⬆️  Incremented to: $new_version"
    fi

    # Output the new version for GitHub Actions (if available)
    if [[ -n "${GITHUB_OUTPUT:-}" ]]; then
        echo "NEW_VERSION=$new_version" >> "$GITHUB_OUTPUT"
        echo "PREVIOUS_VERSION=$current_version" >> "$GITHUB_OUTPUT"
    fi

    # Also output to stdout for local usage
    echo "📦 New version: $new_version"
    echo "$new_version"
}

# Run main function
main "$@"