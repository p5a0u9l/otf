import bs4
import imaplib
import yaml
import sqlite3
import time
from dateutil.parser import parse as datetime_parser
from email.parser import BytesHeaderParser

with open("config.yml") as c:
    config = yaml.load(c)
print("CONFIG: loaded...")

def get_timestamp(txt):
    header = BytesHeaderParser().parsebytes(txt)

    if 'Received' in header.keys():
        datetime = header['Received'].split(';')[1].strip()
        timestamp = datetime_parser(datetime).timestamp()
    else:
        raise Exception("GMAIL: unable to parse header...")

    return timestamp

def init_db():
    db = sqlite3.Connection(config['database']['name'])
    print("SQL: connected...")
    dbc = db.cursor()
    dbc.execute(config['sql']['create'])
    db.commit()
    dbc.close()
    print("SQL: table iniz'd...")
    return db

def logn():
    gmail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    print("GMAIL: connected...")
    with open(config["gmail"]["secret"]) as fp:
        secret = yaml.load(fp)

    typ, resp = gmail.login(secret['uname'], secret['passw'])

    if resp[0].find(b'authenticated') > 0:
        print("GMAIL: authenticated...")
    else:
        raise Exception('GMAIL: login failed...')

    return gmail

def iter_emails(gmail, db):
    typ, ids = gmail.select('otf')
    markers = config['database']['columns'].keys()
    dbc = db.cursor()

    for mid in ids[0].split():
        print("GMAIL: parsing message...")
        typ, data = gmail.fetch(mid, '(RFC822)')
        bytetxt = data[0][1]
        ts = get_timestamp(bytetxt)
        dbc.execute(config['sql']['exists'].format(ts))
        if dbc.fetchall()[0][0] == 1:
            print("SQL: skipping existing record stamped {}...".format(
                    time.ctime(ts)))
            continue

        soup = bs4.BeautifulSoup(bytetxt, "html.parser")
        tags = soup.findAll('td')

        D = {}
        for tag in tags:
            txt = tag.text
            for m in markers:
                if m in txt and m not in D.keys():
                    D[m] = int(txt.split(" ")[0].replace(",", ""))

        script = config['sql']['insert'].format(
                ts, D["CALORIES BURNED"],
                D["AVG HR"], D["% AVG"],
                D["SPLAT POINTS"], ts)

        print("SQL: storing record...")
        dbc.execute(script)
        db.commit()

def main():
    db = init_db()
    gmail = logn()
    iter_emails(gmail, db)
    db.close()

if __name__ == '__main__':
    main()
