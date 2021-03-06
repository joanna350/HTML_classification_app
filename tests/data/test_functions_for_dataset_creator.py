from main.data.functions_for_dataset_creator import is_visible
from main.data.functions_for_dataset_creator import preprocess_text
from main.data.functions_for_dataset_creator import preprocess_list
from main.data.functions_for_dataset_creator import (
    html_str_to_one_string_of_visible_text,
)
from main.data.functions_for_dataset_creator import text_from_html_main
from main.data.functions_for_dataset_creator import base_site_from_html
from main.data.functions_for_dataset_creator import filter_dict_creator
from main.data.functions_for_dataset_creator import get_key_from_val
import os
from bs4 import BeautifulSoup
import pytest
from collections import defaultdict


root = "main/data_store/examples/"
fps = os.listdir(root)  # id list
testdata0 = {}  # for the first
testdata1 = {}  # for the 2 consecutive
for fp in fps:
    with open(os.path.join(root, fp), "r", encoding="utf-8") as text_file:
        ex = text_file.read()
        testdata0[fp] = ex
        soup = BeautifulSoup(ex, "html.parser")
        ele = soup.findAll()
        testdata1[fp] = ele


def test_html_in_one_chunk():
    base0 = {
        "example_out_of_stock.html": "women men kids sale + x@ off bags new in trending designers clothing shoes bags accessories jewelry pre owned we re sorry but the item you were looking for is no longer available here are some items you might like instead sale shop up to @ off more designers added shop now sorry this piece is currently out of stock email me when itâ € ™s back sold out junya watanabe sequin mesh top same brand different style just for you knitted tops by junya watanabe junya watanabe $ @ junya watanabe $ @ @ | @ off $ @ junya watanabe $ @ @ | @ off $ @ junya watanabe $ @",
        "example_product_landing.html": "store locator log in register womens mens bostonian originals kids sale @ home womens sandals breeze sea breeze sea $ @ @ $ @ @ ★★★★★ @ off @ product description an eva midsole and a soft eva footbed allow this classic flip flop to be incredibly lightweight and comfortably supportive a subtle closure on its strap makes for a secure adjustable fit while providing extra visual interest perfect for every beach on your summer getaway list color navy synthetic select size size guide @ @ @ @ @ @ @ select width medium add to shopping bag product details shoe care returns upper material synthetic lining material textile heel height @ cm sole material tpr fastening type riptape removable insole no others also viewed @ off arla jacory womens sand $ @ @ $ @ @ @ off step glow slip womens shoes natural $ @ @ $ @ @ @ off tilden cap mens shoes wine leather $ @ @ $ @ @ @ off arla glison womens sandals blue fabric $ @ @ $ @ @ reviews write a review",
        "example_site_error.html": "this site canâ € ™t be reached â € ™s server ip address could not be found www lookout trendz com try checking the connection checking the proxy firewall and dns configuration err name not resolved reload details",
    }
    for fp in fps:
        # call strucure: html_str_to_one_string_of_visible_text -> text_from_html_main -> is_visible
        assert html_str_to_one_string_of_visible_text(testdata0[fp]) == base0[fp]


def test_text_from_html_main():
    base1 = {
        "example_out_of_stock.html": 37,
        "example_product_landing.html": 82,
        "example_site_error.html": 9,
    }
    for fp in fps:
        assert len(text_from_html_main(testdata1[fp])) == base1[fp]


def test_is_visible():
    base2 = {
        "example_out_of_stock.html": 65,
        "example_product_landing.html": 116,
        "example_site_error.html": 11,
    }
    for fp in fps:
        visibles = list(filter(is_visible, testdata1[fp]))
        assert len(visibles) == base2[fp]


testdata3 = [
    ("sale + x20% off bags", "sale + x@ off bags"),
    (
        "We're sorry but the item you were looking for is no longer available. Here are some items you might like instead.",
        "we re sorry but the item you were looking for is no longer available here are some items you might like instead",
    ),
]


@pytest.mark.parametrize(
    "input, output",
    testdata3,
    ids=["replace number with @", "special character removal and lowercase"],
)
def test_preprocess_text(input, output):
    assert preprocess_text(input) == output


testdata4 = [
    (
        [
            "This site canâ€™t be reached",
            "â€™s server IP address could not be found.",
            "www.lookout-trendz.com",
            "Try:",
            "Checking the connection",
            "Checking the proxy, firewall and DNS configuration",
            "ERR_NAME_NOT_RESOLVED",
            "\n",
            "\n",
            "\n",
            "Reload",
            "Details",
        ],
        [
            "this site canâ € ™t be reached",
            "â € ™s server ip address could not be found",
            "www lookout trendz com",
            "try",
            "checking the connection",
            "checking the proxy firewall and dns configuration",
            "err name not resolved",
            "reload",
            "details",
        ],
    )
]


@pytest.mark.parametrize("input, output", testdata4)
def test_preprocess_list(input, output):
    assert preprocess_list(input) == output


testdata5 = [
    ("0a95bd9bbe7b14f39eaf16713e90ede1_desktop_1400_1000.html", "www.yoox.com")
]


@pytest.mark.parametrize("input, output", testdata5)
def test_base_site_from_html(input, output):
    train_path = "main/data_store/train/out_of_stock"
    assert base_site_from_html(input, train_path) == output


testdata6 = [
    ("www.victoriassecret.com", [True, 3]),
    ("www.marksandspencer.com", [False, 15]),
    ("www.waterstones.com", [True, 1]),
]

testdata7 = {"www.marksandspencer.com": 15, "www.victoriassecret.com": 2}
testdata7 = defaultdict(int, testdata7)


@pytest.mark.parametrize("input, output", testdata6)
def test_filter_dict_creator(input, output):
    bool_, upd_dict = filter_dict_creator(
        input, testdata7.copy()
    )  # prevent mutable obj from updating
    assert bool_ == output[0]  # bool
    assert upd_dict[input] == testdata7[input] + int(bool_)  # increase and not


def test_get_key_from_val():
    class_num = {
        "out_of_stock": 0,
        "popup": 1,
        "product_landing_page": 2,
        "product_listing": 3,
        "site_error": 4,
        "bot": 5,
    }
    for i, k in zip(range(5), list(class_num.keys())):
        assert get_key_from_val(i, class_num) == k
