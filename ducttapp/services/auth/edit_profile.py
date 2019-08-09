from ducttapp import repositories, extensions
from ducttapp.helpers.validators import valid_phone_number, valid_username
from datetime import datetime
import config


def edit_profile_user(user_id=None, **kwargs):
    user = repositories.user.find_one_by_id(
        user_id=user_id)
    if not user:
        raise extensions.exceptions.BadRequestException(
            message="User not found"
        )
    for k in kwargs.keys():
        if k not in ["username", "fullname", "phone_number", "gender", "birthday", "avatar"]:
            raise extensions.exceptions.BadRequestException(
                message=f"Invalid data payload {k}"
            )
    # validate username
    username = kwargs.get("username", None)
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

    # validate avatar
    avatar = kwargs.get("avatar", None)
    if avatar is None:
        kwargs.pop("avatar", None)
    elif not isinstance(avatar, str):
        raise extensions.exceptions.BadRequestException(
            message="Avatar is invalid"
        )

    # validate birthday
    birthday = kwargs.get("birthday", None)
    if birthday is None:
        kwargs.pop("birthday", None)
    else:
        try:
            time = datetime.strptime(birthday, '%Y-%m-%dT%H:%M:%S.%fZ')
            kwargs["birthday"] = time
        except ValueError:
            raise extensions.exceptions.BadRequestException(
                message="Birthday is invalid"
            )
    user_updated = repositories.user.update_user(
        user=user,
        **kwargs
    )
    repositories.user.add_user_action(
        user_id=user.id,
        action_name=config.UPDATED
    )
    return user_updated
