import sys
import argparse
import copy
from math import sqrt
import numpy as np
import cv2
from dwt import dwt2D, idwt2D, details_thresholding

def map_toImage(matrix):
  max_value = -100
  min_value = 100
  for l in matrix:
    max_value = max(max_value, max(l))
    for c in l:
      min_value = min(min_value, c) if c > 0.0 else min_value
  mapped = []
  for l in matrix:
    mapped.append( list(map(lambda x: ((x - min_value) / max_value) if x > 0.0 else x , l)) )
  mapped = np.asmatrix(mapped)
  return mapped

def map_detail(matrix):
  max_value = -100
  for l in matrix:
    max_value = max(max_value, max(l))
  max_value = max_value if max_value != 0.0 else 0.0000000000000000001
  mapped = []
  for l in matrix:
    mapped.append( list(map(lambda x: x / max_value, l)) )
  mapped = np.asmatrix(mapped)
  return mapped

def map_result(filtered, details):
  plot = map_toImage(filtered)

  for level in reversed(details):
    detailLH = map_detail(level[0])
    detailHL = map_detail(level[1])
    detailHH = map_detail(level[2])

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
  return plot

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Processa um sinal 1D com a DWT')
  parser.add_argument('-i', '--image', metavar='image', type=str, default='./barbara.jpg', help='Imagem a ser processada')
  parser.add_argument('-o', '--output', metavar='output', type=str, default='./threshold.jpg', help='Resultado da decomposição da imagem')
  parser.add_argument('-j', type=int, default=1, help='Nível máximo de decomposição da DWT')
  parser.add_argument('-a', '--alpha', type=float, default=0.8, help='Alpha do filtro de thresholding')
  args = parser.parse_args()
  
  image_path = args.image
  output = args.output
  J = args.j
  alpha = args.alpha

  haar_c = [1/sqrt(2), 1/sqrt(2)]
  haar_d = [-1/sqrt(2), 1/sqrt(2)]
  haar_f = [1/sqrt(2), 1/sqrt(2)]
  haar_g = [1/sqrt(2), -1/sqrt(2)]
  
  img = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2GRAY)
  print("Imagem Original\n", img[:4,:4])
  cv2.imshow("Imagem Carregada", img)

  filtered, details = dwt2D(img, J, haar_c, haar_d)

  plot = map_result(filtered, details)
  print("Imagem Processada\n", np.asmatrix(plot)[:4,:4])
  cv2.imshow("Processed", plot)

  thres_details = details_thresholding(details, alpha)
  plot2 = map_result(filtered, thres_details)
  cv2.imshow("Threshold", plot2)

  reconstructed = idwt2D(filtered, thres_details, haar_f, haar_g)
  for i in range(len(reconstructed)):
    reconstructed[i] = list(map(lambda x: x / 255.0 , reconstructed[i]))
  cv2.imshow("reconstruida", np.asmatrix(reconstructed))
  for i in range(len(reconstructed)):
    reconstructed[i] = list(map(lambda x: x * 255.0 , reconstructed[i]))
  cv2.imwrite(output, np.asmatrix(reconstructed))
  print("Resultado Salvo")
  
  cv2.waitKey()
  cv2.destroyAllWindows()