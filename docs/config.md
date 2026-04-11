# Configuration

This page documents how to add support for other games and add your own sources of mods,
by adding or editing configuration files located in `~/.config/blasmodcli/`.

## Contents

1. [Games](#games)
   1. [General information](#general-information)
   2. [Modding tools](#modding-tools-mandatory)
      1. [Dependencies](#dependencies-optional)
2. [Sources](#sources)

## Games

Support for new games can be done by adding a new TOML file under the `games` directory.
The file of the name doesn't matter, but it is preferable to use the same name as the game's identifier you chose.

Every game supported by this tool is uniquely identified by a string, which is neither the game's title nor the Steam
app ID. This is because the game's title has a chance to not be unique and is slightly more inconvenient to type, and
the Steam app ID is hard to remember and is an integer.

The identifier string you chose does not impact the way the game is managed or mods are installed, so when choosing a
new name, chose one that is easy to type and remember, and also makes sense. It is used in the tool's database and
sources configuration files however, so only change an existing identifier if you know what you are doing.

### General information

The name of the main section should be the identifier of the game, for example if "My Game" is identified by `mygame`,
then the main section should be:
```toml
[mygame]
# ...
```

It is technically possible to have the configuration for multiple games in the same file on this basis, but this is
untested and not a recommended practice.

Here is the list of fields that this section contains:

| Field             | Type    | Description                                                           |
|-------------------|---------|-----------------------------------------------------------------------|
| `title`           | string  | The title of the game.                                                |
| `steamapp_id`     | integer | The game's Steam app ID.                                              |
| `developer`       | string  | The game's developer or development studio name.                      |
| `publisher`       | string  | The game's publisher.                                                 |
| `linux_native`    | boolean | Indicates if the game runs natively on Linux or runs through Proton.  |
| `saves_directory` | string  | The location of the directory containing the save files for the game. |

The `title`, `developer` and `publisher` fields are used as metadata, meant to be displayed by the tool at during
certain steps, their value don't matter other than to inform the user.

The `steamapp_id`, `linux_native` and `saves_directory` fields are used by the installer for some technical tasks
however, so make sure to input the correct values, or it will crash or have an undefined behavior.

### Modding tools (mandatory)

The modding tools (or mod loaders) are what games use to load mods during startup. They are in charge of injecting the
code of each mod when booting the game. In the case of this software, linux native games are always assumed to use
[BepInEx](https://github.com/BepInEx/BepInEx), while non-native games running through Proton are always assumed to use
[MelonLoader](https://github.com/LavaGang/MelonLoader). This could change in the future if support to other modding
tools is asked, and by specifying which modding tools you want to see supported.

Keeping the same example as earlier with "My Game" identified with `mygame`, the section name for the modding tools must
be `mygame.tools` (or `<game identifier>.tools`). Note that this section is mandatory for every game configuration.

This is the list of fields that this section contains:

| Field        | Type   | Description                                                                                                          |
|--------------|--------|----------------------------------------------------------------------------------------------------------------------|
| `mod_loader` | string | Name of the mod loader, must be either `BepInEx` or `MelonLoader`.                                                   |
| `format`     | string | The format type of the modding tools, used to determine how to install them. Currently only `official` is supported. |
| `url`        | string | The URL of a ZIP archive containing the modding tools, that the software will download and extract.                  |
| `author`     | string | The author or maintainer of the modding tools, used as credit.                                                       |

#### Dependencies (optional)

Some modding tools, like MelonLoader, can require some additional dependencies, such as the .NET Desktop Runtime.
They are indicated in the `mygame.tools.dependencies` section, which is used as dictionary with the following syntax:
```toml
[mygame.tools.dependencies]
winetricks_action_name = "Display name of the Winetricks action"
```

They are, in fact, [Winetricks](https://github.com/Winetricks/winetricks) action names, as they are run using
[Protontricks](https://github.com/Matoking/protontricks) in order to install them.
The display name is just to display a user-friendly and easy to understand and lookup name instead of something like
this: `dotnetdesktop6`, during some steps of the configuration of a game.

## Sources

New sources for mods can be added for one or multiple games by adding a new TOML file under the `sources` directory.
The file name doesn't matter, but it is recommended to name it with the same name as the source.

The name of a source doesn't really matter, but is used to distinguish the different sources when a mod with the same
name is provided by multiple sources. Make it easy to distinguish from other source names and easy to type.

If a source `mysource` provides mods for "My Game" identified by `mygame` and "My Other Game" identified by
`myothergame`, these are the sections that should appear in the source configuration file:
```toml
[mysource.mygame]
# ...

[mysource.myothergame]
# ...
```

Each section describes how the mods metadata are retrieved from the source for each game.

This is the list of fields that is contained in each of those sections:

| Field        | Type   | Description                                                                     |
|--------------|--------|---------------------------------------------------------------------------------|
| `format`     | string | The format type of the source. For now only `official` is supported as a value. |
| `url`        | string | The URL of the source data to fetch.                                            |
| `maintainer` | string | The name of the author or maintainer of the source.                             |
