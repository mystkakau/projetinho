from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resultado', methods=['POST'])
def resultado():
    sem10 = float(request.form['sem10'])
    pix = float(request.form['pix'])
    debito = float(request.form['debito'])
    credito = float(request.form['credito'])
    dinheiro = float(request.form['dinheiro'])

    comissao = sem10 * 0.08
    com10 = sem10 * 1.10
    boletas = pix + debito + credito + dinheiro
    casa = sem10 * 1.02
    fechamento = casa - boletas
    sobra = boletas - com10

    situacao = ""
    alerta = ""

    if boletas > casa:
        situacao = f"""
        Suas boletas (dinheiro e cartões) - o que deve a casa → R${boletas:.2f} - R${casa:.2f} = R${boletas - casa:.2f}
        Ou seja, você deve dar em dinheiro R${boletas - casa:.2f} para a casa. Sua comissão (R${comissao:.2f}) já está com você!
        """
        if com10 - boletas != 0:
            alerta = f"Tem R${sobra:.2f} sobrando no seu caixa, ou seja, que provavelmente não veio de uma compra no estabelecimento."
    elif casa > boletas:
        situacao = f"""
        O que você deve a casa - o valor das boletas → R${casa:.2f} - R${boletas:.2f} = R${casa - boletas:.2f}
        Ou seja, a casa deve te voltar parte da comissão. Sua comissão é R${comissao:.2f}, e a casa deve te voltar R${abs(fechamento):.2f}.
        """
        if com10 != 0:
            alerta = f"Tem R${sobra:.2f} sobrando no seu caixa, ou seja, que provavelmente não veio de uma compra no estabelecimento."

    return render_template("resultado.html", comissao=comissao, casa=casa, boletas=boletas,
                           pix=pix, debito=debito, credito=credito, dinheiro=dinheiro,
                           situacao=situacao, alerta=alerta)

if __name__ == '__main__':
    app.run(debug=True)
