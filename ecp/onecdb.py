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
                                server=os.getenv('ONEC_DB_HOST'),
                                database=os.getenv('ONEC_DB'),
                                PWD=os.getenv('DB_PASS'),
                                UID=os.getenv('DB_USER'),
                                TrustServerCertificate='yes',
                                   )
        return conn
    except pyodbc.Error as ex:
        return None


def persons_from_1c(fio: str):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        raw_sql = '''select  convert(varchar(1000), sotr._IDRRef, 2) as id
                            , sotr._Description as Name
                            , case when kadrDann._Fld22345 = '2001-01-01 00:00:00' then NULL else convert(NVARCHAR, 
                            DateAdd(year, -2000, kadrDann._Fld22345), 4) end as Date
                        from _InfoRg22338 kadrDann 
                                inner join _Reference372 sotr on kadrDann._Fld22340RRef = sotr._IDRRef and 
                                (kadrDann._Fld22345 = '2001-01-01 00:00:00'  or DATEADD(year, -2000, kadrDann._Fld22345) 
                                >= DATEADD(day, 90, GetDate()))
                        where sotr._Description like ? 
                        order by kadrDann._Fld22345
        '''
        cursor.execute(raw_sql, fio)
        resp = cursor.fetchall()
        cursor.close()
        conn.close()
    else:
        resp = None
    return resp


def import_person_from_1c(id_sotr: str):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        raw_sql = '''
        select  fizLica._Fld34918 as fam
            , fizLica._Fld34919 as im
            , fizLica._Fld34920 as ot
            , sotr._Fld33569 as УточнениеНаименования
            , dateadd(yy, -2000, cast(fizLica._Fld34899 as date)) as db
            , fizLica._Fld34903 as bitrh_place
            , case when tel._Fld34926 is null then '' else tel._Fld34926 end as phone
            , fizLica._Fld34902 as snils
            , fizLica._Fld34901 as inn
            , pasp._Fld18333 as pasp_s
            , pasp._Fld18334 as pasp_n
            , dateadd(yy, -2000, cast(pasp._Fld18335 as date)) as pasp_date
            , pasp._Fld18337 as pasp_kem
            , pasp._Fld18338 as pasp_dep
            ,_Fld22348 as ДатаПриема
            ,_Fld22345 as ДатаУвольнения
            , podr._Description as dep
            , doljn._Description as post
            , doljn._Fld39511
            , doljn._Description
           , kadrDannInter._Fld19171
           , kadrDannInter._Fld19170
        from 
            _InfoRg22338 kadrDann 
            inner join _Reference372 sotr on kadrDann._Fld22340RRef = sotr._IDRRef 
                                            and kadrDann._Fld22345 = '2001-01-01 00:00:00'
            inner join _Reference453 fizLica on sotr._Fld33564RRef = fizLica._IDRRef
            left join _Reference453_VT34922 tel on fizLica._IDRRef = tel._Reference453_IDRRef  
                                            and tel._Fld34925RRef = 0x9434902B341C2EB911E9BF35BA23DB71
            inner join _InfoRg18330 pasp on pasp._Fld18331RRef = fizLica._IDRRef and 
                                        pasp._Period = (select max(_Period) from _InfoRg18330 
                                        where _Fld18331RRef = fizLica._IDRRef and 
                                        convert(varchar(1000), _Fld18332RRef, 2) in 
                                        ('9434902B341C2EB911E9BF35E4BE91F7', '9434902B341C2EB911E9BF35E4BE91F8', 
                                        '9434902B341C2EB911E9BF35E4BE91FF', '9434902B341C2EB911E9BF35E4BE9203') 
                                        and _Fld18339 = 1 )
            inner join _InfoRg19168 kadrDannInter on kadrDannInter._Fld19169RRef = sotr._IDRRef 
                                                    and dateadd(yy, 2000, cast(GetDate() as date)) 
                                                    between kadrDannInter._Fld19171 and kadrDannInter._Fld19170
            inner join _Reference111 doljn on kadrDannInter._Fld19179RRef = doljn._IDRRef
            inner join _Reference291 podr on podr._IDRRef = kadrDannInter._Fld19183RRef
        where convert(varchar(1000), sotr._IDRRef, 2) = ?
        '''
        cursor.execute(raw_sql, id_sotr)
        resp = cursor.fetchall()
        cursor.close()
        conn.close()
    else:
        resp = None
    return resp
