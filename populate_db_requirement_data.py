from rms.requirements.models import RequirementTypes, RequirementPriority, RequirementStatuses
from rms.db import db
from rms import create_app

app = create_app()

with app.app_context():
    new_req_types = [
        RequirementTypes(type="черновик"),
        RequirementTypes(type="функциональное требование"),
        RequirementTypes(type="не функциональное требование")
    ]

    for type in new_req_types:
        db.session.add(type)

    new_req_statuses = [
        RequirementStatuses(status="утверждено"),
        RequirementStatuses(status="отклонено"),
        RequirementStatuses(status="на рассмотрении")
    ]

    for status in new_req_statuses:
        db.session.add(status)

    new_req_priorities = [
        RequirementPriority(priority="высокий"),
        RequirementPriority(priority="низкий"),
        RequirementPriority(priority="средний")
    ]

    for priority in new_req_priorities:
        db.session.add(priority)
    db.session.commit()
