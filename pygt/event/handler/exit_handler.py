
""" Base Exit Event Handler """


#   EXTERNAL IMPORTS
pass


#   INTERNAL IMPORTS
from pygt.window.service import ServiceEndpoint


#   GLOBAL DEFINITIONS
pass


#   CLASSES
class ExitHandler:
    """ Base exit event handler. """
    def __init__(self, final_call, post_exit_call=None) -> None:
        self.__exit_prerequisites: dict[str, ServiceEndpoint] = {}
        self.__final_exit = final_call if callable(final_call) else None
        self.__post_exit = post_exit_call if callable(post_exit_call) else None
        self.__rolling_index: int = 0

    def exit_prerequisites(self) -> list[str]:
        """ Returns list of exit requirement identifiers. """
        return [prerequisite_id for prerequisite_id in self.__exit_prerequisites.keys()]

    def is_existing_exit_prerequisite(self, identifier: str) -> bool:
        """ Returns true if a exit prerequisite exists with provided identifier. """
        return identifier in self.__exit_prerequisites.keys()

    def add_exit_prerequisite(self, task: ServiceEndpoint, identifier: str = None) -> bool:
        """ Add task to be completed before exit can occur. """
        if (identifier is not None) and self.is_existing_exit_prerequisite(identifier):
            return False

        if identifier is None:
            identifier = f"exit_prereq_{self.__rolling_index}"

        self.__exit_prerequisites[identifier] = task
        self.__rolling_index += 1

    def remove_exit_prerequisite(self, identifier: str) -> bool:
        """ Remove task from exit requirements. """
        if not self.is_existing_exit_prerequisite(identifier):
            return False

        del self.__exit_prerequisites[identifier]
        return True

    def do_forceful_exit(self) -> int:
        """ Forcefully exit, overriding exit prerequisites. """
        self.__final_exit()
        return 400

    def do_graceful_exit(self) -> int:
        """ Initiate exit sequence. """
        try:
            for prereq_id, prerequisite in self.__exit_prerequisites.items():
                prerequisite.execute()
        except Exception:
            return self.do_forceful_exit()

        self.__final_exit()
        return 0

    def post_exit(self, **kwargs) -> any:
        """ Initiate post exit sequence. """
        return self.__post_exit(**kwargs)
