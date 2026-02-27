from aiohttp import ClientSession
from pathlib import Path

from blasmodcli.model import Mod, Version
from blasmodcli.repositories.filesystems.caching import CacheDirectory
from blasmodcli.utils.resolver import ModVersion

from blasmodcli.utils.jobs.job import Job, JobList


DOWNLOAD_CHUNK_SIZE = 1024
DOWNLOAD_JOBS = 8


async def download(session: ClientSession, url: str, file: Path, chunk_size: int = DOWNLOAD_CHUNK_SIZE):
    async with session.get(url) as response:
        with file.open("wb") as fd:
            async for chunk in response.content.iter_chunked(chunk_size):
                fd.write(chunk)


class DownloadJob(Job):

    def __init__(self, job_list: 'JobList', cache_directory: CacheDirectory, mod: Mod, version: Version):
        super().__init__(job_list)
        self.cache_directory = cache_directory
        self.mod = mod
        self.version = version

    @property
    def archive(self) -> Path:
        return self.cache_directory.get_archive(self.mod, self.version)

    @property
    def download_url(self) -> str:
        return self.mod.get_download_url(self.version)

    async def internal_run(self):
        async with ClientSession() as session:
            await download(session, self.download_url, self.archive)


class Downloader(JobList):

    def __init__(self, mod_versions: list[ModVersion], cache_directory: CacheDirectory, jobs: int = DOWNLOAD_JOBS):
        super().__init__(jobs, len(mod_versions))
        self.mod_versions = mod_versions
        self.cache_directory = cache_directory

    def get_next_job(self) -> 'Job':
        index = self.completed_jobs + self.running_jobs
        mod, version = self.mod_versions[index]
        return DownloadJob(self, self.cache_directory, mod, version)
