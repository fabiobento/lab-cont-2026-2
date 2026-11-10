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
#
# Pede a senha de administrador (sudo). Leva ≈ 5–10 min, conforme a internet.
# Depois de rodar: SAIA DA SESSÃO E ENTRE DE NOVO (ou reinicie) — é o que faz
# a permissão da porta serial valer.
# =============================================================================
set -euo pipefail

VENV="$HOME/venv-controle"
BIN="$HOME/.local/bin"

echo "==> 1/5  Pacotes do sistema"
sudo apt-get update
sudo apt-get install -y python3-venv python3-pip git curl

echo "==> 2/5  Removendo o brltty (conflita com o CH340 das placas Arduino clone)"
if dpkg -s brltty >/dev/null 2>&1; then
    sudo apt-get remove -y brltty
else
    echo "    brltty não está instalado — ok"
fi

echo "==> 3/5  Permissão para a porta serial (grupo dialout)"
sudo usermod -aG dialout "$USER"

echo "==> 4/5  Ambiente Python em $VENV"
python3 -m venv "$VENV"
"$VENV/bin/pip" install --upgrade pip
"$VENV/bin/pip" install "control==0.10.2" numpy scipy matplotlib jupyter pyserial

echo "==> 5/5  arduino-cli, núcleo AVR (Arduino Uno) e biblioteca Adafruit SSD1306"
mkdir -p "$BIN"
if [ ! -x "$BIN/arduino-cli" ] && ! command -v arduino-cli >/dev/null 2>&1; then
    curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR="$BIN" sh
fi
ACLI="$(command -v arduino-cli || echo "$BIN/arduino-cli")"
"$ACLI" core update-index
"$ACLI" core install arduino:avr
"$ACLI" lib install "Adafruit SSD1306"       # traz junto a Adafruit GFX e a BusIO

# atalho: digitar "controle" no terminal ativa o ambiente Python
if ! grep -q "alias controle=" "$HOME/.bashrc"; then
    echo "alias controle='source $VENV/bin/activate'" >> "$HOME/.bashrc"
fi

echo
echo "==> Teste rápido das bibliotecas Python"
"$VENV/bin/python" -c "import control, numpy, scipy, matplotlib, serial; print('    ok — python-control', control.__version__)"
echo
echo "PRONTO. Agora SAIA DA SESSÃO E ENTRE DE NOVO (ou reinicie o computador)."
echo "Depois, para trabalhar:"
echo "    cd $(pwd)/projeto_final"
echo "    controle            # ativa o ambiente Python"
echo "    jupyter notebook    # abre o navegador com os roteiros"
