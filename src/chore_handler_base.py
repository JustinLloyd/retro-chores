import json
import cfg
import evt

from src.chore import Chore
from util import ee


class ChoreHandlerBase:
    def __init__(self, filename: str):
        self.filename = filename
        self._chores = []
        self.__load_chores__()

    def __load_chores__(self):
        try:
            filepath = 'data/' + self.filename
            with open(filepath) as f:
                chore_data = json.load(f)
            f.close()
            self._chores = [Chore.from_dict(item) for item in chore_data['chores']]
        except Exception:
            self._chores = []
        # for item in chore_data['chores']:
        #     chore = Chore.from_dict(item)
        #     self.chores.append(chore)

    def _save_chores(self):
        chores_dict = {'chores': [chore.to_dict() for chore in self._chores if chore is not None and not chore.is_complete()]}
        try:
            filepath = 'data/' + self.filename
            with open(filepath, 'w') as f:
                json.dump(chores_dict, f, indent=4)
            f.close()
        except Exception:
            pass

    def append(self, chore):
        self._chores.append(chore)
        self._save_chores()
        ee.emit(evt.CHORE_ADDED, chore)

    # def add(self, chore):
    #     self.chores.append(chore)
    #     self._save_chores__()
    #
    # def remove(self, chore):
    #     self.chores.remove(chore)
    #     self._save_chores__()
    #
    # def get(self, idx):
    #     return self.chores[idx]

    def count(self):
        return len(self._chores)
