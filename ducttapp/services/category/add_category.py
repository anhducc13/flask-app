from ducttapp import repositories, models


def add_category(user_id=None, name="", description="", **kwargs):
    user = repositories.user.find_one_by_id(user_id=user_id)
    category_log = models.UserCategoryAction(log_name=models.LogAction.CREATED)
    category_log.category = models.Category(name=name, description=description, **kwargs)
    user.categories.append(category_log)
    models.db.session.commit()
