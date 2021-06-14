import logging
import pickle

module_logger = logging.getLogger('main_app.io')


def pickle_save(filename, a_object):
    '''
    Serialize a given object to the path based on protocol 4, details in
    https://www.python.org/dev/peps/pep-3154/

    Parameters
    ----------
    filename: path in Str
    a_object: object supported by pickle module
    '''
    with open(filename, 'wb') as outputfile:
        pickle.dump(a_object, outputfile, protocol=4)


def pickle_load(filename):
    '''
    De-serialize the object on a path

    Parameters
    ----------
    filename: path in Str
    '''
    with open(filename, 'rb') as inputfile:
        a_object = pickle.load(inputfile, encoding='bytes')

    return a_object


def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as text_file:
        data = text_file.read()

    return data

