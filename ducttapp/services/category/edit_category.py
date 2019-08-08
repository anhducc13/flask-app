from ducttapp import extensions, repositories


def edit_category(user_id=None, category_id=None, **kwargs):
    field_can_edit = ["name", "description", "is_active"]
    for k in kwargs.keys():
        if k not in field_can_edit:
            raise extensions.exceptions.BadRequestException(
                message="Invalid data edit"
            )
    repositories.category.update_category(
        user_id=user_id,
        category_id=category_id,
        **kwargs
    )
    return {
        "update": True
    }
