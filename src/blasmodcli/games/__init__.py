from blasmodcli.utils import MODDING_INSTALLER_REPOSITORY
from .blasphemous import Blasphemous
from .blasphemous2 import BlasphemousII
from .game import Game
from .modding_tools import ModdingTools

BLASPHEMOUS = Blasphemous()
BLASPHEMOUS.add_mod_source(MODDING_INSTALLER_REPOSITORY + "/raw/main/BlasphemousMods.json")

BLASPHEMOUS_II = BlasphemousII()
BLASPHEMOUS_II.add_mod_source(MODDING_INSTALLER_REPOSITORY + "/raw/main/BlasphemousIIMods.json")
