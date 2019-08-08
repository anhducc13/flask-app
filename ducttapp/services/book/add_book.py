from ducttapp import repositories, extensions


def add_book(username="", **kwargs):
    user = repositories.user.find_one_by_email_or_username_in_user_ignore_case(
        username=username
    )
    if not user:
        raise extensions.exceptions.NotFoundException("User not found")

    book_existed = repositories.book.find_one_by_name_ignore_case(
        book_name=kwargs["name"]
    )
    if book_existed:
        raise extensions.exceptions.BadRequestException("This book has already existed")
    repositories.book.add_book(
        user=user,
        **kwargs
    )
