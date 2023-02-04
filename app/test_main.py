from app import main
from fastapi import testclient

client = testclient.TestClient(main.app)

def test_healthcheck(monkeypatch, tmpdir):
    monkeypatch.setenv("JOHNNY_CACHE_PREFIX", str(tmpdir))
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "Truckin'"}

def test_put_and_get(monkeypatch, tmpdir):
    monkeypatch.setenv("JOHNNY_CACHE_PREFIX", str(tmpdir))
    response = client.put("/foo", json=["bar"])
    assert response.status_code == 200
    response = client.get("/foo")
    assert response.status_code == 200
    assert response.json() == ["bar"]

def test_get_nonexistent_key(monkeypatch, tmpdir):
    monkeypatch.setenv("JOHNNY_CACHE_PREFIX", str(tmpdir))
    response = client.get("/doesnt-exits-ayy-lmao")
    assert response.status_code == 404


def test_put_twice(monkeypatch, tmpdir):
    monkeypatch.setenv("JOHNNY_CACHE_PREFIX", str(tmpdir))
    response1 = client.put("/foo", json={"foo": "foo"})
    assert response1.status_code == 200
    response2 = client.put("/foo", json={"bar": "bar"})
    assert response2.status_code == 200
    response3 = client.get("/foo")
    assert response3.status_code == 200
    assert response3.json() == {"bar": "bar"}


def test_404_after_delete(monkeypatch, tmpdir):
    monkeypatch.setenv("JOHNNY_CACHE_PREFIX", str(tmpdir))
    response1= client.put("/foo", json=["bar"])
    assert response1.status_code == 200
    response2 = client.delete("/foo")
    assert response2.status_code == 200
    response3 = client.get("/foo")
    assert response3.status_code == 404

def test_put_str(monkeypatch, tmpdir)
