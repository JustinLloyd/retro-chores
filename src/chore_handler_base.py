import json

from src.chore import Chore


class ChoreHandlerBase:
    def __init__(self, filename):
        self.chores = []
        self.filename = filename
        self.__load_chores__()

    def __load_chores__(self):
        try:
            chore_data = None
            self.chores.clear()
            with open(self.filename) as f:
                chore_data = json.load(f)
            f.close()
            self.chores = [Chore.from_dict(item) for item in chore_data['chores']]
        except Exception:
            return
        # for item in chore_data['chores']:
        #     chore = Chore.from_dict(item)
        #     self.chores.append(chore)

    def __save_chores__(self):
        chores_dict = {'chores': [chore.to_dict() for chore in self.chores]}

        with open(self.filename, 'w') as f:
            json.dump(chores_dict, f, indent=4)
        f.close()

    def add(self, chore):
        self.chores.append(chore)
        self.__save_chores__()

    def remove(self, chore):
        self.chores.remove(chore)
        self.__save_chores__()

    def get(self, idx):
        return self.chores[idx]