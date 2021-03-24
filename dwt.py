
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
def single_dwt_reconstruction(signal, detail, f, g):
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
    A, dt = single_dwt_decomposition(A, c, d)
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
    A = single_dwt_reconstruction(A, d, f, g)
  return A