from copy import deepcopy
import json
from helper.helper import get_base_directory, singleton
from models.config.config_model import ConfigModel


@singleton
class Config:
    __config_model: ConfigModel

    def __init__(self) -> None:
        self.__load()

    def __load(self) -> None:
        config_path = f"{get_base_directory()}/config.json"

        with open(config_path, "r") as config_file:
            self.__config_model = json.load(config_file, object_hook=lambda x: ConfigModel.from_json(x))

    def __save(self) -> None:
        config_path = f"{get_base_directory()}/config.json"

        with open(config_path, "w") as config_file:
            json.dump(self.__config_model.to_json(), config_file, indent=4)

    @property
    def config(self) -> ConfigModel:
        return deepcopy(self.__config_model)
