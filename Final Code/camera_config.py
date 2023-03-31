class CameraConfig():
    def __init__(self):
        self.config_done = False

    def set_config(self, initial_frame_area, coordinate_thresh, area_thresh):
        self.initial_frame_area = initial_frame_area
        self.coordinate_thresh = coordinate_thresh
        self.area_thresh = area_thresh

        self.config_done = True

    def check_config_status(self):
        return self.config_done
