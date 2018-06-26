from util import decorator


class API(object):
    base_url = None


@decorator
def GET(func, suffix=None):
    def wrapper(self, *args, **kwargs):
        Type = func(self, *args, **kwargs)
        the_suffix = suffix
        if the_suffix is None:
            the_suffix = Type.suffix
        print("I am:", self.__class__.__name__)
        print("requesting", self.base_url + the_suffix)
        print("as", Type)
        return Type(self)
    return wrapper


def POST(f):
    pass
