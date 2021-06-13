import pytest
from nate.util.io_funcs import pickle_save, pickle_load, read_text_file
from mock import mock_open, patch
import pickle

import shutil
import subprocess
import textwrap

import pytest

pythonlist = ["python3.6", "python3.7", "python3.8"]


@pytest.fixture(params=pythonlist)
def python1(request, tmpdir):
    picklefile = tmpdir.join("data.pickle")
    return Python(request.param, picklefile)


@pytest.fixture(params=pythonlist)
def python2(request, python1):
    return Python(request.param, python1.picklefile)


class Python:
    def __init__(self, version, picklefile):
        self.pythonpath = shutil.which(version)
        if not self.pythonpath:
            pytest.skip(f"{version!r} not found")
        self.picklefile = picklefile

    def dumps(self, obj):
        dumpfile = self.picklefile.dirpath("dump.py")
        dumpfile.write(
            textwrap.dedent(
                r"""
                import pickle
                f = open({!r}, 'wb')
                s = pickle.dump({!r}, f, protocol=4)
                f.close()
                """.format(
                    str(self.picklefile), obj
                )
            )
        )
        subprocess.check_call((self.pythonpath, str(dumpfile)))

    def load_and_is_true(self, expression):
        loadfile = self.picklefile.dirpath("load.py")
        loadfile.write(
            textwrap.dedent(
                r"""
                import pickle
                f = open({!r}, 'rb')
                obj = pickle.load(f)
                f.close()
                res = eval({!r})
                if not res:
                    raise SystemExit(1)
                """.format(
                    str(self.picklefile), expression
                )
            )
        )
        print(loadfile)
        subprocess.check_call((self.pythonpath, str(loadfile)))


@pytest.mark.parametrize("obj", [42, {}, {1: 3}])
def test_basic_objects(python1, python2, obj):
    python1.dumps(obj)
    python2.load_and_is_true(f"obj == {obj}")


def test_pickle_save(pickle):
    pickle_save('mock/test_obj', pickle())

def test_pickle_load(pickle):

    result = pickle_load({'a': 1, 'b': 2, 'c': 3})
    self.assertEqual(, obj)



def test_read_text_file():
    pass