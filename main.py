from flask import Flask, render_template
import requests
import datetime
import locale
import threading


locale.setlocale(locale.LC_ALL, 'pt-PT')


app = Flask(__name__)


@app.route('/')
def index():

    def reloadapi():
        threading.Timer(5.0, reloadapi).start()
        i = requests.get(" https://economia.awesomeapi.com.br/last/EUR-USD,EUR-BRL,EUR-GBP,EUR-ARS,EUR-JPY,EUR-CHF")
        info = i.json()

        # Euro/Dólar Americano
        eur_usd = info['EURUSD']['bid']
        eur_usd_hora = info['EURUSD']['create_date']
        # Transformar em datetime
        eur_usd_hora = datetime.datetime(int(eur_usd_hora[0:4]), int(eur_usd_hora[5:7]), int(eur_usd_hora[8:10]),
                                         int(eur_usd_hora[11:13]), int(eur_usd_hora[14:16]), int(eur_usd_hora[17:19]))

        # Euro/Real Brasileiro
        eur_blr = info['EURBRL']['bid']
        eur_blr_hora = info['EURBRL']['create_date']
        # Transformar em datetime
        eur_blr_hora = datetime.datetime(int(eur_blr_hora[0:4]), int(eur_blr_hora[5:7]), int(eur_blr_hora[8:10]),
                                         int(eur_blr_hora[11:13]), int(eur_blr_hora[14:16]), int(eur_blr_hora[17:19]))

        # Euro/Libra Esterlina
        eur_gbp = info['EURGBP']['bid']
        eur_gbp_hora = info['EURGBP']['create_date']
        # Transformar em datetime
        eur_gbp_hora = datetime.datetime(int(eur_gbp_hora[0:4]), int(eur_gbp_hora[5:7]), int(eur_gbp_hora[8:10]),
                                         int(eur_gbp_hora[11:13]), int(eur_gbp_hora[14:16]), int(eur_gbp_hora[17:19]))

        # Euro/Peso Argentino
        eur_ars = info['EURARS']['bid']
        eur_ars_hora = info['EURARS']['create_date']
        # Transformar em datetime
        eur_ars_hora = datetime.datetime(int(eur_ars_hora[0:4]), int(eur_ars_hora[5:7]), int(eur_ars_hora[8:10]),
                                         int(eur_ars_hora[11:13]), int(eur_ars_hora[14:16]), int(eur_ars_hora[17:19]))

        # Euro/Iene Japonês
        eur_jpy = info['EURJPY']['bid']
        eur_jpy_hora = info['EURJPY']['create_date']
        # Transformar em datetime
        eur_jpy_hora = datetime.datetime(int(eur_jpy_hora[0:4]), int(eur_jpy_hora[5:7]), int(eur_jpy_hora[8:10]),
                                         int(eur_jpy_hora[11:13]), int(eur_jpy_hora[14:16]), int(eur_jpy_hora[17:19]))

        # Euro/Franco Suíço
        eur_chf = info['EURCHF']['bid']
        eur_chf_hora = info['EURCHF']['create_date']
        # Transformar em datetime
        eur_chf_hora = datetime.datetime(int(eur_chf_hora[0:4]), int(eur_chf_hora[5:7]), int(eur_chf_hora[8:10]),
                                         int(eur_chf_hora[11:13]), int(eur_chf_hora[14:16]), int(eur_chf_hora[17:19]))
        return eur_blr, eur_usd, eur_usd_hora, eur_blr_hora, eur_chf_hora, eur_jpy_hora, \
               eur_ars_hora, eur_gbp_hora, eur_chf, eur_gbp, eur_jpy, eur_ars

    eur_blr, eur_usd, eur_usd_hora, eur_blr_hora, eur_chf_hora, eur_jpy_hora, eur_ars_hora, eur_gbp_hora, eur_chf, eur_gbp, eur_jpy, eur_ars = reloadapi()

    return render_template("index.html", eur_blr=eur_blr, eur_usd=eur_usd, eur_usd_hora=eur_usd_hora,
                           eur_blr_hora=eur_blr_hora, eur_chf_hora=eur_chf_hora, eur_jpy_hora=eur_jpy_hora,
                           eur_ars_hora=eur_ars_hora, eur_gbp_hora=eur_gbp_hora, eur_chf=eur_chf, eur_gbp=eur_gbp,
                           eur_jpy=eur_jpy, eur_ars=eur_ars)


if __name__ == '__main__':
    app.run(debug=True)

