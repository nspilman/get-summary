import datetime
import os
import resend

from src.llm import summarize_pages_from_today
from src.run_pipeline import run_pipeline

def run_application():
    run_pipeline()
    summary = summarize_pages_from_today()

    resend.api_key = os.environ["RESEND_API_KEY"]

    params: resend.Emails.SendParams = {
        "from": "your CRE Daily <your-cre-daily@natespilman.com>",
        "to": ["nate.spilman@gmail.com", "topherstep@gmail.com"],
        "subject": f"{datetime.datetime.now().strftime('%Y-%m-%d')} Maine Business Update",
        "html": summary,
    }

    email = resend.Emails.send(params)
    print(email)

    if __name__ == "__main__":
        run_application()