import handTrackingModule as htm
import cv2
import numpy as np
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


# capturing the video
cap = cv2.VideoCapture(0)

# hand tracking
detector = htm.handDetector()

# Volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange= volume.GetVolumeRange()
vol = 0
volBar = 400

minVol = volRange[0]
maxVol = volRange[1]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    if len(lmList) != 0:
        # print(lmList[4],lmList[8])

        x1, y1 = lmList[4][1],lmList[4][2]
        x2, y2 = lmList[8][1],lmList[8][2]
        cx, cy = (x1+x2)//2 ,(y1+y2)//2

        cv2.circle(img, (x1,y1),12,(255,0,255),cv2.FILLED)
        cv2.circle(img, (x2,y2),12,(255,0,255),cv2.FILLED)
        cv2.circle(img, (cx,cy),12,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)

        length = math.hypot(x2-x1,y2-y1)
        # print(length)

        # hand range 30 - 230
        # volume range - -96 -0

        vol = np.interp(length,[30,230],[minVol,maxVol])
        volBar = np.interp(length,[30,230],[400,150])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length<30:
            cv2.circle(img, (cx, cy), 12, (0, 255, 0), cv2.FILLED)

    # showing level of volume in rectangle format
    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img,(50,int(volBar)),(85,400),(0,255,0),cv2.FILLED)

    cv2.imshow("img",img)
    cv2.waitKey(1)

cap.release()
cap.destroyAllWindows()
