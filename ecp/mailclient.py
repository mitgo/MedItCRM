import re
from pytils.translit import translify
from datetime import datetime, timedelta
import imaplib
import os
import email
import base64
from .utils import get_esign_by_req_num, get_esign_by_req_uuid, get_esign_by_fio, create_esign_status, \
    get_all_settings_email_subject, update_esign_by_fio
from zipfile import ZipFile
from django_cron.models import CronJobLog
# ------------------------------------MAIL FUNCTIONS-----------------------------------------


def connect():
    mail_pass = os.getenv('MAIL_PASS')
    mail_user = os.getenv('MAIL_USER')
    imap_server = os.getenv('IMAP_SERVER')
    if not (mail_pass and mail_user and imap_server):
        return False
    imap = imaplib.IMAP4_SSL(imap_server)
    try:
        return_code, res = imap.login(mail_user, mail_pass)
        if return_code == 'OK':
            return imap
        else:
            return False
    except Exception as error:
        return repr(error)


def logout(imap):
    try:
        imap.close()
        return_code, res = imap.logout()
        return return_code
    except Exception as error:
        return repr(error)


# -----------------------------------END MAIL FUNCTIONS--------------------------------------

def get_id_messages_about_certs(imap, subject):
    term = subject.encode('utf-8')
    imap.literal = term
    res, msgs = imap.uid('search', "UNSEEN", 'charset', 'utf-8', 'SUBJECT')
    if res == 'OK':
        return msgs
    else:
        return False


def get_msg_body(msg):
    body = None
    for part in msg.walk():
        if part.get_content_maintype() == 'text' and (
                part.get_content_subtype() == 'plain' or part.get_content_subtype() == 'html'):
            body = base64.b64decode(part.get_payload()).decode()
    return body


def get_fio(msg_body):
    start_index_of_fio = msg_body.find('ФИО:') + 5
    end_index_of_fio = msg_body.find('</div>', start_index_of_fio)
    fio = msg_body[start_index_of_fio: end_index_of_fio]
    return fio


def get_request_num(msg_body):
    index_of_request_num = msg_body.find('кат №') + 5
    request_num = msg_body[index_of_request_num: index_of_request_num + 6]
    return request_num


def get_link_copy_request(msg_body):
    start_index_of_link = msg_body.find('/requests/edit/') + 15
    end_index_of_link = msg_body.find('">ссылке</a>, указав', start_index_of_link)
    link = 'https://fzs.roskazna.ru/Requests/FzsRefuseDisplay' + msg_body[start_index_of_link: end_index_of_link]
    return link


def get_request_uuid(msg_body):
    request_uuid = msg_body[-36:]
    return request_uuid


def get_reason(msg_body):
    end_index_of_reason = msg_body.find('</div>')
    reason = msg_body[:end_index_of_reason].replace('<br />', '')
    return reason


def get_date_time(msg_body):
    date_time_str = re.search(r'[0-3][0-9]\.[0-1][0-9]\.20[2-3][0-9]\s[0-2][0-9]+:[0-5][0-9]', msg_body)[0]
    date_time = datetime.strptime(date_time_str, '%d.%m.%Y %H:%M') + timedelta(hours=9)
    return date_time


def get_info_about_cert(msg_body):
    start_index_cert_num = msg_body.find(' № ') + 3
    end_index_cer_num = msg_body.find(' ', start_index_cert_num)
    cert_num = msg_body[start_index_cert_num: end_index_cer_num]
    start_index_date_get = msg_body.find('действия сертификата: с ') + 24
    date_str = msg_body[start_index_date_get: start_index_date_get + 10]
    date_get = datetime.strptime(date_str, "%d.%m.%Y").date()
    start_index_date_end = msg_body.find(' по ', start_index_date_get) + 4
    date_str = msg_body[start_index_date_end: start_index_date_end + 10]
    date_valid = datetime.strptime(date_str, "%d.%m.%Y").date()
    return cert_num, date_get, date_valid


def store_cer_on_uploads(message):
    for part in message.walk():
        if (part.get_content_type() == 'application/octet-stream' and part.get_filename()[-3:] == 'zip') or \
                part.get_content_type() == 'application/zip':
            filename = 'file.zip'
            att_path = os.path.join('/opt/MedItCRM/uploads', filename)
            if not os.path.isfile(att_path):
                try:
                    zip_file = open(att_path, 'wb')
                    zip_file.write(part.get_payload(decode=True))
                    zip_file.close()
                except Exception as err:
                    print('Не смог создать архивный файл: ' + repr(err) + ' - ' + att_path)
                    return False
            with ZipFile(att_path, 'r') as zfile:
                for name in zfile.namelist():
                    (dirname, zfilename) = os.path.split(name)
                    if zfilename[-4:] == '.cer':
                        zfile.extract(name, '/opt/MedItCRM/uploads')
                        _now = datetime.now()
                        path = f'/opt/MedItCRM/uploads/cers/{_now.strftime("%Y")}-{_now.strftime("%m")}'
                        os.makedirs(path, exist_ok=True)
                        new_path = f'{path}/{translify(zfilename)}'
                        os.replace(f'/opt/MedItCRM/uploads/{zfilename}', new_path)
                        zfile.close()
                        os.remove(att_path)
                        return new_path
    return False


def update_certs_from_mail():
    imap = connect()
    if not imap:
        return False
    status, messages = imap.select('INBOX')
    if status != 'OK':
        return False

    # subject, encoding = decode_header(msg["Subject"])[0]
    # Запрос прошел проверки в СМЭВ

    # Get all email_subjects settings
    for subj in get_all_settings_email_subject():
        # Get all emails according to subject
        id_messages = get_id_messages_about_certs(imap, subj['setting_value'])
        if id_messages:
            # Decoding message retrieved by subject
            unseen_messages = id_messages[0].decode('utf-8').split(' ')
            if unseen_messages[0]:
                for message_id in unseen_messages:
                    # Extract msg from email
                    res, msg = imap.uid("fetch", message_id, '(RFC822)')
                    unseen = True
                    if res == 'OK':
                        msg = email.message_from_bytes(msg[0][1])
                        # Extract msg_body from msg
                        msg_body = get_msg_body(msg)
                        if subj['setting_name'] == 'subject_email_cert_02_reject_operator_ufk':
                            if reject_by_operator_ufk_processing(msg_body):
                                unseen = False
                        if subj['setting_name'] == 'subject_email_cert_03_reject_bot':
                            if reject_bot_processing(msg_body):
                                unseen = False
                        if subj['setting_name'] == 'subject_email_cert_04_reject_link':
                            if msg_body.find('Запрос на сертификат №') != -1:
                                if reject_bot_processing(msg_body):
                                    unseen = False
                            if msg_body.find(
                                    'Запрос на сертификат отклонен оператором регионального центра регистрации') != -1:
                                if reject_by_operator_processing(msg_body):
                                    unseen = False
                        if subj['setting_name'] == 'subject_email_cert_05_reject_operator':
                            if reject_by_operator_ufk_processing(msg_body, trusted_person=True):
                                unseen = False
                        if subj['setting_name'] == 'subject_email_cert_09_visit_prompt':
                            if visit_prompt_processing(msg_body):
                                unseen = False
                        if subj['setting_name'] == 'subject_email_cert_10_is_ready':
                            if msg_body.find('Файл сертификата № ') != -1:
                                if ready_processing(msg, msg_body):
                                    unseen = False
                    if unseen:
                        imap.uid('STORE', message_id, '-FLAGS', '(\\SEEN)')
    imap.close()
    CronJobLog.objects.filter(pk__in=CronJobLog.objects.filter(is_success=True).order_by('-id').values('pk')[10:]).\
        delete()
    return True


def reject_bot_processing(msg_body):
    esign = get_esign_by_req_num(get_request_num(msg_body))
    date_reject = get_date_time(msg_body)
    if esign:
        request_response = {"esign": esign,
                            "status_txt": 'Отклонен ботом',
                            "link": get_link_copy_request(msg_body),
                            "status_code": 1,
                            }
        if date_reject:
            request_response['date'] = date_reject
        if create_esign_status(request_response):
            return True
    return False


def reject_by_operator_processing(msg_body):
    fio = get_fio(msg_body)
    esign = get_esign_by_fio(fio)
    if esign:
        request_response = {"esign": esign,
                            "status_txt": 'Отклонен оператором регионального центра регистрации',
                            "reason": get_reason(msg_body[msg_body.find('Причина отклонения:') + 19:]),
                            "status_code": 1,
                            }
        if create_esign_status(request_response):
            return True
    return False


def reject_by_operator_ufk_processing(msg_body, trusted_person=None):
    esign = get_esign_by_req_uuid(get_request_uuid(msg_body[:msg_body.find('">Запрос на сертификат</a>')]))
    status = 'Отклонен оператором Удостоверяющего центра Федерального Казначейства'
    if trusted_person:
        status.replace('Удостоверяющего центра', 'доверенного лица')
    if esign:
        request_response = {"esign": esign,
                            "status_txt": status,
                            "reason": get_reason(msg_body[msg_body.find('Причина отклонения: ') + 20:]),
                            "status_code": 1,
                            }
        if create_esign_status(request_response):
            return True
    return False


def visit_prompt_processing(msg_body):
    fio = get_fio(msg_body)
    fio = fio[:-1]
    esign = get_esign_by_fio(fio)
    visit_prompt_date = get_date_time(msg_body)
    if esign:
        request_response = {"esign": esign,
                            "status_txt": 'Приглашение на личный визит',
                            "status_code": 2,
                            }
        if visit_prompt_date:
            request_response['date'] = visit_prompt_date
        if create_esign_status(request_response):
            return True
    return False


def ready_processing(message, msg_body):
    fio = get_fio(msg_body)
    try:
        [cer_num, date_get, date_valid] = get_info_about_cert(msg_body)
    except Exception:
        return False
    cer_path = store_cer_on_uploads(message)
    if cer_path:
        content = {
            'cer': cer_path,
            'key': cer_num,
            'date_get': date_get,
            'date_valid': date_valid
        }
        if update_esign_by_fio(fio, content):
            return True
        else:
            os.remove(cer_path)
    return False

#
# class MailClient():
#     connection = None
#     error = None
#
#     def __init__(self, server, username, password):
#         if not (username and password and server):
#             self.error = 'No username or pass or server'
#         self.connection = imaplib.IMAP4_SSL(server)
#         try:
#             return_code, res = self.login(username, password)
#             if return_code != 'OK':
#                 self.error = 'Could not connect to server'
#         except Exception as error:
#             self.error = repr(error)
#         self.connection.select(readonly=False)  # so we can mark mails as read
#
#     def close_connection(self):
#         self.connection.close()
#
#     def save_attachment(self, msg, download_folder="/tmp"):
#         """
#         Given a message, save its attachments to the specified
#         download folder (default is /tmp)
#
#         return: file path to attachment
#         """
#         att_path = "No attachment found."
#         for part in msg.walk():
#             if part.get_content_maintype() == 'multipart':
#                 continue
#             if part.get('Content-Disposition') is None:
#                 continue
#
#             filename = part.get_filename()
#             att_path = os.path.join(download_folder, filename)
#
#             if not os.path.isfile(att_path):
#                 fp = open(att_path, 'wb')
#                 fp.write(part.get_payload(decode=True))
#                 fp.close()
#         return att_path
#
#     def fetch_unread_messages(self):
#         """
#         Retrieve unread messages
#         """
#         emails = []
#         (result, messages) = self.connection.search(None, 'UnSeen')
#         if result == "OK":
#             for message in messages[0].split(' '):
#                 try:
#                     ret, data = self.connection.fetch(message,'(RFC822)')
#                 except:
#                     print "No new emails to read."
#                     self.close_connection()
#                     exit()
#
#                 msg = email.message_from_bytes(data[0][1])
#                 if isinstance(msg, str) == False:
#                     emails.append(msg)
#                 response, data = self.connection.store(message, '+FLAGS','\\Seen')
#
#             return emails
#
#         self.error = "Failed to retreive emails."
#         return emails
#
#
# mc = MailClient(getenv('IMAP_SERVER', ''), getenv('MAIL_USER', ''),
# getenv('MAIL_PASS', ''))
#
#
