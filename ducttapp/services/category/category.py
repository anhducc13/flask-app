from ducttapp import repositories, extensions


def get_one_category(category_id):
    category = repositories.category.find_one_by_id(category_id)
    if category:
        return category
    raise extensions.exceptions.BadRequestException('Category Not Found')