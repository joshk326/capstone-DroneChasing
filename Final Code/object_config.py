class ObjectConfig():
    def __init__(self):
        self.detected = False
        self.area_thresh = 0
        self.coordinate_thresh = 0
        self.initial_frame_area = 0
        self.intiali_box_dimensions = 0
    def set_config(self, initial_frame_area, intail_box_dim, coordinate_thresh, area_thresh):
        self.initial_frame_area = initial_frame_area
        self.coordinate_thresh = coordinate_thresh
        self.area_thresh = area_thresh
        self.intial_box_dimensions = intail_box_dim
    def check_detected_status(self):
        return self.detected
    def get_area_thresh(self):
        return self.area_thresh
    def get_intial_area(self):
        return self.initial_frame_area
    def update_detected_status(self, status):
        self.detected = status
