from celery import shared_task


@shared_task
def adding_task(x, y):
    print(x+y)
    return x + y
