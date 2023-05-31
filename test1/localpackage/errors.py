class GatewayError(Exception):

    def __init__(self,reason:str=None,code:int=None,*args):
        super(GatewayError, self).__init__(*args)
        self.reason = reason
        self.code = code

    def __str__(self):
        return f"{self.reason}({self.code})"

class InvalidGatewayAdmin(GatewayError):
    def __init__(self,reason="Invalid gateway admin"):
        super(InvalidGatewayAdmin, self).__init__(reason=reason,code=10)

class InvalidAPIKey(GatewayError):
    def __init__(self,reason="Invalid API key"):
        super(InvalidAPIKey, self).__init__(reason=reason,code=11)

class QuotaError(GatewayError):
    def __init__(self,reason="Number of requests limit reached"):
        super(QuotaError, self).__init__(reason,code=12)


class APIError(Exception):
    def __init__(self,reason:str,code:int,*args):
        super(APIError, self).__init__(*args)
        self.reason = reason
        self.code = code

    def __str__(self):
        return f"APIError: {self.reason}({self.code})"

class APIDidntStartedYet(APIError):
    """
    this error happens when api didn't start
    properly
    """
    def __init__(self):
        super(APIDidntStartedYet, self).__init__(reason="API didn't started yet",code=600)

class APIDidntStoppedYet(APIError):

    def __init__(self):
        super(APIDidntStoppedYet, self).__init__(reason="API didn't stopped yet",code=601)


