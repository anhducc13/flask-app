from ducttapp import models, repositories


def add_book(user, **kwargs):
    list_categories = []
    if "categories" in kwargs.keys():
        list_categories = [models.Category.query.filter(models.Category.id == x).first() for x in kwargs['categories']]
        kwargs.pop('categories', None)
        pass
    book_log = models.UserBookAction(log_name=models.LogAction.CREATED)
    book_log.book = models.Book(**kwargs)
    for c in list_categories:
        if c is not None:
            book_log.book.categories.append(c)
    user.books.append(book_log)
    models.db.session.commit()


def find_one_by_id(book_id):
    book = models.Book.query.filter(
        models.Book.id == book_id
    ).first()
    return book or None


def find_one_by_name_ignore_case(book_name=""):
    book = models.Book.query.filter(
        models.Book.name.ilike(book_name)
    ).first()
    return book or None


def get_list_book(_page, _limit, q, _sort, _order, is_active):
    list_all = models.db.session.query(
        models.Book
    ).filter(
        models.Book.name.ilike('%{}%'.format(q))
    ).filter(
        models.Book.is_active.in_(is_active)
    )
    total = len(list_all.all())
    results = []
    if _order == 'descend':
        results = list_all \
            .order_by(getattr(models.Book, _sort).desc()) \
            .limit(_limit) \
            .offset((_page - 1) * _limit) \
            .all()
    else:
        results = list_all \
            .order_by(getattr(models.Book, _sort).asc()) \
            .limit(_limit) \
            .offset((_page - 1) * _limit) \
            .all()
    return {
        'total': total,
        'results': [x.to_dict() for x in results]
    }

