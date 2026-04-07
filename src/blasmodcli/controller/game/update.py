from asyncio import TaskGroup
from pathlib import Path

from blasmodcli.controller.game.group import GameCommandGroup
from blasmodcli.model import Mod, Source
from blasmodcli.utils import Color, Message
from blasmodcli.utils.parsing import OfficialModListParser, ModListParser
from blasmodcli.view import format_mod_name, Counter, step, NumberedList


# TODO: show upgrades available
class Update(GameCommandGroup):
    """ Updates the mod database and fetches the latest mod version, allowing to detect upgradable mods. """

    parsers: list[ModListParser]
    mods: list[Mod]

    def post_init(self):
        super().post_init()
        self.mods = []
        self.parsers = []

    @step("Reading mod source files...")
    async def read_configs(self):
        async with TaskGroup() as task_group:
            files = list(self.config.sources.files())
            numbered_list = NumberedList(len(files))
            for file in files:
                task_group.create_task(self.load_config(numbered_list, file))

    @step("Fetching sources...")
    async def fetch_sources(self):
        for source in self.config.sources.all:
            await self.fetch_source(source)

    @step("Resolving dependencies...")
    def resolve_dependencies(self):
        for parser in self.parsers:
            parser.resolve_dependencies()

    @step("Committing to database...")
    def commit_to_database(self):
        self.tables.sources.update_all(self.config.sources.all)
        self.tables.mods.update_all(self.mods)

    async def fetch_source(self, source: Source):
        parser = OfficialModListParser(source)
        await parser.fetch()
        counter = Counter(parser.total, f"Parsing mod source '{parser.source.name}' for '{parser.source.game_id}'")
        counter.print()
        async with TaskGroup() as task_group:
            for data in parser.data():
                task_group.create_task(self.fetch_mod(counter, parser, data))
        parser.extend(self.mods)
        self.parsers.append(parser)

    async def fetch_mod(self, counter: Counter, parser: ModListParser, data: dict):
        mod = await parser.parse(data)
        self.mods.append(mod)
        counter.increment()
        counter.print()

    async def load_config(self, numbered_list: NumberedList, file: Path):
        relative_name = file.relative_to(self.config.sources.directory)
        progress = numbered_list.add_progress(str(relative_name))
        sources = self.config.sources.load_file(file)
        progress.status(f"{sources} sources found", Color.YELLOW)

    @step("Checking for upgrades...")
    def check_for_upgrades(self):
        upgrades = self.fs.installations.get_upgrades(self.game)
        number_of_upgrades = len(upgrades)
        if number_of_upgrades > 0:
            Message.info(f"{number_of_upgrades} new upgrades are available:")
            for mod, version in upgrades:
                prefix = f"  {Color.GREEN.fmt("-")}"
                current_version = Color.YELLOW.fmt(version)
                newest_version = Color.YELLOW.fmt(mod.latest_version)
                print(f"{prefix} {format_mod_name(mod)} {current_version} -> {newest_version}")
        else:
            Message.info("Nothing to show.")

    # TODO: handle timeouts
    async def handle(self) -> int:
        await self.read_configs()
        await self.fetch_sources()
        self.resolve_dependencies()
        self.commit_to_database()
        self.check_for_upgrades()
        Message.success("Update successful!")
        return 0
