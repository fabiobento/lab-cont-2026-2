# Galeria oficial de exemplos da `python-control` 0.10.2 — mapa para o curso

A documentação da biblioteca traz exemplos prontos (scripts e notebooks) em
<https://python-control.readthedocs.io/en/0.10.2/examples.html>, com código-fonte no
repositório (`examples/`). Abaixo, o mapa do que **casa com a ementa** — use como material
complementar dos labs — e do que fica **além do escopo** (repertório para quem quiser ir além).

## Diretamente ligados aos labs

| Exemplo oficial | Link | Usa no curso |
|---|---|---|
| *Secord order system (MATLAB module)* | [secord-matlab](https://python-control.readthedocs.io/en/0.10.2/examples/secord-matlab.html) | Lab 04 — resposta/Bode de 2ª ordem (mostra também a interface compatível com MATLAB, útil para quem vem do Ogata/Nise) |
| *Phase plot examples* | [phase_plane_plots](https://python-control.readthedocs.io/en/0.10.2/examples/phase_plane_plots.html) | Lab 06 §6 — retratos de fase (mesma API `phase_plane_plot`/`phaseplot` usada no lab) |
| *Describing function analysis* | [describing_functions](https://python-control.readthedocs.io/en/0.10.2/examples/describing_functions.html) | **Incorporado ao Lab 07 §2.2** — previsão gráfica do ciclo-limite ($`G(j\omega) \times -1/N(a)`$); o E5 do lab reproduz o caso da saturação |
| *Cruise control* (FBS) | [cruise](https://python-control.readthedocs.io/en/0.10.2/examples/cruise.html) | Labs 06–08 — PI sobre planta não linear **com o mesmo anti-windup** do curso; excelente leitura paralela ao Lab 07 §1 |
| *Interconnect Tutorial* | [interconnect_tutorial](https://python-control.readthedocs.io/en/0.10.2/examples/interconnect_tutorial.html) | Labs 06/07 — referência completa de `nlsys` + `interconnect` por nomes de sinais |
| *Simulating interconnections (discrete/nonlinear)* | [simulating_discrete_nonlinear](https://python-control.readthedocs.io/en/0.10.2/examples/simulating_discrete_nonlinear.html) | Lab 10 — malha híbrida contínua + discreta, como na simulação do PID digital |
| *Caltech CDS 110 Colab notebooks* | [pasta no Google Drive](https://drive.google.com/drive/folders/1LI2xWVn1kqrZ5lIcM5Ktxr2B7X730cCj?usp=share_link) | Todo o curso — os mesmos notebooks CDS 110 usados como referência, executáveis no Colab |

## Além do escopo da ementa (repertório/IC)

- *PVTOL* (nested, LQR, output feedback), *vehicle steering* (gain scheduling, ótimo, flatness),
  *MPC aircraft*, *MRAC* (MIT/Lyapunov), *robust SISO/MIMO + H2/H∞*, *disk margins*,
  *Markov/ERA*, *stochastic response* — controle no espaço de estados, ótimo, adaptativo e
  robusto. São a continuação natural para estudantes de iniciação científica após a disciplina;
  o *disk margin* em particular estende as margens do Lab 05 para perturbações simultâneas de
  ganho e fase.

**Como usar em aula:** cada exemplo tem link "View page source" com o `.ipynb`/`.py` para
download; todos rodam no mesmo ambiente do curso (`pip install control`).
