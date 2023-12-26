import abc
from datetime import datetime
from typing import List, Dict
from .base_feeding_tracking_system import BaseFeedingTrackingSystem

class LocalFeedingTrackingSystem(BaseFeedingTrackingSystem, abc.ABC):
    def __init__(self, config: Dict) -> None:
        super().__init__(config)
        self._filepath = config['data_filepath']
        self._datetime_format = config['datetime_format']

    def _load_data(self) -> List[datetime]:
        past_feeding_times = []
        with open(self._filepath, 'r') as f:
            for line in f.readlines():
                past_feeding_times.append(datetime.strptime(line[:-1], self._datetime_format))
        past_feeding_times.sort()
        return past_feeding_times
    
    def _save_data(self, feeding_times: List[datetime]) -> None:
        with open(self._filepath, 'w') as f:
            for feeding_time in feeding_times:
                f.write(feeding_time.strftime(self._datetime_format))
                f.write('\n')

    def get_past_feeding_times(self) -> List[datetime]:
        """return past few feeding times in sorted order"""
        past_feeding_times = self._load_data()
        if len(past_feeding_times) > 5:
            past_feeding_times = past_feeding_times[-5:]
        return past_feeding_times
    
    def save_feeding_time(self, feeding_time: datetime) -> None:
        feeding_times = self._load_data()
        if len(feeding_times) > 100:
            feeding_times = feeding_times[-100:]
        feeding_times.append(feeding_time)
        self._save_data(feeding_times)

    def erase_most_recent_feeding_time(self) -> None:
        feeding_times = self._load_data()
        if len(feeding_times) == 0:
            return
        self._save_data(feeding_times[:-1])
