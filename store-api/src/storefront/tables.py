PARENT_TABLES = {
    's': 'CREATE TABLE s '
         '(k VARCHAR(64) NOT NULL, '
         'v VARCHAR(64) NOT NULL, '
         'UNIQUE (k), '
         'INDEX k_ind(k), '
         'PRIMARY KEY (k))',
    'vendor': 'CREATE TABLE vendor '
              '(vendor_id INT NOT NULL AUTO_INCREMENT, '
              'vendor_name VARCHAR(32) NOT NULL, '
              'UNIQUE (vendor_id, vendor_name), '
              'INDEX vn_ind(vendor_name), '
              'PRIMARY KEY (vendor_id))',
    'person': 'CREATE TABLE person '
              '(person_id INT NOT NULL AUTO_INCREMENT, '
              'person_first_name VARCHAR(18), '
              'person_last_name VARCHAR(18), '
              'create_date DATETIME NOT NULL, '
              'UNIQUE (person_id), '
              'INDEX pid_ind(person_id), '
              'PRIMARY KEY (person_id))',
}
CHILDREN_TABLES = {
    'vendor_address': 'CREATE TABLE vendor_address '
                      '(vendor_id INT NOT NULL, '
                      'street_address VARCHAR(32) NOT NULL, '
                      'city VARCHAR(16) NOT NULL, '
                      'zip_code INTEGER NOT NULL, '
                      'state VARCHAR(16) NOT NULL, '
                      'INDEX vid_ind(vendor_id), '
                      'FOREIGN KEY (vendor_id) REFERENCES vendor(vendor_id) ON DELETE CASCADE)',
    'person_address': 'CREATE TABLE person_address '
                      '(person_id INT NOT NULL, '
                      'street_address VARCHAR(32) NOT NULL, '
                      'city VARCHAR(16) NOT NULL, '
                      'zip_code INTEGER NOT NULL, '
                      'state VARCHAR(16) NOT NULL, '
                      'INDEX pid_ind(person_id), '
                      'FOREIGN KEY (person_id) REFERENCES person(person_id) ON DELETE CASCADE)',
    'person_login': 'CREATE TABLE person_login '
                    '(person_id INT NOT NULL, '
                    'email_address VARCHAR(64) NOT NULL, '
                    'password VARCHAR(64), '
                    'INDEX e_ind(email_address), '
                    'FOREIGN KEY (person_id) REFERENCES person(person_id) ON DELETE CASCADE)',
    'order_request': 'CREATE TABLE order_request '
                     '(order_id INT NOT NULL AUTO_INCREMENT, '
                     'person_id INT, '
                     'UNIQUE (order_id), '
                     'PRIMARY KEY (order_id), '
                     'INDEX o_ind(order_id), '
                     'INDEX p_ind(person_id), '
                     'FOREIGN KEY (person_id) REFERENCES person(person_id) ON DELETE SET NULL)',
    'item': 'CREATE TABLE item '
            '(item_id INT NOT NULL AUTO_INCREMENT, '
            'item_name VARCHAR(32) NOT NULL, '
            'vendor_id INT NOT NULL, '
            'UNIQUE (item_id), '
            'INDEX i_ind(item_name), '
            'PRIMARY KEY (item_id), '
            'FOREIGN KEY vendor_id REFERENCES vendor(vendor_id) ON DELETE CASCADE)',
}
GRAND_CHILDREN_TABLES = {
    'order_item': 'CREATE TABLE order_detail '
                  '(order_id INT NOT NULL, '
                  'item_id INT, '
                  'quantity TINYINT(1) NOT NULL, '
                  'INDEX o_ind(order_id), '
                  'FOREIGN KEY (item_id) REFERENCES item(item_id) ON DELETE SET NULL, '
                  'FOREIGN KEY (order_id) REFERENCES order_request(order_id) ON DELETE NO ACTION)',
    'order_status': 'CREATE TABLE order_status '
                    '(order_id INT NOT NULL, '
                    'status VARCHAR(16) NOT NULL, '
                    'update_date DATETIME NOT NULL, '
                    'INDEX o_ind(order_id), '
                    'FOREIGN KEY (order_id) REFERENCES order_request(order_id) ON DELETE NO ACTION)'
}
