from ducttapp import models


def get_all_roles():
    roles = models.Role.query.all()
    return roles


def set_role_user(user=None, list_role=None):
    if not list_role:
        list_role = []
    user.roles = []
    roles = models.Role.query.filter(models.Role.id.in_(list_role)).all()
    for r in roles:
        user.roles.append(r)
    models.db.session.commit()
