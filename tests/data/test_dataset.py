import os
import pytest
from main.data.dataset import Dataset


def test_Dataset():
    ds = Dataset(dataset_dir=".", training_set=True)
    assert ds.dataset_dir == "."
    assert ds.training_set == True
    assert ds.list_of_text_strs == []
    assert ds.class_value_counter == {}
    assert ds.max_items_per_class == None


def test_load_from_directory_of_htmls():
    # refreshing
    ds = Dataset(dataset_dir="tests/data/", training_set=True)
    ds.load_from_directory_of_htmls("tests/data/out_of_stock", "out_of_stock")
    assert len(ds.list_of_text_strs) == 2
    assert ds.class_value_counter["out_of_stock"] == 2


def test_load_from_class_names():
    # refreshing
    ds = Dataset(dataset_dir="tests/data/", training_set=True)
    ds.load_from_class_names(["out_of_stock"])
    assert len(ds.list_of_text_strs) == 2
    assert ds.class_value_counter[0] == 2


def test_load_from_list_of_strings():
    root = "main/data_store/examples/"
    fps = os.listdir(root)  # id list
    testdata = {}
    base = {
        "example_out_of_stock.html": "women men kids sale + x@ off bags new in trending designers clothing shoes bags accessories jewelry pre owned we re sorry but the item you were looking for is no longer available here are some items you might like instead sale shop up to @ off more designers added shop now sorry this piece is currently out of stock email me when itâ € ™s back sold out junya watanabe sequin mesh top same brand different style just for you knitted tops by junya watanabe junya watanabe $ @ junya watanabe $ @ @ | @ off $ @ junya watanabe $ @ @ | @ off $ @ junya watanabe $ @",
        "example_product_landing.html": "store locator log in register womens mens bostonian originals kids sale @ home womens sandals breeze sea breeze sea $ @ @ $ @ @ ★★★★★ @ off @ product description an eva midsole and a soft eva footbed allow this classic flip flop to be incredibly lightweight and comfortably supportive a subtle closure on its strap makes for a secure adjustable fit while providing extra visual interest perfect for every beach on your summer getaway list color navy synthetic select size size guide @ @ @ @ @ @ @ select width medium add to shopping bag product details shoe care returns upper material synthetic lining material textile heel height @ cm sole material tpr fastening type riptape removable insole no others also viewed @ off arla jacory womens sand $ @ @ $ @ @ @ off step glow slip womens shoes natural $ @ @ $ @ @ @ off tilden cap mens shoes wine leather $ @ @ $ @ @ @ off arla glison womens sandals blue fabric $ @ @ $ @ @ reviews write a review",
        "example_site_error.html": "this site canâ € ™t be reached â € ™s server ip address could not be found www lookout trendz com try checking the connection checking the proxy firewall and dns configuration err name not resolved reload details",
    }
    ds = Dataset()
    for fp in fps:
        print(fp)
        with open(os.path.join(root, fp), "r", encoding="utf-8") as text_file:
            ex = text_file.read()
            testdata[fp] = [ex]
            ds.load_from_list_of_strings(testdata[fp])
            assert ds.list_of_text_strs[0] == base[fp]
