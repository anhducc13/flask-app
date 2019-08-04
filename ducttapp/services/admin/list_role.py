from ducttapp import repositories


def get_all_roles():
    roles = repositories.role.get_all_roles()
    return roles
