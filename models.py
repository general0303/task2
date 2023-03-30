class Group:
    i = 1

    def __init__(self, name, description=None):
        self.id = Group.i
        self.name = name
        self.description = description
        self.participants = []
        Group.i += 1


class Participant:
    i = 1

    def __init__(self, name, wish=None):
        self.id = Participant.i
        self.name = name
        self.wish = wish
        self.recipient = None
        Participant.i += 1
