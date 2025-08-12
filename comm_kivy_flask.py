#parte da comm entre o app e o servidor
#(app pega os dados do opencv e o PyAudio e manda aos sevidores do flask(localmente))
#gera a urç e compartilho a tela para poder fazer a camera virtual
from flask import Flask,render_template
#from pyaudio import *
app = Flask(__name__)
#por enquanto somente a rota principal
@app.route("/")#home page
def cam_virt_mobile():
	return render_template()#retornar o audio e o video do app
app.run(host="0.0.0.0",port=5000)
