# SEL0337 — Prática 5: Systemd, Git e GitHub

**Disciplina:** SEL0337 — Projetos em Sistemas Embarcados  
**Atividade:** Checkpoints 1 e 2  
**Plataforma:** Raspberry Pi com Raspberry Pi OS  
**Alunos:** Guilherme Pereira Loredo e Pedro Calarge Jankauskis

## 1. Introdução

A Prática 5 aborda a execução de aplicações durante a inicialização de um sistema Linux embarcado, utilizando o gerenciador de serviços **systemd**. Para demonstrar esse funcionamento, o projeto controla um LED conectado à Raspberry Pi por meio de programas em Python.

Foram utilizados dois exemplos: `blink_LED.py`, que alterna os estados ligado/desligado do LED, e `LED_PWM.py`, que varia gradualmente sua intensidade luminosa. O serviço `blink.service` foi configurado para executar **`LED_PWM.py`** durante o boot. O controle de versões e a documentação são realizados com Git e GitHub.

## 2. Objetivos

- Controlar uma saída GPIO da Raspberry Pi utilizando Python.
- Demonstrar o acionamento digital e a modulação por largura de pulso (**PWM**).
- Criar uma unidade `.service` com `ExecStart` e `ExecStop` para gerenciar a aplicação.
- Habilitar a aplicação para execução automática no boot do Raspberry Pi OS.
- Registrar o desenvolvimento com Git e documentar os programas e a montagem no GitHub.

## 3. Fundamentação teórica

### 3.1 Inicialização do Linux e systemd

Após o carregamento do kernel Linux e a montagem do sistema de arquivos, o sistema de inicialização gerencia os processos necessários ao sistema operacional. No Raspberry Pi OS, o **systemd** permite cadastrar serviços personalizados em arquivos `.service`, definindo qual programa executar, em qual usuário e em que etapa da inicialização.

Uma unidade de serviço contém seções como `[Unit]` (descrição e dependências), `[Service]` (comandos e condições de execução) e `[Install]` (habilitação do serviço no processo de inicialização).

### 3.2 GPIO e PWM

Uma GPIO pode atuar como saída digital, assumindo níveis lógicos alto e baixo. Neste projeto, isso é usado para acender e apagar o LED.

Com **PWM (Pulse Width Modulation)**, a saída alterna rapidamente entre esses níveis e o ciclo de trabalho (*duty cycle*) determina a fração do período em nível alto. Por meio da classe `PWMLED` da biblioteca GPIO Zero, a propriedade `value` varia de **0** (apagado) até **1** (ciclo de trabalho de 100%). Isso permite controlar o brilho médio percebido do LED.

### 3.3 Git e GitHub

O **Git** registra versões dos arquivos do projeto. O **GitHub** hospeda o repositório com os códigos, a documentação e as evidências fotográficas, conforme solicitado no Checkpoint 2.

## 4. Materiais utilizados

- Raspberry Pi com Raspberry Pi OS e Python 3.
- LED vermelho e resistor limitador de corrente.
- Protoboard e fios de conexão (*jumpers*).
- Bibliotecas Python `RPi.GPIO` e `gpiozero`.
- Gerenciador `systemd` e ferramentas Git/GitHub.

## 5. Desenvolvimento

### 5.1 Montagem do circuito

Os programas utilizam a **GPIO12** (numeração BCM, pino físico **32** da Raspberry Pi). O LED é acionado por essa saída através de um resistor limitador de corrente e possui retorno ao GND da placa.

O código de acionamento digital e o código PWM atuam sobre **o mesmo pino**. Por isso, devem ser testados separadamente, nunca simultaneamente.

A fotografia da montagem é apresentada na **Seção 8.1**.

### 5.2 Programa `blink_LED.py` — acionamento digital

O arquivo [`blink_LED.py`](blink_LED.py) utiliza `RPi.GPIO`. Inicialmente, `GPIO.setmode(GPIO.BCM)` seleciona a numeração BCM e `GPIO.setup(12, GPIO.OUT)` configura a GPIO12 como saída. O laço alterna os níveis alto e baixo, mantendo o LED **aceso por 1 segundo e apagado por 1 segundo**. Foi acrescentado tratamento para desligar o LED e liberar o pino quando o programa é encerrado.

Trecho central do código:

```python
while True:
    GPIO.output(PINO_LED, True)   # Liga o LED
    sleep(1)
    GPIO.output(PINO_LED, False)  # Desliga o LED
    sleep(1)
```

Esse arquivo é um exemplo independente e **não** é o processo executado automaticamente pelo serviço.

### 5.3 Programa `LED_PWM.py` — controle de intensidade

O arquivo [`LED_PWM.py`](LED_PWM.py) utiliza `PWMLED` da biblioteca `gpiozero` para controlar o brilho do LED na GPIO12. O programa percorre os valores de **0 a 100**, atribuindo `b/100` à saída PWM a cada **0,01 segundo**. O brilho aumenta gradualmente até o máximo e, ao terminar o ciclo, retorna a zero para iniciar outra subida. Esse comportamento corresponde ao código original desenvolvido para a prática.

Trecho central do código:

```python
while executando:
    for brilho in range(101):
        if not executando:
            break
        led.value = brilho / 100
        sleep(0.01)
```

O programa inclui tratamento do sinal `SIGTERM` para encerrar o laço e desligar o LED com `led.off()` e `led.close()` ao interromper o serviço.

### 5.4 Programa `parar_led.py` — ação de parada

O roteiro exige que o `ExecStop` de `blink.service` chame um programa quando o serviço for interrompido. O arquivo [`parar_led.py`](parar_led.py) recebe o identificador do processo Python (`$MAINPID`) e envia um sinal `SIGTERM`. O próprio `LED_PWM.py` trata esse sinal, desliga o LED e libera a GPIO.

Essa separação é necessária porque **`blink_LED.py` possui um laço contínuo** e, portanto, não é adequado como rotina de encerramento do serviço.

### 5.5 Arquivo `blink.service` — inicialização automática

O arquivo [`blink.service`](blink.service) registra o programa PWM como serviço do systemd. A configuração utilizada é:

```ini
[Unit]
Description=Blink LED - Controle PWM (SEL0337)
After=local-fs.target

[Service]
Type=simple
User=sel
WorkingDirectory=/home/sel/6190
ExecStart=/usr/bin/python3 /home/sel/6190/LED_PWM.py
ExecStop=/usr/bin/python3 /home/sel/6190/parar_led.py $MAINPID
TimeoutStopSec=10

[Install]
WantedBy=multi-user.target
```

- **`ExecStart`** executa o programa `LED_PWM.py` com Python 3.
- **`ExecStop`** chama `parar_led.py` para solicitar o encerramento da aplicação.
- **`User` e `WorkingDirectory`** definem, respectivamente, o usuário `sel` e o diretório `/home/sel/6190` observados na Raspberry Pi.
- **`WantedBy=multi-user.target`** permite habilitar o serviço na inicialização do sistema.

## 6. Gerenciamento e verificação do serviço

Para o systemd reconhecer a unidade, o arquivo `blink.service` deve estar instalado em `/etc/systemd/system/`. Os comandos relacionados à atividade são:

```bash
sudo cp /home/sel/6190/blink.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable blink.service
sudo systemctl start blink.service
systemctl status blink.service
```

O comando `start` inicia o programa PWM e `status` permite consultar o estado do serviço. Para verificar a rotina de parada, utiliza-se:

```bash
sudo systemctl stop blink.service
```

Após habilitar a unidade, o teste pedido no Checkpoint 1 consiste em reiniciar a Raspberry Pi e verificar se o LED passa a ser controlado automaticamente **sem executar o script Python manualmente**. As fotografias apresentadas neste README não incluem o resultado do `systemctl status` após o boot, portanto **essa comprovação ainda precisa ser registrada**.

## 7. Controle de versões com Git

O Git foi utilizado como ferramenta de versionamento do projeto, e o GitHub foi escolhido para disponibilizar os programas Python, o serviço systemd e a documentação solicitada na Prática 5. O histórico de commits deve ser exportado **no repositório local da Raspberry Pi** para o arquivo `historico_git.txt`, conforme o roteiro. Esse histórico precisa refletir os commits reais; não é substituído por um texto produzido manualmente.

## 8. Registros experimentais

### 8.1 Montagem prática

![LED vermelho aceso na montagem prática](imagens/01_montagem_raspberry_led.jpg)

*Figura 1 — Montagem do circuito com LED aceso, resistor limitador, protoboard e Raspberry Pi.*

### 8.2 Organização dos arquivos e edição da unidade

![Terminal mostrando arquivos do projeto e arquivo de serviço aberto no editor](imagens/02_arquivos_e_servico.jpg)

*Figura 2 — Terminal do Raspberry Pi OS mostrando a pasta de trabalho `/home/sel/6190` e a edição do arquivo de serviço no GNU nano.*

### 8.3 Inicialização no boot

A documentação do Checkpoint 1 requer confirmar que o programa inicia automaticamente com a Raspberry Pi. Para concluir a evidência, ainda é necessário registrar o resultado real de `systemctl status blink.service` após reiniciar a placa e, se a prática for realizada fora do horário de aula, apresentar o vídeo curto solicitado pelo roteiro.

## 9. Resultados e discussão

A montagem fotografada apresenta o LED vermelho aceso na protoboard conectada à Raspberry Pi, evidenciando um estado de acionamento da saída. Também foi documentada a presença de arquivos de trabalho e a edição de uma unidade de serviço no sistema operacional.

Os códigos fornecidos permitem comparar dois métodos de controle: a alternância digital, com intervalos de 1 segundo, e a variação progressiva do ciclo de trabalho PWM, com atualizações de 0,01 segundo. O arquivo `blink.service` fornece a configuração para integrar o programa PWM à inicialização do sistema e interrompê-lo por meio do `ExecStop`.

As fotografias **não permitem confirmar**, isoladamente, a variação temporal do brilho nem a inicialização automática do serviço após o boot. Esses testes devem ser documentados separadamente para completar a validação experimental.

## 10. Conclusão

O projeto reúne programação Python, acionamento de GPIO, controle PWM e configuração de um serviço personalizado no Linux embarcado. Os programas `blink_LED.py` e `LED_PWM.py` implementam diferentes comportamentos de um LED, enquanto `blink.service` define a execução automática da aplicação PWM e sua rotina de parada.

O repositório organiza o código e os registros fotográficos pedidos nos Checkpoints 1 e 2. A comprovação final da inicialização automática depende do teste do serviço durante o boot da Raspberry Pi e do registro do histórico real de commits.

## 11. Referências

- USP — SEL0337, *Prática 5: Configuração do SystemD para Personalização de Serviços de Inicialização de S.O. em Linux Embarcado, Controle de Versão e Repositório de Códigos com Git e GitHub*. Roteiro da disciplina.
- [Documentação da Raspberry Pi](https://www.raspberrypi.com/documentation/).
- [Documentação da biblioteca GPIO Zero](https://gpiozero.readthedocs.io/).
- [Documentação do systemd](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html).
- [Documentação do Git](https://git-scm.com/doc).
