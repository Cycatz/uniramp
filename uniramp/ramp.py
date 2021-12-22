from termgraph import termgraph as tg


def show_ramp(coverage, print_graph: bool):
    if not print_graph:
        print(''.join([c[0] for c in coverage]))
    else:
        labels = [c[0] for c in coverage]
        data = [[c[1]] for c in coverage]

        args = {'filename': '-', 'title': None, 'width': 50,
                'format': '{:<.0f}', 'suffix': '', 'no_labels': False, 'no_values': False,
                'color': None, 'vertical': False, 'stacked': False, 'histogram': False,
                'different_scale': False, 'calendar': False,
                'start_dt': None, 'custom_tick': '', 'delim': '',
                'verbose': False, 'version': False}
        tg.chart([], data, args, labels)


