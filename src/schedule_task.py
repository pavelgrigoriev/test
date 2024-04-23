import schedule
import time

dct = {
    '1mail@mail.ru': False,
    '2mail@mail.ru': True,
    '3mail@mail': True,
    '4mail@mail': False
}


def _func(email):
    print(f'hello world for {email}')


def check_and_schedule():
    while True:
        for email, value in dct.items():
            if value:
                if not schedule.get_jobs(tag=email):
                    schedule.every(3).seconds.do(_func, email).tag(email)
            else:
                if schedule.get_jobs(tag=email):
                    schedule.clear(tag=email)

        schedule.run_pending()
        time.sleep(1)

check_and_schedule()