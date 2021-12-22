from ._uniramp import Typeface

class Coverage:
    def __init__(self, args):
        self.DEFAULT_CHARSET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.tf = Typeface(str(args.font))
        if args.character_set is None or len(args.character_set) == 0:
            self.character_set = self.DEFAULT_CHARSET
        else:
            self.character_set = list(set(args.character_set))

    def get_coverage(self):
        coverage = sorted([(c, self.tf.get_coverage(ord(c))) for c in self.character_set], key=lambda x: x[1], reverse=True)
        return coverage
