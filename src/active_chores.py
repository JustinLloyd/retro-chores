from src.chore_handler_base import ChoreHandlerBase


class ActiveChores(ChoreHandlerBase):
    def __init__(self):
        super().__init__('active-chores.json')

    def complete(self):
        pass

    def uncomplete(self):
        pass

    # skip a chore
    def skip(self):
        pass

