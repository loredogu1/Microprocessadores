# SEL0337 — Prática 5

## Checkpoints 1 e 2 — Controle de LED com Raspberry Pi

### 1. Objetivo

Esta prática tem como objetivo desenvolver aplicações de controle de GPIO utilizando uma Raspberry Pi e a linguagem Python, além de explorar a execução automática de programas por meio de serviços `systemd`.

Foram utilizados dois programas: um para controlar o acionamento intermitente de um LED e outro para variar sua intensidade luminosa utilizando PWM.

### 2. Arquivos do projeto

- `blink_LED.py` — Programa responsável por ligar e desligar o LED.
- `LED_PWM.py` — Programa responsável por variar o brilho do LED utilizando PWM.
- `blink.service` — Arquivo de configuração de um serviço `systemd` para executar o controle PWM.

### 3. Funcionamento dos programas

**Controle de acionamento — blink_LED.py**

O programa utiliza a biblioteca `RPi.GPIO` para configurar o GPIO 12 como saída digital.

Em um laço infinito, o LED permanece ligado durante 1 segundo e desligado durante 1 segundo, repetindo continuamente o ciclo.

**Controle de brilho — LED_PWM.py**

O segundo programa utiliza a biblioteca `gpiozero` e a classe `PWMLED` para controlar a intensidade luminosa.

A variável `led.value` recebe valores de 0 a 1, representando o ciclo de trabalho do PWM de 0% a 100%.

O brilho aumenta progressivamente em incrementos de 1%, com um intervalo de 0,01 segundo entre as atualizações. Ao completar o ciclo, o programa retorna ao brilho mínimo e inicia uma nova subida.

### 4. Serviço systemd

O arquivo `blink.service` foi criado para permitir a execução do programa de controle PWM como um serviço do sistema operacional.

O serviço utiliza o interpretador Python 3 para executar `LED_PWM.py`.

O `systemd` permite gerenciar a aplicação por comandos de inicialização, parada, consulta de estado e habilitação para execução durante a inicialização do sistema.

Os principais comandos utilizados são:

- `sudo systemctl daemon-reload`
- `sudo systemctl start blink.service`
- `sudo systemctl status blink.service`
- `sudo systemctl stop blink.service`
- `sudo systemctl enable blink.service`

**Observação:** a configuração original de parada precisa ser ajustada para garantir o desligamento adequado da aplicação.

### 5. Conceitos utilizados

**GPIO:** interface de entrada e saída digital da Raspberry Pi, utilizada para controlar componentes eletrônicos.

**PWM:** modulação por largura de pulso, técnica que permite controlar a intensidade luminosa média de um LED alterando o ciclo de trabalho do sinal.

**Python:** linguagem utilizada para implementar os programas de controle.

**systemd:** gerenciador de serviços do Linux, responsável por iniciar, supervisionar e interromper aplicações.

### 6. Evidências experimentais

*Inserir aqui as evidências obtidas durante a execução da prática.*

**Foto 1 — Montagem do circuito**

[Inserir fotografia da Raspberry Pi conectada ao LED.]

**Foto 2 — Funcionamento do LED**

[Inserir fotografia ou captura demonstrando o acionamento.]

**Foto 3 — Serviço systemd**

[Inserir captura do comando `systemctl status blink.service`, após a validação.]

### 7. Versionamento

O projeto será versionado utilizando Git e hospedado no GitHub.

O arquivo `historico_git.txt` deve conter o histórico dos commits realizados na Raspberry Pi, gerado com o comando:

`git log > historico_git.txt`

### 8. Resultados e conclusão

A prática permite observar a diferença entre o acionamento digital de um LED e o controle de sua intensidade luminosa utilizando PWM.

Também introduz a utilização de serviços `systemd` para gerenciar programas Python em sistemas Linux embarcados.

Os resultados experimentais, incluindo o funcionamento do serviço após a inicialização da Raspberry Pi, deverão ser registrados após os testes no equipamento.
