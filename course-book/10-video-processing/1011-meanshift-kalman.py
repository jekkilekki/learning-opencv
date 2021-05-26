# 1011.py
import cv2
import numpy as np

#1
roi = None
drag_start = None
mouse_status = 0
tracking_start = False

def onMouse(event, x,y, flags, param = None):
    global roi
    global drag_start
    global mouse_status
    global tracking_start

    if event == cv2.EVENT_LBUTTONDOWN:
        drag_start = (x,y)
        mouse_status = 1
        tracking_start = False
    elif event == cv2.EVENT_MOUSEMOVE:
        if flags == cv2.EVENT_FLAG_LBUTTON:
            xmin = min(x, drag_start[0])
            ymin = min(y, drag_start[1])
            xmax = max(x, drag_start[0])
            ymax = max(y, drag_start[1])
            roi = (xmin, ymin, xmax, ymax)
            mouse_status = 2 # dragging
    elif event == cv2.EVENT_LBUTTONUP:
        mouse_status = 3 # complete

#2
cv2.namedWindow('tracking')
cv2.setMouseCallback('tracking', onMouse)

cap = cv2.VideoCapture('../data/ball.wmv')
if ( not cap.isOpened() ):
    print('Error opening video.')

h,w = (int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
roi_mask = np.zeros((h,w), dtype = np.uint8)
term_crit = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 10, 1)

#3: Kalman filter setup
q = 1e-5 # process noise covariance
r = 0.01 # measurement noise covariance, 1, 0.0001
dt = 1
KF = cv2.KalmanFilter(4,2,0)
KF.transitionMatrix = np.array([[1,0,dt,0],
                                [0,1,0,dt],
                                [0,0,1,0],
                                [0,0,0,1]], np.float32) # A
KF.measurementMatrix = np.array([[1,0,0,0],
                                [0,1,0,0]], np.float32) # H

#4
t = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    t += 1
    print('t = ', t)

    frame2 = frame.copy() # CamShift
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (0, 60, 32), (180, 255, 255))

    if mouse_status == 2:
        x1,y1,x2,y2 = roi
        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,0,255), 2)

    if mouse_status == 3:
        print('initialize...')
        mouse_status = 0

        x1,y1,x2,y2 = roi
        mask_roi = mask[y1:y2, x1:x2]
        hsv_roi = hsv[y1:y2, x1:x2]

        hist_roi = cv2.calcHist([hsv_roi], [0], mask_roi, [16], [0,180])

        cv2.normalize(hist_roi, hist_roi, 0, 255, cv2.NORM_MINMAX)
        H1 = hist_roi.copy()
        cv2.normalize(H1, H1, 0.0, 1.0, cv2.NORM_MINMAX)

        track_win = (x1,y1,x2-x1,y2-y1) # meanShift

        #4-1: Kalman filter initialize
        KF.processNoiseCov = q * np.eye(4, dtype = np.float32) # Q
        KF.measurementNoiseCov = r * np.eye(2, dtype = np.float32) # R
        KF.errorCovPost = np.eye(4, dtype = np.float32) # P0 = I

        x,y,w,h = track_win
        KF.statePost = np.array([[x],[y],[0.],[0.]], dtype = np.float32)
        tracking_start = True

    if tracking_start:
        #4-2
        predict = KF.predict()

        #4-3
        backP = cv2.calcBackProject([hsv], [0], hist_roi, [0,180], 1)
        backP &= mask

        ret, track_win = cv2.meanShift(backP, track_win, term_crit)
        x,y,w,h = track_win
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)

        #4-4: Kalman correct
        z = np.array([[x][y]], dtype = np.float32) # measurement # error here
        estimate = KF.correct(z)
        estimate = np.int0(estimate)

        #4-5
        x2,y2 = estimate[0][0], estimate[1][0]
        cv2.rectangle(frame, (x2,y2), (x2+w,y2+h), (255,0,0), 2)
        ## track_win = x2,y2,w,h
    
    cv2.imshow('tracking', frame) # meanShift
    key = cv2.waitKey(25)
    if key == 27:
        break

if cap.isOpened():
    cap.release()
cv2.destroyAllWindows()