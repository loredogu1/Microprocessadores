#!/usr/bin/env bash

set -euo pipefail
cd "$(dirname "$0")"
git log > historico_git.txt
echo "Gerado: historico_git.txt"
