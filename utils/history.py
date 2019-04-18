import csv
import os
from collections import defaultdict


class HistoryTracker:
    def __init__(self, save_path=None):
        self.history = defaultdict(list)
        self.save_path = save_path
        self.is_train = True

    def train(self):
        self.is_train = True

    def eval(self):
        self.is_train = False

    def step(self, metrics):
        reports = list()
        for k, v in metrics.items():
            k = k if self.is_train else f'val_{k}'
            self.history[k].append(v)
            reports.append('{} = {:.4f}'.format(k, v))

        return ', '.join(reports)

    def log(self):
        # metrics = [sum(r) / len(r) for r in self.history.values()]
        metrics = {
            k: sum(v) / len(v)
            for k, v in self.history.items()
            if k.startswith('val_') != self.is_train
        }
        return ', '.join('average {} = {:.4f}'.format(name, value)
                         for name, value in metrics.items()).capitalize()

    def save(self):
        """Save averaged metrics in this epoch to csv file."""

        metrics = [sum(r) / len(r) for r in self.history.values()]
        if not os.path.exists(self.save_path):
            # create a new csv file
            with open(self.save_path, 'w') as fp:
                writer = csv.writer(fp)
                writer.writerow(self.history.keys())
                writer.writerow(metrics)
        else:
            with open(self.save_path, 'a') as fp:
                writer = csv.writer(fp)
                writer.writerow(metrics)

    def clear(self):
        """Clear stored history."""

        self.history.clear()