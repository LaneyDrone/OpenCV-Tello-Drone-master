# Utility progrm to interface with your webcam.
import cv2
import threading
import pyautogui

class WebCam:
    def __init__(self):
        self.ret = False
        self.frame = None
        self.stream_state = False
        self.video_thread = threading.Thread(target=self._video_thread)
        self.video_thread.daemon = False
        self.video_thread.start()
        self.count = 0
    def _video_thread(self):
        # Creating stream capture object
        cap = cv2.VideoCapture(0)
        while True:
            self.ret, self.frame = cap.read()
            if self.stream_state and self.ret:
                cv2.imshow('space to capture', self.frame)
                # Video Stream is closed if escape key is pressed
                k = cv2.waitKey(1) & 0xFF
                if k == 27:
                    break
                    cap.release()
                    cv2.destroyAllWindows()
                elif k == 32:
                    file_name = "web_cam_capture_" + str(self.count)
                    cv2.imwrite(file_name + ".png", self.frame)
                    self.count += 1

    def streamon(self):
        self.stream_state = True

    def streamoff(self):
        self.stream_state = False

    def get_frame(self):
        while not self.ret:
            pass
        return self.frame
