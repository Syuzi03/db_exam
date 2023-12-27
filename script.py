import json
import random
import string
from sqlalchemy.orm import sessionmaker
from connection import Buyer, engine

Session = sessionmaker(bind=engine)
session = Session()

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))

large_data = {"key_{}".format(i): generate_random_string(10) for i in range(1000)}

json_large_data = json.dumps(large_data)

new_product = Buyer(
    name="Large Data Buyer",
    address="Large Data Manufacturer",
    phone="",
    contact_person="",
    json_data=json_large_data
)

session.add(new_product)
session.commit()
