from django_cron import CronJobBase, Schedule
import ecp.mailclient as mailclient
class Mail(CronJobBase):
    RUN_EVERY_MINS = 10
    RETRY_AFTER_FAILURE_MINS = 10
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'ecp.mail_job'

    def do(self):
        mailclient.update_certs_from_mail()
