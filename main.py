import smtplib
from email.mime.text import MIMEText

import click


def upload_recipients_list(path_to_recipients_list):
    emails = list()
    click.echo(click.style("uploading recipients file ", bold=True), nl=False)
    with open(path_to_recipients_list, "r") as file:
        for email in file:
            emails.append(email.rstrip())
    click.echo(click.style("[successful uploading]", fg="green", bold=True))
    return emails


def upload_message_text(path_to_message_text):
    message = ""
    click.echo(click.style("uploading message file ", bold=True), nl=False)
    with open(path_to_message_text, "r") as file:
        message = file.read()
    click.echo(click.style("[successful uploading]", fg="green", bold=True))
    return message


@click.command()
@click.option("--recipients", "-r", default="recipients.txt")
@click.option("--header", "-h", default="Header")
@click.option("--message-text", "-m", default="message.txt")
@click.option("--from-email", "-fe", prompt="Your email:")
@click.option("--from-password", "-fp", prompt="Password for your email:")
def main(from_email, from_password, header, message_text, recipients):
    try:
        emails = upload_recipients_list(recipients)
        msg = upload_message_text(message_text)

        click.echo(click.style("sending message ", bold=True), nl=False)
        smtp = smtplib.SMTP("smtp.gmail.com", 587)
        smtp.starttls()
        smtp.login(from_email, from_password)
        message = MIMEText(msg)
        message["Subject"] = header
        message["From"] = from_email
        message["To"] = ", ".join(emails)
        smtp.sendmail(from_email, emails, message.as_string())
        smtp.quit()
        click.echo(click.style("[successful sending]", fg="green", bold=True))
    except smtplib.SMTPAuthenticationError:
        click.echo(
            click.style(
                "[unsuccessful: Your email (--from-email, -fe) or password (--from-password, -fp) doesn't accepted]",
                fg="red",
                bold=True))
    except FileNotFoundError:
        click.echo(
            click.style(
                "[unsuccesful: Message or recipients file not found]",
                fg="red",
                bold=True))
    except Exception as ex:
        click.echo("Something went wrong....", ex)


if __name__ == "__main__":
    main()
