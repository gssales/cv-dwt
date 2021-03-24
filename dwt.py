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
def single_dwt1D(signal, c, d):
  y0, y1 = [], []
  S = [0] + signal + [0]
  for i in range(len(S)-1): # convolução
    y0.append( S[i] * c[0] + S[i+1] * c[1] )
    y1.append( S[i] * d[0] + S[i+1] * d[1] )
  A, D = [], []
  for i in range(1,len(S)-1,2): # down-sampling
    A.append( y0[i] )
    D.append( y1[i] )
  return (A, D)

"""
função DWT simples de reconstrução
  - sinal 1D
  - detalhes
  - filtro de reconstrução passa-baixa
  - filtro de reconstrução passa-alta
returna 
  - Sinal Reconstruído
"""
def single_idwt1D(signal, detail, f, g):
  I = []
  A, D = [0], [0]
  for i in range(len(detail)): # up-sampling
    A.extend( [signal.pop(0), 0] )
    D.extend( [detail.pop(0), 0] )
  for i in range(len(D)-1): # reconstrução
    a = A[i] * f[0] + A[i+1] * f[1]
    d = D[i] * g[0] + D[i+1] * g[1]
    I.append(a + d)
  return I

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
  Ds = []
  A = signal
  while j > 0:
    A, dt = single_dwt1D(A, c, d)
    Ds.append(dt)
    j -= 1
  return (A, Ds)

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
def idwt1D(signal, details, f, g):
  Ds = []
  A = signal
  while len(details) > 0:
    d = details.pop()
    A = single_idwt1D(A, d, f, g)
  return A

"""
função DWT 2D de decomposição simples em uma direção
  - sinal 2D matriz
  - direction direção de decomposição, colunas ou linhas
  - filtro de decomposição passa-baixa
  - filtro de decomposição passa-alta
retorna 
  - Detalhes (low, high)
"""
def partial_dwt2D(matrix, direction, c, d):
  low, high = [], []
  if direction == 'columns':
    np.transpose(matrix)
  for component in matrix :
    l, h = single_dwt1D(component, c, d)
    low.append(l)
    high.append(h)
  if direction == 'columns':
    np.transpose(low)
    np.transpose(high)
  return (low, high)

"""
função DWT 2D de decomposição completa
  - sinal 2D matriz
  - filtro de decomposição passa-baixa
  - filtro de decomposição passa-alta
retorna 
  - filtrados [LL, LH, HL, HH]
"""
def complete_dwt2D(matrix, c, d):
  lowlow, lowhigh, highlow, highhigh = [], [], [], []

  low, high = partial_dwt2D(matrix, 'columns', c, d)
  lowlow, lowhigh = partial_dwt2D(low, 'lines', c, d)
  highlow, highhigh = partial_dwt2D(high, 'lines', c, d)

  return [lowlow, lowhigh, highlow, highhigh]
  
"""
função DWT 2D de reconstrução simples em uma direção
  - sinal 2D matriz low
  - sinal 2D matriz high
  - direction direção de reconstrução, colunas ou linhas
  - filtro de reconstrução passa-baixa
  - filtro de reconstrução passa-alta
retorna 
  - matriz reconstruída
"""
def partial_idwt2D(low, high, direction, f, g):
  A = []
  if direction == 'columns':
    np.transpose(matrix)
  for i in range(len(low)) :
    a = single_idwt1D(low[i], high[i], f, g)
    A.append(a)
  if direction == 'columns':
    np.transpose(A)
  return A
  
"""
função DWT 2D de reconstrução completa
  - tupla de filtrados (LL, LH, HL, HH)
  - filtro de reconstrução passa-baixa
  - filtro de reconstrução passa-alta
retorna 
  - Matrix reconstruída
"""
def complete_dwt2D(filtered_matrices, f, g):
  A = []
  lowlow, lowhigh, highlow, highhigh = filtered_matrices

  high = partial_idwt2D(highlow, highhigh, 'lines', f, g)
  low = partial_idwt2D(lowlow, lowhigh, 'lines', f, g)
  A = partial_idwt2D(low, high, 'columns', f, g)

  return A