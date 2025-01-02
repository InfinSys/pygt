
""" Standalone Application Window Service """


#   EXTERNAL IMPORTS
pass


class WindowService:
    def __init__(self, func, **func_args) -> None:
        self.__func = func if callable(func) else None
        self.__args: dict = func_args

    def endpoint(self) -> any:
        return self.__func

    def execute(self, **kwargs) -> any:
        if not kwargs:
            return self.__func(**self.__args)
        else:
            return self.__func(**kwargs)
