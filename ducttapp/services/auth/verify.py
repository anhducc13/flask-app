from ducttapp import repositories
import jwt as jwt_os
import config


def verify(token_string):
    user_signup_request = repositories.signup.find_one_by_token_string(
        token=token_string)
    if not user_signup_request:
        return {
                   "message": "Not found account verify"
               }, 400
    try:
        repositories.signup.delete_one_in_signup_request(
            user_signup_request)
        decode = jwt_os.decode(token_string, config.FLASK_APP_SECRET_KEY)
        user = repositories.user.add_user(
            username=user_signup_request.username,
            email=user_signup_request.email,
            password_hash=user_signup_request.password_hash,
            is_admin=user_signup_request.is_admin,
        )
        if user:
            repositories.user.add_new_password_to_history_pass_change_table(
                user_id=user.id,
                created_at=user.updated_at,
                password_hash=user.password_hash
            )
            repositories.user.add_user_action(
                user_id=user.id,
                action_name=config.CREATED
            )
            return {
                       "ok": True
                   }, 200
    except:
        return {
                   "message": "Hết hạn xác thực"
               }, 403
