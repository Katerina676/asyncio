import asyncio
import aiosqlite3
import aiosmtplib
from more_itertools import chunked
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


MAILS = 5
TIME = 10


PARAMS = {
    'host': 'smtp.mailtrap.io',
    'username': 'username',
    'password': 'password',
    'port': 25,
    'mailfrom': 'test@example.com'
}


async def db_contacts():
    async with aiosqlite3.connect('contacts.db') as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM contacts;")
            list_contacts = await cur.fetchall()
    return list_contacts


async def sendmail_async(to, name, **params):
    mail_params = params.get("mail_params", PARAMS)
    msg = MIMEMultipart()
    msg['Subject'] = "THANKS!"
    msg['From'] = mail_params.get('mailfrom')
    msg['To'] = to

    body = f'''Уважаемый(ая) {name}! Спасибо, что пользуетесь нашим сервисом объявлений.'''

    msg.attach(MIMEText(body, 'plain'))

    host = mail_params.get('host', 'localhost')
    port = mail_params.get('port')
    smtp = aiosmtplib.SMTP(hostname=host, port=port)
    await smtp.connect()
    if 'username' in mail_params:
        await smtp.login(mail_params['username'], mail_params['password'])
    result = await smtp.send_message(msg)
    await smtp.quit()
    return result


async def main():
    contacts = await db_contacts()
    for contacts_chunk in chunked(contacts, MAILS):
        sendmail_coroutines = [
            sendmail_async(to=to, name=f'{first_name} {last_name}')
            for _, first_name, last_name, to, *other in contacts_chunk
        ]
        await asyncio.gather(*sendmail_coroutines)
        time.sleep(TIME)


if __name__ == '__main__':
    asyncio.run(main())
