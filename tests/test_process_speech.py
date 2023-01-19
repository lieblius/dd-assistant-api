from tests.conftest import prepare_data, post_stream


def test_123():
    fname = "123"
    data = prepare_data(f'tests/test_data/{fname}.wav')
    r = post_stream(data)
    assert r.text == "1 2 3"


def test_498():
    fname = "498"
    data = prepare_data(f'tests/test_data/{fname}.wav')
    r = post_stream(data)
    assert r.text == "498"


def test_598():
    fname = "598"
    data = prepare_data(f'tests/test_data/{fname}.wav')
    r = post_stream(data)
    assert r.text == "598"


def test_add1sandwich():
    fname = "add1sandwich"
    data = prepare_data(f'tests/test_data/{fname}.wav')
    r = post_stream(data)
    assert r.text == "add one sandwich"


def test_add3sandwich():
    fname = "add3sandwich"
    data = prepare_data(f'tests/test_data/{fname}.wav')
    r = post_stream(data)
    assert r.text == "add three sandwich"


def test_add3sandwich32():
    fname = "add3sandwich32"
    data = prepare_data(f'tests/test_data/{fname}.wav')
    r = post_stream(data)
    assert r.text == "ask me a sandwich"  # mistranscription


def test_add3sandwiches():
    fname = "add3sandwiches"
    data = prepare_data(f'tests/test_data/{fname}.wav')
    r = post_stream(data)
    assert r.text == "add three sandwiches"


def test_addonesandwich():
    fname = "addonesandwich"
    data = prepare_data(f'tests/test_data/{fname}.wav')
    r = post_stream(data)
    assert r.text == "add one sandwich"


def test_clearcart():
    fname = "clearcart"
    data = prepare_data(f'tests/test_data/{fname}.wav')
    r = post_stream(data)
    assert r.text == "deer cart"  # mistranscription


def test_deleteonesandwich():
    fname = "deleteonesandwich"
    data = prepare_data(f'tests/test_data/{fname}.wav')
    r = post_stream(data)
    assert r.text == "delete one sandwich"


def test_nothing():
    fname = "nothing"
    data = prepare_data(f'tests/test_data/{fname}.wav')
    r = post_stream(data)
    assert r.text == ""


def test_placeorder():
    fname = "placeorder"
    data = prepare_data(f'tests/test_data/{fname}.wav')
    r = post_stream(data)
    assert r.text == "place order"
