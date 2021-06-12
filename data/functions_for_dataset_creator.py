import os
from itertools import groupby, chain
from urllib.parse import urlparse
import re
import json

from bs4 import BeautifulSoup
import numpy as np

from util.io_funcs import read_text_file


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
    return preprocess_list(list_of_text)


def dataset_creator_single_tag(path, tag, examples):
    """

    Parameters
    ----------
    path : str of folder name with examples of a certain tag
    tag : int of class number
    examples : numpy array, already added dataset examples

    Returns
    -------

    """
    one_hot_vector = np.zeros((6, 1))
    one_hot_vector[tag] = 1
    dict_of_domains = {}
    for file in os.listdir(path):
        if "1400_1000.html" in file:
            can_continue = filtering_dict_creator(base_site_from_html(file, path), dict_of_domains)[0]
            dict_of_domains = filtering_dict_creator(base_site_from_html(file, path), dict_of_domains)[1]
            if can_continue:
                html = open(path + "/" + file, 'r').read()
                soup = BeautifulSoup(html, 'html.parser')
                elements = soup.findAll()

                if elements[0].has_attr('nate_visible'):
                    example = [[file, text_from_html_nate(elements), tag]]
                    examples = np.append(examples, example, axis=0)
                    print("logging")

    print(dict_of_domains)
    print("-----------")
    print("done folder")
    return examples


def base_site_from_html(file, path):
    """
    Gives the base domain of the html.
    This is specifically from blackbox.options_detector.data, where we have metadata for htmls.

    Parameters
    ----------
    file : str - name of html file
    path : str with metadata files

    Returns
    -------
    base_domain : str
    """
    file_json_name = file[:-4] + 'json'
    f = open(path + "/" + file_json_name)
    metadata = json.load(f)
    domain = urlparse(metadata['extended_url']).netloc
    return domain


def filtering_dict_creator(domain, dict_of_domains):
    """
    This function tell you if this site has appeared too many times in the dataset (for balance).
    A limit per webpage is hardcoded to 15.
    It also alters the dict_of_domains by adding 1 to the value of domain.


    Parameters
    ----------
    domain : str of base domain name
    dict_of_domains : dict where key is the domain name, value is how many time it has appeared in dataset

    Returns
    -------
    can_continue : bool if example is to be added to dataset
    dict_of_domains : dict where key is the domain name, value is how many time it has appeared in dataset
    """
    if domain in dict_of_domains:
        if dict_of_domains[domain] < 15:
            dict_of_domains[domain] += 1
            can_continue = True
            return can_continue, dict_of_domains
        else:
            can_continue = False
            return can_continue, dict_of_domains
    else:
        dict_of_domains[domain] = 1
        can_continue = True
        return can_continue, dict_of_domains


def dataset_creator(list_of_folders, path_to_sorted):
    """
    This function saved the dataset in an npz file
    Parameters
    ----------
    list_of_folders : list of folder names
    path_to_sorted : path to the sorted folder

    Returns
    -------


    """
    examples = np.array([[1, 2, 3]])
    for index in range(len(list_of_folders)):
        if index == 0:
            examples = dataset_creator_single_tag(path_to_sorted + list_of_folders[index], 4, examples)
        else:
            examples = dataset_creator_single_tag(path_to_sorted + list_of_folders[index], index - 1, examples)
    examples = np.delete(examples, 0, 0)
    np.save('generated_examples_for_sklearn', examples)

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


if __name__ == "__main__":

    # DOM = read_text_file('/home/anagh/PycharmProjects/nate.blackbox.options.detector.data/screenshots/sorted/popup/0b0347888954f1549c9a6c6f243438fe_desktop_1400_1000.html')

    CLASS_NUMBER_FROM_NAME =  {'out_of_stock': 0,
                               'popup': 1,
                               'product_landing_page': 2,
                               'product_listing': 3,
                               'site_error': 4,
                               'bot': 4
                               }

    print(inverse_map_dict(CLASS_NUMBER_FROM_NAME)[4])
    for i in range(5):
        print('for ', i)
        print(get_key_from_val(i, CLASS_NUMBER_FROM_NAME))