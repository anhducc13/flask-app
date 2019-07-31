from ducttapp import repositories, extensions, helpers
from ducttapp.helpers.validators import valid_username, valid_phone_number


def edit_user(user_id, form_data):
    user = repositories.user.find_one_by_id(user_id=user_id)
    if not user:
        raise extensions.exceptions.BadRequestException(
            message="User not found"
        )
    username = form_data.get('username')
    fullname = form_data.get('fullname')
    phone_number = form_data.get('phoneNumber')
    gender = form_data.get('gender')
    birthday = form_data.get('birthday')

    if not valid_username(username):
        raise extensions.exceptions.BadRequestException(
            message="Username contain letter and number and not special character"
        )
    # if not valid_phone_number(phone_number):
    #     raise extensions.exceptions.BadRequestException(
    #         message="Phone number is invalid"
    #     )
    # if gender not in ["null", "true", "false"]:
    #     raise extensions.exceptions.BadRequestException(
    #         message="Gender is invalid"
    #     )
    # validate birthday
    repositories.user.update_user(
        user=user,
        username=username,
    )
    return {
        "update": True
    }
