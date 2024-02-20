import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self,mode= False,maxHands =2,modelComplexity=1, detectionCon= 0.5,trackCon =0.5):
        self.mode =mode
        self.maxHands =maxHands
        self.modelComplex = modelComplexity
        self.detectionCon =detectionCon
        self.trackCon = trackCon

        self.mpDrawings= mp.solutions.drawing_utils
        self.mpHands =mp.solutions.hands
        self.hand = self.mpHands.Hands(self.mode,self.maxHands,self.modelComplex,self.detectionCon,self.trackCon)

    def findHands(self,img,draw =True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hand.process(imgRGB)
        if self.result.multi_hand_landmarks:
            for hand_landmarks in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDrawings.draw_landmarks(img, hand_landmarks,self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self,img,handNo=0,draw = True):
        lmList = []
        if self.result.multi_hand_landmarks:
            myHand= self.result.multi_hand_landmarks[handNo]
            for id, ln in enumerate(myHand.landmark):
                h,w,c = img.shape
                cx ,cy = int(ln.x*w), int(ln.y*h)
                # print(id,cx,cy)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),5,(255,0,255),cv2.FILLED)

        return lmList


def main():
    ctime = 0
    ptime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList)!=0:
            print(lmList[4])
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("image", img)
        cv2.waitKey(1)

    # cap.release()
    # cap.destroyAllWindows()



if __name__ ==  "__main__":
  main()
