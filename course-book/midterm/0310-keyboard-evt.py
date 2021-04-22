import cv2
import numpy as np

width, height = 512, 512
x, y, R = 256, 256, 50
direction = 0  # right

while True:
    key = cv2.waitKeyEx(30)
    if key == 0x1B:
        break

    # Direction keys
    elif key == 0x270000:  # right
        direction = 0
    elif key == 0x280000:  # down
        direction = 1
    elif key == 0x250000:  # left
        direction = 2
    elif key == 0x260000:  # up
        direction = 3

    # Direction movement
    if direction == 0:  # right
        x += 10
    elif direction == 1:  # down
        y += 10
    elif direction == 2:  # left
        x -= 10
    elif direction == 3:  # up
        y -= 10

    # Checking the borders
    if x < R - width:
        x = R
        direction = 0
    if x > width:
        x = R - width
        direction = 2
    if y < R - height:
        y = R
        direction = 1
    if y > height:
        y = R - height
        direction = 3

    # Erase and redraw
    img = np.zeros((width, height, 3), np.uint8) + 255  # erase the old one
    cv2.circle(img, (x, y), R, (0, 0, 255), -1)
    cv2.imshow('img', img)

# cv2.waitKey(0)  #wait for any key
cv2.destroyAllWindows()
