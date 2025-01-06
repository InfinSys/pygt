
""" Application View Event Handler """


#   EXTERNAL IMPORTS
from tkinter import Event


#   INTERNAL IMPORTS
pass


#   GLOBAL DEFINITIONS
pass


#   CLASSES
class ViewEventHandler:
    """ Application view event handler. """
    def __init__(self, bind_call, schedule_call) -> None:
        self.__bind_call = bind_call if callable(bind_call) else None
        self.__schedule_call = schedule_call if callable(schedule_call) else None
        self.__bindings: dict[str, dict[str, any]] = {}
        self.__binding_subs: dict[str, list[dict[str, any]]] = {}

    def bound_sequences(self) -> list[str]:
        """ Returns list of sequences view is bound to. """
        return [sequence for sequence in self.__bindings.keys()]

    def forwarded_sequences(self) -> list[str]:
        """ Returns list of bound sequences that are
        forwarded to other components. """
        return [sequence for sequence in self.__binding_subs.keys()]

    def is_existing_definition(self, sequence: str) -> bool:
        """ Returns true if provided sequence
        contains an existing binding definition. """
        return sequence in self.__bindings.keys()

    def bindings(self) -> list[str]:
        """ Returns list of binding identifiers. """
        binding_ids: list[str] = []

        for _, bind_def in self.__bindings.items():
            binding_ids.extend(bind_def.keys())

        return binding_ids

    def is_existing_identifier(self, identifier: str) -> bool:
        """ Returns true if a binding exist with provided identifier. """
        return identifier in self.bindings()

    def forwarded_bindings(self) -> list[str]:
        """ Returns list of binding identifiers that are
        forwarded to other components. """
        binding_ids: list[str] = []

        for sequence in self.__binding_subs.keys():
            binding_ids.extend(self.__bindings[sequence].keys())

        return binding_ids

    def get_binding_definition(self, sequence: str) -> dict[str, any]:
        """ Returns binding ids and their defined commands. """
        if sequence not in self.__bindings:
            return []

        return self.__bindings[sequence]

    def get_binding(self, identifier: str, sequence: str = None) -> any:
        """ Returns binding command. """
        if sequence is not None:
            if type(self.__bindings[sequence][identifier]) is dict:
                return self.__bindings[sequence][identifier]['cmd']
            return self.__bindings[sequence][identifier]
        else:
            for _, bind_def in self.__bindings.items():
                if identifier not in bind_def.keys():
                    continue
                elif (identifier in bind_def.keys()) and (type(bind_def[identifier]) is dict):
                    return bind_def[identifier]['cmd']
                else:
                    return bind_def[identifier]

        return None

    def bind(self, sequence: str, cmd, identifier: str = None, **extra) -> bool:
        """ Bind event to view. """
        if (identifier is None) or (identifier.strip() == ""):
            identifier = "not_sure_yet"

        sequence = self.__format_sequence_str(sequence)
        identifier = self.__format_binding_identifier(identifier)

        bind_args: dict = {
            'sequence': sequence,
            'func': None,
            'add': "+"
        }

        if not self.is_existing_definition(sequence):
            self.__new_bind_definition(sequence)
            bind_args['add'] = None
        elif self.is_existing_identifier(identifier):
            return False

        if not extra:
            bind_args['func'] = lambda e: self.__binding_wrapper(func=cmd, event=e, sequence=sequence)
            self.__bindings[sequence][identifier] = {'cmd': cmd}
        else:
            bind_args['func'] = lambda e: self.__binding_wrapper(func=cmd, event=e, sequence=sequence, **extra)
            self.__new_extended_option_binding(
                sequence=sequence,
                identifier=identifier,
                cmd=cmd,
                **extra
            )

        self.__bind_call(**bind_args)

        return True

    def forward(self, sequence: str, func, **call_args) -> bool:
        """ Forward view event on occurrence to provided function. """
        sequence = self.__format_sequence_str(sequence)

        if not self.is_existing_definition(sequence):
            return False

        if not self.__is_existing_subscription_group(sequence):
            self.__new_subscription_group(sequence)

        self.__binding_subs[sequence].append({'call': func})

        if call_args:
            self.__binding_subs[sequence][-1].update({'args': call_args})

        return True

    def schedule(self, func, delay: int) -> None:
        """ Schedule function for execution n milliseconds from now. """
        self.__schedule_call(ms=delay, func=lambda: self.__scheduled_execution_wrapper(func))

    def __is_existing_subscription_group(self, sequence: str) -> bool:
        return sequence in self.__binding_subs.keys()

    def __new_bind_definition(self, sequence: str) -> None:
        self.__bindings[sequence] = {}

    def __new_subscription_group(self, sequence: str) -> None:
        self.__binding_subs[sequence] = []

    def __binding_wrapper(self, func, event: Event, sequence: str, **fargs) -> None:
        func(event, **fargs.get('args', {}))

        if not self.__is_existing_subscription_group(sequence):
            return

        for subscription in self.__binding_subs[sequence]:
            self.__forward_event(subscription=subscription, event=event)

    def __new_extended_option_binding(self, sequence: str, identifier: str, cmd, **extra) -> None:
        if type(extra.get('args')) is dict:
            self.__bindings[sequence][identifier] = {
                'cmd': cmd,
                'args': extra.pop('args')
            }
        else:
            self.__bindings[sequence][identifier] = {'cmd': cmd}

        self.__bindings[sequence][identifier].update(extra)

    @staticmethod
    def __scheduled_execution_wrapper(func) -> None:
        func()

    @staticmethod
    def __format_binding_identifier(identifier: str) -> str:
        return identifier.lower().replace(' ', '_')

    @staticmethod
    def __format_sequence_str(sequence: str) -> str:
        if not sequence.startswith('<'):
            sequence = f"<{sequence}"

        if not sequence.endswith('>'):
            sequence = f"{sequence}>"

        return sequence

    @staticmethod
    def __forward_event(subscription: dict, event: Event) -> None:
        """ Forward event to subscriber. """
        if type(subscription.get('args')) is dict:
            subscription['call'](event=event, **subscription.get('args'))
        else:
            subscription['call'](event=event)
