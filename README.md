# Microprocessadores

SEL0337 — Prática 5: Systemd, Git e GitHub

Disciplina: SEL0337 — Projetos em Sistemas Embarcados
Atividade: Checkpoint 1 e Checkpoint 2
Plataforma: Raspberry Pi — Raspberry Pi OS
Integrantes: Guilherme Pereira Loredo nusp - 11885190; Pedro Calarge nusp -

1. Introdução

Esta prática tem como objetivo compreender o funcionamento do sistema de inicialização de sistemas Linux embarcados, utilizando o systemd para configurar e gerenciar serviços personalizados na Raspberry Pi.

Também é utilizado o Git para controle de versões e o GitHub para armazenamento, documentação e compartilhamento dos códigos desenvolvidos.

O projeto proposto consiste em controlar um LED conectado à GPIO18 da Raspberry Pi por meio de um programa Python, configurando sua execução automática durante a inicialização do sistema operacional.

2. Objetivos

- Compreender o processo de boot de um sistema Linux embarcado.
- Configurar um serviço personalizado utilizando systemd.
- Executar automaticamente um programa Python durante a inicialização da Raspberry Pi.
- Implementar comandos de inicialização e encerramento do serviço.
- Utilizar Git para controle de versões.
- Documentar o projeto em um repositório GitHub.

3. Fundamentação teórica

3.1 Systemd

O systemd é um sistema de inicialização e gerenciamento de serviços utilizado em diversas distribuições Linux.

Sua função é controlar os processos e serviços necessários para o funcionamento do sistema operacional, permitindo que aplicações sejam inicializadas automaticamente durante o boot.

3.2 Systemctl

O systemctl é a ferramenta utilizada para controlar os serviços gerenciados pelo systemd.

Entre suas principais funcionalidades estão iniciar, parar, reiniciar, habilitar e verificar o estado de um serviço.

3.3 Unit File

Um unit file é um arquivo de configuração utilizado pelo systemd para definir o comportamento de determinado serviço.

Arquivos de serviço possuem a extensão ".service" e são divididos em três seções principais:

- [Unit]: contém a descrição e as dependências do serviço.
- [Service]: define os programas executados durante a inicialização e o encerramento.
- [Install]: determina como o serviço será habilitado para iniciar automaticamente.

3.4 Git e GitHub

O Git é um sistema de controle de versões que permite registrar e acompanhar alterações realizadas nos arquivos de um projeto.

O GitHub é uma plataforma utilizada para hospedar repositórios Git, facilitando o compartilhamento de códigos, a documentação e o desenvolvimento colaborativo.

4. Materiais utilizados

- Raspberry Pi
- Protoboard
- LED
- Resistor de 470 Ω
- Jumpers

5. Desenvolvimento do projeto

5.1 Montagem do circuito

O circuito proposto utiliza um LED conectado à GPIO18 da Raspberry Pi, com um resistor em série para limitar a corrente elétrica.

As conexões são:

- GPIO18 (pino físico 12) → resistor → ânodo do LED.
- Cátodo do LED → GND (pino físico 6).

O LED será controlado digitalmente pelo programa Python, alternando entre os estados ligado e desligado.

5.2 Programa Python

O programa "blink.py" utiliza a biblioteca GPIO Zero para controlar a GPIO18 da Raspberry Pi.

Seu funcionamento é baseado em um laço de repetição que liga o LED durante 0,2 segundo e o desliga durante 0,2 segundo.

O programa permanece em execução enquanto o serviço estiver ativo.

Ao receber um sinal de encerramento, o programa desliga o LED e libera os recursos utilizados.

5.3 Configuração do serviço

Foi preparado um arquivo chamado "blink.service", responsável por definir o comportamento da aplicação no systemd.

A configuração estabelece:

- ExecStart: execução do programa Python responsável pelo controle do LED.
- ExecStop: execução do programa auxiliar de encerramento.
- WantedBy: associação ao "multi-user.target", permitindo habilitar a inicialização automática.

5.4 Comandos utilizados

Para iniciar o serviço:

"sudo systemctl start blink.service"

Para verificar seu estado:

"systemctl status blink.service"

Para interromper sua execução:

"sudo systemctl stop blink.service"

Para habilitar sua inicialização automática:

"sudo systemctl enable blink.service"

Para reiniciar a Raspberry Pi e verificar o funcionamento no boot:

"sudo reboot"

Após reiniciar, o estado do serviço poderá ser verificado novamente por meio do comando "systemctl status".

6. Controle de versões

O controle de versões do projeto é realizado utilizando Git, com armazenamento remoto no GitHub.

Os principais comandos utilizados são:

- "git clone" — copiar o repositório remoto.
- "git add" — selecionar arquivos para o próximo commit.
- "git commit" — registrar as alterações realizadas.
- "git push" — enviar alterações ao repositório remoto.
- "git pull" — atualizar o repositório local.
- "git log" — visualizar o histórico de alterações.

O histórico de commits será exportado da Raspberry Pi para o arquivo "historico_git.txt", utilizando:

"git log > historico_git.txt"

Esse arquivo será utilizado para documentar o processo de versionamento desenvolvido durante a atividade.

7. Registros da montagem e funcionamento

7.1 Montagem prática

Fotografia da montagem: a inserir após a realização do experimento.

7.2 Funcionamento do programa

Fotografia ou captura de tela do programa em execução: a inserir após a realização dos testes.

7.3 Inicialização automática

Será verificado se o serviço é inicializado corretamente durante o boot da Raspberry Pi, sem necessidade de executar manualmente o programa Python.

Resultado do teste: pendente de validação na Raspberry Pi.

8. Resultados e discussão

A implementação proposta permite estudar a integração entre aplicações Python e o gerenciador de serviços systemd.

A utilização de um serviço personalizado possibilita automatizar a execução de aplicações em sistemas embarcados, eliminando a necessidade de inicialização manual após ligar o equipamento.

Os testes práticos deverão confirmar o funcionamento do LED, os comandos de gerenciamento do serviço e a inicialização automática durante o boot.

Os resultados experimentais serão documentados nesta seção após a execução na Raspberry Pi.

9. Conclusão

A Prática 5 permite estudar conceitos relacionados à inicialização de sistemas Linux embarcados, gerenciamento de serviços e controle de versões.

A configuração do systemd demonstra como uma aplicação pode ser integrada ao processo de inicialização do sistema operacional.

A utilização do Git e GitHub complementa o desenvolvimento, permitindo registrar alterações, compartilhar códigos e manter a documentação organizada.

A validação final do projeto dependerá dos testes de funcionamento na Raspberry Pi e do registro das evidências experimentais.

10. Referências

- USP — SEL0337: Projetos em Sistemas Embarcados. Prática 5: Configuração do SystemD, Git e GitHub.
- Systemd — Documentação oficial: https://systemd.io/
- Raspberry Pi — Documentação oficial: https://www.raspberrypi.com/documentation/
- Git — Documentação oficial: https://git-scm.com/doc
- GitHub Docs: https://docs.github.com/