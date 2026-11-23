# SEL0337 — Prática 5: Systemd, Git e GitHub

**Disciplina:** SEL0337 — Projetos em Sistemas Embarcados  
**Atividade:** Checkpoint 1 (serviço systemd) e Checkpoint 2 (Git/GitHub)  
**Plataforma:** Raspberry Pi com Raspberry Pi OS  
**Repositório:** [loredogu1/Microprocessadores](https://github.com/loredogu1/Microprocessadores)

> **Estado da validação:** os programas e a configuração do serviço estão disponíveis neste repositório. A comprovação do funcionamento real no boot e as fotografias precisam ser adicionadas depois dos testes na Raspberry Pi. Não são apresentados testes como concluídos sem a respectiva evidência.

## 1. Introdução e objetivos

O projeto demonstra o controle de um LED ligado ao **GPIO 12** da Raspberry Pi por meio de dois programas Python: `blink_LED.py` (acionamento digital periódico) e `LED_PWM.py` (controle gradual de intensidade luminosa usando PWM). O `systemd` executa automaticamente o programa PWM durante o boot. O Git e o GitHub registram versões do código e centralizam a documentação.

Objetivos: controlar GPIO usando Python; compreender PWM e duty cycle; configurar um arquivo `.service` com `ExecStart` e `ExecStop`; testar os comandos do `systemctl`; registrar alterações com Git e documentá-las no GitHub.

## 2. Conceitos utilizados

- **Boot e init system:** após o carregamento do kernel Linux e a montagem do sistema de arquivos, um gerenciador de inicialização como `systemd` inicia os serviços configurados.
- **systemd:** gerenciador de unidades (units) que permite iniciar, interromper e supervisionar aplicações.
- **systemctl:** ferramenta para `start`, `stop`, `status`, `enable`, `disable` e `daemon-reload`.
- **GPIO:** pinos de entrada e saída digitais da Raspberry Pi, controlados por software.
- **PWM (Pulse Width Modulation):** varia a razão cíclica (duty cycle) do sinal; valores `0`, `0.5` e `1` na propriedade `PWMLED.value` correspondem a 0%, 50% e 100% de duty cycle.
- **Git/GitHub:** ferramentas de versionamento local e publicação/documentação do repositório.

## 3. Materiais e montagem

- Raspberry Pi com Raspberry Pi OS, cartão microSD e Python 3;
- LED, protoboard, jumpers e **resistor limitador de corrente em série** (por exemplo, 330 Ω para um LED vermelho típico em 3,3 V);
- Bibliotecas `gpiozero` e `RPi.GPIO` (esta última utilizada no exemplo de acionamento digital).

**Ligação:** GPIO12 (numeração BCM, **pino físico 32**) → resistor em série → ânodo do LED; cátodo do LED → GND da Raspberry Pi (por exemplo, pino físico 34). Não ligar o LED diretamente ao GPIO sem resistor.

> Somente um dos programas deve controlar o GPIO12 por vez. Para testar `blink_LED.py`, interrompa antes o serviço PWM.

## 4. Arquivos do projeto

```text
Microprocessadores/
├── README.md
├── LICENSE                   # já existente no repositório remoto
├── blink_LED.py              # LED liga/desliga a cada 1 s
├── LED_PWM.py                # brilho sobe e desce por PWM
├── parar_led.py              # encerramento solicitado por ExecStop
├── blink.service             # arquivo de configuração do systemd
├── instalar_servico.sh       # instala o serviço com o usuário/caminho locais
├── gerar_historico.sh        # exporta o histórico Git real
├── .gitignore
└── imagens/                  # evidências fotográficas, após testes
```

### 4.1. `blink_LED.py`

Configura o pino 12 como saída usando `RPi.GPIO`. Em um laço, liga o LED por 1 segundo e o desliga por 1 segundo. Ao receber interrupção, deixa o pino em nível baixo e libera a GPIO com `cleanup`.

### 4.2. `LED_PWM.py`

Cria um `PWMLED(12)` com a biblioteca GPIO Zero. O duty cycle aumenta de 0% a 100%, em passos de 1%, e diminui de 99% a 0%, com 10 ms entre passos. A transição é repetida enquanto o serviço estiver ativo. Um tratador de `SIGTERM` permite apagar o LED e liberar a GPIO no encerramento.

### 4.3. `blink.service` e `parar_led.py`

O arquivo de unidade possui três seções:

- `[Unit]`: descrição e ordenação do serviço;
- `[Service]`: programa Python chamado por `ExecStart`, programa auxiliar `parar_led.py` chamado por `ExecStop`, usuário e diretório de trabalho;
- `[Install]`: `WantedBy=multi-user.target`, permitindo habilitar a inicialização automática.

`ExecStop` **não** chama `blink_LED.py`, pois ele entra em um laço contínuo. Em vez disso, chama `parar_led.py`, que envia `SIGTERM` ao processo principal e espera seu encerramento. O próprio `LED_PWM.py` desliga o LED no bloco `finally`.

O `blink.service` versionado usa o caminho de referência `/home/sel/6190` e o usuário `sel`, conforme os arquivos originais da prática. O script `instalar_servico.sh` substitui esses valores **na unidade instalada** pelos valores reais do usuário e da pasta do projeto, sem modificar o arquivo do Git.

## 5. Instalação na Raspberry Pi (Checkpoint 1)

Em um terminal da Raspberry Pi, com o repositório clonado, execute:

```bash
sudo apt update
sudo apt install -y python3-gpiozero python3-rpi.gpio git
cd ~/Microprocessadores
bash instalar_servico.sh
```

O instalador solicita `sudo`, copia o arquivo `.service` adaptado para `/etc/systemd/system/`, recarrega o `systemd`, habilita o serviço e o reinicia. Para conferir os resultados:

```bash
systemctl status blink.service
systemctl is-enabled blink.service
sudo systemctl stop blink.service
sudo systemctl start blink.service
sudo reboot
```

**Teste de boot:** após reiniciar a Raspberry Pi, conferir visualmente o brilho variando e executar `systemctl status blink.service` para registrar o estado `active (running)`. Não basta que o serviço tenha sido habilitado; é necessário verificar a inicialização real.

**Para testar o blink digital separadamente:**

```bash
sudo systemctl stop blink.service
python3 blink_LED.py
# Encerrar com Ctrl+C; depois:
sudo systemctl start blink.service
```

Para investigar falhas:

```bash
journalctl -u blink.service -b --no-pager
sudo systemctl daemon-reload
```

Caso o usuário ou diretório seja alterado, executar novamente `bash instalar_servico.sh` para reinstalar o serviço atualizado.

> Dependendo do modelo da Raspberry Pi e da versão do Raspberry Pi OS, as bibliotecas de GPIO podem diferir. Se o teste de importação ou o acesso ao GPIO falhar, verificar a compatibilidade das bibliotecas antes de atribuir o erro ao `systemd`.

## 6. Controle de versões (Checkpoint 2)

No terminal da Raspberry Pi, após clonar o repositório:

```bash
git clone https://github.com/loredogu1/Microprocessadores.git
cd Microprocessadores
git status
git add README.md blink_LED.py LED_PWM.py parar_led.py blink.service instalar_servico.sh gerar_historico.sh .gitignore imagens/
git commit -m "Conclui estrutura da Pratica 5: Python, systemd e documentacao"
git push origin main
```

Se os arquivos foram enviados pelo site do GitHub, fazer `git pull` na Raspberry Pi antes de criar novos commits locais.

Para gerar o arquivo exigido pelo roteiro, **na Raspberry Pi e dentro do clone do repositório**, executar:

```bash
bash gerar_historico.sh
# Equivalente a: git log > historico_git.txt
```

Esse arquivo deve conter o histórico **real** de commits (não deve ser inventado). Após gerá-lo, o arquivo `historico_git.txt` pode ser adicionado ao repositório e enviado em um commit posterior.

## 7. Registros experimentais a incluir (Checkpoint 2)

Os itens abaixo devem ser substituídos por fotos e prints **reais** dos ensaios:

- **Fotografia da montagem:** inserir `imagens/montagem.jpg` e depois incluir no README `![Montagem real](imagens/montagem.jpg)`.
- **Controle digital:** registrar `blink_LED.py` funcionando, se possível em foto ou vídeo.
- **Controle PWM:** registrar o LED variando o brilho.
- **Serviço durante o boot:** inserir `imagens/status-boot.png` com print de `systemctl status blink.service` depois da reinicialização.
- **Vídeo da inicialização:** se a atividade for realizada antecipadamente/fora do horário de aula, o roteiro pede vídeo curto mostrando o funcionamento desde o boot, substituindo a demonstração em sala.

**Ainda não há fotos ou prints reais incluídos nesta versão.** A pasta `imagens/` contém apenas um marcador para preservá-la no Git.

## 8. Resultados e discussão

Pelo código, `blink_LED.py` implementa acionamento digital com período de 2 segundos, enquanto `LED_PWM.py` implementa modulação do brilho com aproximadamente 2 segundos por ciclo de subida e descida. O serviço `blink.service` contém a configuração necessária para iniciar automaticamente o PWM na inicialização e chamar um programa de parada no `ExecStop`.

**Resultado experimental pendente:** a operação em hardware, o encerramento sem erros e a inicialização real após reboot precisam ser comprovados por fotos/prints e demonstração na Raspberry Pi.

## 9. Conclusão

A atividade reúne acionamento de GPIO, controle PWM, programação em Python, gerenciamento de serviços com `systemd` e versionamento com Git/GitHub. Os arquivos fornecem uma implementação preparada para execução e testes. A confirmação dos objetivos práticos depende da validação física e da documentação das evidências no repositório.

## 10. Referências

- USP. **SEL0337 — Projetos em Sistemas Embarcados.** Prática 5: Configuração do SystemD, Controle de Versão e GitHub (roteiro da disciplina).
- [Documentação da Raspberry Pi](https://www.raspberrypi.com/documentation/)
- [GPIO Zero — documentação](https://gpiozero.readthedocs.io/)
- [systemd — documentação](https://systemd.io/)
- [Git — documentação](https://git-scm.com/doc)
