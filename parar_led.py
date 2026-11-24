"""SEL0337 - Pratica 5: programa executado em ExecStop do blink.service.

Envia SIGTERM para o processo de LED_PWM.py, que desliga o LED no finally.
O PID e fornecido pelo systemd por meio da variavel $MAINPID.
"""

import os
import signal
import sys
import time


def main():
    if len(sys.argv) != 2:
        print("Uso: parar_led.py PID", file=sys.stderr)
        return 2

    try:
        pid = int(sys.argv[1])
        if pid <= 1:
            return 2
        os.kill(pid, signal.SIGTERM)  # Solicita parada do programa PWM.
    except (ValueError, ProcessLookupError):
        return 0  # PID ja finalizado ou invalido.

    # Aguarda o encerramento antes de devolver o controle ao systemd.
    for _ in range(100):
        try:
            with open(f"/proc/{pid}/stat", encoding="utf-8") as arquivo:
                estado = arquivo.read().rsplit(") ", 1)[1].split()[0]
            if estado == "Z":  # Processo terminado, aguardando coleta.
                return 0
        except FileNotFoundError:
            return 0
        time.sleep(0.05)

    print("Aviso: processo PWM ainda ativo apos 5 segundos.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
