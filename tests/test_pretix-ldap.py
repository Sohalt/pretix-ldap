import subprocess
import pytest
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from lxml import etree


@pytest.fixture(scope="module")
def start_pretix():
    import os

    print(os.getcwd())
    print(os.system("ls"))
    print("start pretix")
    subprocess.Popen(["podman-compose", "up"])
    print("started pretix")
    yield
    print("stop pretix")
    subprocess.run(["podman-compose", "down"])
    print("stopped pretix")


@pytest.fixture(scope="module")
def wait_for_pretix(start_pretix):
    """Wait for pretix to become responsive"""
    request_session = requests.Session()
    retries = Retry(total=10, backoff_factor=10, status_forcelist=[500, 502, 503, 504])
    request_session.mount("http://", HTTPAdapter(max_retries=retries))

    api_url = "http://localhost:8080"
    print(api_url)
    assert request_session.get(api_url)
    return api_url


@pytest.fixture(scope="function")
def login(wait_for_pretix):
    s = requests.Session()
    try:

        def _login(email, password):
            res = s.get(wait_for_pretix + "/control/login?backend=pretix_ldap")
            assert "Log in" in res.text
            dom = etree.HTML(res.text)
            csrf_token = dom.xpath('//input[@name="csrfmiddlewaretoken"]')[0].get(
                "value"
            )
            s.post(
                res.url,
                data={
                    "csrfmiddlewaretoken": csrf_token,
                    "email": email,
                    "password": password,
                },
            )
            return s, wait_for_pretix

        yield _login
    finally:
        s.post(wait_for_pretix + "/control/logout")


def test_login_available(wait_for_pretix):
    res = requests.get(wait_for_pretix + "/control")
    assert "Log in" in res.text
    assert "LDAP Authentication" in res.text


def test_login_wrong_user(login):
    s, url = login("foo@example.com", "password")
    assert "Log in" in s.get(url + "/control").text


def test_login_wrong_password(login):
    s, url = login("admin@example.com", "foo")
    assert "Log in" in s.get(url + "/control").text


def test_login_success(login):
    s, url = login("admin@example.com", "password")
    assert "Log out" in s.get(url + "/control").text
