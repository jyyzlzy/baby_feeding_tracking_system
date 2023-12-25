from datetime import datetime, timedelta
from .local_feeding_tracking_system import LocalFeedingTrackingSystem

class LiamLocalFeedingTrackingSystem(LocalFeedingTrackingSystem):
    def calculate_next_feeding_time(self, last_time: datetime) -> datetime:
        next_time = last_time + timedelta(hours=3)
        if next_time.hour >= 1 and next_time.hour <= 6:
            next_time = datetime(next_time.year, next_time.month, next_time.day, 7)
        return next_time