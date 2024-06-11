export DJANGO_DEBUG=0 <br />
export DJANGO_SECRET_KEY=your_django_sec_key <br />
export DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1] <br />
export POSTGRES_HOST=db <br />
export POSTGRES_PORT=5432 <br />
export POSTGRES_USER=your_pg_user <br />
export POSTGRES_PASSWORD=your_pg_pass <br />
export POSTGRES_DB=crm <br />
export NGINX_EXTERNAL_PORT=80 <br />
export DATABASE=postgres <br />
export ONEC_DB_HOST=ip_of_your_1c_zarplata_i_kadri_db_(ms sql) <br />
export ONEC_DB=name_of_1c_db(sql) <br />
export MIS_DB_HOST=tcp:your_tm_mis_db_ip,your_tm_mis_db_port <br />
export IS_DB=dbname_tm_mis <br />
export DB_USER=username_tm_mis_db # **from installation step 3**<br />
export DB_PASS=userpass_tm_mis_db # **from installation step 3**<br />
export ENC=no <br />
export USE_LDAP = 1 # **- if you have and want to use LDAP for AUTH users, else set this to "0" and leave the following 6 fields blank**<br />
export AUTH_LDAP_SERVER_URI = "ldap://yourdomain" (or your PDC) <br />
export AUTH_LDAP_BIND_DN = "user@domain" # user who can get data from domain <br />
export AUTH_LDAP_BIND_PASSWORD = "pass" # user pass who can get data from domain <br />
export AUTH_LDAP_ROOT_DN = "DC=example,DC=ru" <br />
export AUTH_LDAP_USERS_OU = "OU=ГБУЗ АО БГКБ" # ou which users can get access to MedItCRM <br />
export AUTH_LDAP_SU_CN = "CN=Admins,CN=Users" # this group become superuser in MedItCRM <br />
export MAIL_USER = "user@domain.ru" #user from mail.ru mailbox <br />
export MAIL_PASS = "secret_key_for_external_app" # **look at pic.**<br />
export IMAP_SERVER = "imap.mail.ru" <br />
![pic](./images/externalMailApp.png)