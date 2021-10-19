from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import os
# Create your views here.
from user.models import User


@login_required(login_url='/login')
def activar(request):
    """
        Vista desplegada a usuarios no activados  03/09/21
    """
    msg(request.user.email)
    return render(request, 'user/activar.html')


# import necessary packages
from email.message import EmailMessage
# https://www.google.com/settings/security/lesssecureapps aceptar
# https://www.google.com/accounts/DisplayUnlockCaptcha


# import necessary packages

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
listadeemail=[]


def msg(email1):
    """
            Metodo para el avisar a los administradores sobre intento de acceso al sistema  11/10/21
    """
    # create message object instance
    if email1 not in listadeemail:
        usuario = User.objects.filter(rolSistema="Administrador")
        if len(usuario) > 1 :
            listadeemail.append(email1)
            for u in usuario:
                msg = MIMEMultipart()
                usuarios="http://127.0.0.1:8080/home/usuarios"
                message = "El usuario con email " + email1 + " ha intentado ingresar al sistema" +", puede activarlo en el sector "+ usuarios

                # setup the parameters of the message
                # password = os.environ["password_sgp"]
                password = 'sgp12345'
                msg['From'] = "sistemagestordeproyectos@gmail.com"
                msg['To'] = u.email
                msg['Subject'] = "Usuario no autorizado"
                fromaddr = "chapiparrizo@gmail.com"
                # add in the message body
                msg.attach(MIMEText(message, 'plain'))

                smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
                smtpserver.ehlo()
                smtpserver.starttls()
                smtpserver.ehlo()
                smtpserver.login(msg['From'], password)
                smtpserver.sendmail(msg['From'], msg['To'], msg.as_string())
                smtpserver.quit()

def msg2(email1,nombre,rol):
    # create message object instance
    """
                Metodo de confirmacion de acceso  11/10/21
    """
    msg = MIMEMultipart()
    usuarios="http://127.0.0.1:8080/home"
    message = "Su usuario "+nombre+ " Ha sido activado en el sistema gestor de proyectos con el rol de "+rol+". Ya puede ingresar al sistema  "+usuarios

    # setup the parameters of the message
    # password = os.environ["password_sgp"]
    password = 'sgp12345'
    msg['From'] = "sistemagestordeproyectos@gmail.com"
    msg['To'] = email1
    msg['Subject'] = "Usuario activado"

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
    smtpserver.login(msg['From'], password)
    smtpserver.sendmail(msg['From'], msg['To'], msg.as_string())
    smtpserver.quit()

def msg3(user_story,nombre,scrum_email):
    """
              Metodo para el avisar a los administradores sobre intento de acceso al sistema  18/10/21
      """
    # create message object instance
    listaemail=[]
    listaemail.append(scrum_email)
    completado=[]
    for u in user_story:
        listaemail.append(u.miembro_asignado.email)

    for u in listaemail:
        if u not in completado:
            completado.append(u)
            msg = MIMEMultipart()
            if u==scrum_email:
                message = "El sprint del proyecto " + nombre + " ha sido iniciado"
            else:
                message = "El sprint al cual fue asignado del proyecto "+nombre+" ha sido iniciado"

            # setup the parameters of the message
            # password = os.environ["password_sgp"]
            password = 'sgp12345'
            msg['From'] = "sistemagestordeproyectos@gmail.com"
            msg['To'] = u
            msg['Subject'] = "Inicio de sprint"
            # add in the message body
            msg.attach(MIMEText(message, 'plain'))

            smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo()
            smtpserver.login(msg['From'], password)
            smtpserver.sendmail(msg['From'], msg['To'], msg.as_string())
            smtpserver.quit()

def error_404(request,exception):
    return render(request, 'error/404.html')

def error_403(request,exception):
    return render(request, 'error/403.html')