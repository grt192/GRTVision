import cv2
from pipelines.pipeline_interface import PipelineInterface


class ExamplePipeline2(PipelineInterface):
    def __init__(self, name='0'):
        self.name = name
        self.cap = self.get_capture()
        self.frame = None

    def process(self):
        error_msg = None
        ret, self.frame = self.cap.read()

        # If frame was received, process the frame
        if ret:
            data = self.process_frame()

        # If no frame was received, re-capture
        else:
            self.cap = self.get_capture()
            error_msg = 'cannot get capture'

        return {'test': 'test!'}, error_msg

    def process_frame(self):
        cv2.circle(self.frame, (100, 100), 100, (0, 0, 255), 5)
        return {'test': 'test!'}

    def device_num(self):
        return 1

    def get_name(self):
        return self.name