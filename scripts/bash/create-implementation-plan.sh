#!/usr/bin/env bash

set -e

JSON_MODE=false
ARGS=()
for arg in "$@"; do
    case "$arg" in
        --json) JSON_MODE=true ;;
        --help|-h) echo "Usage: $0 [--json] [feature_branch]"; exit 0 ;;
        *) ARGS+=("$arg") ;;
    esac
done

FEATURE_BRANCH="${ARGS[*]}"

# Function to find the repository root by searching for existing project markers
find_repo_root() {
    local dir="$1"
    while [ "$dir" != "/" ]; do
        if [ -d "$dir/.git" ] || [ -f "$dir/manifest.yml" ] || [ -d "$dir/forge-specs" ]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    return 1
}

# Resolve repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if git rev-parse --show-toplevel >/dev/null 2>&1; then
    REPO_ROOT=$(git rev-parse --show-toplevel)
    HAS_GIT=true
else
    REPO_ROOT="$(find_repo_root "$SCRIPT_DIR")"
    if [ -z "$REPO_ROOT" ]; then
        echo "Error: Could not determine repository root." >&2
        exit 1
    fi
    HAS_GIT=false
fi

cd "$REPO_ROOT"

# If no feature branch specified, use current branch
if [ -z "$FEATURE_BRANCH" ]; then
    if [ "$HAS_GIT" = true ]; then
        FEATURE_BRANCH=$(git rev-parse --abbrev-ref HEAD)
    else
        echo "Error: No feature branch specified and git not available." >&2
        exit 1
    fi
fi

SPECS_DIR="$REPO_ROOT/forge-specs"
FEATURE_DIR="$SPECS_DIR/$FEATURE_BRANCH"

if [ ! -d "$FEATURE_DIR" ]; then
    echo "Error: Feature directory not found: $FEATURE_DIR" >&2
    exit 1
fi

SPEC_FILE="$FEATURE_DIR/feature-spec.md"
if [ ! -f "$SPEC_FILE" ]; then
    echo "Error: Specification file not found: $SPEC_FILE" >&2
    exit 1
fi

PLAN_FILE="$FEATURE_DIR/implementation-plan.md"
TEMPLATE="$REPO_ROOT/templates/plan-template.md"

if [ -f "$TEMPLATE" ]; then
    cp "$TEMPLATE" "$PLAN_FILE"
else
    touch "$PLAN_FILE"
fi

if $JSON_MODE; then
    printf '{"BRANCH_NAME":"%s","SPEC_FILE":"%s","PLAN_FILE":"%s"}\n' "$FEATURE_BRANCH" "$SPEC_FILE" "$PLAN_FILE"
else
    echo "BRANCH_NAME: $FEATURE_BRANCH"
    echo "SPEC_FILE: $SPEC_FILE"
    echo "PLAN_FILE: $PLAN_FILE"
fi
