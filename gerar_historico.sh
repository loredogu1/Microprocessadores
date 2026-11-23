#!/usr/bin/env bash
# Salva os commits reais do repositorio local, conforme o Checkpoint 2.
set -euo pipefail
cd "$(dirname "$0")"
git log > historico_git.txt
echo "Gerado: historico_git.txt"
