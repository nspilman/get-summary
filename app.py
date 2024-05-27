import os
import resend

resend.api_key = os.environ["RESEND_API_KEY"]

params: resend.Emails.SendParams = {
    "from": "Nate <pioneer@natespilman.com>",
    "to": ["nate.spilman@gmail.com"],
    "subject": "Pioneer",
    "html": "<strong>WE OUT HERE</strong>",
}

email = resend.Emails.send(params)
print(email)
