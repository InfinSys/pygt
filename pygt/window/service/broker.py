
""" Application Window Instace Service Broker """


#   EXTERNAL IMPORTS
pass


#   INTERNAL IMPORTS
from pygt.window.service import ServiceEndpoint


#   GLOBAL DEFINITIONS
pass


#   CLASSES
class WindowServiceBroker:
    """ Application window instance service broker. """
    def __init__(self) -> None:
        self.__services: dict[str, dict[str, ServiceEndpoint]] = {}

    def services(self) -> list[str]:
        """ Returns list of global window service endpoints. """
        return [service_id for service_id in self.__services.keys()]

    def is_existing_service(self, identifier: str) -> bool:
        """ Returns true if provided service identifer
        contains an endpoint context. """
        return identifier in self.__services.keys()

    def service_endpoint_context(self, identifier: str) -> dict[str, ServiceEndpoint]:
        """ Returns service endpoint context for provided identifier. """
        if not self.is_existing_service(identifier):
            return None

        return self.__services[identifier]

    def new(self, identifier: str, service: ServiceEndpoint, **extra) -> bool:
        """ Add new endpoint to global window services. """
        if self.is_existing_service(identifier):
            return False

        self.__new_service_key(identifier)
        self.__services[identifier]['endpoint'] = service

        if extra:
            extra.pop('endpoint')
            self.__services[identifier].update(extra)

        return True

    def request(self, service: str, **request_args) -> ServiceEndpoint:
        """ Returns requested service endpoint. """
        if not self.is_existing_service(service):
            return None

        return self.__services[service]['endpoint']

    def __new_service_key(self, identifier: str) -> None:
        self.__services[identifier] = {}
