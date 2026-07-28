# Preparação do ambiente de laboratório

Todo o curso usa **Python ≥ 3.10**, **Jupyter** e a **Python Control Systems Library** (`python-control`, versão 0.10.x).

## Opção A — Máquina local (recomendada para o projeto final)
Entre na pasta do curso e execute os comandos abaixo no terminal (Linux/macOS) ou no Anaconda Prompt (Windows):
```bash
# criar e ativar um ambiente virtual isolado na pasta venv
python3 -m venv venv
source venv/bin/activate

# instalar as dependências
pip install --upgrade pip
pip install "control>=0.10,<0.11" numpy scipy matplotlib jupyterlab ipykernel pandas

# (opcional) slycot habilita algumas rotinas adicionais baseadas em SLICOT
pip install slycot   # requer compilador Fortran; pode ser pulado sem prejuízo

# abrir o JupyterLab na pasta do curso
jupyter lab
```

No Windows, recomenda-se instalar via [Anaconda/Miniconda](https://docs.conda.io):

```bash
conda create -n controle python=3.11
conda activate controle
conda install -c conda-forge control slycot jupyterlab matplotlib pandas
```

## Opção B — Google Colab (sem instalação)

Basta abrir o notebook no [Colab](https://colab.research.google.com) e executar na primeira célula:

```python
%pip install "control>=0.10,<0.11"
```

## Verificação do ambiente

Execute o notebook `lab00_introducao_python_control.ipynb`. A primeira célula deve imprimir a versão da biblioteca (esperado: `0.10.x`) e gerar um gráfico de resposta ao degrau.

## Convenções de código adotadas no curso

- **Identificadores em inglês** (`sys`, `step_response`, `Kp`), como na documentação oficial;
- **Comentários e textos em português (pt-BR)**;
- Importações padronizadas em todos os notebooks:

```python
import numpy as np
import matplotlib.pyplot as plt
import control as ct
```

## Hardware do projeto final (Semanas 13–15)

O projeto final usa um sistema físico real. Sugestões de plantas de baixo custo:

| Planta | Variável controlada | Atuador | Sensor |
|---|---|---|---|
| Motor CC com encoder | velocidade/posição | ponte H (PWM) | encoder incremental |
| Sistema térmico (TCLab ou resistor + LM35) | temperatura | transistor/PWM | LM35/NTC |
| Kit motor CC — controle de posição | posição angular do eixo | ponte H + PWM | encoder de quadratura |

A aquisição pode ser feita com Arduino + comunicação serial com Python (`pyserial`), mantendo o projeto do controlador inteiramente na `python-control`.
