import cv2
from os import listdir
from os.path import isfile, join


class Camera:
    def __init__(self, write_video=False, folder_capture='capture'):
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

        if folder_capture is not None:
            self.folder_capture = folder_capture
        else:
            self.folder_capture = 'capture'
        onlyfiles = [f for f in listdir(
            self.folder_capture) if isfile(join(self.folder_capture, f))]
        self.next_img_id = int(onlyfiles[-1].split('-')[1][:3])+1

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

    def save_frame(self):
        cv2.imwrite(self.folder_capture+'/capture-' +
                    '{0:03d}'.format(self.next_img_id)+'.png', self.frame)
        self.next_img_id += 1
        print('Pose saved !')


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
