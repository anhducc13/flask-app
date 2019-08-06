from ducttapp import extensions, repositories


def get_all_action(category_id, _page, _limit, _order):
    if not category_id:
        raise extensions.exceptions.BadRequestException(
            message="Invalid data category id"
        )
    try:
        category_id = int(category_id)
        _page = int(_page)
        _limit = int(_limit)
    except ValueError:
        raise extensions.exceptions.BadRequestException(
            message="Invalid data params"
        )
    if _order.lower() not in ['descend', 'ascend']:
        raise extensions.exceptions.BadRequestException(
            message='Invalid data sort type'
        )
    result = repositories.category.get_all_action(
        category_id, _page, _limit, _order.lower())
    return result
