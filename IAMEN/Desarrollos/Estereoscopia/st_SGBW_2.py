import cv2
import numpy as np

def main():
    # Configura las cámaras estéreo (asegúrate de tener las matrices de calibración)
    # Puedes obtener las matrices utilizando herramientas como el Calibrador de Cámara de OpenCV.

    # Cargar las matrices de calibración
    #camera_matrix_left = np.load('camera_matrix_left.npy')
    #camera_matrix_right = np.load('camera_matrix_right.npy')
    #dist_coeff_left = np.load('dist_coeff_left.npy')
    #dist_coeff_right = np.load('dist_coeff_right.npy')
    #R = np.load('R.npy')
    #T = np.load('T.npy')

    blockSize = 11
    min_disparity = 50
    max_disparity = 150
    P1 = 8
    P2 = 32
    # Configura el objeto StereoSGBM para la disparidad
    stereo = cv2.StereoSGBM_create(
            minDisparity=min_disparity,
            numDisparities=(max_disparity - min_disparity),
            blockSize=blockSize,
            P1=3 * blockSize * blockSize * P1,
            P2=3 * blockSize * blockSize * P2,
            disp12MaxDiff=0,
            preFilterCap=0,
            uniquenessRatio=10
            #	speckleWindowSize=100,
            #	speckleRange=1,
            #	mode=cv.StereoSGBM_MODE_SGBM
            #	#mode=cv.StereoSGBM_MODE_HH
        )

    def redraw():
        disparity = stereo.compute(gray_left, gray_right)
        out = (disparity / np.float32(16)) / max_disparity
        # disparity = stereo.compute(imgR,imgL)
        cv2.imshow('Disparidad en tiempo real', out)

    # Inicializa las cámaras
    cap = cv2.VideoCapture(2)  # Ajusta el índice según tu configuración
    #cap_right = cv2.VideoCapture(1)  # Ajusta el índice según tu configuración
    w, h = 2560, 960
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

    def on_blockSize(pos):
        global blockSize
        blockSize = 1 - (1 - pos) // 2 * 2
        stereo.setBlockSize(blockSize)
        redraw()

    def on_mindisparity(pos):
        global min_disparity
        min_disparity = pos
        stereo.setMinDisparity(min_disparity)
        stereo.setNumDisparities(max_disparity - min_disparity)
        redraw()

    def on_maxdisparity(pos):
        global max_disparity
        max_disparity = pos
        stereo.setNumDisparities(max_disparity - min_disparity)
        redraw()

    def on_P1(pos):
        global P1
        P1 = pos
        stereo.setP1(3 * blockSize * blockSize * P1)
        redraw()

    def on_P2(pos):
        global P2
        P2 = pos
        stereo.setP2(3 * blockSize * blockSize * P2)
        redraw()

    def set_disp12MaxDiff(pos):
        stereo.setDisp12MaxDiff(pos)
        redraw()

    def set_preFilterCap(pos):
        stereo.setPreFilterCap(pos)
        redraw()

    cv2.namedWindow("out")
    cv2.createTrackbar("blockSize", "out", blockSize, 51, on_blockSize)
    cv2.createTrackbar("minDisparity", "out", min_disparity, 200, on_mindisparity)
    cv2.createTrackbar("maxDisparity", "out", max_disparity, 200, on_maxdisparity)
    cv2.createTrackbar("P1", "out", P1, 64, on_P1)
    cv2.createTrackbar("P2", "out", P2, 64, on_P2)
    cv2.createTrackbar("disp12MaxDiff", "out", 0, 100, set_disp12MaxDiff)
    cv2.createTrackbar("preFilterCap", "out", 0, 100, set_preFilterCap)

    while True:
        # Captura un par de imágenes estéreo
        ret, frame = cap.read()
        frame_left = frame[:,0:int(w/2),:]
        frame_right = frame[:,int(w/2):w,:]

        if not ret:
            print("Error al capturar imágenes")
            break

        # Rectifica las imágenes
        #rectified_left = cv2.undistort(frame_left, camera_matrix_left, dist_coeff_left)
        #rectified_right = cv2.undistort(frame_right, camera_matrix_right, dist_coeff_right)

        # Convierte las imágenes a escala de grises
        gray_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2GRAY)
        gray_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2GRAY)

        # Calcula la disparidad
        redraw()

        # Maneja eventos del teclado
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera los recursos
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
