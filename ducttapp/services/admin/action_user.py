from ducttapp import models


def get_all_action(user_id, _page, _limit, _order, action_name):
    list_all = models.UserAction.query \
            .filter(models.UserAction.user_id == user_id) \
            .filter(models.UserAction.action_name.in_(action_name))
    total = len(list_all.all())
    results = []
    if _order == 'descend':
        results = list_all \
            .order_by(models.UserAction.created_at.desc()) \
            .limit(_limit) \
            .offset((_page - 1) * _limit) \
            .all()
    else:
        results = list_all \
            .order_by(models.UserAction.created_at.asc()) \
            .limit(_limit) \
            .offset((_page - 1) * _limit) \
            .all()
    return {
        'total': total,
        'results': results
    }
