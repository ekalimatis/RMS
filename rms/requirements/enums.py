import enum


class Requirement_status(enum.Enum):
    new = 'new'
    on_review = 'on_review'
    active = 'active'
    old = 'old'
    changed = 'changed'