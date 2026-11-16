# Instalação no desktop da bancada (Ubuntu 24.04)

**Projeto final — Laboratório de Controle Automático — Ifes Guarapari**

## Por que não no Google Colab?

Até agora os notebooks rodavam no Colab, que executa o Python **num servidor do Google**. Nos
roteiros do projeto, o notebook conversa com o Arduino pela **porta USB do computador da
bancada** — e o servidor do Colab não enxerga essa porta. Por isso, **o projeto final roda no
próprio desktop da bancada**, com o Jupyter instalado nele. (Os laboratórios de teoria dos módulos
continuam funcionando no Colab.)

O professor normalmente já deixa os computadores prontos. Se o seu não estiver, siga a Seção 1
(automática) **ou** a Seção 2 (passo a passo). Depois, a Seção 3 diz como abrir os roteiros todo
dia.

---

## 1. Instalação automática (recomendada) · ≈ 10 min

Abra um **Terminal** (Ctrl+Alt+T) e digite:

```bash
git clone https://github.com/fabiobento/lab-cont-2026-2.git
cd lab-cont-2026-2
bash projeto_final/instalar_ubuntu.sh
```

O script pede a senha de administrador e faz tudo o que está na Seção 2. No fim, **saia da sessão
e entre de novo** (ou reinicie): é isso que faz a permissão da porta serial valer.

## 2. Instalação passo a passo (o que o script faz)

**2.1 Pacotes do sistema**
```bash
sudo apt update
sudo apt install -y python3-venv python3-pip git curl
```

**2.2 Remover o `brltty`** — é um programa para terminais braille que vem no Ubuntu e "captura"
o conversor USB-serial **CH340** usado nas placas Arduino clone: a porta `/dev/ttyUSB0` aparece e
some em seguida. Se ninguém no laboratório usa display braille:
```bash
sudo apt remove -y brltty
```

**2.3 Permissão para usar a porta serial** — no Ubuntu, só quem está no grupo `dialout` pode
abrir `/dev/ttyUSB0`:
```bash
sudo usermod -aG dialout $USER
```
⚠️ Vale só depois de **sair da sessão e entrar de novo**.

**2.4 Ambiente Python do curso** — o Ubuntu 24.04 não deixa instalar bibliotecas com `pip` no
Python do sistema (erro *externally-managed-environment*); por isso criamos um **ambiente
virtual** só para o curso:
```bash
python3 -m venv ~/venv-controle
~/venv-controle/bin/pip install --upgrade pip
~/venv-controle/bin/pip install "control==0.10.2" numpy scipy matplotlib jupyter jupyterlab pyserial
echo "alias controle='source ~/venv-controle/bin/activate'" >> ~/.bashrc
```

**2.5 Gravador do Arduino (`arduino-cli`)** — no Ubuntu 24.04 a Arduino IDE 2 (AppImage) costuma
exigir ajustes (`libfuse2t64`, `--no-sandbox`). O `arduino-cli` grava pelo terminal e não tem
esses problemas:
```bash
mkdir -p ~/.local/bin
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR=~/.local/bin sh
~/.local/bin/arduino-cli core update-index
~/.local/bin/arduino-cli core install arduino:avr
~/.local/bin/arduino-cli lib install "Adafruit SSD1306"
```
(Quem preferir a Arduino IDE pode usá-la: abra `firmware/pid_motor/pid_motor.ino`, placa
**Arduino Uno**, porta `/dev/ttyUSB0`, instale a biblioteca *Adafruit SSD1306* e clique em
Carregar.)

**2.6 JupyterLab com senha fixa** — sem senha, o Jupyter cria a cada vez uma chave temporária
(*token*) e a página pede **"Password or token"** quando o navegador não a recebe. Com uma senha
fixa, o endereço é sempre `http://localhost:8888/lab` e basta digitar a senha.
```bash
controle                                   # ativa o ambiente Python
mkdir -p ~/.jupyter
cat > ~/.jupyter/jupyter_server_config.py <<'EOF'
c.ServerApp.ip = "localhost"
c.ServerApp.use_redirect_file = False
EOF
jupyter server password                    # digite a senha da bancada duas vezes
```
- `ip = "localhost"`: só o próprio computador acessa o Jupyter (ninguém da rede).
- `jupyter server password` grava a senha (criptografada) em
  `~/.jupyter/jupyter_server_config.json`. **Esqueceu a senha?** Rode o comando de novo e escolha
  outra.

E um atalho que faz tudo de uma vez (ativa o ambiente, entra na pasta e abre o JupyterLab):
```bash
sed -i '/^alias projeto=/d' ~/.bashrc
echo "alias projeto='source ~/venv-controle/bin/activate && cd ~/lab-cont-2026-2/projeto_final && jupyter lab'" >> ~/.bashrc
```
(Ajuste o caminho `~/lab-cont-2026-2` se o repositório estiver em outro lugar. Vale para os
próximos Terminais que abrir.)

## 3. Todo dia, para trabalhar

Num Terminal, digite apenas:

```bash
projeto
```

(É o mesmo que `cd ~/lab-cont-2026-2/projeto_final`, depois `controle` — que ativa o ambiente
Python — e depois `jupyter lab`.) O navegador abre o **JupyterLab**: digite a **senha do
Jupyter** da bancada. À esquerda fica a lista de arquivos; dê dois cliques no roteiro
da aula (`aula1_….ipynb` etc.). **Não feche o Terminal** enquanto estiver
usando o notebook. Para gravar o firmware (Aula 1), abra **outra aba** do Terminal
(Ctrl+Shift+T), vá para a mesma pasta e rode:

```bash
bash gravar_firmware.sh
```

**Qual é a porta?** Placas clone com CH340: `/dev/ttyUSB0`. Arduino Uno original:
`/dev/ttyACM0`. A primeira célula de cada roteiro lista as portas encontradas.

## 4. Se algo der errado

| Sintoma | Causa | Solução |
|---|---|---|
| `Permission denied: '/dev/ttyUSB0'` | usuário fora do grupo `dialout`, ou não saiu da sessão depois de entrar nele | 2.3 e sair/entrar da sessão |
| a porta aparece e some; `ls /dev/ttyUSB*` vazio | `brltty` capturou o CH340 | 2.2 e desconectar/reconectar o USB |
| `error: externally-managed-environment` | `pip` usado fora do ambiente virtual | `controle` antes do `pip`, ou use `~/venv-controle/bin/pip` |
| a página pede **"Password or token"** | a senha fixa não foi definida (o Jupyter usa uma chave temporária) | **na hora:** no Terminal do Jupyter, Ctrl+clique no endereço `http://localhost:8888/lab?token=…`. **De vez:** 2.6, `pkill -f jupyter` e `projeto` |
| a senha do Jupyter não é aceita / foi esquecida | — | `controle`, depois `jupyter server password` (escolha outra), `pkill -f jupyter` e `projeto` |
| `ModuleNotFoundError: No module named 'control'` no notebook | Jupyter aberto sem ativar o ambiente | feche, rode `projeto` (ou `controle` e depois `jupyter lab`) |
| `ModuleNotFoundError: ferramentas_projeto` | notebook aberto fora da pasta `projeto_final/` | abra o Jupyter de dentro de `projeto_final/` |
| `projeto: comando não encontrado` | atalho ainda não criado, ou Terminal aberto antes de criá-lo | 2.6, depois feche e abra o Terminal |
| `arduino-cli: comando não encontrado` | `~/.local/bin` ainda não está no PATH | saia da sessão e entre de novo, ou use `~/.local/bin/arduino-cli` |
| `coletar()` diz que o Arduino não respondeu | firmware antigo; porta errada; outro programa usando a porta | `bash gravar_firmware.sh`; confira `PORTA`; feche a Arduino IDE / Monitor Serial |
| gravou ("Carregado"), mas o display não mostra **PRONTO** | firmware antigo, que deixava pouca RAM para o display (a IDE dizia "deixando 1065 bytes") | baixe o `pid_motor.ino` atualizado e grave de novo: a IDE deve dizer "deixando ≈ 1320 bytes". O aviso sobre `platform.txt` da Arduino IDE do Ubuntu pode ser ignorado |
| erro `Adafruit_SSD1306.h: No such file` ao gravar | biblioteca não instalada | 2.5 (`lib install`) ou `#define USAR_OLED 0` no `pid_motor.ino` |
