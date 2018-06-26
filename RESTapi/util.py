

# decorator annotation
def decorator(func):
    """
    Decorator for decorator functions. Allows for syntax:
    ```
    @decorator
    def foo(func, kwarg1=None):
        pass
    ```
    which works both when a parameter list is given when using the decorator foo or not.
    ```
    @foo
    def bar():
        pass

    @foo(5)
    def bar():
        pass

    ```

    """
    def wrapper(*args, **kwargs):
        # If no parameters given (only function)
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            return func(*args, **kwargs)
        # If parameters given
        def decorator(f):
            return func(f, *args, **kwargs)
        return decorator

    return wrapper
