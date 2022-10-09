from datetime import datetime

from sqlalchemy_mptt import tree_manager

from rms import db
from rms.projects.models import Project
from rms.requirements.models import RequirementTree, Requirement


def save_project_in_bd(form):
    project = Project(
        name = form.name.data,
        description = form.description.data
    )

    root_requirement_tree_node = RequirementTree()
    tree_manager.register_events(remove=True)
    root_requirement_tree_node.left = 0
    root_requirement_tree_node.right = 0

    root_requirement = Requirement(
        name = 'Коренвое требование проекта',
        description = f'Проект - "{form.name.data}"',
        created_date = datetime.utcnow(),
        update_date = datetime.utcnow(),
        version = '1.0.0'
    )

    root_requirement_tree_node.requirements.append(root_requirement)
    project.requirement_tree_nodes.append(root_requirement_tree_node)

    db.session.add(project)
    db.session.commit()
    tree_manager.register_events()
    #RequirementTree.rebuild_tree(db.session, 1)