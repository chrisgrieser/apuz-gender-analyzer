"""
This type stub file was generated by pyright.
"""

import requests
from collections import namedtuple
from itertools import chain, islice

"""
Client for Genderize.io web service.
"""
__all__ = ['Genderize', 'GenderizeException']
__version__ = ...
class GenderizeException(Exception):
    """
    Exception from Genderize.io web service.
    """
    ...


_GenderizeResponse = ...
class Genderize:
    """
    Client for Genderize.io web service.
    Uses a Requests session for persistent HTTP connections.
    """
    BATCH_SIZE = ...
    def __init__(self, user_agent=..., api_key=..., timeout=...) -> None:
        """
        :param user_agent: Optional user agent string.
        :type user_agent: Optional[str]
        :param api_key: Optional API key.
        :type api_key: Optional[str]
        :param timeout: Optional connect/read timeout in seconds.
        :type timeout: Optional[float]
        """
        ...
    
    def get(self, names: list[str], country_id=..., language_id=..., retheader=...) -> list[dict[str, str|float]]:
        """
        Look up gender for a list of names.
        Can optionally refine search with locale info.
        May make multiple requests if there are more names than
        can be retrieved in one call.

        :param names: List of names.
        :type names: Iterable[str]
        :param country_id: Optional ISO 3166-1 alpha-2 country code.
        :type country_id: Optional[str]
        :param language_id: Optional ISO 639-1 language code.
        :type language_id: Optional[str]
        :param retheader: Optional
        :type retheader: Optional[boolean]
        :return:
        If retheader is False:
            List of dicts containing 'name', 'gender',
                     'probability', 'count' keys. If 'gender' is None,
                     'probability' and 'count' will be omitted.
        else:
            A dict containing 'data' and 'headers' keys.
            Data is the same as when retheader is False.
            Headers are the response header
            (a requests.structures.CaseInsensitiveDict).
            If multiple requests were made,
            the header will be from the last one.
        :rtype: Union[dict, Sequence[dict]]
        :raises GenderizeException: if API server returns HTTP error code.
        """
        ...
    
    def get1(self, name, **kwargs): # -> list[Any]:
        """
        Look up gender for a single name.
        See :py:meth:`get`.
        Doesn't support retheader option.
        """
        ...
    


