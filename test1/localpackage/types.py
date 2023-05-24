import abc
from enum import Enum

from pydantic import BaseSettings, Field


class ServerStopType(Enum):

    TERMINATION = 0
    KILL = 1
    CLOSE = 2

class ServerStartType(Enum):
    PROCESS = 0
    THREAD = 1
    ASYNC = 2

class Manageable:

    @abc.abstractmethod
    def pre_start(self):
        pass
    @abc.abstractmethod
    def post_start(self):
        pass

    @abc.abstractmethod
    def start(self):
        """
        starts the API server
        """
        raise NotImplemented()
    @abc.abstractmethod
    def pre_stop(self):
        pass

    @abc.abstractmethod
    def post_stop(self):
        pass

    @abc.abstractmethod
    def stop(self, stop_type: ServerStopType = None):
        """
        stops the server based on the given
        stop type. to respect any stop methodology.
        """
        raise NotImplemented()



class GatewayConfig(BaseSettings):
    """
    Settings for a gateway.
    It can intrect with environment
    variables to as settings
    """

    version:int

    gateway_name : str = None

    api_name:str = Field(
        title="Target API Name ",
        description="The Target API that this gateway is going to handle"
        )
    start_api_header: str = Field(
        default= 'X-API-START',
        title="Start API Header",
        description="Start API header name to starting"
                     "the api by default : X-API-START"
                     )
    stop_api_header: str = Field(
        default= "X-API-STOP",
        title= "Stop API Header",
        description="Stop API header name to stoping"
                    "the api api default: X-API-STOP"
    )

    gateway_authorization: str = Field(
        default= "X-GATEWAY-AUTHORIZATION",
        title= "Gateway Authorization",
        description="Gateway authorization header name for authorizing the Admin privilege"
    )

    gateway_timeout : int|float = Field(
        default= 10,
        title= "Gateway Timeout",
        description="Request timeout in seconds"
    )


class APIConfig(BaseSettings):
    """
    Settings of the Target API.
    """

    name : str
    target_api_start_endpoint:str = Field(
        '/',
        title="Start Endpoint",
        description="Start endpoint of the api. in otherwords it is the base url of the api",
        )
    target_api_port : int = 8000
    target_api_host_url: str
    target_api_scheme: str

    target_api_with_thread: bool = Field(
        default= False,
        title="Start Target API Thread" ,
        description= "Start target API server in New Thread"
    )

    target_api_with_process: bool = Field(
        default= False,
        title="Start Target API Process" ,
        description= "Start target API server in new process"
    )

    target_api_with_async: bool = Field(
        default= False,
        title="Start Target API Async" ,
        description= "Start target API server with AsyncIO"
    )
