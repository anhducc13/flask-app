from ducttapp import repositories

admin = {
    'username': 'anhducc13',
    'email': 'trantienduc10@gmail.com',
    'password': 'Anhducc13',
    'is_admin': True
}


def init_data_db():
    user_not_verify = repositories.signup.find_one_by_email_or_username_in_signup_request_ignore_case(
        email=admin['email'],
        username=admin['username']
    )
    if user_not_verify:
        repositories.signup.delete_one_in_signup_request(user_not_verify)
    user_with_email = repositories.user.find_one_by_email_or_username_in_user_ignore_case(
        email=admin['email']
    )
    user_with_username = repositories.user.find_one_by_email_or_username_in_user_ignore_case(
        username=admin['username']
    )
    if user_with_email['email'] == user_with_username['email']:
        repositories.user.update_user(user_with_email, **admin)
    else:
        repositories.user.delete_one_in_user(user_with_email)
        repositories.user.delete_one_in_user(user_with_username)
        repositories.user.add_user(**admin)



