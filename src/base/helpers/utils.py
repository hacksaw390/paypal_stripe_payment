import re
from typing import Callable, List
from django.db.models import Lookup
from django.apps import apps
import uuid
import random
from django.db import connection


def create_slug(title: str, random_str: str = None) -> str:
    title = re.sub('[^A-Za-z ]+', ' ', title).lower().strip()
    title = re.sub(' +', '-', title)
    if random_str:
        return title + '-' + random_str
    return title


def entries_to_remove(data: dict, removable_keys: tuple) -> dict:
    for k in removable_keys:
        data.pop(k, None)
    return data


def format_filter_string(old_dict, keys):
    filtered_dict = {}
    for k in keys:
        if old_dict.get(k):
            filtered_dict[k] = old_dict.get(k)
    return filtered_dict


def get_model_from_app(app_name: str, model_name: str):
    try:
        return apps.get_model(app_label=app_name, model_name=model_name)
    except Exception as ex:
        return None


def flatten(l_data):
    return [item for sublist in l_data for item in sublist]


def snake_to_title(string: str):
    return string.replace("_", " ").title()


class NotEqual(Lookup):
    lookup_name = 'ne'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return '%s <> %s' % (lhs, rhs), params


def remove_duplicate_from_list(iterable: List, key:  Callable = None) -> List:
    if key is None:
        def key(x): return x

    seen = set()
    for elem in iterable:
        k = key(elem)
        if k in seen:
            continue

        yield elem
        seen.add(k)



def my_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4())
    random = random.upper()
    random = random.replace("-", "")
    return random[0:string_length]


def identifier_builder(table_name: str, prefix: str = None) -> str:
    with connection.cursor() as cur:
        query = f'SELECT id FROM {table_name} ORDER BY id DESC LIMIT 1;'
        cur.execute(query)
        row = cur.fetchone()
    try:
        seq_id = str(row[0] + 1)
    except:
        seq_id = "1"
    random_suffix = random.randint(10, 99)
    if not prefix:
        return seq_id.rjust(8, '0') + str(random_suffix)
    return prefix + seq_id.rjust(8, '0') + str(random_suffix)