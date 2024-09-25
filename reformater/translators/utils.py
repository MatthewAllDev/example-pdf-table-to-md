from urllib.request import Request, urlopen
from ..constants_and_types import PathLike


def download_file(url: str, path: PathLike, headers: dict = {}) -> PathLike:
    req : Request = Request(url, headers=headers)
    with open(path, 'wb') as f:
        f.write(urlopen(req).read())
    return path
