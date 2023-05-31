from localpackage.types import Manageable, ServerStopType
from .types import APIConfig
from fastapi.applications import AppType
from threading import Thread
import uvicorn
from .errors import APIDidntStartedYet,APIDidntStoppedYet

class APIManager(Manageable):
    """
    Manages the configuration and server
    of the API.
    this
    """

    def __init__(self,config:APIConfig,app:AppType) -> None:
        self._config = config
        self.app = app
        self.server_thread :Thread = None

    @property
    def started(self):
        return self.server_thread.is_alive()

    def pre_start(self):
        pass

    def post_start(self):
        pass

    def start(self):
        self.pre_start()
        self.server_thread = self.prepare_server()
        self.server_thread.start()
        self.post_start()

    def pre_stop(self,stop_type: ServerStopType):
        if not self.server_thread:
            raise APIDidntStartedYet()

    def post_stop(self,stop_type: ServerStopType):
        if self.server_thread.is_alive():
            raise APIDidntStoppedYet()

    def stop(self, stop_type: ServerStopType):
        self.pre_stop(stop_type)
        self.server_thread.join(timeout=5)
        self.post_stop(stop_type)

    def prepare_server(self):
        """
        prepares the server
        Returns:

        """
        th = Thread(
            name=f"{self.app.title}-app-thread",
            target= uvicorn.run,
            kwargs= self.get_server_config()
        )
        return th

    def get_server_config(self):
        return {
            'host':self._config.target_api_host_url,
            'port':self._config.target_api_port,
            'app' : 'main:app'
        }

    def as_app(self):
        """
        return the created app instance
        Returns:

        """
        return self.app

    def __del__(self):
        print('API Deleting')
        self.stop(ServerStopType.CLOSE)

