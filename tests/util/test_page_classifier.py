import pytest

from main.util.page_classifier import PageClassifier
from main.util.io_funcs import read_text_file
from main.data.functions_for_dataset_creator import (
    html_str_to_one_string_of_visible_text,
)
from main.util.io_funcs import pickle_load

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
import numpy as np
import os


"""
tests here will only pass with the current files under saved_predictor_temp
"""


class DataSet:
    def __init__(self, html_str):
        self.list_of_text_strs = [
            html_str_to_one_string_of_visible_text(hstr) for hstr in [html_str]
        ]


pg = PageClassifier({"models": {"NAME": "SGD"}})


def test_PageClassifier():

    assert pg.config == {"models": {"NAME": "SGD"}}
    assert isinstance(pg.vectorizer, TfidfVectorizer)
    assert isinstance(pg.clf, SGDClassifier)

    base = {
        "example_site_error.html": (
            [4],
            [0.099036, 0.12707462, 0.12858985, 0.08324735, 0.32321404, 0.23883814],
        ),
        "example_product_landing.html": (
            [2],
            [0.04487083, 0.01430674, 0.73620608, 0.01140521, 0.14678729, 0.04642387],
        ),
        "example_out_of_stock.html": (
            [3],
            [0.07218344, 0.0218594, 0.06108213, 0.6292346, 0.10222567, 0.11341476],
        ),
    }

    root = "main/data_store/examples/"
    fns = os.listdir(root)
    for fn in fns:
        html_string = read_text_file(os.path.join(root, fn))
        data = DataSet(html_string)

        # test model uploaded
        pg.clf = pickle_load(os.path.join("main/saved_predictor_temp", "clf.pickle"))
        pg.vectorizer = pickle_load(
            os.path.join("main/saved_predictor_temp", "vectorizer.pickle")
        )
        classnum_in_list, confidence_array = pg.predict(data)

        assert classnum_in_list == base[fn][0]
        for i in range(len(confidence_array)):
            assert np.isclose(confidence_array[i], base[fn][1][i], atol=10 ** -7)


testdata = [
    (
        [[-1.69252517, -1.44323409, -1.43138068, -1.86619224, -0.5096938, -0.81222246]],
        [0.099036, 0.12707462, 0.12858985, 0.08324735, 0.32321404, 0.23883814],
    )
]


@pytest.mark.parametrize("input, output", testdata)
def test_softmax(input, output):
    compare = pg.softmax(input)
    for i in range(len(output)):
        assert np.isclose(compare[i], output[i], atol=10 ** -8)
