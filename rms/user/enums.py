import enum


class Roles(enum.Enum):
    admin = 'admin'
    user = 'user'

    def __str__(self):
        return self.name  # value string

    def __html__(self):
        return self.value  # label string

