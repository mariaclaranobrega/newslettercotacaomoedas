from email.mime.image import MIMEImage
from leituras import reloadapi
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time


def enviar():

    eur_blr, eur_usd, eur_usd_hora, eur_blr_hora, eur_chf_hora, eur_jpy_hora, eur_ars_hora, eur_gbp_hora, eur_chf, \
    eur_gbp, eur_jpy, eur_ars = reloadapi()

    estilo = """
        .um {{max-width:37.5rem; display: flex; flex-direction:column; justify-content:center; align-items: center;padding:1rem;margin: auto;border:0.125rem solid grey;border-radius:0.625rem;box-shadow: 0.313rem 0.313rem #DCDCDC}}
        .dois {{max-width:10rem;margin-bottom:1rem;}}
        .tres{{display: flex; flex-direction:column; justify-content:center; align-items: center;}}
        .quatro{{font-size: 1.5rem;font-family: 'Oswald', sans-serif;padding:0;margin-bottom:0;margin-top:0}}
        .cinco{{font-size: 1.2rem;font-family: 'Oswald', sans-serif;padding:0;margin-top:0}}
        .seis{{font-family: 'Inter', sans-serif;text-align: center;font-size:1rem;}}
        .sete{{font-family: 'Inter', sans-serif;text-align: center;font-size:0.8rem}}
        .oito{{font-family: 'Inter', sans-serif;text-align: center;font-size: 0.5rem;color:grey}}
        """

    message_html = f'''
    <!doctype html>
<html lang="pt-PT">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link href="https://fonts.googleapis.com/css2?family=Beau+Rivage&family=Oswald&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+SC:wght@700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300&display=swap" rel="stylesheet">
    <style type="text/css"> {estilo} </style>
    <title>Cotação de Moedas</title>
</head>
<body>


<div class="um">

    <img class="dois" src="cid:image1"" alt="Moedas">

    <div class="tres">
        <p class="quatro">COTAÇÃO DE MOEDAS - EURO</p>
        <p class="cinco">{eur_usd_hora}</p>
    </div>

    <div>
        <b><p class="seis">Dólar Americano - USD</p></b>
        <p class="sete">{eur_usd}</p>
    </div>
    <div>
        <b><p class="seis">Real Brasileiro - BLR</p></b>
        <p class="sete">{eur_blr}</p>
    </div>
    <div>
        <b><p class="seis"">Libra Esterlina - GBP</p></b>
        <p class="sete">{eur_gbp}</p>
    </div>
    <div>
        <b><p class="seis">Peso Argentino - ARS</p></b>
        <p class="sete">{eur_ars}</p>
    </div>
    <div>
        <b><p class="seis">Iene Japonês - JPY</p></b>
        <p class="sete">{eur_jpy}</p>
    </div>
    <div>
        <b><p class="seis">Franco Suíço - CHF</p></b>
        <p class="sete">{eur_chf}</p>
    </div>


    <p class="oito">Todos os dados foram 
    reunidos pelo AwesomeAPI e podem ser encontrados em https://docs.awesomeapi.com.br/api-de-moedas.</p>

</div>

</body>
</html>
    '''

    host = 'smtp.gmail.com'
    port = 587
    user = 'EMAIL_REMETENTE@gmail.com'
    password = 'SUA_SENHA_DE_APP'
    server = smtplib.SMTP(host, port)

    server.ehlo()
    server.starttls()
    server.login(user, password)

    email_msg = MIMEMultipart()
    email_msg['From'] = user
    # Lista de destinatários
    destinatarios = ['email1@gmail.com', 'email2@gmail.com', 'email3@gmail.com']
    # Transformar a lista de destinatários em uma str divididindo os emails por vírgulas.
    email_msg['To'] = str(destinatarios).replace('[','').replace(']','').replace("'",'').replace(" ",'')
    email_msg['Subject'] = 'Cotação de Moedas'

    # Logo
    logo = open('static/images/logo_pequena.png', 'rb')
    logoImage = MIMEImage(logo.read())
    logo.close()
    logoImage.add_header('Content-ID', '<image1>')
    email_msg.attach(logoImage)

    email_msg.attach(MIMEText(message_html, 'html'))

    # Receberá email_msg['To'] um por um
    multidest = MIMEMultipart()
    loop = 1
    while loop <= len(destinatarios):
        # Abrir e fechar o terminal a cada envio, para driblar o problema com o servidor do SMTP
        server.quit()

        server = smtplib.SMTP(host, port)
        server.ehlo()
        server.starttls()
        server.login(user, password)
        # Iniciar sempre com essa variável limpa
        multidest.__delitem__('To')
        # Se a lista do email_msg['To'] tiver mais de 1 elemento:
        if (email_msg['To'].find(',')) != -1:
            # Salvar na variável transitória o email (até a vírgula)
            multidest['To'] = email_msg['To'][0:(email_msg['To'].find(',')) + 1]
        # Se não houver vírgula, significa que só há 1 elemento:
        else:
            # Salvar o elemento inteiro
            multidest['To'] = email_msg['To'][0:]
        # Enviar para este elemento
        server.sendmail(email_msg['From'], f"<{multidest['To']}>", email_msg.as_string())
        print("Email enviado para ", multidest['To'])
        # Apagar este email da listagem do email_msg['To']
        att = str(email_msg['To'].split(',')[1:]).replace('[', '').replace(']', '').replace("'", '').replace(" ", '')
        # Limpar variável
        email_msg.__delitem__('To')
        # Adicionar os emails restantes na lista
        email_msg['To'] = att
        print("Seguintes: ", email_msg['To'], "\n")

        loop += 1
        time.sleep(2)

    server.quit()


if __name__ == '__main__':
    schedule.every(15).seconds.do(enviar)
    while True:
        schedule.run_pending()
        time.sleep(1)


