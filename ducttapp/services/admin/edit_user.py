from ducttapp import repositories, extensions, helpers
from ducttapp.helpers.validators import valid_username, valid_phone_number
from datetime import datetime
import config


def edit_user(user_id, form_data):
    user = repositories.user.find_one_by_id(user_id=user_id)
    if not user:
        raise extensions.exceptions.BadRequestException(
            message="User not found"
        )
    if user.is_admin:
        raise extensions.exceptions.ForbiddenException(
            message="You can't edit this user"
        )

    field_can_edit = ["fullname", "phoneNumber", "gender", "birthday", "isAdmin", "isActive", "avatar", "roles"]
    for k in form_data.to_dict(flat=True).keys():
        if k not in field_can_edit:
            raise extensions.exceptions.BadRequestException(
                message="Invalid form data"
            )

    dict_edit_user = {}
    fullname = form_data.get('fullname') \
        if "fullname" in form_data and form_data.get("fullname") != "null" else None
    phone_number = form_data.get('phoneNumber') \
        if "phoneNumber" in form_data and form_data.get("phoneNumber") != "null" else None
    gender = form_data.get('gender') \
        if "gender" in form_data and form_data.get("gender") != "null" else None
    birthday = form_data.get('birthday') \
        if "birthday" in form_data and form_data.get("birthday") != "null" else None
    is_admin = form_data.get('isAdmin') \
        if "isAdmin" in form_data and form_data.get("isAdmin") != "null" else None
    is_active = form_data.get('isActive') \
        if "isActive" in form_data and form_data.get("isActive") != "null" else None
    roles = form_data.get('roles', None)

    # fullname
    if fullname:
        dict_edit_user.update({"fullname": fullname})

    # phone_number
    if phone_number:
        if not valid_phone_number(phone_number):
            raise extensions.exceptions.BadRequestException(
                message="Phone number is invalid"
            )
        else:
            dict_edit_user.update({"phone_number": phone_number})

    # gender
    if gender:
        if gender.lower() not in ["true", "false"]:
            raise extensions.exceptions.BadRequestException(
                message="Gender is invalid"
            )
        else:
            gender = True if gender.lower() == "true" else False
            dict_edit_user.update({"gender": gender})

    # is_admin
    if is_admin:
        if is_admin.lower() not in ["true", "false"]:
            raise extensions.exceptions.BadRequestException(
                message="Field admin is invalid"
            )
        else:
            is_admin = True if is_admin.lower() == "true" else False
            dict_edit_user.update({"is_admin": is_admin})

    # is_active
    if is_active:
        if is_active.lower() not in ["true", "false"]:
            raise extensions.exceptions.BadRequestException(
                message="Field active is invalid"
            )
        else:
            is_active = True if is_active.lower() == "true" else False
            dict_edit_user.update({"is_active": is_active})
            if not is_active:
                dict_edit_user.update({"time_unlock": config.MAX_TIMESTAMP})

    # birthday
    if birthday:
        try:
            birthday_format_datetime = datetime.strptime(birthday, "%Y-%m-%d")
            dict_edit_user.update({"birthday": birthday_format_datetime})
        except ValueError:
            raise extensions.exceptions.BadRequestException(
                message="Birthday is invalid"
            )

    # role
    list_role = []
    try:
        if roles.strip() != "":
            list_role_string = roles.split(',')
            list_role = [int(z) for z in list_role_string]
    except ValueError:
        raise extensions.exceptions.BadRequestException(
            message="Invalid role data"
        )
    repositories.role.set_role_user(
        user=user,
        list_role=list_role
    )

    repositories.user.update_user(
        user=user,
        **dict_edit_user
    )
    repositories.user.add_user_action(
        user_id=user.id,
        action_name=config.UPDATED
    )
    return {
        "update": True
    }
