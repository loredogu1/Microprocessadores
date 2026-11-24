"""SEL0337 - Pratica 5: controle de brilho do LED por PWM.

Mantem o funcionamento do programa original: o brilho sobe de 0 a 100%
em passos de 1%, retornando a 0% ao final de cada ciclo.
O script e executado pelo systemd por meio do arquivo blink.service.
"""

import signal
from time import sleep
from gpiozero import PWMLED

PINO_LED = 12  # GPIO12 (BCM), pino fisico 32.
led = PWMLED(PINO_LED)
executando = True


def solicitar_parada(signum, frame):
    """Recebe SIGTERM quando o servico e interrompido pelo systemd."""
    global executando
    executando = False


signal.signal(signal.SIGTERM, solicitar_parada)
signal.signal(signal.SIGINT, solicitar_parada)

try:
    while executando:
        for brilho in range(101):
            if not executando:
                break
            led.value = brilho / 100  # Duty cycle: 0 a 1.
            sleep(0.01)  # Intervalo de 10 ms entre os passos.
finally:
    led.off()    # Garante que o LED seja desligado ao parar o servico.
    led.close()  # Libera os recursos da GPIO.
