from abc import ABC, abstractmethod
from typing import Optional


class FaceDetector(ABC):
    @abstractmethod
    def capture_frame(self) -> Optional[dict]:
        raise NotImplementedError


class FaceEncoder(ABC):
    @abstractmethod
    def encode(self, frame: dict) -> list[float]:
        raise NotImplementedError


class FaceMatcher(ABC):
    @abstractmethod
    def identify_user(self, probe_encoding: list[float]) -> dict:
        raise NotImplementedError
