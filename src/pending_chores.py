from src.chore_handler_base import ChoreHandlerBase


class PendingChores(ChoreHandlerBase):
    def __init__(self):
        super().__init__('pending-chores.json')


