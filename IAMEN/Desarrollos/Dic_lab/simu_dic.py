import numpy as np
import matplotlib.pyplot as plt
import cv2

def normalize(arr, t_min, t_max):
    diff = t_max - t_min
    diff_arr = np.max(np.max(arr)) - np.min(np.min(arr))
    temp = (((arr - np.min(np.min(arr)))*diff)/diff_arr) + t_min
    return temp

def speckle_G(Im,tam_g):
    c=100/tam_g
    tam_col, tam_raw = len(Im[0,:]), len(Im[:,0])
    ph_rand=1j*2 * np.pi * np.random.random((tam_raw,tam_col))
    rand_field=np.exp(ph_rand)
    X, Y = np.meshgrid(range(tam_col), range(tam_raw))
    gauss_0 = np.exp(-1 / (2 * (1.5*100) ** 2) * ((X - tam_col / 2) ** 2 + (Y - tam_raw / 2) ** 2))
    gauss_2 = np.exp(-1 / (2 * c ** 2) * ((X - tam_col / 2) ** 2 + (Y - tam_raw / 2) ** 2))
    bandpass = gauss_2
    scatter_field=np.fft.fftshift(np.fft.fft2(rand_field))
    gauss_lens=bandpass*scatter_field
    imagefield=np.fft.ifft2(np.fft.fftshift(gauss_lens))
    speck=np.abs(imagefield)**2
    return speck/np.max(np.max(speck))

SP=speckle_G(np.zeros((640,820)),1.25)
(thresh, BnW_image) = cv2.threshold(SP, 0.15, 1, cv2.THRESH_BINARY)
h,w=640,820
zona=48 #tamaño de zonas donde se correlaciona una porcion interior
div=zona/3
campo=50 #Cantidad de discretizaciones (discrt)
raw_in = 40
col_in = 150
discrt = 4
rgy=range(int(raw_in+zona/2),int(raw_in+zona/2+campo*discrt),int(discrt))
rgx=range(int(col_in+zona/2),int(col_in+zona/2+campo*discrt),int(discrt))
map_def_x = np.zeros((len(rgy), len(rgx)))
map_def_y = np.zeros((len(rgy), len(rgx)))
map_def = np.zeros((len(rgy), len(rgx)))
image_stres = np.zeros((h, w))
frame=(1-BnW_image)
for g in range(10):
    nn, kk = 0, 0
    srcTri = np.array([[0, 0], [frame.shape[1] - 1, 0], [0, frame.shape[0] - 1]]).astype(np.float32)
    dstTri = np.array([[0, frame.shape[1] * 0.33], [frame.shape[1] * 0.85, frame.shape[0] * 0.25],
                       [frame.shape[1] * 0.15, frame.shape[0] * 0.7]]).astype(np.float32)
    warp_mat = cv2.getAffineTransform(srcTri, dstTri)
    frame2 = cv2.warpAffine(frame, warp_mat, (frame.shape[1], frame.shape[0]))
    for n in rgy:
        for k in rgx:
            sub_frame_0 = frame[int(n - zona / 2):int(n + zona / 2), int(k - zona / 2):int(k + zona / 2)]
            sub_frame_1 = frame2[int(n - zona / 2):int(n + zona / 2), int(k - zona / 2):int(k + zona / 2)]
            sub_frame = sub_frame_0[int(div):int(2 * div), int(div):int(2 * div)]
            a, b, c, sub_int_def = cv2.minMaxLoc(cv2.matchTemplate(sub_frame_1, sub_frame, cv2.TM_CCOEFF_NORMED))
            map_def_x[nn, kk] += sub_int_def[0] - div
            map_def_y[nn, kk] += sub_int_def[1] - div
            map_def[nn, kk] = np.sqrt(map_def_x[nn, kk] ** 2 + map_def_y[nn, kk] ** 2)
            kk += 1
        nn += 1
        kk = 0
    if discrt > 1:
        mapa = cv2.resize(map_def, (int(campo * discrt), int(campo * discrt)), interpolation=cv2.INTER_AREA)
    else:
        mapa = map_def
    stress_x = (mapa[:-int(discrt), int(discrt):] - mapa[:-int(discrt), :-int(discrt)]) / (2 * discrt)
    stress_y = (mapa[int(discrt):, :-int(discrt)] - mapa[:-int(discrt), :-int(discrt)]) / (2 * discrt)
    # stress = np.where(stress_x+stress_y>=0,np.sqrt(stress_x**2+stress_y**2),0)
    # stress = np.where(stress_x+stress_y< 0, -np.sqrt(stress_x ** 2 + stress_y ** 2), stress)
    # stress-=np.min(stress)
    stress = np.sqrt(stress_x ** 2 + stress_y ** 2)
    # stress=normalize(stress,0,255)
    image_stres[int(raw_in + zona / 3 + discrt / 2):int(raw_in + zona / 3 + (campo - 1) * discrt + discrt / 2),
    int(col_in + zona / 3 + discrt / 2):int(col_in + zona / 3 + (campo - 1) * discrt + discrt / 2)] = 5 * mapa[
                                                                                                          :-int(discrt),
                                                                                                          :-int(discrt)]
    stress_color = cv2.applyColorMap(image_stres.astype('uint8'), cv2.COLORMAP_INFERNO)
    merge = cv2.add(frame2, stress_color)
    cv2.imshow('dic_sim', merge)
    key = cv2.waitKey(20)
    if key & 0xFF == ord('q'):  # exit on q
        break
    frame=frame2
cv2.destroyWindow('dic_sim')

