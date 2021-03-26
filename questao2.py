import sys
import argparse
import copy
from math import sqrt
import numpy as np
import cv2
from dwt import dwt2D, idwt2D

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Processa um sinal 1D com a DWT')
  parser.add_argument('-i', '--image', metavar='image', type=str, default='./barbara.jpg', help='Imagem a ser processada')
  parser.add_argument('-o', '--output', metavar='output', type=str, default='./result.jpg', help='Resultado da decomposição da imagem')
  parser.add_argument('-j', type=int, default=1, help='Nível máximo de decomposição da DWT')
  args = parser.parse_args()

  image_path = args.image
  output = args.output
  J = args.j

  haar_c = [1/sqrt(2), 1/sqrt(2)]
  haar_d = [-1/sqrt(2), 1/sqrt(2)]
  haar_f = [1/sqrt(2), 1/sqrt(2)]
  haar_g = [1/sqrt(2), -1/sqrt(2)]

  img = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2GRAY)
  print("Imagem Original\n", img[:4,:4])
  cv2.imshow("Imagem Carregada", img)
  
  filtered, details = dwt2D(img, J, haar_c, haar_d)

  plot = copy.deepcopy(filtered)
  ds = copy.deepcopy(details)

  max_filter = -100
  min_filter = 100
  for l in plot:
    max_filter = max(max_filter, max(l))
    for c in l:
      min_filter = min(min_filter, c) if c > 0.0 else min_filter
  for i in range(len(plot)):
    plot[i] = list(map(lambda x: ((x - min_filter) / max_filter) if x > 0.0 else x , plot[i]))
  plot = np.asmatrix(plot)

  for level in reversed(ds):
    for i in range(len(level)):
      max_level = -100
      for l in level[i]:
        max_level = max(max_level, max(l))
      for j in range(len(level[i])):
        level[i][j] = list(map(lambda x: (x - 0) / max_level , level[i][j]))

    detailLH = np.asmatrix(level[0])
    detailHL = np.asmatrix(level[1])
    detailHH = np.asmatrix(level[2])
    
    plot = np.concatenate((plot, detailLH), axis=1)
    detailHL = np.concatenate((detailHL, detailHH), axis=1)

    nx_plot, ny_plot = np.shape(plot)
    nx_detail, ny_detail = np.shape(detailHL)
    px = nx_plot - nx_detail
    py = ny_plot - ny_detail
    if px < 0:
      while px < 0:
        plot = np.append(plot, np.zeros((1,ny_plot), dtype=int), axis=0)
        px += 1
    elif px > 0:
      while px > 0:
        detailHL = np.append(detailHL, np.zeros((1,ny_detail), dtype=int), axis=0)
        px -= 1

    if py < 0:
      while py < 0:
        plot = np.append(plot, np.zeros((nx_plot,1), dtype=int), axis=1)
        py += 1
    elif py > 0:
      while py > 0:
        detailHL = np.append(detailHL, np.zeros((nx_detail,1), dtype=int), axis=1)
        py -= 1

    plot = np.concatenate((plot, detailHL), axis=0)

  print("Imagem Filtrada\n", np.asmatrix(plot)[:4,:4])
  cv2.imshow("LL", plot)

  for i in range(len(plot)):
    plot[i] = list(map(lambda x: x * 255.0 , plot[i]))
  cv2.imwrite(output, plot)
  print("Resultado Salvo")

  reconstructed = idwt2D(filtered, details, haar_f, haar_g)
  for i in range(len(reconstructed)):
    reconstructed[i] = list(map(lambda x: x / 255.0 , reconstructed[i]))
  cv2.imshow("reconstruida", np.asmatrix(reconstructed))
  
  cv2.waitKey()
  cv2.destroyAllWindows()

