import requests


API_URL = ("https://api.mailgun.net/v3/sandbox7a42c277707c4b7ca74a46ba28667b" +
           "fd.mailgun.org/messages")
API_KEY = "key-8adab74bb944ff2aeb02b29535cde446"


def send_email(from_address, to_address, subject, text):
    return requests.post(
        (API_URL),
        auth=("api", API_KEY),
        data={"from": from_address,
              "to": to_address,
              "subject": subject,
              "text": text})


if __name__ == "__main__":
    body = """Hi there,

    Here's the update report...
    """
    send_email("Andrew Wang <me@andrewwang.ca>",
               "Andrew Wang <andrewwang963@gmail.com>",
               "Test Email",
               "Hello World!")
