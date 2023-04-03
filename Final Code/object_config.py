class ObjectConfig():
    def __init__(self):
        self.detected = False

    def set_config(self, initial_frame_area, coordinate_thresh, area_thresh):
        self.detected = True
        self.initial_frame_area = initial_frame_area
        self.coordinate_thresh = coordinate_thresh
        self.area_thresh = area_thresh

    def check_detected_status(self):
        return self.detected
