# SEL0337 — Prática 5: Systemd, Git e GitHub

**Disciplina:** SEL0337 — Projetos em Sistemas Embarcados  
**Atividade:** Checkpoints 1 e 2  
**Plataforma:** Raspberry Pi — Raspberry Pi OS  
**Integrantes:** [Inserir nomes e números USP]

## 1. Introdução

A Prática 5 tem como objetivo estudar a configuração e o gerenciamento de serviços personalizados em sistemas Linux embarcados, utilizando a ferramenta systemd na Raspberry Pi.

O projeto desenvolvido consiste no controle de um LED conectado à GPIO12 da Raspberry Pi, utilizando dois programas Python: um responsável pela modulação da intensidade luminosa por PWM e outro pelo acionamento intermitente do LED.

Também são abordados os conceitos de controle de versões com Git e documentação de projetos por meio do GitHub.

## 2. Objetivos

- Compreender o processo de inicialização de sistemas Linux embarcados.
- Implementar programas Python para controle de GPIO.
- Utilizar PWM para controlar a intensidade luminosa de um LED.
- Configurar serviços personalizados com systemd.
- Automatizar a execução de programas durante o boot.
- Utilizar Git para versionamento e GitHub para documentação e compartilhamento de códigos.

## 3. Fundamentação teórica

### 3.1 Systemd

O systemd é um sistema de inicialização e gerenciamento de serviços presente em diversas distribuições Linux.

Permite configurar programas para serem executados automaticamente durante a inicialização do sistema operacional, além de oferecer recursos para iniciar, interromper e monitorar processos.

### 3.2 Systemctl

O systemctl é a ferramenta utilizada para controlar serviços gerenciados pelo systemd.

Seus principais comandos são:

- `start`: inicia um serviço.
- `stop`: solicita a interrupção de um serviço.
- `status`: verifica seu estado.
- `enable`: habilita a inicialização automática.
- `disable`: desabilita a inicialização automática.
- `daemon-reload`: atualiza as configurações dos serviços.

### 3.3 PWM — Pulse Width Modulation

PWM é uma técnica de modulação por largura de pulso utilizada para controlar a potência média entregue a uma carga.

No projeto desenvolvido, o PWM é utilizado para variar a intensidade luminosa de um LED.

A biblioteca GPIO Zero permite definir a intensidade do LED por meio da propriedade `value`, que aceita valores entre 0 e 1.

- Valor 0: LED desligado.
- Valor 0,5: aproximadamente 50% de duty cycle.
- Valor 1: duty cycle de 100%.

### 3.4 Git e GitHub

O Git é um sistema distribuído de controle de versões utilizado para registrar alterações realizadas em arquivos de código.

O GitHub é uma plataforma de hospedagem de repositórios Git que permite compartilhar, organizar e documentar projetos de desenvolvimento.

## 4. Materiais utilizados

- Raspberry Pi com Raspberry Pi OS.
- Cartão microSD.
- LED.
- Resistor limitador de corrente.
- Protoboard e jumpers.
- Python 3.
- Biblioteca RPi.GPIO.
- Biblioteca GPIO Zero.
- Systemd.
- Git e GitHub.

## 5. Desenvolvimento

### 5.1 Montagem do circuito

O circuito utiliza um LED conectado à GPIO12 da Raspberry Pi (numeração BCM), correspondente ao pino físico 32.

O LED deve ser conectado com um resistor limitador de corrente em série, e seu terminal negativo conectado ao GND.

A GPIO12 é configurada como saída digital, permitindo controlar o LED por meio dos programas Python.

### 5.2 Programa blink_LED.py

O primeiro programa utiliza a biblioteca RPi.GPIO para controlar diretamente o estado lógico da GPIO12.

Inicialmente, configura-se a numeração BCM e define-se a GPIO12 como saída.

Em seguida, um laço infinito alterna o estado do pino entre nível alto e nível baixo, com intervalo de 1 segundo.

Dessa forma, o LED permanece ligado durante 1 segundo e desligado durante 1 segundo, repetidamente.

O programa permite demonstrar o controle digital de uma GPIO utilizando Python.

### 5.3 Programa LED_PWM.py

O segundo programa utiliza a biblioteca GPIO Zero, especificamente a classe PWMLED, para realizar o controle da intensidade luminosa do LED.

A GPIO12 é configurada como saída PWM.

Dentro de um laço infinito, a intensidade luminosa é incrementada de 0 até 1, em passos de 0,01, com intervalo de 0,01 segundo.

Esse funcionamento produz um aumento gradual do brilho do LED, até atingir sua intensidade máxima.

Após atingir o valor máximo, a intensidade retorna ao valor inicial, reiniciando o ciclo.

O programa demonstra uma aplicação prática de PWM para controle da intensidade luminosa.

### 5.4 Configuração do systemd

Para integrar a aplicação ao processo de inicialização do sistema operacional, foi criado o arquivo `blink.service`.

O arquivo contém três seções principais:

**[Unit]**

Define a descrição do serviço e suas dependências.

**[Service]**

Define os comandos de execução da aplicação.

Na configuração desenvolvida:

- `ExecStart` chama o interpretador Python para executar `LED_PWM.py`.
- `ExecStop` foi configurado para chamar `blink_LED.py`.
- `User` define o usuário responsável pela execução do serviço.

**[Install]**

Utiliza `WantedBy=multi-user.target` para permitir que o serviço seja habilitado durante a inicialização do sistema.

O projeto foi organizado no diretório `/home/sel/6190/` da Raspberry Pi, conforme os caminhos registrados no arquivo de serviço.

## 6. Gerenciamento do serviço

Os principais comandos utilizados para configurar e gerenciar o serviço são:

**Atualizar as configurações do systemd:**

`sudo systemctl daemon-reload`

**Iniciar o serviço:**

`sudo systemctl start blink.service`

**Verificar o estado:**

`systemctl status blink.service`

**Interromper o serviço:**

`sudo systemctl stop blink.service`

**Habilitar a inicialização automática:**

`sudo systemctl enable blink.service`

**Reiniciar a Raspberry Pi:**

`sudo reboot`

A inicialização automática deverá ser verificada observando o comportamento do LED após o boot e consultando o estado do serviço.

## 7. Controle de versões com Git

O projeto utiliza o Git para registrar as alterações realizadas nos programas e arquivos de configuração.

Os principais comandos para o versionamento são:

- `git clone`: clonar o repositório remoto.
- `git status`: verificar alterações locais.
- `git add`: adicionar arquivos ao próximo commit.
- `git commit`: registrar uma versão.
- `git push`: enviar alterações para o GitHub.
- `git pull`: obter atualizações do repositório remoto.
- `git log`: consultar o histórico de versões.

Para exportar o histórico de commits, utiliza-se:

`git log > historico_git.txt`

O arquivo gerado registra os commits existentes no repositório local.

## 8. Registros experimentais

### 8.1 Montagem prática

**Fotografia do circuito montado na Raspberry Pi:**

[A inserir após disponibilização da fotografia.]

### 8.2 Controle digital do LED

**Registro do funcionamento do programa blink_LED.py:**

[A inserir.]

### 8.3 Controle PWM

**Registro do funcionamento do programa LED_PWM.py:**

[A inserir.]

### 8.4 Inicialização automática

**Registro do serviço systemd inicializado durante o boot:**

[A inserir após validação.]

## 9. Resultados e discussão

Os programas desenvolvidos apresentam duas formas distintas de controle de um LED conectado à Raspberry Pi.

No programa `blink_LED.py`, a saída digital alterna entre os estados ligado e desligado, enquanto no programa `LED_PWM.py` a intensidade luminosa é modificada gradualmente por meio da modulação PWM.

A configuração do serviço systemd permite integrar o programa Python ao gerenciamento de processos do sistema operacional.

O funcionamento efetivo da inicialização automática deverá ser confirmado durante os testes práticos, após a habilitação do serviço e a reinicialização da Raspberry Pi.

O Git e o GitHub permitem documentar as diferentes etapas do desenvolvimento, preservando o histórico de alterações realizadas.

## 10. Conclusão

A Prática 5 permite aplicar conceitos de programação embarcada em Linux, controle de GPIO, modulação PWM e gerenciamento de serviços com systemd.

Os programas desenvolvidos demonstram diferentes possibilidades de acionamento de um LED, utilizando as bibliotecas RPi.GPIO e GPIO Zero.

A configuração do systemd estabelece a estrutura necessária para executar aplicações Python automaticamente durante o processo de inicialização do sistema.

O uso de Git e GitHub complementa a atividade, proporcionando controle de versões, organização e documentação do projeto.

A conclusão experimental dependerá da validação do serviço na Raspberry Pi e da inclusão dos registros de funcionamento.

## 11. Referências

- USP — SEL0337: Projetos em Sistemas Embarcados. Prática 5: Configuração do SystemD, Git e GitHub.
- Raspberry Pi Documentation: https://www.raspberrypi.com/documentation/
- GPIO Zero: https://gpiozero.readthedocs.io/
- Systemd: https://systemd.io/
- Git Documentation: https://git-scm.com/doc
- GitHub Docs: https://docs.github.com/
