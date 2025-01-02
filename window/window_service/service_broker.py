
""" Application Window Service Broker """


#   EXTERNAL IMPORTS
from window.window_service import WindowService


class WindowServiceBroker:
    def __init__(self, instance_hash: int) -> None:
        self.__owner_hash: int = instance_hash if type(instance_hash) is int else None
        self.__services: dict[str, WindowService] = {}

    def services(self) -> list[str]:
        return [service_name for service_name in self.__services.keys()]

    def new_service(self, name: str, service: WindowService) -> bool:
        if name in self.services():
            return False

        self.__services[name] = service

        return True

    def request(self, service: str) -> any:
        if service not in self.services():
            return None

        return self.__services[service].endpoint()

    def get(self, service: str) -> WindowService:
        if service not in self.services():
            return None

        return self.__services[service]
