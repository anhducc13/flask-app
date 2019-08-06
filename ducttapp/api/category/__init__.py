from ducttapp.extensions.namespace import Namespace

ns = Namespace('category', description='Category operators')

from .add_category import CategoryAdd
from .list_category import CategoryList
from .category import Category