from itertools import groupby, chain
import re
from bs4 import BeautifulSoup


def is_visible(element):
    """
    Checks if an element is visible in the DOM using the nate visible attribute

    Parameters
    ----------
    element : soup element

    Returns
    -------
    is_visible : bool
    """
    if element.has_attr('nate_visible') and (element.attrs['nate_visible'] == 'true'):
        return True
    else:
        return False


def preprocess_text(text):
    """
    Takes in a string of text and cleans it up i.e. removes punctuation, replaces numbers with @ etc.

    Parameters
    ----------
    text : str

    Returns
    -------
    text : str
    """
    punctuation_blacklist = '±-!"#%\'()*,./:;<=>?@[\\]^_`{}~\n\t'  # want to keep some symbols e.g. £ $ + -
    currency_symbols = ['£', '$', '€']
    text = re.sub(r'\n+', '', text)
    text = re.sub(r'\t+', '', text)
    text = re.sub(r' +', ' ', text)
    re_split_on_title_case = re.compile(r'.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)')
    text = ' '.join(re.findall(re_split_on_title_case, text))  # splits e.g. 'AddToBag' into 'Add To Bag'
    text = text.lower()

    table = str.maketrans(punctuation_blacklist, len(punctuation_blacklist) * ' ')
    text = text.translate(table)  # remove blacklisted punctuation
    for symbol in currency_symbols:
        text = text.replace('{}'.format(symbol), ' {} '.format(symbol))  # split currency symbols from number
    text = ' '.join(text.split())
    text = text.strip()
    grouped = groupby(text, str.isdigit)
    text = ''.join(chain.from_iterable("@" if k else g for k, g in grouped))
    return text


def preprocess_list(final_list):
    """
    Preprocesses (removes spaces, punctuation etc.) for elements in list

    Parameters
    ----------
    final_list : list of strings

    Returns
    -------
    new_final_list : list
    """
    new_final_list = []
    for text in final_list:
        if not preprocess_text(text).isspace():
            new_final_list.append(preprocess_text(text))
    new_final_list = [text for text in new_final_list if text != '']
    print('........')
    print(new_final_list)
    print('...')
    return new_final_list


def html_str_to_one_string_of_visible_text(html_str):
    """
    Takes a DOM and gives only the already preprocessed visible text from it as one string

    Parameters
    ----------
    html_str : str


    Returns
    -------
    text_str : str

    """
    soup = BeautifulSoup(html_str, 'html.parser')
    elements = soup.findAll()
    list_of_text = text_from_html_nate(elements)

    text_str = " ".join(list_of_text)
    return text_str


def text_from_html_nate(elements):
    """
    This function gives out a list of visible text from different elements.
    Every element of list is visible text from a different element of DOM.

    Parameters
    ----------
    elements : list of soup elements

    Returns
    -------
    list_of_text : list of visible text

    """
    list_of_visible_elements = list(filter(is_visible, elements))
    list_of_text = []

    for element in list_of_visible_elements:
        inner_text = element.findAll(text=True, recursive=False)
        list_of_text = list_of_text + inner_text
    print('after processing')
    print(len(list_of_text))
    print(list_of_text)
    return preprocess_list(list_of_text)


def get_key_from_val(givenV, dict):
    '''
    As the testing labels are 1 short of training labels (namely, 'bot')
    handles this
    '''
    out = ''
    for k, v in dict.items():
        if givenV == v:
            if out != '':
                out += ',' + k
            else:
                out += k
    return out if out != '' else 'no matching class'

