#!/usr/bin/env python3
# SEL0337 - Pratica 5 - Controle digital de LED
# Pisca um LED conectado ao GPIO 12 (pino fisico 32), com intervalo de 1 s.
# Executar este exemplo separadamente, com o servico blink.service parado.

import signal
from time import sleep
import RPi.GPIO as GPIO

PINO_LED = 12  # Numero BCM, nao o numero do pino fisico
executando = True


def solicitar_parada(sinal, quadro):
    """Encerra o laco ao receber SIGTERM ou Ctrl+C."""
    global executando
    executando = False


signal.signal(signal.SIGTERM, solicitar_parada)
signal.signal(signal.SIGINT, solicitar_parada)

GPIO.setmode(GPIO.BCM)
GPIO.setup(PINO_LED, GPIO.OUT, initial=GPIO.LOW)

try:
    while executando:
        GPIO.output(PINO_LED, GPIO.HIGH)
        sleep(1)
        if not executando:
            break
        GPIO.output(PINO_LED, GPIO.LOW)
        sleep(1)
finally:
    # Desliga o LED e devolve o controle do GPIO ao sistema.
    GPIO.output(PINO_LED, GPIO.LOW)
    GPIO.cleanup(PINO_LED)
