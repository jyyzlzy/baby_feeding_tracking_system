import abc
from datetime import datetime
from typing import List, Optional
from .base_feeding_tracking_system import BaseFeedingTrackingSystem

class LocalFeedingTrackingSystem(BaseFeedingTrackingSystem, abc.ABC):
    def __init__(
            self,
            filepath: str,
            *,
            datetime_format: Optional[str] = '%m/%d/%y %H:%M:%S',
            width: Optional[int] = 1000,
            height: Optional[int] = 800,
            primary_font_size: Optional[int] = 60,
            secondary_font_size: Optional[int] = 30,
            primary_text_location_x: Optional[int] = 200,
            primary_text_location_y: Optional[int] = 150,
            secondary_text_location_x: Optional[int] = 250,
            secondary_text_location_y: Optional[int] = 500,
            warning_text_location_x: Optional[int] = 100,
            warning_text_location_y: Optional[int] = 100,
        ) -> None:
        super().__init__(
            width=width,
            height=height,
            primary_font_size=primary_font_size,
            secondary_font_size=secondary_font_size,
            primary_text_location_x=primary_text_location_x,
            primary_text_location_y=primary_text_location_y,
            secondary_text_location_x=secondary_text_location_x,
            secondary_text_location_y=secondary_text_location_y,
            warning_text_location_x=warning_text_location_x,
            warning_text_location_y=warning_text_location_y,
        )
        self._filepath = filepath
        self._datetime_format = datetime_format

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
        self._save_data(feeding_times[:-1])
