class FileLine:
    def __init__(self, index, **kwargs):
        print(f'{self}')
        self.filename = kwargs['filename']
        self.enable = kwargs['enable']
        self.x = kwargs['x']
        self.y = kwargs['y']
        self.tile = kwargs['tile']
        self.target_x = kwargs['target_x']
        self.target_tile = kwargs['target_tile']
        self.mergeline()

    def mergeline(self):
        self.line = {0: self.filename, 1: self.enable, 2: self.x, 3: self.y, 4: self.tile, 5: self.target_x, 6: self.target_tile}
        print(self.line)

