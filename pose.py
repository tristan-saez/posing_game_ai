import cv2 as cv
import numpy as np
from camera import Camera


def set_constants_pose():
    cam = Camera(write_video=False)

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

    threshold = 0.2

    return cam, net, threshold, BODY_PARTS, POSE_PAIRS


def boucle_pose(cam, net, threshold, BODY_PARTS, POSE_PAIRS):
    cam.actualize_frame()
    frame = cam.frame

    photo_height = frame.shape[0]
    photo_width = frame.shape[1]
    net.setInput(cv.dnn.blobFromImage(frame, 1.0, (cam.frame_width, cam.frame_height),
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

    t, _ = net.getPerfProfile()

    cv.imshow("Camera", frame)

    # waits for user to press any key
    # (this is necessary to avoid Python kernel form crashing)
    cv.waitKey(0)

    # closing all open windows
    cv.destroyAllWindows()


def test_pose():
    cam, net, threshold, BODY_PARTS, POSE_PAIRS = set_constants_pose()
    boucle_pose(cam, net, threshold, BODY_PARTS, POSE_PAIRS)


if __name__ == '__main__':
    test_pose()
