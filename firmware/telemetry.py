#!/usr/bin/env python3
"""
telemetry.py — Laboratório de Controle Automático (Ifes Guarapari)

Coleta a telemetria serial do Arduino (firmware prbs_aquisicao ou pid_motor)
e grava um CSV pronto para análise em Python (numpy/pandas/control).

Uso:
    python telemetry.py --porta /dev/ttyUSB0 --saida dados_motor.csv
    python telemetry.py --porta COM5 --saida ensaio_pid.csv --timeout 90

O script ignora linhas de comentário (iniciadas com '#') e encerra quando
receber "# fim do ensaio" ou estourar o tempo limite.

Dependência: pip install pyserial
"""

import argparse
import sys
import time

import serial  # pyserial


def main() -> int:
    ap = argparse.ArgumentParser(description="Coleta telemetria serial do Arduino para CSV.")
    ap.add_argument("--porta", required=True, help="porta serial (ex.: /dev/ttyUSB0, COM5)")
    ap.add_argument("--saida", required=True, help="arquivo CSV de saída")
    ap.add_argument("--baud", type=int, default=115200, help="baud rate (padrão: 115200)")
    ap.add_argument("--timeout", type=float, default=120.0,
                    help="tempo máximo de coleta [s] (padrão: 120)")
    args = ap.parse_args()

    n_linhas = 0
    t_inicio = time.time()

    with serial.Serial(args.porta, args.baud, timeout=1.0) as ser, \
         open(args.saida, "w", encoding="utf-8") as f:

        print(f"[telemetry] porta {args.porta} @ {args.baud} — gravando em {args.saida}")
        print("[telemetry] resete o Arduino para iniciar o ensaio...")

        while time.time() - t_inicio < args.timeout:
            raw = ser.readline().decode("utf-8", errors="replace").strip()
            if not raw:
                continue
            if raw.startswith("#"):
                print(f"[telemetry] {raw}")
                if "fim do ensaio" in raw:
                    break
                continue

            # linha de dados CSV: t,u,y  ou  t,r,angle,pwm
            campos = raw.split(",")
            try:
                [float(c) for c in campos]
            except ValueError:
                print(f"[telemetry] linha ignorada: {raw!r}", file=sys.stderr)
                continue

            f.write(raw + "\n")
            n_linhas += 1
            if n_linhas % 250 == 0:
                print(f"[telemetry] {n_linhas} linhas...")

    print(f"[telemetry] coleta encerrada: {n_linhas} linhas em {args.saida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
