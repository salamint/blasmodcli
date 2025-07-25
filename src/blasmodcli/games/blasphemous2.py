from blasmodcli.utils import Directories

from blasmodcli.games.game import Game


class BlasphemousII(Game):

    def __init__(self):
        wine_emulated_root = Directories.STEAM_APPS / "compatdata" / "2114740" / "pfx" / "drive_c"
        super().__init__(
            "Blasphemous 2",
            "blas2modcli",
            "MelonLoader",
            "https://github.com/BrandenEK/BlasII.ModdingTools",
            wine_emulated_root / "users" / "steamuser" / "AppData" / "LocalLow" / "The Game Kitchen" / "Blasphemous 2",
            is_native=False
        )

    # TODO: configure Blasphemous II
    def configure_modding_tools(self) -> int:
        return 0
