import cv2

CAMERA_PORTS = []
CAMERAS = {}


def get_cameras():
    global CAMERA_PORTS
    non_working_ports = []
    test_port = 0
    working_ports = []

    while len(non_working_ports) < 4:
        camera = cv2.VideoCapture(test_port)
        if not camera.isOpened():
            non_working_ports.append(test_port)
            print("Port {0} is not working".format(test_port))
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if is_reading:
                print("Camera at port {0} is available with capture res {1} x {2}".format(test_port, w, h))
                working_ports.append(test_port)
                camera.release()
        test_port += 1

    CAMERA_PORTS = working_ports
    return working_ports, non_working_ports


def load_cameras():
    global CAMERA_PORTS
    global CAMERAS

    for port in CAMERA_PORTS:
        CAMERAS[port] = cv2.VideoCapture(port)


def release_cameras():
    global CAMERAS
    global CAMERA_PORTS

    for port in CAMERA_PORTS:
        CAMERAS[port].release()

    CAMERAS.clear()


class CamManager:

    def __init__(self):

        release_cameras()
        get_cameras()
        load_cameras()

        self.num_cams = len(CAMERA_PORTS)
        self.current_cam = 0
        self.recent_images = {}

        for port in CAMERA_PORTS:
            frame = self.get_image_gray_blurred(port)
            self.recent_images[port] = frame

    def next_camera(self):
        self.current_cam = (self.current_cam + 1) % self.num_cams

    def camera_valid(self, cameraID):

        if not cameraID in CAMERA_PORTS:
            raise Exception("Invalid camera id " + cameraID)

        return CAMERAS[cameraID].isOpened()

    def update_cameras(self):

        release_cameras()
        get_cameras()
        load_cameras()

        self.recent_images.clear()

        self.num_cams = len(CAMERA_PORTS)

        if not (self.current_cam in CAMERA_PORTS):
            self.current_cam = 0  # camera got disconnected?

    def get_camera_resolution(self, cameraID=None):

        if cameraID is None:
            cameraID = self.current_cam

        if not self.camera_valid(cameraID):
            raise Exception("Invalid camera id " + cameraID)

        return CAMERAS[cameraID].get(3), CAMERAS[cameraID].get(4)

    def get_image(self, cameraID=None):

        if cameraID is None:
            cameraID = self.current_cam

        if not self.camera_valid(cameraID):
            raise Exception("Invalid camera id " + cameraID)

        ret, frame = CAMERAS[cameraID].read()

        while not ret:
            ret, frame = CAMERAS[cameraID].read()

        return ret, frame

    def update_recent_image(self):
        frame = self.get_image_gray_blurred(self.current_cam)
        self.recent_images[self.current_cam] = frame

    def get_image_gray_blurred(self, cameraID):

        ret, frame = self.get_image(cameraID)

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.GaussianBlur(frame, (21, 21), 0)

        return frame

    def get_recent_image(self):
        return self.recent_images[self.current_cam]

    def shutdown_camera_manager(self):
        release_cameras()