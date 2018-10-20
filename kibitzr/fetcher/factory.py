"""
Kibitzr supports a number of fetchers and the list can be extended by plugins.

In the nutshell each fetcher takes conf and returns a tuple: ok, content.
where ok is boolean meaning success, and content is a Unicode string with fetch result.

Each fetcher has a promoter.
Promoter knows if the fetcher is applicable for given conf and
sets a priority for conflict resolution.

Promoter instance is initialized with conf and delegates calls to fetcher.
"""

from kibitzr.exceptions import ConfigurationError

from .loader import load_promoters


PROMOTERS = None


def fetcher_factory(conf):
    """Return initialized fetcher capable of processing given conf."""
    global PROMOTERS
    applicable = []
    if not PROMOTERS:
        PROMOTERS = load_promoters()
    for promoter in PROMOTERS:
        if promoter.is_applicable(conf):
            applicable.append((promoter.PRIORITY, promoter))
    if applicable:
        best_match = sorted(applicable, reverse=True)[0][1]
        return best_match(conf)
    else:
        raise ConfigurationError(
            'No fetcher is applicable for "{0}"'.format(conf['name'])
        )
