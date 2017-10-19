class Singleton(type):
    '''
    Manage classes that have this meta-class so that there is only one
    instance of the class in the application.
    '''

    # Keep track of the classes that have been instantiated.
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # Class has not been instantiated.  Keep track of the object
            # in the _instances list so that it can be returned the next
            # time there is a request to instantiate the class.
            cls._instances[cls] = super().__call__(*args, **kwargs)

        # Return the new or existing instance.
        return cls._instances[cls]
