__all__ = [
    'show_ramp'
]

def get_bar(ratio: float, width: int) -> str:
    BLOCK_CHARS = ['▏', '▎', '▍', '▌', '▋', '▊', '▉', '█']

    num_whole_char = int(ratio * width)
    remainder_width = ratio * width - num_whole_char
    partial_char_index = int(remainder_width * len(BLOCK_CHARS))

    bar = BLOCK_CHARS[-1] * num_whole_char
    if num_whole_char < width:
        bar += BLOCK_CHARS[partial_char_index]

    return bar

 
def show_ramp(coverage, print_graph: bool, width: int):
    if not print_graph:
        print(''.join([c[0] for c in coverage]))
    else:
        if width is None or width <= 0:
            width = 160
        for label, ratio in coverage:
            print('{}: {} {:.4f}'.format(label, get_bar(ratio, width), ratio))
