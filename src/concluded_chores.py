from src.chore_handler_base import ChoreHandlerBase


class ConcludedChores(ChoreHandlerBase):
    def __init__(self):
        super().__init__('concluded-chores.json')

    def clean_up(self):
        pass
