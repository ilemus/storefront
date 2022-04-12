from typing import List, Dict

from storefront.common.exceptions import NoRecordException


def get_person_by_id(cursor, person_id: int) -> Dict[str, str]:
    cursor.execute('SELECT person_first_name, person_last_name, person_email from vendor where person_id=%s',
                   (person_id,))
    result = cursor.fetchone()
    if result is None:
        raise NoRecordException(f'Cannot find vendor for id: {id}')
    return {
        'first_name': result[0][0],
        'last_name': result[0][1],
        'person_email': result[0][1]
    }


def get_person_addresses(cursor, person_id: int) -> List[Dict]:
    """
    Get a list of addresses associated to a vendor
    :param cursor:
    :param person_id:
    :return:
    """
    cursor.execute('SELECT street_address, city, zip_code, state FROM person_address WHERE person_id=%s', (person_id,))
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
