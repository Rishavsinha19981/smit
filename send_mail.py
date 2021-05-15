import smtplib
from email.mime.text import MIMEText


def send_mail(EmailID,Employee, Location,EmployeeID,Designation,Department, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '52b37a9830b1b1'
    password = 'ec41c0d7b382b1'
    message = f"<h3>New Feedback Submission mail .</h3><ul><li><li>EmailId:{EmailID}<li><li>Employee: {Employee}</li><li>Location: {Location}</li><li>EmployeeID: {EmployeeID}</li><li>Designation:{Designation}</li><li>Department:{Department}</li><li>Rating:{rating}</li><li>Comments: {comments}</li></ul>"

    sender_email = 'rishav@example.com'
    receiver_email = 'email2@example.com,06524455ae6707'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Employee Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
