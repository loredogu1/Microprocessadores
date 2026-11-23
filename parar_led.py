#!/usr/bin/env python3
# SEL0337 - Pratica 5 - Programa executado pela diretiva ExecStop.
# Solicita ao processo PWM que encerre e aguarda sua finalizacao.
# O proprio LED_PWM.py, ao tratar SIGTERM, apaga o LED e libera a GPIO.

import os
import signal
import sys
import time


def processo_terminou(pid):
    """Verifica se o processo saiu ou esta como zumbi (aguardando coleta)."""
    try:
        with open(f"/proc/{pid}/stat", encoding="utf-8") as arquivo:
            # Apos o ultimo ')' vem: estado, ppid, ...
            estado = arquivo.read().rsplit(") ", 1)[1].split()[0]
            return estado == "Z"
    except FileNotFoundError:
        return True


def main():
    if len(sys.argv) != 2:
        print("Uso: parar_led.py PID_DO_PROCESSO_PRINCIPAL", file=sys.stderr)
        return 2
    try:
        pid = int(sys.argv[1])
    except ValueError:
        print("PID invalido", file=sys.stderr)
        return 2
    if pid <= 1:
        print("PID nao permitido", file=sys.stderr)
        return 2

    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        return 0  # Processo ja terminou.

    limite = time.monotonic() + 5
    while time.monotonic() < limite:
        if processo_terminou(pid):
            return 0
        time.sleep(0.05)

    print("O processo nao encerrou em 5 s; o systemd aplicara seu timeout.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
