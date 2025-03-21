import pose as p
import cv2 as cv
import time
import os
import random


class Game:
    def __init__(self, pose_time: float = 8.0, poses_folder="poses/", result_layers_folder="layers/"):
        print("Initializing stats")
        self.life = 5
        self.score = 0
        self.pose_time = pose_time
        self.is_game_playing = False

        print("Getting poses")
        self.poses_list = []
        for filename in os.listdir(poses_folder):
            img = cv.imread(os.path.join(poses_folder, filename))
            if img is not None:
                self.poses_list.append(img)

        self.result_layers_list = []
        for filename in os.listdir(result_layers_folder):
            img = cv.flip(cv.imread(os.path.join(
                result_layers_folder, filename)), 1)
            if img is not None:
                self.result_layers_list.append(img)

        self.current_pose = None

        print("Initializing camera")
        self.cam, self.detector, self.point_ids = p.set_constants_pose(
            folder_capture='capture')

    def start_game(self):
        self.is_game_playing = True

        print("Innitializing game")
        self.current_pose = self.poses_list[0]
        self.current_color = self.current_pose[0][0]
        while self.is_game_playing:

            self.cam.actualize_frame()
            self.cam.frame, pose_data = p.ajout_squelette(
                self.cam.frame, self.detector, self.point_ids)
            self.cam.frame = p.add_layer(self.cam.frame, self.current_pose)
            self.update_display()

            if cv.waitKey(1) == ord('q'):
                exit(0)

            result = self.pose_diff(pose_data)
            print(result)
            if result:
                break

        self.poses_list.pop(0)

        print("Starting game")
        while self.is_game_playing:
            timer = 0
            self.select_pose()
            start = time.time()

            while timer < self.pose_time:
                self.cam.actualize_frame()
                self.cam.frame, pose_data = p.ajout_squelette(
                    self.cam.frame, self.detector, self.point_ids)
                self.cam.frame = p.add_layer(self.cam.frame, self.current_pose)
                self.update_display()

                if cv.waitKey(1) == ord('q'):
                    exit(0)

                timer = time.time() - start
                if (round(timer, 1) % 0.5) == 0:
                    print(f"{self.pose_time - round(timer, 1)} left !")

            print("Checking pose !")
            # pose_data = True
            result = self.check_pose(pose_data)

            start = time.time()
            end = time.time()
            while (end - start) < 1.5:
                self.cam.actualize_frame()
                self.cam.frame = p.add_layer(
                    self.cam.frame, self.result_layers_list[1 if result else 0], 0.1, 0.8, 0.1)
                self.update_display()

                if cv.waitKey(1) == ord('q'):
                    exit(0)

                end = time.time()

            if self.life == 0:
                print(f"Game lost ! Number of points : {self.score}")
                self.is_game_playing = False

    def check_pose(self, pose_data):
        result = self.pose_diff(pose_data)
        if result:
            self.score += 1
            print(f"Good ! Current score : {self.score}")
        else:
            self.life -= 1
            print(f"Nope ! Life -1... Remaining life : {self.life}")

        return result

    def pose_diff(self, pose_data):
        point_in = False
        width = len(self.current_pose)
        height = len(self.current_pose[0])
        for point in pose_data:
            if point[1] >= 0 and point[1] < width:
                if point[0] >= 0 and point[0] < height:
                    point_in = True
                    color_point = self.current_pose[point[1]][point[0]]
                    if color_point[0] == self.current_color[0] or color_point[1] == self.current_color[1] and color_point[2] == self.current_color[2]:
                        return False
        if len(pose_data) == 0 or point_in == False:
            return False
        return True

    def display_random_layer(self):
        pass

    def select_pose(self):
        self.current_pose = random.choice(self.poses_list)
        self.current_color = self.current_pose[0][0]

    def update_display(self):
        self.cam.frame = cv.resize(self.cam.frame, (1150, 830))
        self.cam.show_frame()
