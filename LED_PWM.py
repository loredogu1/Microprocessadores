#!/usr/bin/env python3
# SEL0337 - Pratica 5 - Controle da intensidade de LED por PWM
# Varia suavemente o brilho de 0 a 100% e de volta a 0% no GPIO 12.
# Este e o programa iniciado automaticamente pelo servico blink.service.

import signal
from time import sleep
from gpiozero import PWMLED

PINO_LED = 12  # Numero BCM, pino fisico 32
PASSO = 0.01   # Incremento de brilho por etapa
INTERVALO = 0.01  # Tempo entre etapas, em segundos
executando = True


def solicitar_parada(sinal, quadro):
    """Pede parada limpa ao receber SIGTERM do systemd ou Ctrl+C."""
    global executando
    executando = False


signal.signal(signal.SIGTERM, solicitar_parada)
signal.signal(signal.SIGINT, solicitar_parada)

led = PWMLED(PINO_LED, initial_value=0)

try:
    while executando:
        # Aumenta o duty cycle de 0% a 100%.
        for passo in range(0, 101):
            if not executando:
                break
            led.value = passo * PASSO
            sleep(INTERVALO)

        # Diminui o duty cycle de 99% a 0%.
        for passo in range(99, -1, -1):
            if not executando:
                break
            led.value = passo * PASSO
            sleep(INTERVALO)
finally:
    # Garante o LED apagado ao encerrar o servico.
    led.off()
    led.close()
