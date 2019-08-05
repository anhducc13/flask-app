from ducttapp import repositories, models


def add_category(username="", name="", description="", **kwargs):
    user = repositories.user.find_one_by_email_or_username_in_user_ignore_case(username=username)
    category_log = models.UserCategoryAction(log_name=models.CategoryAction.CREATED)
    category_log.category = models.Category(name=name, description=description, **kwargs)
    user.categories.append(category_log)
    models.db.session.commit()
