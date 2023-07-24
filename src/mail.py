from os import path
from decouple import config
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.logging import Logging


logging = Logging()


def email_body(body):
    html = """
    <table style="width:100%; border: 1px solid black; border-collapse: collapse;">
    <tr>
        <th>Colaborador</th>
        <th>Cidade</th>
        <th>Estado</th>
        <th>Descrição</th>
        <th>Cargo</th>
        <th>Empresa</th>
        <th>Clima</th>
    </tr>
    """
    for line in body:
        html += """
                <tr>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                </tr>
                    """.format(line.name,
                               line.city,
                               line.state,
                               line.description,
                               line.office,
                               line.company,
                               line.climate)

    html += """
    </table>
    
    """

    return """
        <h1>Olá,</h1>
        <p>Segue abaixo a lista de colaboradores que foram encontrados no LinkedIn:</p>
        
        {}
        
        <p>Atenciosamente,</p>
        <p>Equipe de Automação</p>
    """.format(html)


def sendmail(to, subject, body, attach=None):
    # Configurations to send e-mail
    smtp_server = config('SMTP_SERVER')
    smtp_port = config('SMTP_PORT')
    smtp_username = config('SMTP_USERNAME')
    smtp_password = config('SMTP_PASSWORD')
    from_addr = config('SMTP_USERNAME')

    # Create the body of the message (a plain-text and an HTML version).
    body = email_body(body)

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to

    if attach:  # If has attachment
        with open(attach, 'rb') as file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{path.basename(attach)}"')
        msg.attach(part)

    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP(smtp_server, int(smtp_port))  # Create server
    try:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_addr, to, msg.as_string())
        logging.info(f"Sent e-mail to {to}")
    except Exception as e:
        logging.error(f"Error to send e-mail to {to}: {e}")
    finally:
        server.quit()
