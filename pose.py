import cv2 as cv
import numpy as np
from camera import Camera
from Keypoint import Keypoint


def set_constants_pose(folder_capture=None):
    cam = Camera(write_video=False, folder_capture=folder_capture)

    BODY_PARTS = {"Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                  "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                  "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
                  "LEye": 15, "REar": 16, "LEar": 17, "Background": 18}

    POSE_PAIRS = [["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
                  ["RElbow", "RWrist"], ["LShoulder",
                                         "LElbow"], ["LElbow", "LWrist"],
                  ["Neck", "RHip"], ["RHip", "RKnee"], [
        "RKnee", "RAnkle"], ["Neck", "LHip"],
        ["LHip", "LKnee"], ["LKnee", "LAnkle"], [
        "Neck", "Nose"], ["Nose", "REye"],
        ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"]]

    net = cv.dnn.readNetFromTensorflow("data/graph_opt.pb")
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)

    threshold = 0.2

    return cam, net, threshold, BODY_PARTS, POSE_PAIRS


def ajout_squelette(frame, size, net, threshold, BODY_PARTS, POSE_PAIRS):

    photo_height = frame.shape[0]
    photo_width = frame.shape[1]
    net.setInput(cv.dnn.blobFromImage(frame, 1.0, (size['width'], size['height']),
                                      (127.5, 127.5, 127.5), swapRB=True, crop=False))

    out = net.forward()
    out = out[:, :19, :, :]

    assert (len(BODY_PARTS) == out.shape[1])

    points = []
    for i in range(len(BODY_PARTS)):
        # Slice heatmap of corresponging body's part.
        heatMap = out[0, i, :, :]

        # Originally, we try to find all the local maximums. To simplify a sample
        # we just find a global one. However only a single pose at the same time
        # could be detected this way.
        _, conf, _, point = cv.minMaxLoc(heatMap)
        x = (photo_width * point[0]) / out.shape[3]
        y = (photo_height * point[1]) / out.shape[2]
        # Add a point if it's confidence is higher than threshold.
        points.append((int(x), int(y)) if conf > threshold else None)

    for pair in POSE_PAIRS:
        partFrom = pair[0]
        partTo = pair[1]
        assert (partFrom in BODY_PARTS)
        assert (partTo in BODY_PARTS)

        idFrom = BODY_PARTS[partFrom]
        idTo = BODY_PARTS[partTo]

        if points[idFrom] and points[idTo]:
            cv.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
            cv.ellipse(frame, points[idFrom], (3, 3), 0,
                       0, 360, (0, 0, 255), cv.FILLED)
            cv.ellipse(frame, points[idTo], (3, 3), 0,
                       0, 360, (0, 0, 255), cv.FILLED)

    return frame


def test_pose():
    cam, net, threshold, BODY_PARTS, POSE_PAIRS = set_constants_pose(
        folder_capture='capture')
    size = {'width': cam.frame_width, 'height': cam.frame_height}
    while True:
        cam.actualize_frame()
        cam.frame = ajout_squelette(
            cam.frame, size, net, threshold, BODY_PARTS, POSE_PAIRS)
        cam.show_frame()

        # Press 'q' to exit the loop
        if cv.waitKey(1) == ord('q'):
            break

        if cv.waitKey(1) == ord('s'):
            cam.save_frame()


if __name__ == '__main__':
    test_pose()
