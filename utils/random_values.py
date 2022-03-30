from django.utils.crypto import get_random_string



def random_str(length=10):
    """
        generate random str
    """
    return '{}'.format(get_random_string(length=length))
