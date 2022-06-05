from tempfile import TemporaryDirectory
from page_loader.get_request import load
from page_loader.get_resources import download
import os
import requests_mock

RESOURES_DIR_NAME = 'ru-hexlet-io-courses_files'
HTML_FILE_NAME = 'ru-hexlet-io-courses.html'
RESOURSES_FILE_NAME = 'ru-hexlet-io-assets-professions-nodejs.png'
URL = 'https://ru.hexlet.io/courses'
TEST_HTML = 'tests/fixtures/test_html.html'
HTML_LOCAL_LINKS = os.path.join('tests/fixtures', HTML_FILE_NAME)
RESOURCE = 'https://ru.hexlet.io/courses/assets/professions/nodejs.png'
LOCAL_RESOURCE = 'tests/fixtures/ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-nodejs.png'

def read_file(path, mode='r'):
    with open(path, mode) as f:
        return f.read()



def test_loader(requests_mock):
    requests_mock.get('https://ru.hexlet.io/courses', text='data')



    with TemporaryDirectory() as tmpdir:
        print('!!!', tmpdir)
        load('https://ru.hexlet.io/courses',tmpdir)
        actual = read_file(os.path.join(tmpdir, 'ru-hexlet-io-courses.html'))
        # expected = read_file('./tests/fixtures/mytest-com.html')
        assert actual == 'data'



def test_download():
    with TemporaryDirectory() as test_dir:
        with requests_mock.Mocker() as mock:
            mock.get(URL, text=read_file(TEST_HTML))
            mock.get(RESOURCE, content=read_file(LOCAL_RESOURCE, 'rb'))
                    
            html_file_path = download(URL, test_dir)
            file1 = read_file(html_file_path)
            file2 = read_file(HTML_LOCAL_LINKS)
            assert file1 == file2
            assert HTML_FILE_NAME == os.path.split(html_file_path)[1]
            dir_path = os.path.join(test_dir, RESOURES_DIR_NAME)
            assert os.path.isdir(dir_path)
            path_to_file = os.path.join(dir_path, RESOURSES_FILE_NAME)
            print(path_to_file)
            assert os.path.isfile(path_to_file)
            assert read_file(path_to_file, 'rb') == read_file(LOCAL_RESOURCE, 'rb')
                



def test_local_resources():
    with TemporaryDirectory() as tmpdir:
        load('https://ru.hexlet.io/courses', tmpdir)
        expected = os.path.join(
            'ru-hexlet-io-courses',
            tmpdir,
        )
        assert len(os.listdir(os.path.join(expected))) != 0
