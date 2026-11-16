#!/usr/bin/env bash
# =============================================================================
# instalar_ubuntu.sh — prepara um desktop Ubuntu 24.04 para o projeto final
# Laboratório de Controle Automático — Ifes Guarapari
#
# Uso (no terminal, dentro da pasta do repositório):
#     bash projeto_final/instalar_ubuntu.sh
#
# O que faz (detalhes e versão manual em projeto_final/INSTALACAO_UBUNTU.md):
#   1. pacotes do sistema (venv do Python, git, curl)
#   2. remove o brltty, que "sequestra" o conversor USB-serial CH340 das placas clone
#   3. dá ao usuário permissão de usar a porta serial (grupo dialout)
#   4. cria o ambiente Python ~/venv-controle com as bibliotecas do curso
#   5. instala o arduino-cli, o núcleo do Arduino Uno e a biblioteca do display
#   6. define a senha fixa do JupyterLab e cria o atalho "projeto"
#      (abre os roteiros com um comando)
#
# Pede a senha de administrador (sudo). Leva ≈ 5–10 min, conforme a internet.
# Depois de rodar: SAIA DA SESSÃO E ENTRE DE NOVO (ou reinicie) — é o que faz
# a permissão da porta serial valer.
# =============================================================================
set -euo pipefail

VENV="$HOME/venv-controle"
BIN="$HOME/.local/bin"

echo "==> 1/6  Pacotes do sistema"
sudo apt-get update
sudo apt-get install -y python3-venv python3-pip git curl

echo "==> 2/6  Removendo o brltty (conflita com o CH340 das placas Arduino clone)"
if dpkg -s brltty >/dev/null 2>&1; then
    sudo apt-get remove -y brltty
else
    echo "    brltty não está instalado — ok"
fi

echo "==> 3/6  Permissão para a porta serial (grupo dialout)"
sudo usermod -aG dialout "$USER"

echo "==> 4/6  Ambiente Python em $VENV"
python3 -m venv "$VENV"
"$VENV/bin/pip" install --upgrade pip
"$VENV/bin/pip" install "control==0.10.2" numpy scipy matplotlib jupyter jupyterlab pyserial

echo "==> 5/6  arduino-cli, núcleo AVR (Arduino Uno) e biblioteca Adafruit SSD1306"
mkdir -p "$BIN"
if [ ! -x "$BIN/arduino-cli" ] && ! command -v arduino-cli >/dev/null 2>&1; then
    curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR="$BIN" sh
fi
ACLI="$(command -v arduino-cli || echo "$BIN/arduino-cli")"
"$ACLI" core update-index
"$ACLI" core install arduino:avr
"$ACLI" lib install "Adafruit SSD1306"       # traz junto a Adafruit GFX e a BusIO

echo "==> 6/6  JupyterLab com senha fixa e atalho \"projeto\""
# Com uma senha fixa, o Jupyter deixa de usar a chave temporária (token) que muda a cada vez
# e o endereço fica sempre http://localhost:8888/lab. ip = localhost: só este computador
# acessa. use_redirect_file = False: o navegador abre o endereço http direto.
mkdir -p "$HOME/.jupyter"
CFG="$HOME/.jupyter/jupyter_server_config.py"
[ -f "$CFG" ] && mv "$CFG" "$CFG.bak-$(date +%Y%m%d%H%M%S)"
cat > "$CFG" <<'EOF'
# Laboratório de Controle Automático — Jupyter só neste computador
c.ServerApp.ip = "localhost"
c.ServerApp.use_redirect_file = False
EOF
if grep -q "hashed_password" "$HOME/.jupyter/jupyter_server_config.json" 2>/dev/null; then
    echo "    já existe uma senha do Jupyter neste usuário (para trocar: jupyter server password)"
else
    echo "    Escolha a SENHA DO JUPYTER desta bancada (será pedida ao abrir o JupyterLab)."
    echo "    Ela não aparece enquanto você digita; digite duas vezes."
    "$VENV/bin/jupyter" server password
fi

# atalhos no terminal:
#   controle -> ativa o ambiente Python
#   projeto  -> ativa o ambiente, entra em projeto_final/ e abre o JupyterLab
REPO="$(pwd)"
if ! grep -q "alias controle=" "$HOME/.bashrc"; then
    echo "alias controle='source $VENV/bin/activate'" >> "$HOME/.bashrc"
fi
sed -i '/^alias projeto=/d' "$HOME/.bashrc"
echo "alias projeto='source $VENV/bin/activate && cd $REPO/projeto_final && jupyter lab'" >> "$HOME/.bashrc"

echo
echo "==> Teste rápido das bibliotecas Python"
"$VENV/bin/python" -c "import control, numpy, scipy, matplotlib, serial; print('    ok — python-control', control.__version__)"
echo
echo "PRONTO. Agora SAIA DA SESSÃO E ENTRE DE NOVO (ou reinicie o computador)."
echo "Depois, para trabalhar, abra um Terminal e digite apenas:"
echo "    projeto             # ativa o ambiente e abre os roteiros no JupyterLab"
echo "e entre com a senha do Jupyter que você acabou de escolher."
