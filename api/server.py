from typing import Iterator
from api.handler import url_handlers


def app(environ, start_reponse) -> Iterator[bytes]:
    return iter([url_handlers(environ, start_reponse)])
