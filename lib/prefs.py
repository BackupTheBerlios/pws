
class MatchPrefs(dict):
    """
    Match preferences dict type with the abilty to load prefs from disk
    """
    
    def __init__(self, filename=None):
        if filename:
            self._loadFromFile(filename)

    def _loadFromFile(self, filename): pass
