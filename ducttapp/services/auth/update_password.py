from ducttapp import repositories, helpers
import config


def update_pass(username, old_password, new_password):
  list_history_pass_change = repositories.user.find_history_pass_change_with_times(
    username=username,
    times=config.TIMES_CHECK_PASSWORD
  )
  if repositories.user.is_duplicate_password_before(new_password, list_history_pass_change):
    return {
             "message": f"Mật khẩu không được trùng với {config.TIMES_CHECK_PASSWORD} lần thay đổi trước đó"
           }, 400

  user = repositories.user.find_one_by_email_or_username_in_user(
    username=username)
  if not user.check_password(old_password):
    return {
             "message": "Mật khẩu không chính xác"
           }, 400

  repositories.user.update_user(
    user=user,
    password=new_password
  )
  return {
           "ok": True
         }, 200
