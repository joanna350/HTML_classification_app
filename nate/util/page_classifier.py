from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import logging
import os


module_logger = logging.getLogger('main_app.train_page_classifier')


class PageClassifier:

    def __init__(self, config):
        # user's choice of parameter received in dictionary
        self.config = config

        self.vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.6, stop_words='english', ngram_range=(1, 3))
        # instantiates the model given in config parameter as an attribute to the class
        self.clf = self.build_model()

    def build_model(self):
        '''
        Creates instances of models for classification
        Supports Linear SVM, RFC and SGD Classifier
        '''

        model = self.config['models']['NAME']
        model_dict = {"LinearSVM": LinearSVC(penalty='l1', dual=False, tol=1e-3),
                      "RFC": RandomForestClassifier(n_estimators=100),
                      "SGD": SGDClassifier(alpha=.0001, max_iter=50, penalty='l1')
                      }

        # return the model with the matching name (will be controlled)
        clf = model_dict[model]
        return clf

    def train(self, dataset):
        """
        This method trains the classifier and fits the vectorizer.

        Parameters
        ----------
        dataset : list of data.dataset.Dataset
                        dataset objects.

        """

        x_train = self.vectorizer.fit_transform(dataset.list_of_text_strs)
        self.clf.fit(x_train, dataset.list_of_class_values)

    def predict(self, dataset):
        """
        This method gives out a prediction and it's confidence for a single DOM.
        The confidence only works for SVC, otherwise it doesn't make much sense.

        Parameters
        ----------
        dataset : data.dataset.Dataset
                        A dataset object loaded with an html str
                        Example: 'this is the visible text from the html DOM'

        Returns
        -------
        predictions : list of predicted class values
        confidence_array : list of lists of predicted confidence values for every category

        """
        x_test = self.vectorizer.transform(dataset.list_of_text_strs)
        # sparse matrix of shape (1,1973)

        # returns [n_samples], predicted class per sample
        predictions = self.clf.predict(x_test)

        # returns array shape (n_samples, n_classes)
        distance_hpp = self.clf.decision_function(x_test)
        confidence_array = self.softmax(distance_hpp)

        return predictions, confidence_array

    def save(self, path_to_directory, file1, file2):
        """
        Save trained vectorizer and classifier

        Parameters
        ----------
        path_to_directory : str
                            Path to where the vectorizer and classifier are to be saved,
                            remember they have hardcoded names.

        """
        if not os.path.isdir(path_to_directory):
            os.mkdir(path_to_directory)

        from util.io_funcs import pickle_save
        pickle_save(os.path.join(path_to_directory, file1), self.clf)
        pickle_save(os.path.join(path_to_directory, file2), self.vectorizer)

    def load(self, path_to_directory, file1, file2):
        """
        Loads saved vectorizer and classifier

        Parameters
        ----------
        path_to_directory : str
                            Path to where the saved vectorizer and classfier are,
                            remember they have hardcoded names.

        """
        from util.io_funcs import pickle_load
        self.clf = pickle_load(os.path.join(path_to_directory, file1))
        self.vectorizer = pickle_load(os.path.join(path_to_directory, file2))

    @staticmethod
    def softmax(list):
        '''
        performs softmax over the given list.
        namely take the exponent of each integer, divide by the sum of them

        Parameters
        ----------
        list: List[List[int]] is the accepted format

        Returns
        -------
        new_list: List[List[int]] retained format, softmax-operated list
        '''
        for x in list:
            return np.exp(x)/np.sum(np.exp(x), axis=0)


def execute(filename):
    # Rids error when using this script as a module from pytest
    from config.models.page_classifier_models import page_classifier_model
    from data.dataset import Dataset
    from data.functions_for_dataset_creator import get_key_from_val
    from util.io_funcs import read_text_file


    html_string = read_text_file(filename)

    # de-seralize the models that were serialised after training
    page_classifier = PageClassifier({'models': {'NAME': 'SGD'}})
    page_classifier.load('saved_predictor_temp',
                         page_classifier_model['models']['OUTPUT1'],
                         page_classifier_model['models']['OUTPUT2'])

    # prepare test data
    dataset = Dataset()
    dataset.load_from_list_of_strings([html_string])

    # return predicted class with confidence level from the data
    predictions, confidence_array = page_classifier.predict(dataset)
    predicted_class_value = int(predictions[0])

    # output to a dict/jsonify-able format
    results_dict = {
        'pageClass': get_key_from_val(predicted_class_value, page_classifier_model['models']['CLASS_NUMBER_FROM_NAME']),
        'confidence': confidence_array[predicted_class_value]
    }
    return results_dict


# to run as module 'python -m path_to_file' (. in place of /)
if __name__ == '__main__':

    fn = '../data_store/examples/example_out_of_stock.html'
    results = execute(fn)
    module_logger.info(f'result: {results}')