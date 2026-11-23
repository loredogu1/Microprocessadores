#!/usr/bin/env bash
# Instala o servico usando a pasta e o usuario atuais da Raspberry Pi.
# Uso: bash instalar_servico.sh (sem sudo; o script solicitara sudo).
set -euo pipefail

if [[ "${EUID}" -eq 0 ]]; then
    echo "Execute com seu usuario normal: bash instalar_servico.sh (sem sudo)." >&2
    exit 1
fi

PASTA="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
USUARIO="$(id -un)"

if [[ "$PASTA" == *' '* || "$PASTA" == *'%'* ]]; then
    echo "Utilize uma pasta sem espacos nem '%' no caminho: $PASTA" >&2
    exit 1
fi
if [[ ! -f "$PASTA/LED_PWM.py" || ! -f "$PASTA/parar_led.py" ]]; then
    echo "Execute este script na pasta que contem os arquivos .py." >&2
    exit 1
fi
if [[ ! -x /usr/bin/python3 ]]; then
    echo "Python nao encontrado em /usr/bin/python3." >&2
    exit 1
fi
if ! /usr/bin/python3 -c 'import gpiozero' >/dev/null 2>&1; then
    echo "Biblioteca gpiozero nao encontrada. Instale-a primeiro:" >&2
    echo "  sudo apt update && sudo apt install python3-gpiozero" >&2
    exit 1
fi

ARQUIVO_TEMP="$(mktemp)"
trap 'rm -f "$ARQUIVO_TEMP"' EXIT

# Monta o unit file sem alterar a copia versionada no Git.
sed -e "s|/home/sel/6190|$PASTA|g" \
    -e "s|^User=sel$|User=$USUARIO|" \
    "$PASTA/blink.service" > "$ARQUIVO_TEMP"

sudo install -m 0644 "$ARQUIVO_TEMP" /etc/systemd/system/blink.service
sudo systemctl daemon-reload
sudo systemctl enable blink.service
sudo systemctl restart blink.service

echo
printf 'Servico instalado com User=%s e WorkingDirectory=%s\n' "$USUARIO" "$PASTA"
sudo systemctl --no-pager --full status blink.service
