import uuid

import pytest

from assistantapi.dash import dash, resolve_cart_id, get_cart


def test_add_item_no_qty():
    transcription = "add sprite"
    with pytest.raises(Exception):
        dash(transcription)


def test_add_item_711():
    transcription = "add 1 sprite"
    dash(transcription, store_="711")


def test_add_item_joe():
    transcription = "add 1 pepperoni pizza"
    dash(transcription, store_="joe")


def test_add_item_mcdonalds():
    transcription = "add 1 fries"
    dash(transcription, store_="mcdonalds")


def test_clear_cart_invalid():
    transcription = "clear mart"
    with pytest.raises(Exception):
        dash(transcription)


def test_clear_cart():
    transcription = "clear cart"
    r = dash(transcription)


def test_remove_item():
    transcription = "remove 1 sandwich"
    r = dash(transcription)


def test_resolve_cart():
    try:
        uuid.UUID(resolve_cart_id())
    except ValueError:
        raise Exception("Failed to resolve cart id")
