from ._uniramp import Typeface
from termgraph import termgraph as tg

class Ramp:
    def __init__(self, args):
        self.DEFAULT_CHARSET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

        self.tf = Typeface(str(args.font))
        self.print_graph = args.graph
        self.character_set = list(set(args.character_set))
        if self.character_set is None or len(self.character_set) == 0:
            self.character_set = self.DEFAULT_CHARSET

    def get_ramp(self):
        ramp = sorted([(c, self.tf.get_coverage(ord(c))) for c in self.character_set], key=lambda x: x[1], reverse=True)
        return ramp

    def show_ramp(self):
        ramp = self.get_ramp()

        if not self.print_graph:
            print(''.join([c[0] for c in ramp]))
        else:
            labels = [c[0] for c in ramp]
            data = [[c[1]] for c in ramp]

            args = {'filename': '-', 'title': None, 'width': 50,
                    'format': '{:<.0f}', 'suffix': '', 'no_labels': False, 'no_values': False,
                    'color': None, 'vertical': False, 'stacked': False, 'histogram': False,
                    'different_scale': False, 'calendar': False,
                    'start_dt': None, 'custom_tick': '', 'delim': '',
                    'verbose': False, 'version': False}
            tg.chart([], data, args, labels)


