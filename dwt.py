
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
  y1, y2 = [], []
  S = [0] + signal + [0]
  for i in range(len(S)-1): # convolução
    y1.append( S[i] * c[0] + S[i+1] * c[1] )
    y2.append( S[i] * d[0] + S[i+1] * d[1] )
  A, D = [], []
  for i in range(1,len(S)-1,2): # down-sampling
    A.append( y1[i] )
    D.append( y2[i] )
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
  A, D = [], []
  for i in range(2*len(signal)-1): # up-sampling
    A.append( 0 if i%2 == 1 else signal.pop(0) )
    D.append( 0 if i%2 == 1 else detail.pop(0) )
  A = A + [0]
  D = D + [0]
  for i in range(len(A)-1): # reconstrução
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
    A, d = single_dwt_decomposition(A, c, d)
    Ds.insert(0, d)
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
def idwt1D(signal, details, j, f, g):
  Ds = []
  A = signal
  while j > 0 or len(details) > 0:
    d = details.pop(0)
    A = single_dwt_reconstruction(A, d, f, g)
    j -= 0
  return A