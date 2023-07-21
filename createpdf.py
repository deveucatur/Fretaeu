from reportlab.pdfgen import canvas
from datetime import date
import mysql.connector
from io import BytesIO


conexao = mysql.connector.connect(
    passwd='bdfretaeu123',
    port=3306,
    user='admin',
    host='bd-fretau.c7rugjkck183.sa-east-1.rds.amazonaws.com',
    database='BDFRETAEU'
)

mycursor = conexao.cursor()


###### PEGANDO INFORMAÇÕES DOS CARROS
cm_sql = 'SELECT * FROM FrotaCarros;'
mycursor.execute(cm_sql)
bd_carros = mycursor.fetchall()
mycursor.close()


def limpaValorDIC(orcament):
    text = ''
    for a in orcament:
        text+=str(f'/// {a} : {orcament[a]} /// ').replace('{','').replace('}','').replace("'", "")
    
    return text


def limpaValorLIST(orcament):
    text = ''
    for a in orcament:
        text+=str(f'{a}, ').replace('{','').replace('}','').replace("'", "")

    
    return text[:len(text) - 2]


def quebrarLinhas(texto, range_digits):
    textoSplit = texto.strip().split(' ')

    list_linhas = []
    soma_palavras =''
    for a in textoSplit:
        
        soma_palavras += f' {a}'

        if len(soma_palavras) > range_digits:
            list_linhas.append(soma_palavras)
            soma_palavras = ''
    
    if soma_palavras not in list_linhas:
        list_linhas.append(soma_palavras)
    return list_linhas


def add_background(canvas, background_path):
    canvas.drawImage(background_path, 0, 0, width=canvas._pagesize[0], height=canvas._pagesize[1], preserveAspectRatio=True)


def CreatePDF(ddOrcament, ddCliente):
    ########## TRATAR DADOS DOS ORÇAMENTOS ##########
    #FORMA DOS DADOS --> 1-QUANTIDADE DE VEÍCULOS, CARACTERÍSTICAS, VALOR POR VEÍCULO, VALOR TOTAL

    #CRIANDO BUFFER TEMPORÁRIO NA MEMÓRIA PARA ARMAZENAR O PDF
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=(595.276, 841.890))  

    background_image_path = "modeloRelatorioWord.jpg"

    add_background(pdf, background_image_path)

    pdf.setFont("Helvetica-Bold", 12)
    pdf.setFillColorRGB(1, 1, 1)
    pdf.drawString(475, 411, f'{date.today().strftime("%d/%m/%Y")}')


    pdf.setFont("Helvetica", 8)
    pdf.setFillColorRGB(0, 0, 0)
    ########### DADOS DO CONTRATADO ###########
    #ADD NOME EMPRESA
    altura = 647
    pdf.drawString(20, altura, 'EUMAIS MULTISERVIÇOS LTDA')
    #ADD CNPJ EMPRES
    pdf.drawString(158, altura, '34.026.458/0001-31')
    #ADD ENDEÇO EMPRES
    pdf.drawString(270, altura, 'Av Adelino Cardana, 293, sala 610, Centro, Barueri-SP, CEP:06404-301')


    ########### REPRESENTANTE COMERCIAL ###########
    #ADD NOME REPRESENTANTE
    altura = 589
    pdf.drawString(10, altura, 'RODRIGO VASCONCELOS DO CARMO')
    #ADD CIDADE REPRESENTANTE
    pdf.drawString(170, altura, 'JI-PARANÁ')
    #ADD TELFONE REPRESENTANTE
    pdf.drawString(285, altura, '69 4002-8922')
    #ADD EMAIL REPRESENTANTE
    pdf.drawString(375, altura, 'teste@emailrepresentate.com')


    ########### DADOS CONTRATANTE ###########
    #ADD NOME CLIENTE
    altura = 531
    pdf.drawString(10, altura, ddCliente['Cliente'])
    #ADD CPF CLIENTE
    pdf.drawString(173, altura, ddCliente['cpf/cnpj'])
    #ADD TELFONE CLIENTE
    pdf.drawString(285, altura, ddCliente['TelefCliet'])
    #ADD EMAIL CLIENTE
    pdf.drawString(375, altura, ddCliente['EmailCliet'])

    ############ ROTA DE VIAGEM ############
    texto_relat = f'''{ddCliente['CidadeOri']} x {ddCliente['CidadeDest']} // Data de ida: {ddCliente['DtIda']} // Data de retorno: {ddCliente['DtVolta']} // Quantidade de passageiros: {ddCliente['passageiros']}'''
    
    TextQuebr = quebrarLinhas(texto_relat, 140)

    altura = 492
    for linha in TextQuebr:
        pdf.drawString(20, altura, str(linha).strip())
        altura -= 20


    ########### DADOS COTAÇÃO ###########

    list_pdf = []

    for a in ddOrcament:
        list_pdf.append([limpaValorLIST(a[0]), limpaValorDIC(a[1]), a[2], str(a[3])])
    
    
    altura = 360
    for contac in list_pdf:
        #ADD QUANTIDADE/VEICULO
        pdf.setFont("Helvetica-Bold", 9)

        TextQuebr = quebrarLinhas(contac[0], 10)   
        
        altura_quebra = altura
        for linha in TextQuebr:
            pdf.drawString(20, altura_quebra, str(linha).strip())
            altura_quebra -= 10

        
        #ADD CARACTERÍSTICAS
        pdf.setFont("Helvetica", 8)
        TextQuebr = quebrarLinhas(contac[1], 47)
        altura_quebra = altura
        for linha in TextQuebr:
            pdf.drawString(140, altura_quebra, str(linha).strip())
            altura_quebra -= 10
        
        
        #ADD VALOR POR VEÍCULO
        pdf.setFont("Helvetica", 8)
        altura_quebra = altura
        for dic_dd in contac[2]:
            dic_aux = str({dic_dd: f'{contac[2][dic_dd]}'}).replace('{','').replace('}','').replace('"','').replace("'","")
            
            TextQuebr = quebrarLinhas(str(dic_aux), 34)
            
            for linha in TextQuebr:
                pdf.drawString(335, altura_quebra, str(linha).strip())
                altura_quebra -= 8
            altura_quebra -= 7

        #ADD VALOR TOTAL
        pdf.setFont("Helvetica-Bold", 12) 
        pdf.drawString(510, altura - 10, f'R$ {contac[3]}')

        altura -= 80
        

    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    return buffer.getvalue()

