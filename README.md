
# Trabalho de implementação da Tranformada Wavelet
UFRGS - Instituto de Informática
INF01030 - Prof. Claudio Jung
Guilherme Souza Sales
Demetrio Boeira
  

### Questão 1
Arquivo questão1.py executa a transformada wavelet em um sinal digital 1D
  
```bash
usage: questao1.py [-h] [-J J] S [S ...]

Processa um sinal 1D com a DWT

positional arguments:

S Sinal 1D a ser processado

  

optional arguments:

-h, --help show this help message and exit

-J J Nível máximo de decomposição da DWT
```

Exemplo:

```bash
python3 questao1.py -J 2 -2 1 3 2 -3 4 # executa a DWT em 2 níveis sobre [-2 1 3 2 -3 4]
```
