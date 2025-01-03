
""" Application Window Event Handler """


#   EXTERNAL IMPORTS
import tkinter as tk
from tkinter import Event


#   INTERNAL IMPORTS
pass


#   GLOBAL DEFINITIONS
pass


#   CLASSES
class WindowEventHandler:
    """ Application window instance event handler. """
    def __init__(self, bind_func, schedule_func) -> None:
        self.__bind_call = bind_func if callable(bind_func) else None
        self.__schedule_call = schedule_func if callable(schedule_func) else None
        self.__bindings: dict[str, list] = {}
        self.__binding_subs: dict[str, list[any]] = {}

    def get_binding(self, sequence: str) -> list:
        if sequence not in self.__bindings:
            return []

        return self.__bindings[sequence]

    def bind(self, sequence: str, func) -> None:
        if sequence in self.__bindings:
            self.__bindings[sequence].append(func)
            self.__bind_call(
                sequence=sequence,
                func=lambda e: self.__binding_wrapper(func, e),
                add='+'
            )
        else:
            self.__bindings[sequence] = [func]
            self.__bind_call(
                sequence=sequence,
                func=lambda e: self.__binding_wrapper(func, e),
                add=None
            )

    def forward_binding(self, sequence: str, func) -> None:
        if sequence.strip("<>") in self.__binding_subs:
            self.__binding_subs[sequence.strip("<>")].append(func)
        else:
            self.__binding_subs[sequence.strip("<>")] = [func]

    def schedule(self, func, delay: int) -> None:
        self.__schedule_call(ms=delay, func=func)

    def __binding_wrapper(self, func, event: Event) -> None:
        func(event)

        event_type: str = str(event.type.name)

        if event_type in self.__binding_subs.keys():
            for forward in self.__binding_subs[event_type]:
                forward(event)

    def __scheduled_execution_wrapper(self, func) -> None:
        pass
