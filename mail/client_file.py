from imapclient import IMAPClient
import email
from email.header import decode_header

# Configuration du serveur
HOST = "imap.mail.ovh.net"
USERNAME = "paul@delhomme.ovh"
PASSWORD = "Pavel180400&Ovh@Delhomme"

def fetch_emails():
    with IMAPClient(HOST, use_uid=True, ssl=True) as server:
        server.login(USERNAME, PASSWORD)
        server.select_folder('INBOX')
        messages = server.search(['NOT', 'DELETED'])
        response = server.fetch(messages, ['ENVELOPE', 'BODY[]'])

        for msgid, data in response.items():
            envelope = data[b'ENVELOPE']
            message = email.message_from_bytes(data[b'BODY[]'])

            subject, encoding = decode_header(envelope.subject.decode())[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or 'utf-8')

            from_email = envelope.from_[0].mailbox.decode() + '@' + envelope.from_[0].host.decode()
            print(f"Sujet : {subject}")
            print(f"Expéditeur : {from_email}")

            # Vérifier s'il y a un corps de message et l'afficher
            if message.is_multipart():
                for part in message.walk():
                    if part.get_content_type() == "text/plain":
                        print(part.get_payload(decode=True).decode('utf-8'))
                    else:
                        print(part.get_payload(decode=True).decode('utf-8'))

fetch_emails()