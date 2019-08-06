from ducttapp import extensions, repositories


def get_all_category(_page, _limit, q, _sort, _order, is_active):
    if len(is_active) == 0:
        is_active = [True, False]
    else:
        is_active = [z.lower() for z in is_active]
        if not set(is_active).issubset(set(['true', 'false'])):
            raise extensions.exceptions.BadRequestException('Invalid data filter is active')
        is_active = [True if z == 'true' else False for z in is_active]

    try:
        _page = int(_page)
        _limit = int(_limit)
    except ValueError:
        raise extensions.exceptions.BadRequestException('Invalid data page or limit')

    list_sort_field = ["name", "description", "id", "created_at"]
    if (
            not isinstance(q, str) or _sort.lower() not in list_sort_field
            or _order.lower() not in ['descend', 'ascend']
    ):
        raise extensions.exceptions.BadRequestException('Invalid data sort')

    result = repositories.category.get_all_category(
        _page, _limit, q.lower(), _sort.lower(), _order.lower(), is_active)
    return result
