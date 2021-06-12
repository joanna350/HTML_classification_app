import os
import logging

from data.functions_for_dataset_creator import html_str_to_one_string_of_visible_text
from data.functions_for_dataset_creator import filtering_dict_creator, base_site_from_html
from util.io_funcs import pickle_save, read_text_file
from config.models.page_classifier_models import page_classifier_model

module_logger = logging.getLogger('main_app.dataset')
config = page_classifier_model['models']


class Dataset:
    def __init__(self, dataset_dir, training_set=False, max_items_per_class=None):
        """
        Parameters
        ----------
        dataset_dir : str
            directory to the dataset
        training_set : bool
            set to true if this is the taining set - used for filtering many sites
        max_items_per_class : int
        """
        self.list_of_text_strs = []
        self.list_of_class_values = []
        self.dataset_dir = dataset_dir
        self.training_set = training_set
        self.max_items_per_class = max_items_per_class

    def load_from_list_of_strings(self, list_of_html_str):
        """
        Parameters
        ----------
        list_of_html_str : list of str
        """
        self.list_of_text_strs = [html_str_to_one_string_of_visible_text(html_str) for html_str in list_of_html_str]

    def save_list_of_text_strs(self, directory):
        """
        Saves list of text strings in dataset
        Parameters
        ----------
        directory: path for where to save
        """
        pickle_save(directory, self.list_of_text_strs)

    def load_from_directory_of_htmls(self, path_to_directory, class_value, multiple_resolution_dataset=False):
        """
        This method adds the visible text from the DOM to the list of visible text str and class values
        Parameters
        ----------
        path_to_directory : str
                            directory of DOMs of certain class
        class_value : int

        multiple_resolution_dataset: bool
                                        filters out 1400_100- if true

        Returns
        -------

        """
        dict_of_domains = {}
        for file in os.listdir(path_to_directory):

            if self.max_items_per_class and (self.list_of_class_values.count(class_value) >= self.max_items_per_class):
                break

            if not file.endswith('.html'):
                continue

            if multiple_resolution_dataset and not ('1400_1000.html' in file):
                continue

            if self.training_set:
                valid_item = filtering_dict_creator(base_site_from_html(file, path_to_directory), dict_of_domains)[0]
                dict_of_domains = filtering_dict_creator(base_site_from_html(file, path_to_directory), dict_of_domains)[1]

                if not valid_item:
                    module_logger.info('Skipped item {}'.format(file))
                    continue

            module_logger.info('Loading file {}...'.format(file))
            html_str = read_text_file(os.path.join(path_to_directory, file))
            visible_text_str = html_str_to_one_string_of_visible_text(html_str)

            if visible_text_str == '':
                continue

            self.list_of_text_strs.append(visible_text_str)
            self.list_of_class_values.append(class_value)

    def load_from_class_names(self, class_names, multiple_resolution_dataset=False):
        """
        loads from directory named after the class
        Parameters
        ----------
        class_names : list
                        list of class names to be loaded

        multiple_resolution_dataset : bool
        """
        for class_name in class_names:
            class_value = config['CLASS_NUMBER_FROM_NAME'][class_name]
            self.load_from_directory_of_htmls(path_to_directory=os.path.join(self.dataset_dir, class_name),
                                              class_value=class_value,
                                              multiple_resolution_dataset=multiple_resolution_dataset)

    def combine_datasets(self, dataset_to_be_incorporated):
        """
        This method adds the input dataset to this one
        Parameters
        ----------
        dataset_to_be_incorporated: dataset object

        """
        self.list_of_text_strs += dataset_to_be_incorporated.list_of_text_strs

        self.list_of_class_values += dataset_to_be_incorporated.list_of_class_values


if __name__ == "__main__":
    pass
