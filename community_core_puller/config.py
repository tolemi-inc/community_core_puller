from config_error import ConfigError


class Config:
    def __init__(
        self,
        dataset,
        dataset_name,
        start_date,
        end_date,
        community_core_username,
        community_core_password,
    ):
        self.dataset = dataset
        self.dataset_name = dataset_name
        self.start_date = start_date
        self.end_date = end_date
        self.community_core_username = community_core_username
        self.community_core_password = community_core_password

    @property
    def dataset(self):
        return self._dataset

    @dataset.setter
    def dataset(self, value):
        if value is None:
            raise ConfigError("Missing dataset path in config.")
        else:
            self._dataset = value

    @property
    def dataset_name(self):
        return self._dataset_name

    @dataset_name.setter
    def dataset_name(self, value):
        if value is None:
            raise ConfigError("Missing dataset name in config.")
        else:
            self._dataset_name = value

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        if value is None:
            raise ConfigError("Missing start date in config.")
        else:
            self._start_date = value

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        if value is None:
            raise ConfigError("Missing end date in config.")
        else:
            self._end_date = value

    @property
    def community_core_username(self):
        return self._community_core_username

    @community_core_username.setter
    def community_core_username(self, value):
        if value is None:
            raise ConfigError("Missing community core username in config")
        else:
            self._community_core_username = value

    @property
    def community_core_password(self):
        return self._community_core_password

    @community_core_password.setter
    def community_core_password(self, value):
        if value is None:
            raise ConfigError("Missing community core password in config")
        else:
            self._community_core_password = value
