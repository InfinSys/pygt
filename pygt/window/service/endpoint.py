
""" Standalone Application Window Service Endpoint """


#   EXTERNAL IMPORTS
pass


#   INTERNAL IMPORTS
pass


#   GLOBAL DEFINITIONS
pass


#   CLASSES
class ServiceEndpoint:
    """ Standalone application service endpoint. """
    def __init__(self, func, **func_args) -> None:
        self.__func = func if callable(func) else None
        self.__args: dict = func_args

    def is_callable(self) -> bool:
        """ Returns true if service endpoint is callable. """
        return (self.__func is not None) and (callable(self.__func))

    def endpoint(self) -> any:
        """ Returns underlying function pointer. """
        return self.__func

    def execute(self, **override_args) -> any:
        """ Execute endpoint. """
        ex_response: any = None

        if not override_args:
            ex_response = self.__func(**self.__args)
        else:
            ex_response = self.__func(**override_args)

        return ex_response

    def __call__(self, *args, **kwargs) -> any:
        """ Execute endpoint. """
        return self.__func(*args, **kwargs)
