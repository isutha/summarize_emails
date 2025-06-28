#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 09.05.2025 extract email content, Emailverkehr between X and Y

import os
import email
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer


email_path = "" # change path!

# save the email names into a list
email_names = os.listdir(email_path)

desired_sender = ""   # enter sender
recipient1 = ""       # enter recipient 1
recipient2 = ""       # enter recipient 2

dictionary_email= {}

def summarize_text(text, num_sentences = 23):
    parser = PlaintextParser.from_string(text, Tokenizer("german"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return " ".join(str(sentence) for sentence in summary)


def reademailfile():
    # read in the files and show the names of the mails
    for mail in email_names:
        # only consider .eml files
        if mail.endswith(".eml"):
            mail_path = os.path.join(email_path, mail)
            # open content of the mail
            with open(mail_path, "r", encoding='utf-8') as file:
                msg = email.message_from_file(file)

            sender = msg['from']
            rec = msg['to']
            filename = mail
            date = msg['date']

            # check if sender is available
            if sender and desired_sender in sender or recipient1 and recipient2 in rec:
            # Extract email content
                email_content = ""

                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            charset = part.get_content_charset() or 'utf-8'
                            email_content = part.get_payload(decode=True).decode(charset, errors="replace")
                            break
                    else:
                        charset = msg.get_content_charset() or 'utf-8'
                        email_content = msg.get_payload(decode=True).decode(charset, errors="replace")

                # avoid text after Lieber Gruss
                cutoff_phrase = "Lieber Gruss"
                if cutoff_phrase in email_content:
                    email_content = email_content.split(cutoff_phrase)[0].strip()

                # create summary of email
                summary = summarize_text(email_content)

                # save the content into a dictionary
                dictionary_email[filename, date[0:16], sender] = {summary}

    # call function after processing all emails
    createoutput()

def createoutput():
    # print no. of emails to terminal
    print(f'Anzahl Emails: {len(dictionary_email)}\n')

    output_lines = []

    for key, value in dictionary_email.items():
        header = f"\nName der gespeicherten Email und Originaldatum: {key[0]}, {key[1]}\nGesendet von: {key[2]}\n"
        summary = f"{value}\n"
        separator = 72 * "__" + "\n"
        output_lines.extend([header, summary, separator])

        # Print to console
        print(header)
        print(summary)
        print(separator)

    # write all output to a .txt file
    with open("zusammenfassung_emails.txt", "w", encoding="utf-8") as out_file:
        out_file.writelines(output_lines)

# run main function
reademailfile()