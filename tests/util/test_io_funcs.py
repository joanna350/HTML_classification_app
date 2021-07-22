from main.util.io_funcs import pickle_save, pickle_load, read_text_file


def test_pickle_modules(tmpdir):
    # temporary creation using fixture, therefore testing both modules at once
    pfp = tmpdir.mkdir("mock").join("pobj")
    pickle_save(pfp, {"a": 0})
    assert pickle_load(pfp) == {"a": 0}
    assert len(tmpdir.listdir()) == 1


def test_read_text_file(tmpdir):
    tfp = tmpdir.mkdir("mock").join("tobj")
    tfp.write("content")
    assert read_text_file(tfp) == "content"
    assert len(tmpdir.listdir()) == 1
