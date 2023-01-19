from tests.conftest import post_stream, prepare_data


def test_int_123():
    fname = "123"
    data = prepare_data(f'tests/test_data/{fname}.wav')
    r = post_stream(data, 'dash')
    assert r.status_code == 400


def test_int_add3sandwich():
    fname = "add3sandwich"
    data = prepare_data(f'tests/test_data/{fname}.wav')
    r = post_stream(data, "dash")
    assert r.status_code == 400


def test_int_edwinfrenchfries():
    fname = "edwinfrenchfries"
    data = prepare_data(f'tests/test_data/{fname}.wav')
    r = post_stream(data, "dash")
    assert r.status_code == 400


def test_addfries():
    fname = "addfries"
    data = prepare_data(f'tests/test_data/{fname}.wav')
    r = post_stream(data, "dash")
    print(r.json())
    # assert len(r.json()['message'][0]['data']['addCartItemV2']['orders'][0]['orderItems']) == 1


def test_addburger():
    fname = "add2burger"
    data = prepare_data(f'tests/test_data/{fname}.wav')
    r = post_stream(data, "dash")
    print(r.json())


def test_addchicken():
    fname = "chicken"
    data = prepare_data(f'tests/test_data/{fname}.wav')
    r = post_stream(data, "dash")
    print(r.json())


def test_int_ttsclearcart():
    fname = "ttsclearcart"
    data = prepare_data(f'tests/test_data/{fname}.wav')
    r = post_stream(data, "dash")
    print(r.text)
