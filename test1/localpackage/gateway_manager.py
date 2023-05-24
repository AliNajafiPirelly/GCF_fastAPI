from requests import Response,request as make_response
import requests
from flask import Request as FlaskRequest , Response as FlaskResponse

from localpackage.api_manager import APIManager
from localpackage.types import  GatewayConfig, APIConfig
from .errors import GatewayError


class GatewayManager:
    """
    This class is responsible to handle
    API Gateway. it can start , stop and config
    the API . 
    """

    def __init__(self, config: GatewayConfig, api_manager: APIManager):
        self._config = config
        self.started = False
        self._api_manager = api_manager
    
    @property
    def api_name(self):
        return self.api_config.name
    
    @property
    def gateway_name(self):
        return self._config.gateway_name
    @property
    def api_start_end_point(self):
        return self.api_config.target_api_start_endpoint
    
    @property
    def api_config(self) -> APIConfig:
        return self._api_manager._config
    
    @property
    def gateway_config(self) -> GatewayConfig:
        return self._config

    def _check_security(self,request:FlaskRequest):
        """
        checks the api key and admin authorization
        Returns:
        """
        admin_token = request.headers.get(self.gateway_config.gateway_authorization,'')
        if not admin_token:
            from .errors import InvalidGatewayAdmin
            raise InvalidGatewayAdmin()
        self._check_admin(admin_token)
        self._check_api_key("")

    def _check_header(self, request:FlaskRequest):
        """
        check and validate headers base on config
        and return dict of headers
        Args:
            header:

        Returns:

        """
        pass

    def _check_admin(cls, token:str):
        pass

    def _check_api_key(self, key:str):
        pass

    def _handle_files(self, files):
        pass

    def _extract_endpoint(self, request:FlaskRequest):
        pass

    def _handle_cookies(self,request:FlaskRequest):
        pass

    def handle_request(self,flask_request:FlaskRequest):
        """
        handles the GCF request(Flask)
        that api understands it
        Returns:

        """
        headers = self._check_header(flask_request)
        data = self.extract_data(flask_request)
        files = self._handle_files(flask_request)
        endpoint = self._extract_endpoint(flask_request)
        scheme = flask_request.scheme
        host = self.api_config.target_api_host_url
        port = self.api_config.target_api_port
        method = flask_request.method.lower()
        cookies = self._handle_cookies(flask_request)
        params = flask_request.args

        request_params = self._request_factory(
            kwargs_only=True,
            headers=headers,
            data=data,
            files=files,
            endpoint=endpoint,
            scheme=scheme,
            host=host,
            port=port,
            method=method,
            cookies = cookies,
            params = params
        )
        methods = {
            'post' : requests.post,
            'get' : requests.get,
            'put' : requests.put,
            'patch': requests.patch,
            'options': requests.options
        }

        response = methods[method](**request_params)
        return self.handle_response(response)

    def handle_response(self,response:Response):
        """handles the response from api """
        res = FlaskResponse(
            headers=response.headers,
            status=response.status_code,
            response=response.content ,
            content_type= response.headers.get('Content-type')
        )
        return res


    def _request_factory(self,kwargs_only=False,*args,**kwargs) -> Response|dict:
        """integrate with python requests module"""
        host = kwargs.pop('host')
        port = kwargs.pop('port')
        endpoint = kwargs.pop('endpoint')
        scheme = kwargs.pop('scheme')
        headers = kwargs.pop('headers')

        #sanitize the headers from gateway headers
        if headers.get(self.gateway_config.start_api_header):
            headers.pop(self.gateway_config.start_api_header)

        if headers.get(self.gateway_config.stop_api_header):
            headers.pop(self.gateway_config.stop_api_header)

        if headers.get(self.gateway_config.gateway_authorization):
            headers.pop(self.gateway_config.gateway_authorization)

        #create full path
        full_path = f"{scheme}://{host}{':' + str(port) if port else ''}{endpoint}"

        kw = {
            **kwargs,
            'url' : full_path,
            'timeout' : self.gateway_config.gateway_timeout,
        }
        if kwargs_only:
            kwargs.pop('method')
            return kw

        return make_response(**kw)

    def _handel_api(self,request:FlaskRequest):
        """
        handles the api start and stop
        Returns:
        """
        headers = {k: request.headers.get(k) for k in request.headers.keys(lower=True) }

        start_header = self.gateway_config.start_api_header.lower()
        stop_header = self.gateway_config.stop_api_header.lower()

        auth_header = self.gateway_config.gateway_authorization.lower()

        if not headers.get(stop_header) and not headers.get(start_header):
            return

        elif start_header in headers and stop_header in headers:
            raise GatewayError(reason="Both start and stop operation command sent",code=15)

        elif not headers.get(stop_header) and not headers.get(start_header) and not self.started:
            raise GatewayError(reason="API is not running.",code=16)

        if headers.get(stop_header) == '1':
            self._check_admin(headers.get(auth_header))
            self.stop_api()

        if headers.get(start_header) == '1':
            self._check_admin(headers.get(auth_header))
            self.start_api()


    def manage(self,flask_request:FlaskRequest):
        """
        is for managing the request to the api
        Args:
            flask_request:

        Returns: FlaskResponse

        """
        try:
            self._handel_api(flask_request)
            return self.handle_request(flask_request)
        except Exception as err:
            print("error happened : ",err)
            return self._get_message(err)


    def start_api(self):
        if not self.started:
            self._api_manager.start()
            self.started = True
            return
        raise GatewayError(reason="API already started",code=13)

    def stop_api(self):
        if self.started:
            self._api_manager.stop()
            self.started = False
            return

        raise GatewayError(reason="API already stopped",code=14)


    def _get_message(self,err):
        from .errors import GatewayError
        message = {}

        if isinstance(err,GatewayError):
            message['reason'] = err.reason
            message['code'] = err.code
            return message,400
        else:
            return "",500


    
    
