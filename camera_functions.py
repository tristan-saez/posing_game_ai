import cv2


def getCamera(write_video=False):
    # Open the default camera
    cam = cv2.VideoCapture(0)

    # Get the default frame width and height
    frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter object
    if (write_video == True):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('output.mp4', fourcc, 20.0,
                              (frame_width, frame_height))
    else:
        out = None

    return cam, out


def captureCamera(cam, out):
    while True:
        ret, frame = cam.read()

        # Write the frame to the output file
        if (out != None):
            out.write(frame)

        # Display the captured frame
        cv2.imshow('Camera', frame)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) == ord('q'):
            break

    # Release the capture and writer objects
    cam.release()
    if (out != None):
        out.release()
    cv2.destroyAllWindows()


def test():
    cam, out = getCamera(write_video=True)
    captureCamera(cam, out)


if __name__ == '__main__':
    test()
