'''
Code mostly written by Apoorv Kumar, not me. Minor edits from me.
Github: https://github.com/apoorv-kumar/
'''


import re
from collections import deque

import cv2 as cv
import pytesseract as pts
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np

COL = X = 0
ROW = Y = 1

# Cracking captchas (see resources)


def get_adjacent_cells(cell, matrix):
    x_len = len(matrix[0])
    y_len = len(matrix)
    adjacent = []
    if cell[X] > 0 and cell[Y] > 0:
        adjacent.append((cell[X] - 1, cell[Y] - 1))
        adjacent.append((cell[X] - 1, cell[Y]))
        adjacent.append((cell[X], cell[Y] - 1))
    elif cell[X] > 0:
        adjacent.append((cell[X] - 1, cell[Y]))
    elif cell[Y] > 0:
        adjacent.append((cell[X], cell[Y] - 1))

    if cell[X] < x_len - 1 and cell[Y] < y_len - 1:
        adjacent.append((cell[X] + 1, cell[Y] + 1))
        adjacent.append((cell[X] + 1, cell[Y]))
        adjacent.append((cell[X], cell[Y] + 1))
    elif cell[X] < x_len - 1:
        adjacent.append((cell[X] + 1, cell[Y]))
    elif cell[Y] < y_len - 1:
        adjacent.append((cell[X], cell[Y] + 1))

    if cell[X] < x_len - 1 and cell[Y] > 0:
        adjacent.append((cell[X] + 1, cell[Y] - 1))

    if cell[X] > 0 and cell[Y] < y_len - 1:
        adjacent.append((cell[X] - 1, cell[Y] + 1))

    return adjacent



def get_islands(matrix, magic_no, xordered = True):
    visited = set()

    def __get_islands(cell, matrix):
        cqueue = deque([cell])
        island_set = []
        while len(cqueue) > 0:
            current_cell = cqueue.pop()
            if current_cell not in visited:
                visited.add(current_cell)
                if matrix[current_cell[ROW], current_cell[COL]] == magic_no:
                    island_set.append(current_cell)
                    adj_cells = get_adjacent_cells(current_cell, matrix)
                    cqueue.extend(adj_cells)
        return island_set

    islands = []

    for ri, row in enumerate(matrix):
        for ci, col in enumerate(row):
            island_set = __get_islands((ci, ri), matrix)
            if len(island_set):
                islands.append(island_set)

    if xordered:
        xstart = [(min([val[X] for val in island]), island) for island in islands]
        xstart.sort(key=lambda val: val[0])
        islands = [val[1] for val in xstart]
    return islands


def index_to_img(index_list):
    maxc = {}
    for c in [X,Y]:
        maxc[c] = max(index[c] for index in index_list)

    img_matrix = np.ones((maxc[ROW]+1, maxc[COL]+1))*255
    for index in index_list:
        img_matrix[index[ROW]][index[COL]] = 1
    return img_matrix


def render_chars(chars):
    fig, axs = plt.subplots(1,len(chars))
    for ix, char in enumerate(chars):
        axs[ix].imshow(char)
    plt.subplot_tool()
    plt.show()


def chars_to_string(chars):
    char_l = []
    for char in chars:
        img = Image.fromarray(char)
        img = img.convert('RGB')
        s = pts.image_to_string(img, config="-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ -psm 6")
        whitespaces = re.compile(r'\s+')
        s = re.sub(whitespaces, '', s)
        char_l.append(s)
    return ''.join(char_l)


def decode(filename):
    gray = cv.imread(filename, cv.IMREAD_GRAYSCALE)
    ret, thresh = cv.threshold(gray, 100, 255, cv.THRESH_BINARY)
    kernel = np.ones((1,1),np.uint8)
    thresh = cv.dilate(thresh, kernel)
    char_islands = get_islands(thresh, 0)
    mchars = [index_to_img(c) for c in char_islands]
    render_chars(mchars)
    return chars_to_string(mchars)

"https://unifiedportal-epfo.epfindia.gov.in/publicPortal/no-auth/captcha/createCaptcha?_HDIV_STATE_=2-3-4AD84E5016B4536AD2ACB5309ADA4771"
