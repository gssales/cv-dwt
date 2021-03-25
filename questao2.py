import sys
import argparse
from math import sqrt
import numpy as np
import cv2
from dwt import complete_dwt2D, complete_idwt2D, dwt2D, idwt2D

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Processa um sinal 1D com a DWT')
  parser.add_argument('-I', '--image', metavar='image', type=str, default='./barbara.jpg', help='Imagem a ser processada')
  parser.add_argument('-J', type=int, default=1, help='Nível máximo de decomposição da DWT')
  args = parser.parse_args()

  image_path = args.image
  J = args.J

  haar_c = [1/sqrt(2), 1/sqrt(2)]
  haar_d = [-1/sqrt(2), 1/sqrt(2)]
  haar_f = [1/sqrt(2), 1/sqrt(2)]
  haar_g = [1/sqrt(2), -1/sqrt(2)]

  # img = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2GRAY)

  # lowl, lowh, highl, highh = complete_dwt2D(img, haar_c, haar_d)

  # cv2.imshow("Imagem Carregada", img)
  # print(img[0,0],lowl[0][0])
  # cv2.imshow("LL", np.asmatrix(lowl))
  
  # cv2.waitKey()
  # cv2.destroyAllWindows()

  img = [
    [ -2, 1, 3, 2, -3, 4],
    [ -2, 1, 3, 2, -3, 4],
    [ -2, 1, 3, 2, -3, 4],
    [ -2, 1, 3, 2, -3, 4],
    [ -2, 1, 3, 2, -3, 4],
    [ -2, 1, 3, 2, -3, 4]
  ]
  # lowl, lowh, highl, highh = complete_dwt2D(img, haar_c, haar_d)
  # print(lowl, lowh, highl, highh)

  # I = complete_idwt2D((lowl, lowh, highl, highh), haar_f, haar_g)
  # print(I)
  filtered, details = dwt2D(img, J, haar_c, haar_d)
  print(filtered)

  recons = idwt2D(filtered, details, haar_f, haar_g)
  print(recons)

