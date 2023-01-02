import logging
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from metspa.utils import read_environment_variable

email_api_key = "METEO_EMAIL_KEY"

# port = 587  # For SSL
# smtp_server = "smtp.gmail.com"
# sender_email = "meteo.spain.ng@gmail.com"  # Enter your address
# receiver_email = input("Enter receiver address: ")
# password = read_environment_variable("METEO_EMAIL_KEY")
# message = """\
# Subject: Hi there

# This message is sent from Python."""

# context = ssl.create_default_context()
# with smtplib.SMTP(smtp_server, port) as server:
#     server.starttls(context=context)
#     server.login(sender_email, password)
#     server.sendmail(sender_email, receiver_email, message)


class EmailSender:
    port = 587  # SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "meteo.spain.ng@gmail.com"
    password = read_environment_variable(email_api_key)

    logger = logging.getLogger("EmailSender")

    def __call__(self, receiver_email, message):
        context = ssl.create_default_context()
        self.logger.info("Initialising email client")
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls(context=context)
            server.login(self.sender_email, self.password)

            if type(receiver_email) is list:
                for curr_email in receiver_email:
                    self._sendmail(server, curr_email, message)
            else:
                self._sendmail(server, receiver_email, message)

    def _sendmail(self, server, receiver_email, message):
        self.logger.info(f"Sending email to {receiver_email}")
        server.sendmail(self.sender_email, receiver_email, message)

    def generate_html_message(self, receiver_email, df, **kwargs):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Meteorological Report"
        message["From"] = self.sender_email
        message["BCC"] = receiver_email

        station_name = kwargs.get("station_name")
        province = kwargs.get("province")

        text = f"""
            Hi Norberto,

            The monthly meteorological summary at {station_name} in {province} is
            provided below.

            Data from {kwargs.get('start_date')} to {kwargs.get('end_date')}.
            """

        text_for_html = text.replace("\n", "<br>")
        html = f"""\
            <html>
            <body>
                <p>{text_for_html}<br>
                </p>
            </body>
            {df.to_html()}
            </html>
            """
        # html = df.to_html()

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        import pdb

        pdb.set_trace()

        self(receiver_email, message.as_string())
