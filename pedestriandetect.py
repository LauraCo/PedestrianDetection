#Building off of peopledetect.py to include analysis of video footage
#http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html

import numpy as np
import cv2
import time

help_message = '''
USAGE: peopledetect.py <video_name> ...

Press any key to continue, ESC to stop.
'''

def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh

def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)


cap = cv2.VideoCapture('videos/Aber_Pedestrian_1.MP4')

pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)

list = [];

while True:
    flag, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #fourcc = cv2.cv.CV_FOURCC(*'XVID')
    #outVideo = cv2.VideoWriter('output.mp4', -1, 20.0, (640,480))

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )

    found, w = hog.detectMultiScale(frame, winStride=(12,12), padding=(32,32), scale=1.05)
    found_filtered = []
    for ri, r in enumerate(found):
        for qi, q in enumerate(found):
            if ri != qi and inside(r, q):
                break
        else:
            found_filtered.append(r)
    draw_detections(frame, found, 3)
    draw_detections(frame, found_filtered, 3)

    print '%d (%d) found' % (len(found_filtered), len(found))

    list.append('%d (%d) found' % (len(found_filtered), len(found)))
    # write the flipped frame
    #outVideo.write(frame)
    cv2.imshow('video',frame)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        file_name = time.strftime("Output - %Y%m%d-%H%M%S")
        f = open(file_name, 'w+')
        #for item in list:
        f.write(str(list))

        f.close()
        break

cap.release()
cv2.destroyAllWindows()
