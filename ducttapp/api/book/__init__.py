from ducttapp.extensions.namespace import Namespace

ns = Namespace('book', description='Book operators')

from .add_book import BookAdd
from .list_book import BookList
from .all_category import AllCategory
