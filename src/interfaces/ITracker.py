from abc import ABC, abstractmethod


class ITracker(ABC):
    @abstractmethod
    def get_position(self):
        """Get the current tracking position."""
        pass

    @abstractmethod
    def display(self, image):
        """Display the tracking visualization."""
        pass

    @abstractmethod
    def release(self):
        """Release any resources held by the tracker."""
        pass
