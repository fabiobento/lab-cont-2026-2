#!/usr/bin/env bash
# =============================================================================
# gravar_firmware.sh — compila e grava firmware/pid_motor no Arduino Uno da bancada
#
# Uso (num terminal, na pasta projeto_final/):
#     bash gravar_firmware.sh              # acha a porta sozinho
#     bash gravar_firmware.sh /dev/ttyUSB0 # ou diga qual é
#
# Antes: rode o instalar_ubuntu.sh uma vez e FECHE o notebook que estiver usando
# a porta (uma célula coletar() em execução) — a porta só aceita um programa.
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")/.."                 # raiz do repositório

PORTA="${1:-$(ls /dev/ttyUSB* /dev/ttyACM* 2>/dev/null | head -n 1 || true)}"
if [ -z "$PORTA" ]; then
    echo "Nenhum Arduino encontrado em /dev/ttyUSB* ou /dev/ttyACM*."
    echo "Confira o cabo USB. Se o Arduino aparece e some, o brltty pode estar instalado"
    echo "(sudo apt remove brltty — veja projeto_final/INSTALACAO_UBUNTU.md)."
    exit 1
fi
if [ ! -w "$PORTA" ]; then
    echo "Sem permissão para usar $PORTA. Rode o instalar_ubuntu.sh (grupo dialout)"
    echo "e saia da sessão e entre de novo."
    exit 1
fi

ACLI="$(command -v arduino-cli || echo "$HOME/.local/bin/arduino-cli")"
echo "==> Compilando firmware/pid_motor ..."
"$ACLI" compile --fqbn arduino:avr:uno firmware/pid_motor
echo "==> Gravando em $PORTA ..."
"$ACLI" upload -p "$PORTA" --fqbn arduino:avr:uno firmware/pid_motor
echo "Firmware gravado em $PORTA. O display deve mostrar PRONTO."
echo "No notebook, use:  PORTA = \"$PORTA\""
