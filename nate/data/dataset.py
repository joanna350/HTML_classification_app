from data.functions_for_dataset_creator import html_str_to_one_string_of_visible_text


class Dataset:
    def __init__(self, dataset_dir='.', training_set=False, max_items_per_class=None):
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
