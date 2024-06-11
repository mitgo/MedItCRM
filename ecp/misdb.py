# todo сделать функции корректировки пользователей и наблюдения за установленными
#  сертификатами или установку этих сертификатов в мис. надо подумать как...

import os
import pyodbc
if os.environ.get('POSTGRES_USER'):
    driver = '{ODBC Driver 18 for SQL Server}'
else:
    driver = '{SQL Server}'


def connect():
    try:
        conn = pyodbc.connect(
                                DRIVER=driver,
                                server=os.getenv('MIS_DB_HOST'),
                                database=os.getenv('MIS_DB'),
                                PWD=os.getenv('DB_PASS'),
                                UID=os.getenv('DB_USER'),
                                TrustServerCertificate='yes',
                             )
        return conn
    except pyodbc.Error as ex:
        return None


def get_sert_id(fio: str):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        raw_sql = "select u.fam, us.ValueStr from x_User u	inner join x_UserSettings us on " \
                  "u.UserID = us.rf_UserID  and property = 'Номер сертификата пользователя' where u.fio=?"
        cursor.execute(raw_sql, fio)
        resp = cursor.fetchall()
        cursor.close()
        conn.close()
    else:
        resp = None
    return resp


def update_cert_id(fio: str, cert_id: str):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        raw_sql = ""
        cursor.execute(raw_sql, fio, cert_id)
        resp = ''
        cursor.close()
        conn.close()
    else:
        resp = None
    return resp


def get_not_installed_keys(act_keys: str, act_fios: str):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        raw_sql = "select distinct u.fio from x_User u left join x_UserSettings us on u.UserID = us.rf_UserID " \
                  " and property = 'Номер сертификата пользователя' where (UPPER(replace(us.ValueStr, ' ', '')) " \
                  "not in " + act_keys + " or us.ValueStr is null ) and UPPER(fio) in " + act_fios + " except " \
                  "select u.fio from x_User u inner join x_UserSettings us on u.UserID = us.rf_UserID " \
                  "and property = 'Номер сертификата пользователя'  where UPPER(replace(us.ValueStr, ' ', ''))" \
                  " in " + act_keys + "and fio in " + act_fios
        cursor.execute(raw_sql)
        fio = []
        for item in cursor.fetchall():
            fio.append(item[0])
        cursor.close()
        conn.close()
    else:
        fio = None
    return fio
