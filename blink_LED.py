"""SEL0337 - Pratica 5: acionamento digital de LED na GPIO12.

Programa da pratica anterior, utilizado como exemplo de controle liga/desliga.
O LED fica ligado por 1 segundo e desligado por 1 segundo.
Execute separadamente do servico PWM, pois ambos usam o mesmo pino.
"""

import RPi.GPIO as GPIO
from time import sleep

PINO_LED = 12  # Numeracao BCM: GPIO12 corresponde ao pino fisico 32.

GPIO.setmode(GPIO.BCM)
GPIO.setup(PINO_LED, GPIO.OUT)

try:
    while True:
        GPIO.output(PINO_LED, True)   # Liga o LED.
        sleep(1)
        GPIO.output(PINO_LED, False)  # Desliga o LED.
        sleep(1)
except KeyboardInterrupt:
    pass  # Permite interromper com Ctrl+C.
finally:
    GPIO.output(PINO_LED, False)
    GPIO.cleanup(PINO_LED)  # Libera o pino quando o programa termina.
