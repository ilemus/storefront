from typing import List, Dict

from storefront.common.exceptions import NoRecordException


def get_vendor_by_id(cursor, vendor_id: int) -> str:
    cursor.execute('SELECT vendor_name from vendor where vendor_id=%s', (vendor_id,))
    result = cursor.fetchone()
    if result is None:
        raise NoRecordException(f'Cannot find vendor for id: {id}')
    return result[0]


def get_vendor_addresses(cursor, vendor_id: int) -> List[Dict]:
    """
    Get a list of addresses associated to a vendor
    :param cursor:
    :param vendor_id:
    :return:
    """
    cursor.execute('SELECT street_address, city, zip_code, state FROM vendor_address WHERE vendor_id=%s', (vendor_id,))
    addresses = cursor.fetchall()
    if len(addresses) == 0:
        return list()
    addresses = [{
        'street_address': address[0],
        'city': address[1],
        'zip_code': address[2],
        'state': address[3]
    } for address in addresses]
    return addresses


def get_vendor_items(cursor, vendor_id: int) -> List[Dict]:
    """
    Get a list of items sold by the vendor
    :param cursor:
    :param vendor_id:
    :return:
    """
    cursor.execute('SELECT item_id, item_name FROM item WHERE vendor_id=%s', (vendor_id,))
    items = cursor.fetchall()
    if len(items) == 0:
        return list()
    items = [{
        'item_id': item[0],
        'item_name': item[1]
    } for item in items]
    return items
