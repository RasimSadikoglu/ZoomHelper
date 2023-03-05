from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from models.config.update_schedule import UpdateSchedule

from models.time.weekday import WeekDay


@dataclass
class ConfigModel:
    start_time_offset: int
    end_time_offset: int
    auto_delete: bool
    hide_terminal: bool
    first_setup: bool
    auto_update: UpdateSchedule
    force_update: bool
    last_update_check: WeekDay
    open_free_meetings: bool

    def to_json(self) -> dict[str, Any]:  # TODO: generalized json encoder and decoder
        return {
            "start_time_offset": self.start_time_offset,
            "end_time_offset": self.end_time_offset,
            "auto_delete": self.auto_delete,
            "hide_terminal": self.hide_terminal,
            "first_setup": self.first_setup,
            "auto_update": self.auto_update.value,
            "force_update": self.force_update,
            "last_update_check": self.last_update_check.value,
            "open_free_meetings": self.open_free_meetings,
        }

    @staticmethod
    def from_json(json: dict) -> ConfigModel:
        return ConfigModel(
            json["start_time_offset"],
            json["end_time_offset"],
            json["auto_delete"],
            json["hide_terminal"],
            json["first_setup"],
            UpdateSchedule(json["auto_update"]),
            json["force_update"],
            WeekDay(json["last_update_check"]),
            json["open_free_meetings"],
        )
