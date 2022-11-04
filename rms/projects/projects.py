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
    db.session.add(project)
    db.session.commit()

    project_id = project.id

    root_requirement_tree_node = RequirementTree()
    tree_manager.register_events(remove=True)
    root_requirement_tree_node.left = 0
    root_requirement_tree_node.right = 0
    root_requirement_tree_node.tree_id = project_id #так не срабатывает
    root_requirement_tree_node.project_id = project_id

    root_requirement = Requirement(
        name = 'Коренвое требование проекта',
        description = f'Проект - "{form.name.data}"',
        created_date = datetime.utcnow(),
        update_date = datetime.utcnow(),
        version = 1,
        status_id = 0,
        approve = False,
        release = False,
    )

    root_requirement_tree_node.requirements.append(root_requirement)

    db.session.add(root_requirement_tree_node)
    db.session.commit()

    #Меняем tree_id на нужный
    node = db.session.query(RequirementTree).filter(RequirementTree.id == root_requirement_tree_node.id).one()
    node.tree_id = project_id
    db.session.add(node)
    db.session.commit()

    tree_manager.register_events()
    RequirementTree.rebuild_tree(db.session, project_id)