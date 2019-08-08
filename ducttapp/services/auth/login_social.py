from ducttapp import repositories, helpers, extensions


def login_social(social_id, username, email, social_name):
    # check user in social login table
    user = repositories.social_login.find_user_from_social_login_by_social_id_and_social_name(
        social_id=social_id,
        social_name=social_name
    )
    if user:
        if not repositories.user.check_is_active_of_user(user):
            raise extensions.exceptions.ForbiddenException(
                message="Account has been lock. Please try later"
            )
        return user
    # check user if not verify
    user_not_verify = repositories.signup.find_one_by_email_or_username_in_signup_request_ignore_case(
        email=email
    )
    if user_not_verify:
        user_verified = repositories.user.add_user(
            username=user_not_verify.username,
            email=user_not_verify.email,
            password_hash=user_not_verify.password_hash,
        )
        repositories.social_login.add_to_social_login(
            social_id=social_id,
            social_name=social_name,
            user_id=user_verified.id
        )
        return user_verified

    # if not in user table
    user_added = repositories.user.add_user(
        username=username,
        email=email,
        password=helpers.password.generate_password()
    )
    repositories.social_login.add_to_social_login(
        social_id=social_id,
        social_name=social_name,
        user_id=user_added.id
    )
    return user_added
