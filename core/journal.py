import os
import json
from etc.conf import settings

def get_journal(default, journal_loc=settings.LOCAL_JOURNAL_LOCATION):
    """
    Reads journal file, deserialize it to python object
    :param default: Default value if journal file is not yet available.
    :param journal_loc: Location of journal file
    :return: Deserialized journal object.
    """
    local_journal_file = os.path.expanduser(journal_loc)
    try:
        local_journal = json.loads(file(local_journal_file).read())
    except IOError:
        local_journal = default
    return local_journal_file, local_journal