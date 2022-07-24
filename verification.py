import imaplib, email


def get_verification_code(login, password, imap_server):
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(login, password)
    imap.select("Spam")

    result, data = imap.search(None, "ALL")
    ids = data[0] # Получаем сроку номеров писем
    id_list = ids.split() # Разделяем ID писем

    latest_email_id = id_list[-1] # Берем последний ID
    result, msg = imap.fetch(latest_email_id, "(RFC822)") # Получаем тело письма (RFC822) для данного ID
    
    raw_email = msg[0][1] # Тело письма в необработанном виде

    email_message = email.message_from_bytes(raw_email)
    # print(email_message)
    # print (email_message.items())

    def get_first_text_block(email_message_instance):
        maintype = email_message_instance.get_content_maintype()
        if maintype == 'multipart':
            for part in email_message_instance.get_payload():
                if part.get_content_maintype() == 'text':
                    return part.get_payload()
        elif maintype == 'text':
            return email_message_instance.get_payload()

    x = get_first_text_block(email_message)
    lines = x.splitlines()
    code = lines[20][74:78]
    # print(code)

    return code




             