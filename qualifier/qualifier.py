from enum import auto, StrEnum
from re import compile
from warnings import warn

MAX_QUOTE_LENGTH = 50
QUOTE_RE = compile(r'(?P<command>quote uwu|quote piglatin|quote list|quote)( [\"“](?P<quote>.+)[\"”])?')


# The two classes below are available for you to use
# You do not need to implement them
class VariantMode(StrEnum):
    NORMAL = auto()
    UWU = auto()
    PIGLATIN = auto()


class DuplicateError(Exception):
    """Error raised when there is an attempt to add a duplicate entry to a database"""


# Implement the class and function below
class Quote:
    def __init__(self, quote: str, mode: "VariantMode") -> None:
        self.quote = quote
        self.mode = mode
        self.computed = None

    def __str__(self) -> str:
        return self._create_variant()

    def _as_uwu(self) -> str:
        quote_stage_1 = self.quote.replace('l', 'w').replace('r', 'w').replace("L", "W").replace("R", "W")
        quote_stage_2 = quote_stage_1.replace(" U", " U-U").replace(" u", " u-u")
        if quote_stage_2.startswith("U"):
            quote_stage_2 = "U-" + quote_stage_2
        elif quote_stage_2.startswith("u"):
            quote_stage_2 = "u-" + quote_stage_2

        if len(quote_stage_2) > 50:
            warn("Quote too long, only partially transformed")
            return quote_stage_1

        return quote_stage_2

    def _as_piglatin(self) -> str:
        words = self.quote.split()
        piglatin: list[str] = []

        for word in words:
            first_vowel = 0
            for i, letter in enumerate(word):
                if letter in 'aeiouAEIOU':
                    first_vowel = i
                    break

            if first_vowel == 0:
                piglatin.append(word + 'way')
            else:
                piglatin.append(word[first_vowel:] + word[:first_vowel] + 'ay')

        almost = ' '.join(piglatin).capitalize()
        return almost[0].upper() + almost[1:]

    def _create_variant(self) -> str:
        """
        Transforms the quote to the appropriate variant indicated by `self.mode` and returns the result
        """

        match self.mode:
            case VariantMode.NORMAL:
                return self.quote
            case VariantMode.UWU:
                return self._as_uwu()
            case VariantMode.PIGLATIN:
                return self._as_piglatin()


def run_command(command: str) -> None:
    """
    Will be given a command from a user. The command will be parsed and executed appropriately.

    Current supported commands:
        - `quote` - creates and adds a new quote
        - `quote uwu` - uwu-ifys the new quote and then adds it
        - `quote piglatin` - piglatin-ifys the new quote and then adds it
        - `quote list` - print a formatted string that lists the current
           quotes to be displayed in discord flavored markdown
    """
    match = QUOTE_RE.match(command)
    if not match:
        raise ValueError("Invalid command")

    command = match.group('command')
    raw_quote = match.group('quote')

    if command != 'quote list' and not raw_quote:
        raise ValueError("Invalid command")

    if command == 'quote list':
        for quote in Database.get_quotes():
            print("-", quote)
        return

    if len(raw_quote) > 50:
        raise ValueError("Quote is too long")

    if command == 'quote':
        quote = Quote(raw_quote, VariantMode.NORMAL)
    elif command == 'quote uwu':
        quote = Quote(raw_quote, VariantMode.UWU)
        if str(quote) == raw_quote:
            raise ValueError("Quote was not modified")
    elif command == 'quote piglatin':
        quote = Quote(raw_quote, VariantMode.PIGLATIN)
        if len(str(quote)) > 50:
            raise ValueError("Quote was not modified")
    else:
        # This one shouldn't happen, but better safe than sorry
        raise ValueError("Invalid command")

    try:
        Database.add_quote(quote)
    except DuplicateError:
        print("Quote has already been added previously")


# The code below is available for you to use
# You do not need to implement it, you can assume it will work as specified
class Database:
    quotes: list["Quote"] = []

    @classmethod
    def get_quotes(cls) -> list[str]:
        "Returns current quotes in a list"
        return [str(quote) for quote in cls.quotes]

    @classmethod
    def add_quote(cls, quote: "Quote") -> None:
        "Adds a quote. Will raise a `DuplicateError` if an error occurs."
        if str(quote) in [str(quote) for quote in cls.quotes]:
            raise DuplicateError
        cls.quotes.append(quote)
