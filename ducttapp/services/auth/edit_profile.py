from ducttapp import repositories, extensions
from ducttapp.helpers.validators import valid_phone_number, valid_username
from datetime import datetime
import config


def edit_profile_user(user_id=None, form_data=None):
    user = repositories.user.find_one_by_id(
        user_id=user_id)
    if not user:
        raise extensions.exceptions.BadRequestException(
            message="User not found"
        )
    field_can_edit = ["fullname", "phoneNumber", "gender", "birthday", "avatar", "username"]
    for k in form_data.to_dict(flat=True).keys():
        if k not in field_can_edit:
            raise extensions.exceptions.BadRequestException(
                message="Invalid form data"
            )
    dict_edit_user = {}
    username = form_data.get('username') \
        if "username" in form_data and form_data.get("username") != "" else None
    fullname = form_data.get('fullname') \
        if "fullname" in form_data and form_data.get("fullname") != "" else None
    phone_number = form_data.get('phoneNumber') \
        if "phoneNumber" in form_data and form_data.get("phoneNumber") != "" else None
    gender = form_data.get('gender') \
        if "gender" in form_data and form_data.get("gender") != "" else None
    birthday = form_data.get('birthday') \
        if "birthday" in form_data and form_data.get("birthday") != "" else None
    avatar = form_data.get('avatar') \
        if "avatar" in form_data and form_data.get("avatar") != "" else None

    # username
    if username:
        if not valid_username(username):
            raise extensions.exceptions.BadRequestException(
                message="Username is invalid"
            )
        user_existed = repositories.user.find_one_by_email_or_username_in_user_ignore_case(
            username=username
        )
        if user_existed and user_existed.id != user_id:
            raise extensions.exceptions.BadRequestException(
                message="This username has already existed"
            )
        dict_edit_user.update({"username": username})

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

    # birthday
    if birthday:
        try:
            birthday_format_datetime = datetime.strptime(birthday, "%Y-%m-%d")
            dict_edit_user.update({"birthday": birthday_format_datetime})
        except ValueError:
            raise extensions.exceptions.BadRequestException(
                message="Birthday is invalid"
            )

    if avatar:
        dict_edit_user.update({"avatar": avatar})

    user_updated = repositories.user.update_user(
        user=user,
        **dict_edit_user
    )
    repositories.user.add_user_action(
        user_id=user.id,
        action_name=config.UPDATED
    )
    return user_updated
