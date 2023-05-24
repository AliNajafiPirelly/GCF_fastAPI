from localpackage.types import Manageable, ServerStopType
from .types import APIConfig

class APIManager(Manageable):
    """
    Manages the configuration and server
    of the API.
    this
    """

    def __init__(self,config:APIConfig) -> None:
        self._config = config

    def pre_start(self):
        pass

    def post_start(self):
        pass

    def start(self):
        pass

    def pre_stop(self):
        pass

    def post_stop(self):
        pass

    def stop(self, stop_type: ServerStopType):
        pass


    def prepare_server(self):
        """
        prepares the server
        Returns:

        """

    def as_app(self):
        """
        return the created app instance
        Returns:

        """


