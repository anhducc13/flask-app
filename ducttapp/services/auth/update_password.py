from ducttapp import repositories, helpers


def update_pass(username, old_password, new_password):
    if (
            not (old_password and helpers.validators.valid_password(old_password) and
                 new_password and helpers.validators.valid_password(new_password))
    ):
        return {
                   "msg": "Mật khẩu sai cú pháp"
               }, 400
    if old_password == new_password:
        return {
                   "msg": "Mật khẩu cũ và mới không được trùng nhau"
               }, 400

    user = repositories.user.find_one_by_email_or_username_in_user(
        username=username)
    if not user.check_password(old_password):
        return {
                   "msg": "Mật khẩu không chính xác"
               }, 400

    repositories.user.update_user(
        user=user,
        password=new_password
    )
    return {
               "ok": True
           }, 200