import sys
import argparse
import cv2
from math import sqrt
from dwt import single_dwt_decomposition, single_dwt_reconstruction, dwt1D, idwt1D

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Processa um sinal 1D com a DWT')
  parser.add_argument('signal', metavar='S', type=int, nargs='+', default=[1, 2, -1, 3, 6, -2, -1, 3], help='Sinal 1D a ser processado')
  parser.add_argument('-J', type=int, default=1, help='Nível máximo de decomposição da DWT')
  args = parser.parse_args()

  signal = args.signal
  J = args.J

  print('Sinal Original\t', signal)
  
  haar_c = [1/sqrt(2), 1/sqrt(2)]
  haar_d = [-1/sqrt(2), 1/sqrt(2)]
  haar_f = [1/sqrt(2), 1/sqrt(2)]
  haar_g = [1/sqrt(2), -1/sqrt(2)]

  filtrado, detalhes = single_dwt_decomposition(signal, haar_c, haar_d)
  print('Filtro Passa-Baixa\t', filtrado)
  print('Filtro Passa-Alta\t', detalhes)

  reconstruido = single_dwt_reconstruction(filtrado, detalhes, haar_f, haar_g)
  print('Sinal Reconstruído\t', reconstruido)
