import argparse


class ArgParser:
    """
    Argument parser.

    Initialize to set up parsing rules.
    Use parse method to parse argumens.
    """

    def __init__(self):
        """Setting up parse rules here."""
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-cs', help='local or remote')
        self.parser.add_argument('-a', help='Action')
        self.parser.add_argument('-bt', help='Batch period')

    def parse(self):
        """Parsing arguments and creating attribute for each."""
        args = self.parser.parse_args()
        for key, value in args.__dict__.items():
            setattr(self, key, value)
        return self
