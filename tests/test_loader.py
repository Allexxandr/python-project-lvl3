from tempfile import TemporaryDirectory
from page_loader.get_request import load
import os


def read_file(path):
    with open(path) as f:
        return f.read()

def test_loader(requests_mock):
    requests_mock.get('https://ru.hexlet.io/courses', text='data')

    with TemporaryDirectory() as tmpdir:
        print('!!!', tmpdir)
        load('https://ru.hexlet.io/courses',tmpdir)
        actual = read_file(os.path.join(tmpdir, 'ru-hexlet-io-courses.html'))
        # expected = read_file('./tests/fixtures/mytest-com.html')
        assert actual == 'data'



def test_local_resources():
    with TemporaryDirectory() as tmpdir:
        load('https://ru.hexlet.io/courses', tmpdir)
        expected = os.path.join(
            'ru-hexlet-io-courses',
            tmpdir,
        )
        assert len(os.listdir(os.path.join(expected))) != 0
