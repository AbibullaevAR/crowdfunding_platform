from project_management.models import Project


def like_project(project_id: str, user):
    project = Project.objects.get(id=project_id)
    if project.taken_likes.filter(id=user.id).exists():
        project.taken_likes.remove(user)
    else:
        project.taken_likes.add(user)