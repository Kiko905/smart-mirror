from backend_client import BackendApiClient
from services.face.interfaces import FaceMatcher


class BackendFaceMatcher(FaceMatcher):
    def __init__(self, client: BackendApiClient):
        self.client = client

    def identify_user(self, probe_encoding: list[float]) -> dict:
        return self.client.match_face(probe_encoding=probe_encoding)
