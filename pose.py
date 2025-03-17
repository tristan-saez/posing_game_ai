import cv2 as cv
import numpy as np
from camera import Camera
from Keypoint import Keypoint
from cvzone.PoseModule import PoseDetector
import time


def set_constants_pose(folder_capture=None):
    cam = Camera(write_video=False, folder_capture=folder_capture)

    # net = cv.dnn.readNetFromTensorflow("data/graph_opt.pb")
    detector = PoseDetector()

    point_ids = [0, 11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]

    return cam, detector, point_ids


def ajout_squelette(frame, detector, ids):
    coordinates = []

    frame = detector.findPose(frame)
    lmList, bboxInfo = detector.findPosition(frame, draw=False)

    for points in ids:
        coordinates.append((lmList[points][0], lmList[points][1]))

    return frame, coordinates


def add_layer(frame, layer, alpha=0.4, beta=0.6, gamma=0.4):
    new_frame = cv.addWeighted(frame, alpha, layer, beta, gamma)

    return new_frame


def test_pose():
    cam, detector, ids = set_constants_pose(
        folder_capture='capture')
    # size = {'width': cam.frame_width, 'height': cam.frame_height}
    while True:
        cam.actualize_frame()
        cam.frame, coordinate_list = ajout_squelette(cam.frame, detector, ids)
        cam.show_frame()

        # Press 'q' to exit the loop
        if cv.waitKey(1) == ord('q'):
            break

        if cv.waitKey(1) == ord('s'):
            cam.save_frame()


if __name__ == '__main__':
    test_pose()
