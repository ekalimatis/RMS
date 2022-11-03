import enum


class Status(enum.Enum):
    new = 0
    change = 1
    release = 2
    accept = 3
    archive = 4

    def __str__(self):
        return self.name  # value string

    def __html__(self):
        return self.value  # label string