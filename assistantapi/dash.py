import json
import logging

import requests
from flask import abort
from word2number import w2n

from assistantapi.config import HEADERS, MENU, STORE, PASSWORD


def resolve_cart_id():
    url = "https://www.doordash.com/graphql?operation=consumer"

    with open(f"assistantapi/stores/consumer.json") as f:
        payload = f.read()

    if payload is None:
        abort(500, "Error loading consumer payload")

    response = requests.request("POST", url, headers=HEADERS, data=payload)

    try:
        cart_id = response.json()['data']['consumer']['orderCart']['id']
    except Exception:
        abort(500, "Failed to get cart")

    return cart_id


def resolve_item_payload(store_, command, words):
    for item in MENU:
        if item in words:
            payload_file = f"{command}_{item}.json"
            with open(f"assistantapi/stores/{store_}/{payload_file}") as f:
                return f.read()
    return None


def add_item(store_, words, quantity=1):
    payload = resolve_item_payload(store_, "add", words)

    if payload is None:
        abort(400, f"Error resolving item: {words}")

    payload_json = json.loads(payload)
    url = f"https://www.doordash.com/graphql?operation={payload_json['operationName']}"

    if payload_json['operationName'] == "addCartItem":
        payload_json['variables']['addCartItemInput']['quantity'] = quantity

    payload = json.dumps(payload_json)

    response = requests.request("POST", url, headers=HEADERS, data=payload)

    return response.json()


def remove_item(words):
    logging.error("Remove item not supported, use clear cart")
    return None


def get_cart():
    url = "https://www.doordash.com/graphql?operation=detailedCartItems"

    with open(f"assistantapi/stores/get_cart.json") as f:
        payload = f.read()

    if payload is None:
        abort(500, "Error resolving payload")

    payload_json = json.loads(payload)
    payload_json['variables']['orderCartId'] = resolve_cart_id()
    payload = json.dumps(payload_json)

    response = requests.request("POST", url, headers=HEADERS, data=payload)
    return response.json()


def clear_cart():
    responses = []
    url = "https://www.doordash.com/graphql?operation=removeCartItem"
    try:
        order_cart = get_cart()['data']['orderCart']
        order = order_cart['orders'][0]
    except Exception as e:
        if len(order_cart['orders']) == 0:
            abort(400, f"Cart already empty")
        else:
            abort(500, f"Failed to get cart")

    with open(f"assistantapi/stores/remove_item.json") as f:
        payload = f.read()

    if payload is None:
        abort(500, "Error resolving payload")

    payload_json = json.loads(payload)
    payload_json['variables']['cartId'] = resolve_cart_id()

    for item in order['orderItems']:
        payload_json['variables']['itemId'] = item['id']
        payload = json.dumps(payload_json)
        responses.append(requests.request("POST", url, headers=HEADERS, data=payload))

    return responses


def place_order():
    url = "https://www.doordash.com/graphql?operation=createOrderFromCart"

    with open(f"assistantapi/stores/place_order.json") as f:
        payload = f.read()

    if payload is None:
        abort(500, "Error resolving payload")

    payload_json = json.loads(payload)
    payload_json['variables']['cartId'] = resolve_cart_id()
    payload = json.dumps(payload_json)

    response = requests.request("POST", url, headers=HEADERS, data=payload)
    return response.json()


def process_dtmf(store_, dtmf):
    logging.warning(f"DTMF Detected: {dtmf}")
    if dtmf == 1:
        return add_item(store_, "fries")
    elif dtmf == 2:
        return clear_cart()
    return None


def dash(transcription, dtmf=0, store_=STORE):
    words = transcription.lower().split(' ')
    if dtmf != 0:
        return process_dtmf(store_, dtmf)
    elif "add" in words:
        temp = words[words.index("add") + 1:]
        try:
            quantity = w2n.word_to_num(temp[0])
        except ValueError:
            if temp[0] == "to" or temp[0] == "too":
                quantity = 2
            else:
                abort(400, f"Item quantity not detected. Command syntax: \"Add <qty> <item>\". Transcript: {transcription}")

        if not (0 < quantity < 10):
            abort(400, "Item quantity must be a non-zero digit")

        r = add_item(store_, temp[1:], quantity)
        return r
    elif "clear" in words:
        temp = words[words.index("clear") + 1:]

        if "cart" != temp[0]:
            logging.warning(f"Command assumed: {transcription}")
            # abort(400, f"Command not recognized: {transcription}")

        return clear_cart()
    elif "remove" in words:
        return remove_item(words)
    elif "place" in words:
        temp = words[words.index("place") + 1:]

        if "order" != temp[0]:
            abort(400, f"Command not recognized: {transcription}")

        if PASSWORD in words:
            r = place_order()
            resolve_cart_id()
            return r
        else:
            logging.warning("Place Order Failed: INCORRECT PASSWORD")
        return None
    else:
        abort(400, f"Command not recognized: {transcription}")
