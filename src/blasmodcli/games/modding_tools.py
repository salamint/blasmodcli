from blasmodcli.version import Version
import blasmodcli.games.game

from requests import get as request, HTTPError


class ModdingTools:

    def __init__(self, game: 'blasmodcli.games.game.Game', loader: str, repository: str):
        self.loader_directory = game.directory / loader
        self.repository = repository
        platform = "linux" if game.is_native else "windows"
        stem = f"modding-tools-{platform}"
        self.archive_url = f"{repository}/raw/main/{stem}.zip"
        self.archive_file = game.tool_directories.cache / "modding-tools.zip"
        self.version_url = f"{repository}/raw/main/{stem}.version"
        self.version_file = game.tool_directories.data / f"{stem}.version"

    def are_installed(self) -> bool:
        return self.loader_directory.is_dir()

    def get_current_version(self) -> Version | None:
        if not self.version_file.is_file():
            return None
        with self.version_file.open("r") as file:
            current = Version.from_string(file.read())
        return current

    def get_latest_version(self) -> Version:
        response = request(self.version_url)
        if not response.ok:
            raise HTTPError("Unable to fetch the latest version of the modding tools.")
        return Version.from_string(response.text)
