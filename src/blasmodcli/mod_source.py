

class ModSource:
    """
    A source of mods is a URL to a JSON file containing metadata for mods.
    When updating the mod database, this JSON is fetched and parsed, and the
    SQLite database is then updated with the new metadata.

    Resolving dependencies
    ----------------------
    The same mod can be referenced in multiple sources, but can be installed from only one source.
    Dependencies will be resolved within the same source if they are found. If a dependency is not
    found in the same source as the mod, the tool will look for the dependency in other sources.
    """

    def __init__(self, name: str, url: str, maintainer: str):
        """
        Initializes a new mod source.
        :param name: The name or prefix of the mod source.
        This is used to distinguish mods that are referenced in multiple sources.
        :param url: The URL pointing to a JSON file containing the mods metadata.
        :param maintainer: The name of the person maintaining the source of mods.
        """
        self.name = name
        self.url = url
        self.maintainer = maintainer