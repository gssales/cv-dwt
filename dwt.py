import numpy as np

"""
função DWT simples de decomposição
  - sinal 1D
  - filtro de decomposição passa-baixa
  - filtro de decomposição passa-alta
returna 
  - Sinal A
  - Detalhes D
"""
def single_dwt_decomposition(signal, c, d):
  pass

"""
função DWT simples de reconstrução
  - sinal 1D
  - detalhes
  - filtro de reconstrução passa-baixa
  - filtro de reconstrução passa-alta
returna 
  - Sinal Original
"""
def single_dwt_reconstruction(signal, detail, f, g):
  pass

"""
função DWT de decomposição em J níveis
  - sinal 1D
  - J níveis de decomposição
  - filtro de decomposição passa-baixa
  - filtro de decomposição passa-alta
returna 
  - Sinal A
  - Lista FIFO de Detalhes D[J]
"""
def dwt1D(signal, j, c, d):
  pass

"""
função DWT de reconstrução em J níveis
  - sinal 1D
  - Lista FIFO de Detalhes D[J]
  - J níveis de reconstrução
  - filtro de reconstrução passa-baixa
  - filtro de reconstrução passa-alta
returna 
  - Sinal Original
"""
def inverse_dwt1D(signal, details, j, f, g):
  pass