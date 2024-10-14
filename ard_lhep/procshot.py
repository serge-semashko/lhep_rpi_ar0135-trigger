import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')
import cv2
import numpy as np
import sys
import time
import math
t1 = time.time()
def getsr(piece_coord, rect):
    s = 0
    k = 0
    x1 = piece_coord[0][1]
    x2 = piece_coord[1][1]
    y1 = piece_coord[0][0]
    y2 = piece_coord[1][0]
    # print(x1, x2, y1, y2)
    # # print(piece_coord, x1, x2, y1, y2)
    for i in range(x1, x2 + 1):
        for j in range(y1, y2 + 1):
            s += sum(rect[j][i])
            k += 1
    sr = s // k
    return sr

def process_shot(kx, ky, xl, yu, xr, yd, xdlin, ydlin, nx, ny, filename, thick_center, thick_cm, thick_5mm):
    import matplotlib.pyplot as plt

    img = cv2.imread(filename)
    print(img.shape)
    img = img[yu:yd+1, xl:xr+1]
    # print(img.shape)
    xr=xr-xl
    xl=0
    yd=yd-yu
    yu=0

    cv2.imwrite('cat_'+filename, img)

    # cv2.resize(img, cv2.INTER_AREA)

    fin_width = math.trunc(img.shape[1] * kx)
    fin_height = math.trunc(img.shape[0] * ky)

    dim = (fin_width, fin_height)

    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    print(img.shape)
    print(time.time()-t1);
    #пересчет координат
    # xl = int(xl * kx)
    # xr = int(xr * kx)
    # yu = int(yu * ky)
    # yd = int(yd * ky)
    xl = 0
    xr = img.shape[1]
    yu = 0
    yd = img.shape[0]

    center_x = (xl + xr) // 2
    center_y = (yu + yd) // 2

    # print(img.shape)
    # print(xl,yu,xr,yd)

    np.set_printoptions(threshold=sys.maxsize)
    # rabrect = img[yu : yd + 1, xl : xr + 1]
    rabrect = img
    print(img.shape)
    # # print(str(img[:,:,1]))
    # # print('rabrect')
    # # print(rabrect)

    xrange = xr
    yrange = yd
    # # print(xrange, yrange)

    #рассчет сколько пикселей в 5мм и 1см
    pmm = xrange / xdlin
    range_cm = math.trunc(pmm * 10)
    range_mm = math.trunc(pmm * 5)
    # # print(range_cm, range_mm)

    x_piece_range = math.trunc(xrange / nx)
    y_piece_range = math.trunc(yrange / ny)
    # print(x_piece_range, y_piece_range)

    pieces = []
    for i in range(nx):
        for j in range(ny):
            lu = [yu + y_piece_range * j - yu, xl + x_piece_range * i - xl]
            if i != nx - 1:
                piece_xr = xl + x_piece_range * (i + 1) - 1 - xl
            else:
                piece_xr = xr - xl

            if piece_xr == img.shape[1]:
                piece_xr -= 1

            if j != ny - 1:
                piece_yd = yu + y_piece_range * (j + 1) - 1 - yu
            else:
                piece_yd = yd - yu

            if piece_yd == img.shape[0]:
                piece_yd -= 1

            rd = [piece_yd, piece_xr]

            pieces.append([lu, rd])
    print(time.time()-t1);
    rezmatr = np.zeros([nx, ny], dtype=int)
    for i in range(len(pieces)):
        sr = getsr(pieces[i], rabrect)

        rezy = i % ny
        rezx = i // ny

        rezmatr[rezx][rezy] = sr

    # print(rezmatr)

    xinfo = []
    for i in rezmatr:
        xinfo.append(sum(i) // len(rezmatr))
    # print(xinfo)

    yinfo = []
    for j in range(len(rezmatr[0])):
        s = 0
        k = 0
        for i in range(len(rezmatr)):
            s += rezmatr[i][j]
            k += 1
        yinfo.append(s // k)
    # print(yinfo)

    x = [((xl + (x_piece_range * (i + 1))) - center_x) * pmm for i in range(nx)]
    y = [((yu + (y_piece_range * (i + 1))) - center_y) * pmm for i in range(ny)]

    print(x)
    print(y)
    # print(time.time()-t1);
    # plt.margins(0,0)
    # plt.gca().set_axis_off()
    # plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    # plt.margins(0,0)
    # plt.gca().xaxis.set_major_locator(plt.NullLocator())
    # plt.gca().yaxis.set_major_locator(plt.NullLocator())
# Сохраняем изображение, исключив ненужные элементы
    plt.bar(x, xinfo, width=5)
    # fig.suptitle('Распределение по X')
    # plt.savefig(sys.argv[1].split('.')[0]+'-hist.png')
    plt.savefig(filename.split('.')[0] + '-bar.png')
    plt.clf()

    fig, ax = plt.subplots()
    # ax.set_frame_on(False)

    
    ax.barh(y, yinfo, height=5)
    ax.invert_yaxis()
    # fig.suptitle('Распределение по Y')
    # plt.margins(0,0)
    # plt.gca().set_axis_off()
    # plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    # plt.margins(0,0)
    # plt.gca().xaxis.set_major_locator(plt.NullLocator())
    # plt.gca().yaxis.set_major_locator(plt.NullLocator())

    plt.savefig(filename.split('.')[0] + '-barh.png')
    plt.clf()
    # print(time.time()-t1);

    cv2.rectangle(img, (xl, yu), (xr, yd), (0, 0, 0), thickness=thick_center)
    cv2.line(img, (center_x, yu), (center_x, yd), (0, 0, 0), thickness=thick_center)
    cv2.line(img, (xl, center_y), (xr, center_y), (0, 0, 0), thickness=thick_center)

    for i in range(center_x, xl, -1 * range_cm):
        cv2.line(img, (i, yu), (i, yd), (0, 0, 0), thickness=thick_cm)
    for i in range(center_x, xr, range_cm):
        cv2.line(img, (i, yu), (i, yd), (0, 0, 0), thickness=thick_cm)

    for i in range(center_y, yu, -1 * range_cm):
        cv2.line(img, (xl, i), (xr, i), (0, 0, 0), thickness=thick_cm)
    for i in range(center_y, yd, range_cm):
        cv2.line(img, (xl, i), (xr, i), (0, 0, 0), thickness=thick_cm)

    for i in range(center_x, xl, -1 * range_mm):
        cv2.line(img, (i, yu), (i, yd), (0, 0, 0), thickness=thick_5mm)
    for i in range(center_x, xr, range_mm):
        cv2.line(img, (i, yu), (i, yd), (0, 0, 0), thickness=thick_5mm)

    for i in range(center_y, yu, -1 * range_mm):
        cv2.line(img, (xl, i), (xr, i), (0, 0, 0), thickness=thick_5mm)
    for i in range(center_y, yd, range_mm):
        cv2.line(img, (xl, i), (xr, i), (0, 0, 0), thickness=thick_5mm)

    cv2.imwrite(filename.split('.')[0] + '-markup.png', img)
    print(img.shape)

    file = open(filename.split('.')[0]+'.txt', 'w')
    file.write(str(rezmatr))
    file.close()

    return rezmatr

# imname = sys.argv[1]
# print(str(sys.argv))
kx = (2 ** 0.5) / 2
ky = 1 / 2

#imname = 'photo_2024-10-11_11-29-01.jpg'
#1 - коэффициент деформации по х, 2 - коэффициент деформации по у, 3 - левая граница по x, 4 - верхняя граница по y, 5 - правая граница по x, 6 - нижняя граница по y,
#7 - Длина границы х в мм, 8 - длина границы у в мм, 9 - количество ячеек по x, 10 - количество ячеек по y, 11 - название обрабатываемого файла
#12 - толщина центрального креста, 13 - толщина крестов через каждый сантиметр, 14 - толщина крестов через каждые 5 мм



# print('rezult -', process_shot(kx, ky, 260, 284, 644, 762, 100, 70, 16, 12, imname, 4, 2, 1))
# print(time.time()-t1);
