import pytest
from django.urls import reverse

from aguaapp.django_assertions import assert_contains


@pytest.fixture
def resp(client):
    resp = client.get(reverse('home'))
    return resp


@pytest.fixture
def resp_logado(client_com_usuario_logado):
    resp_logado = client_com_usuario_logado.get(reverse('home'))
    return resp_logado


def test_status_code(resp):
    assert resp.status_code == 302


def test_status_code_logado(resp_logado):
    assert resp_logado.status_code == 200


def test_titulo_logado(resp_logado):
    assert_contains(resp_logado, '<title>Agua</title>')
