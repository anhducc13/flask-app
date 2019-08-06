from ducttapp import models, repositories


def get_all_category(_page, _limit, q, _sort, _order, is_active):
    list_all = models.db.session.query(
        models.Category
    ).filter(
        models.Category.name.ilike('%{}%'.format(q))
    ).filter(
        models.Category.is_active.in_(is_active)
    )
    total = len(list_all.all())
    results = []
    if _order == 'descend':
        results = list_all \
            .order_by(getattr(models.Category, _sort).desc()) \
            .limit(_limit) \
            .offset((_page - 1) * _limit) \
            .all()
    else:
        results = list_all \
            .order_by(getattr(models.Category, _sort).asc()) \
            .limit(_limit) \
            .offset((_page - 1) * _limit) \
            .all()
    return {
        'total': total,
        'results': [x.to_dict() for x in results]
    }


def find_one_by_id(category_id):
    category = models.Category.query.filter(
        models.Category.id == category_id
    ).first()
    return category or None


def delete_category_by_id(category_id):
    category = find_one_by_id(category_id)
    if category:
        models.db.session.delete(category)
        models.db.session.commit()
    return category or None


def update_category(username="", category_id=None, **kwargs):
    if username and category_id:
        category = find_one_by_id(category_id)
        if category:
            category.update_attr(**kwargs)
            models.db.session.commit()
            user = repositories.user.find_one_by_email_or_username_in_user_ignore_case(
                username=username)
            category_log = models.UserCategoryAction(log_name=models.CategoryAction.UPDATED)
            category_log.category = category
            user.categories.append(category_log)
            models.db.session.commit()
