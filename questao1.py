import sys
import argparse
import cv2
from math import sqrt
from dwt import single_dwt_decomposition, single_dwt_reconstruction, dwt1D, idwt1D

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Processa um sinal 1D com a DWT')
  parser.add_argument('signal', metavar='S', type=float, nargs='+', default=[-0.7071067811865475, 3.5355339059327373, 0.7071067811865475], help='Sinal 1D a ser processado')
  parser.add_argument('-J', type=int, default=1, help='Nível máximo de decomposição da DWT')
  args = parser.parse_args()

  signal = args.signal
  J = args.J

  print('Sinal Original\n\t', signal)
  
  haar_c = [1/sqrt(2), 1/sqrt(2)]
  haar_d = [-1/sqrt(2), 1/sqrt(2)]
  haar_f = [1/sqrt(2), 1/sqrt(2)]
  haar_g = [1/sqrt(2), -1/sqrt(2)]

  filtrado, detalhes = dwt1D(signal, J, haar_c, haar_d)
  formatted = ['{:.5}' for i in filtrado]
  str_formatted = ', '.join(formatted)
  print('Filtrado\n\t', f"[ {str_formatted.format(*filtrado)} ]")
  print('Detalhes')
  for ix,d in enumerate(detalhes):
    formatted = ['{:.5}' for i in d]
    str_formatted = ', '.join(formatted)
    print(f"#{ix}\t", f"[ {str_formatted.format(*d)} ]")

  reconstruido = idwt1D(filtrado, detalhes, haar_f, haar_g)
  formatted = ['{:.5}' for i in reconstruido]
  str_formatted = ', '.join(formatted)
  print('Sinal Reconstruído\n\t', f"[ {str_formatted.format(*reconstruido)} ]")
