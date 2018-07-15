import sys
from .util import decorator

import requests


@decorator
def API(cls, base_url):
    b = base_url

    class A(cls):
        base_url = b
        suffix = ""

        @property
        def api(self):
            return self

    return A


@decorator
def Entity(cls):
    class E(cls):
        def __init__(self, api, **data):
            self.api = api
            print(data)
            for name in dir(cls):
                attr = getattr(cls, name)
                if isinstance(attr, Property):
                    try:
                        value = attr.parse(data.get(name))
                    except RuntimeError as e:
                        print("Attribute with name '{}' missing".format(name), file=sys.stderr)
                        raise e
                    setattr(self, name, value)

        @property
        def suffix(self):
            return str(self.id)

        @property
        def base_url(self):
            return self.api.base_url

        @property
        def token(self):
            return self.api.token

    return E


@decorator
def GET(func, suffix="", paginate=False):
    def wrapper(self, *args, **kwargs):
        Type = func(self, *args, **kwargs)
        the_suffix = suffix
        print("I am:", self.__class__.__name__)
        print("as", Type)

        # TODO: use urlib join method
        url = self.base_url + self.suffix + '/' + the_suffix
        for arg in args:
            url += '{}/'.format(arg)

        params = {key: arg for key, arg in kwargs.items() if arg is not None}
        params['access_token'] = self.token

        print(url)

        r = requests.get(url, params=params)
        print(r)
        data = r.json()

        if paginate:
            return self.api.paginate(Type, **data)
        else:
            entity = Type(self.api, **data)
            return entity
    return wrapper


def POST(f):
    pass


class Property(object):
    def __init__(self, required=True):
        self.required = required

    def parse(self, value):
        if value is None:
            if self.required:
                raise RuntimeError("Missing required attribute")
            else:
                return

        return self._parse(value)

    def _parse(self, value):
        raise NotImplementedError("subclasses should implement Property.parse")


class StringProperty(Property):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _parse(self, value):
        return str(value)


class IntProperty(Property):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _parse(self, value):
        return int(value)


# class CompoundProperty(Property):
#     def _parse(self, data):
#         for name in dir(self.__class__):
#             attr = getattr(self.__class__, name)
#             if isinstance(attr, Property):
#                 value = attr.parse(data.get(name))
#                 setattr(self, name, value)


class ListProperty(Property):
    def __init__(self, cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cls = cls

    def _parse(self, data):
        elements = list()
        for elem in data:
            instance = self.cls()

            for name in dir(self.cls):
                attr = getattr(self.cls, name)
                if isinstance(attr, Property):
                    value = attr.parse(elem.get(name))
                    setattr(instance, name, value)

            elements.append(instance)
        return elements
