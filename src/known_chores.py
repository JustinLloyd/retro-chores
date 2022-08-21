from src.chore_handler_base import ChoreHandlerBase


class KnownChores(ChoreHandlerBase):
    def __init__(self):
        super().__init__('chores.json')

