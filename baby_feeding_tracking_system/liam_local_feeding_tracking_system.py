from datetime import datetime, timedelta
import os
from .local_feeding_tracking_system import LocalFeedingTrackingSystem

class LiamLocalFeedingTrackingSystem(LocalFeedingTrackingSystem):
    def calculate_next_feeding_time(self, last_time: datetime) -> datetime:
        next_time = last_time + timedelta(hours=3)
        if next_time.hour >= 0 and next_time.hour <= 6:
            next_time = datetime(next_time.year, next_time.month, next_time.day, 7)
        return next_time
    
def main():
    filepath = os.path.join(os.getcwd(), 'data.txt')
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            f.write('07/26/23 17:40:00\n')
    fts = LiamLocalFeedingTrackingSystem(filepath)
    fts.run()

if __name__ == "__main__":
    main()
