class Action:
    _type = None

    @classmethod
    def set(cls, value):
        cls._type = value

    @classmethod
    def get(cls):
        return cls._type

    @classmethod
    def input(cls, value):
        print('Input action type:')
        cls._type = input()
        print('Action type is set {}'.format(cls._type))
