import enum


class Status(enum.Enum):
    New = 0
    Change = 1
    Release = 2
    Accept = 3
    Archive = 4

    def __str__(self):
        return self.name  # value string

    def __html__(self):
        return self.value  # label string