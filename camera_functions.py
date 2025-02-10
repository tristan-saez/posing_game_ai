import cv2


class Camera:
    cam = None
    frame_width = 0
    frame_height = 0
    fourcc = None
    out = None

    frame = []
    ret = None

    def __init__(self, write_video=False):
        # Open the default camera
        self.cam = cv2.VideoCapture(0)

        # Get the default frame width and height
        self.frame_width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Define the codec and create VideoWriter object
        if (write_video == True):
            self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.out = cv2.VideoWriter('output.mp4', self.fourcc, 20.0,
                                       (self.frame_width, self.frame_height))
        else:
            self.out = None

    def __del__(self):
        self.cam.release()
        if (self.out != None):
            self.out.release()
        cv2.destroyAllWindows()

    def info_size(self):
        print("Width : " + str(self.frame_width) +
              ",\tHeight : " + str(self.frame_height))

    def actualize_frame(self):
        self.ret, self.frame = self.cam.read()

    def show_frame(self):
        # Write the frame to the output file
        if (len(self.frame) != 0):
            if (self.out != None):
                self.out.write(self.frame)

            # Display the captured frame
            cv2.imshow('Camera', self.frame)
        else:
            print("No frame to display")


def test():
    cam = Camera()
    cam.info_size()
    while True:
        cam.actualize_frame()
        cam.show_frame()

        # Press 'q' to exit the loop
        if cv2.waitKey(1) == ord('q'):
            break


if __name__ == '__main__':
    test()
