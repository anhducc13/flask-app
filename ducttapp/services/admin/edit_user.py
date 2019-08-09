from ducttapp import repositories, extensions, helpers
from ducttapp.helpers.validators import valid_username, valid_phone_number
from datetime import datetime
import config


def edit_user(user_id, **kwargs):
    user = repositories.user.find_one_by_id(user_id=user_id)
    if not user:
        raise extensions.exceptions.BadRequestException(
            message="User not found"
        )

    for k in kwargs.keys():
        if k not in ["fullname", "phone_number", "gender", "birthday", "is_active", "roles"]:
            raise extensions.exceptions.BadRequestException(
                message=f"Invalid data payload {k}"
            )
    # validate phone number
    phone_number = kwargs.get("phone_number", None)
    if phone_number is None:
        kwargs.pop("phone_number", None)
    elif phone_number != "" and not valid_phone_number(phone_number):
        raise extensions.exceptions.BadRequestException(
            message="Phone number is invalid"
        )

    # validate gender
    gender = kwargs.get("gender", None)
    if gender is None:
        kwargs.pop("gender", None)
    elif not isinstance(gender, bool):
        raise extensions.exceptions.BadRequestException(
            message="Gender is invalid"
        )

    # validate fullname
    fullname = kwargs.get("fullname", None)
    if fullname is None:
        kwargs.pop("fullname", None)
    elif not isinstance(fullname, str):
        raise extensions.exceptions.BadRequestException(
            message="Fullname is invalid"
        )

    # validate is_active
    is_active = kwargs.get("is_active", None)
    if is_active is None:
        kwargs.pop("is_active", None)
    elif not isinstance(is_active, bool):
        raise extensions.exceptions.BadRequestException(
            message="Active is invalid"
        )

    # validate roles
    roles = kwargs.get("roles", None)
    if roles is None:
        kwargs.pop("roles", None)
    elif not isinstance(roles, list):
        raise extensions.exceptions.BadRequestException(
            message="Roles is invalid"
        )
    else:
        for r in roles:
            if not isinstance(r, int):
                raise extensions.exceptions.BadRequestException(
                    message="Roles is invalid"
                )

    repositories.role.set_role_user(
        user=user,
        list_role=roles
    )
    kwargs.pop("roles", None)
    repositories.user.update_user(
        user=user,
        **kwargs
    )
    repositories.user.add_user_action(
        user_id=user.id,
        action_name=config.UPDATED
    )
    return {
        "update": True
    }
