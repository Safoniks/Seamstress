import logging

from seamstress.celery import celery
from django.conf import settings

from worker.models import Worker
from public.models import WorkerTiming

__all__ = (
    'reset_daily_timing',
)


logger = logging.getLogger(__name__)


@celery.task
def reset_daily_timing():
    all_workers = Worker.objects.all()
    for worker in all_workers:
        if not worker.is_last_timing_reset:
            last_timing = worker.timings.last().action
            worker.timer_do(WorkerTiming.RESET)
            if last_timing == WorkerTiming.START:
                worker.timer_do(WorkerTiming.START)

            print('Resetting timing for worker {} was successful'.format(worker.user.username))



