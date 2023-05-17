from flask import Flask, request, Response
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return '''  <b>[GET]</b> <a href="/portador"> /portador </a> &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; Lista todos os portadores<br>
                <b>[GET]</b> <a href="/fatura"> /fatura </a> &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; Lista a fatura de todos os portadores <br>
                <b>[GET]</b> <a href="/fatura?idPortador="> /fatura?idPortador= </a> &emsp;&ensp;&nbsp; Lista as faturas do portador <br>
                <b>[POST]</b> <a href="/cobranca/{idFatura}="> /cobranca/{idFatura}</a> &ensp;&nbsp; Envia uma fatura para cobrança <br>
                <b>[POST]</b> <a href="/insuremo/calculate="> /insuremo/calculate</a> &emsp;&nbsp; Simula o calculate da InsureMO <br>
    '''

# Portador
@app.route("/portador")
def portador_list_all():
    return Response(open("portador.json"), mimetype="application/json")


@app.route("/portador/<idPortador>")
def portador_view(idPortador):
    with open("portador.json") as jsonfile:
        data = json.load(jsonfile)
        # filtra o Portador
        select = [x for x in data if str(x["id"]) == idPortador]
        if select:
            select = select[0]

        return select


# Fatura
@app.route("/fatura")
def fatura_list():
    with open("fatura.json") as jsonfile:
        data = json.load(jsonfile)
        # lista as Faturas por Portador
        if "idPortador" in request.args:
            select = [x for x in data if str(x["idPortador"]) == request.args["idPortador"]]
            return Response(json.dumps(select), mimetype="application/json")

        # lista todas
        else:
            return data


# Cobrança
@app.route("/cobranca/<idFatura>", methods=['POST'])
def cobranca_send(idFatura):
    data = dict()
    data["idFatura"] = int(idFatura)
    data["situacao"] = "ENVIADO_COBRANCA"
    return data


@app.route("/echo", methods=['POST'])
def echo():

    if request.data:
        print(json.dumps(request.json, indent=2))
        return request.json
    else:
        return Response("{}", mimetype="application/json")


@app.route("/insuremo/calculate", methods=['POST'])
def calculate():
    return Response(open("calculate_response.json"), mimetype="application/json")


@app.route("/insuremo/bind", methods=['POST'])
def bind():
    return Response(open("bind_response.json"), mimetype="application/json")


@app.route("/insuremo/issue", methods=['POST'])
def issue():
    return Response(open("issue_response.json"), mimetype="application/json")


#if __name__ == "__main__":
#    app.run()