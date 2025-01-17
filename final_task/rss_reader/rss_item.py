import html
import re
from colorama import Fore, Back, Style, init
from codecs import encode, decode
from dataclasses import asdict, dataclass

import jsonpickle
init()


@dataclass
class RssItem:
    '''
    Represents a single news from RSS channel

    source: stores link to rss channel of the news
    date: stores date on YYYY%MM%DD format
    media: contains link to an image
    img: contains base64 representation of an image
    '''
    title: str
    published: str
    description: str
    link: str
    media: str
    source: str
    date: str
    img: str

    def __post_init__(self):
        self.title = html.unescape(self.title)
        self.published = html.unescape(self.published)
        self.description = html.unescape(self.description)

    @classmethod
    def from_dict(cls, item_dict) -> 'RssItem':
        return cls(**item_dict)

    def __str__(self):
        return f'TITLE: {Back.BLACK + Fore.WHITE + self.title + Style.RESET_ALL}\
            \n\t|| DESCRIPTION: {Fore.MAGENTA + self.description + Fore.RESET}\
            \n\t|| PUBLISHED: {Fore.GREEN + self.published + Fore.RESET}\
            \n\t|| LINK: {Fore.BLUE + self.link + Fore.RESET}\
            \n\t|| MEDIA: {Fore.YELLOW + self.media + Fore.RESET}'

    def to_json(self):
        jsonpickle.load_backend('json', 'dumps', 'loads')
        jsonpickle.set_preferred_backend('json')
        # ensure_ascii = False to solve encoding problems
        jsonpickle.set_encoder_options('json', indent=4, sort_keys=False, ensure_ascii=False)
        json_string = jsonpickle.encode(self, make_refs=False, unpicklable=False)
        # Regex finds base64 string and replaces it
        json_string = re.sub(r'(\"img\":\ )\"b\'.*?\'', r'\1"base64 image', json_string)
        # Unescaping
        json_string = decode(encode(json_string, 'latin-1', 'backslashreplace'), 'unicode-escape')
        print(json_string)

    def asdict(self):
        return asdict(self)
