from abc import ABC, abstractmethod
from asyncio import TaskGroup
from enum import IntEnum


class JobStatus(IntEnum):
    PENDING = 0
    RUNNING = 1
    COMPLETED = 2


class Job(ABC):

    def __init__(self, job_list: 'JobList'):
        self.list = job_list
        self.status = JobStatus.PENDING

    def complete(self):
        self.status = JobStatus.COMPLETED
        self.list.running_jobs -= 1
        self.list.completed_jobs += 1

    @abstractmethod
    async def internal_run(self):
        pass

    async def run(self):
        self.status = JobStatus.RUNNING
        await self.internal_run()
        self.complete()


class JobList(ABC):

    def __init__(self, concurrent_jobs: int, total_jobs: int):
        self.jobs: list['Job'] = []
        self.concurrent_jobs = concurrent_jobs
        self.running_jobs = 0
        self.completed_jobs = 0
        self.total_jobs = total_jobs
        self.task_group = TaskGroup()

    @property
    def jobs_left(self) -> int:
        return self.total_jobs - (self.completed_jobs + self.running_jobs)

    def add_job(self, job: 'Job'):
        self.jobs.append(job)
        self.running_jobs += 1
        self.task_group.create_task(job.run())

    async def run(self):
        async with self.task_group:
            while self.jobs_left != 0:
                if self.running_jobs != self.concurrent_jobs:
                    job = self.get_next_job()
                    self.add_job(job)

    @abstractmethod
    def get_next_job(self) -> 'Job':
        pass
