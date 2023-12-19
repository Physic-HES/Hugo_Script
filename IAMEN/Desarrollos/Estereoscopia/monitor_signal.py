import numpy as np
import time
import sounddevice as sd
import cv2
import scipy.signal as S
import matplotlib.pyplot as plt

cap=cv2.VideoCapture(2)
#cap.set(cv2.CAP_PROP_FPS, 30)
myrecording = sd.rec(int(2 * 1000), samplerate=1000, channels=1, dtype='float64')
time.sleep(2)
f, Spec = S.welch(myrecording[:,0], 1000, window='hann', nperseg=1024,
                  scaling='spectrum')
fq=f[np.argmax(Spec)]
print(fq)
#ret, frame = cap.read()
#cv2.imshow('Con Trigger de Monitoreo',frame)
#cv2.destroyAllWindows()
#myrecording2 = sd.rec(1, samplerate=1000, channels=1, dtype='float64')
#plt.plot(myrecording2,'.')
#plt.show()
#delta=np.max(myrecording)-np.mean(myrecording)
ret, frame = cap.read()
cv2.imshow('Con Trigger de Monitoreo', frame)
numLabels=0
h=0
while numLabels<77:
    ret, frame = cap.read()
    (thresh, binaryIM) = cv2.threshold(frame[:,:int(frame.shape[1]/2),2], int(0.85 * 255), 255, cv2.THRESH_BINARY)
    (numLabels, labels, stats, centroids) = cv2.connectedComponentsWithStats(binaryIM, 3, cv2.CV_32S)
t=time.time()
while True:
    time.sleep(4/fq-(time.time()-t))
    print(1/(time.time()-t))
    ret, frame = cap.read()
    t=time.time()
    cv2.imshow('Con Trigger de Monitoreo', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()