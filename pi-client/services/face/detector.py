from services.face.interfaces import FaceDetector


class MockFaceDetector(FaceDetector):
    def capture_frame(self):
        return {
            "source": "mock-camera",
            "frame_id": "mock-frame-1",
        }


class CameraFaceDetector(FaceDetector):
    def capture_frame(self):
        # Hardware integration entrypoint for Raspberry Pi camera capture.
        return {
            "source": "camera",
            "frame_id": "placeholder-frame",
        }
