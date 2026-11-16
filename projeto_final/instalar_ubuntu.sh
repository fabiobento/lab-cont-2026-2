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
#   6. configura o Jupyter para abrir no Firefox do Ubuntu sem pedir senha
#      e cria o atalho "projeto" (abre os roteiros com um comando)
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
"$VENV/bin/pip" install "control==0.10.2" numpy scipy matplotlib jupyter pyserial

echo "==> 5/6  arduino-cli, núcleo AVR (Arduino Uno) e biblioteca Adafruit SSD1306"
mkdir -p "$BIN"
if [ ! -x "$BIN/arduino-cli" ] && ! command -v arduino-cli >/dev/null 2>&1; then
    curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR="$BIN" sh
fi
ACLI="$(command -v arduino-cli || echo "$BIN/arduino-cli")"
"$ACLI" core update-index
"$ACLI" core install arduino:avr
"$ACLI" lib install "Adafruit SSD1306"       # traz junto a Adafruit GFX e a BusIO

echo "==> 6/6  Jupyter: abrir sem pedir senha/token"
# O Firefox do Ubuntu 24.04 (snap) não consegue abrir a página do Jupyter já com a chave de
# acesso (token), e aparece a tela "Password or token". Como o Jupyter só atende a este
# próprio computador (ip = localhost), desligamos a chave e a senha.
# Um arquivo .json com senha (criado por "jupyter notebook password") teria prioridade
# sobre o .py — por isso ele é renomeado.
mkdir -p "$HOME/.jupyter"
CFG="$HOME/.jupyter/jupyter_server_config.py"
for f in "$CFG" "$HOME/.jupyter/jupyter_server_config.json" "$HOME/.jupyter/jupyter_notebook_config.json"; do
    [ -f "$f" ] && mv "$f" "$f.bak-$(date +%Y%m%d%H%M%S)"
done
cat > "$CFG" <<'EOF'
# Laboratório de Controle Automático — Jupyter só no próprio computador, sem senha/token
c.ServerApp.ip = "localhost"
c.ServerApp.use_redirect_file = False
c.IdentityProvider.token = ""
c.PasswordIdentityProvider.hashed_password = ""
c.PasswordIdentityProvider.password_required = False
EOF

# atalhos no terminal:
#   controle -> ativa o ambiente Python
#   projeto  -> ativa o ambiente, entra em projeto_final/ e abre o Jupyter
REPO="$(pwd)"
if ! grep -q "alias controle=" "$HOME/.bashrc"; then
    echo "alias controle='source $VENV/bin/activate'" >> "$HOME/.bashrc"
fi
if ! grep -q "alias projeto=" "$HOME/.bashrc"; then
    echo "alias projeto='source $VENV/bin/activate && cd $REPO/projeto_final && jupyter notebook'" >> "$HOME/.bashrc"
fi

echo
echo "==> Teste rápido das bibliotecas Python"
"$VENV/bin/python" -c "import control, numpy, scipy, matplotlib, serial; print('    ok — python-control', control.__version__)"
echo
echo "PRONTO. Agora SAIA DA SESSÃO E ENTRE DE NOVO (ou reinicie o computador)."
echo "Depois, para trabalhar, abra um Terminal e digite apenas:"
echo "    projeto             # ativa o ambiente e abre os roteiros no navegador"
