from ducttapp import repositories, extensions


def delete_category(category_id):
    category_del = repositories.category.delete_category_by_id(category_id)
    if category_del:
        return {'message': 'success'}
    raise extensions.exceptions.BadRequestException('Category Not Found')
