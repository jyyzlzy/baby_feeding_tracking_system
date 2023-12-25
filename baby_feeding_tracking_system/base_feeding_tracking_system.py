import abc
from datetime import datetime
import pygame
from pygame import QUIT, K_ESCAPE, K_SPACE, K_LCTRL, K_z
import sys
import time
from typing import List

class BaseFeedingTrackingSystem(abc.ABC):
    def __init__(
            self,
            *,
            width: int, 
            height: int, 
            primary_font_size: int,
            secondary_font_size: int,
            primary_text_location_x: int, 
            primary_text_location_y: int, 
            secondary_text_location_x: int, 
            secondary_text_location_y: int, 
        ) -> None:
        pygame.init()
        pygame.display.set_caption("Feeding Tracking System")
        self.screen = pygame.display.set_mode((width, height))
        self.font_primary = pygame.font.SysFont("arial", primary_font_size)
        self.font_secondary = pygame.font.SysFont("arial", secondary_font_size)
        self._primary_font_size = primary_font_size
        self._secondary_font_size = secondary_font_size
        self._primary_text_location_x = primary_text_location_x
        self._primary_text_location_y = primary_text_location_y
        self._secondary_text_location_x = secondary_text_location_x
        self._secondary_text_location_y = secondary_text_location_y

    def _print_text(self, font, x, y, text, color=None):
        if color is None:
            color = self.white
        img_text = font.render(text, True, color)
        self.screen.blit(img_text, (x, y))

    def _print_text_primary(self, x, y, text, color=None):
        self._print_text(self.font_primary, x, y, text, color)

    def _print_text_secondary(self, x, y, text, color=None):
        self._print_text(self.font_secondary, x, y, text, color)

    def _draw_primary(self):
        # primary text
        text_last = f'Last feeding: {self.past_feeding_times[-1].hour:02d}:{self.past_feeding_times[-1].minute:02d}:{self.past_feeding_times[-1].second:02d}'
        x_line1, y_line1 = self._primary_text_location_x, self._primary_text_location_y
        self._print_text_primary(x_line1, y_line1, text_last)

        text_next = f'Next feeding: {self.next_feeding_time.hour:02d}:{self.next_feeding_time.minute:02d}:{self.next_feeding_time.second:02d}'
        x_line2, y_line2 = x_line1, y_line1 + 1.5 * self._primary_font_size
        self._print_text_primary(x_line2, y_line2, text_next)

        text_now = f'Now: {self.now.hour:02d}:{self.now.minute:02d}:{self.now.second:02d}'
        color_now = self.white if self.now < self.next_feeding_time else self.red
        x_line3, y_line3 = x_line2, y_line2 + 1.5 * self._primary_font_size
        self._print_text_primary(x_line3, y_line3, text_now, color_now)

    def _draw_secondary(self):
        # secondary text
        text = "Earlier feeding times are:"
        x_line, y_line = self._secondary_text_location_x, self._secondary_text_location_y
        self._print_text_secondary(x_line, y_line, text)

        idx = len(self.past_feeding_times) - 1
        while idx >= 0:
            feeding_time = self.past_feeding_times[idx]
            text = f"{feeding_time.hour:02d}:{feeding_time.minute:02d}"
            y_line += 1.2 * self._secondary_font_size
            self._print_text_secondary(x_line, y_line, text)
            idx -= 1

    @abc.abstractmethod
    def get_past_feeding_times(self) -> List[datetime]:
        """return past few feeding times in sorted order"""
        pass

    @abc.abstractmethod
    def save_feeding_time(self, feeding_time: datetime) -> None:
        pass

    @abc.abstractmethod
    def erase_most_recent_feeding_time(self) -> None:
        pass

    def erase_most_recent_feeding_time_with_confirmation(self) -> None:
        self.screen.fill(self.black)
        text = "Erasing most recent feeding time"
        x_line, y_line = self._primary_text_location_x, self._primary_text_location_y
        self._print_text_primary(x_line, y_line, text, color=self.red)

        text = f"{self.past_feeding_times[-1]}"
        y_line += 1.5 * self._primary_font_size
        self._print_text_primary(x_line, y_line, text, color=self.red)

        text = "hold LCTRL and z to confirm"
        y_line += 1.5 * self._primary_font_size
        self._print_text_primary(x_line, y_line, text, color=self.red)
        self._draw_secondary()
        pygame.display.update()

        # get feedback
        keys = pygame.key.get_pressed()
        if keys[K_LCTRL] and keys[K_z]:
            self.erase_most_recent_feeding_time()
            time.sleep(0.3)

    @abc.abstractmethod
    def calculate_next_feeding_time(self, last_time: datetime) -> datetime:
        pass

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            keys = pygame.key.get_pressed()
            if keys[K_ESCAPE]:
                self.screen.fill((0, 0, 100))
                sys.exit()
            
            # append feeding time
            if keys[K_SPACE]:
                self.save_feeding_time(datetime.now())
                time.sleep(0.1)
                continue
            
            # fetch data
            self.past_feeding_times = self.get_past_feeding_times()
            self.next_feeding_time = self.calculate_next_feeding_time(self.past_feeding_times[-1])
            self.now = datetime.now()

            # erase most recent feeding time
            if keys[K_LCTRL]:
                self.erase_most_recent_feeding_time_with_confirmation()
                continue

            # draw and display
            self.screen.fill(self.black)
            self._draw_primary()
            self._draw_secondary()
            pygame.display.update()
    
    @property
    def white(self):
        return 255, 255, 255
    
    @property
    def black(self):
        return 0, 0, 0
    
    @property
    def red(self):
        return 255, 0, 0
    