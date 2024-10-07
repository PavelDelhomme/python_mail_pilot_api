from imapclient import IMAPClient
import email
from email.header import decode_header

# Configuration du serveur
HOST = "imap.mail.ovh.net"
USERNAME = "paul@delhomme.ovh"
PASSWORD = "Pavel180400&Ovh@Delhomme"

def fetch_emails(email, password):
    emails = []
    with IMAPClient(HOST, use_uid=True, ssl=True) as server:
        server.login(email, password)
        server.select_folder('INBOX')
        messages = server.search(['NOT', 'DELETED'])
        response = server.fetch(messages, ['ENVELOPE', 'BODY[]'])

        for msgid, data in response.items():
            envelope = data[b'ENVELOPE']
            subject, encoding = decode_header(envelope.subject.decode())[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or 'utf-8')

            from_email = envelope.from_[0].mailbox.decode() + '@' + envelope.from_[0].host.decode()
            emails.append({
                "subject": subject,
                "from": from_email,
                "date": str(envelope.date),
            })

    return emails
