from tempfile import TemporaryDirectory

import requests
from page_loader.get_request import load
from page_loader.get_resources import download
import os
import requests_mock
import pytest
import tempfile



RESOURES_DIR_NAME = 'ru-hexlet-io-courses_files'
HTML_FILE_NAME = 'ru-hexlet-io-courses.html'
RESOURSES_FILE_NAME = 'ru-hexlet-io-assets-professions-nodejs.png'
URL = 'https://ru.hexlet.io/courses'
TEST_HTML = 'tests/fixtures/test_html.html'
HTML_LOCAL_LINKS = os.path.join('tests/fixtures', HTML_FILE_NAME)
RESOURCE = 'https://ru.hexlet.io/courses/assets/professions/nodejs.png'
LOCAL_RESOURCE = 'tests/fixtures/ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-nodejs.png'
SCRIPT = 'https://ru.hexlet.io/courses/assets/professions/nodejs.js'
LOCAL_SCRIPT = 'tests/fixtures/ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-nodejs.js'
CSS = 'https://ru.hexlet.io/courses/assets/professions/nodejs.css'
LOCAL_CSS = 'tests/fixtures/ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-nodejs.css'

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
            mock.get(SCRIPT, content=read_file(LOCAL_SCRIPT, 'rb'))
            mock.get(CSS, content=read_file(LOCAL_CSS, 'rb'))
                    
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


def test_bad_path():
    with pytest.raises(FileNotFoundError):
        download(URL, '/undefined')


def test_bad_filemod():
    with tempfile.TemporaryDirectory() as tmpdirname:
        os.chmod(tmpdirname, 111)
        with pytest.raises(PermissionError):
            download(URL, tmpdirname)

def test_bad_http_request(requests_mock):
    requests_mock.get('http://401.com', status_code=401)
    requests_mock.get('http://404.com', status_code=404)
    requests_mock.get('http://5xx.com', status_code=501)
    requests_mock.get('https://tests/fixtures/ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-nodejs.png', status_code=404)



    with tempfile.TemporaryDirectory() as tmpdirname:
        with pytest.raises(requests.HTTPError) as e:
            download('http://401.com', tmpdirname)
        assert '401 Client Error: None for url: http://401.com/' == str(e.value)

        with pytest.raises(requests.HTTPError) as e:
            download('http://404.com', tmpdirname)
        assert '404 Client Error: None for url: http://404.com/' == str(e.value)

        with pytest.raises(requests.HTTPError) as e:
            download('http://5xx.com', tmpdirname)
        assert '501 Server Error: None for url: http://5xx.com/' == str(e.value)

        with pytest.raises(requests.HTTPError) as e:
            download('https://tests/fixtures/ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-nodejs.png', tmpdirname)
        resourse_path = os.path.join(
            tmpdirname,
            'ru-hexlet-io-courses_files',
            'ru-hexlet-io-assets-professions-nodejs.png'
        )
        assert '404 Client Error: None for url: https://tests/fixtures/ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-nodejs.png' == str(e.value)