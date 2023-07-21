import streamlit as st
from PIL import Image
import json
from createpdf import CreatePDF
import mysql.connector
from datetime import date
#Variáveis da precificação fretamento
#- Tipo de veículo
#- Mês do ano
#- KM Ida e Volta (cheia c/ passageiros)
#- KM deslocamento (carro vazio cobrir o custo do combustível)
#- Diária (com carro parado)
#- Diária (com carro disponível p/ descolamento)
#- Qtd de veículos
#- % de desconto


icone = Image.open('icone.png')
st.set_page_config(
    page_title="Preço|FretaEU Precificação",
    page_icon=icone,
    layout="centered")

st.image(Image.open("icone.png"), width=180)

conexao = mysql.connector.connect(
    passwd='bdfretaeu123',
    port=3306,
    user='admin',
    host='bd-fretau.c7rugjkck183.sa-east-1.rds.amazonaws.com',
    database='BDFRETAEU'
)

mycursor = conexao.cursor()

cm_sql = 'SELECT * FROM FrotaCarros;'
mycursor.execute(cm_sql)
bd_carros = mycursor.fetchall()
mycursor.close()

with open('CidadeBrasil.json','r') as jsons:
    JSONCidads = json.load(jsons)
    listCidads = JSONCidads['Cidades']


def calCusto(Frota):
    custo = 0
    for i in Frota:
        c = (kmCheio * CustoVeiTrans[TipVei.index(i)]) + ((kmDeslocamento + kmExtra) * CustoVeiDesl[TipVei.index(i)]) + (diaria * CustoDia[TipVei.index(i)])
        custo += c
        #print(i,c )
    return custo


from datetime import datetime
def checkAltaTempor(dataString):
    alta_temporad = [1, 7, 12]
    data = datetime.strptime(str(dataString), "%Y-%m-%d").date()

    mes_atual = data.month

    if mes_atual in  alta_temporad:
        return True
    else:
        return False


TipVei = ["Leito Semi-Leito", "Semi-Leito", "Convencional G7", "Micro Ônibus", "Van"]

alta_temporad = [1, 7, 12]

data_atual = date.today()
mes_atual = data_atual.month


st.divider()
st.subheader("Dados do Cliente")
NomeCliente = st.text_input("Nome")
EmailClient = st.text_input("Email")

col1, col2 = st.columns(2)
with col1:
    telefClient = st.text_input("Telefone")
with col2:
    identiClient = st.text_input("CPF/CNPJ")


st.text('')
st.subheader("Dados do Fretamento")
col1, col2 = st.columns(2)

with col1:
    CidadeOri = st.selectbox("Origem", listCidads)
    DtIda = st.date_input("Data de Ida") # Identificar se são meses normais ou temporada e feriado
    if checkAltaTempor(str(DtIda)):
        CustoVeiTrans = [11.5, 11.5, 8.5, 7.5, 5]#CUSTO POR KM DO TRAJETO
        CustoVeiDesl = [5, 5, 4.5, 4, 3]#CUSTO POR DESLOCAMENTO/KM EXTRA
        CustoDia = [1800, 1800, 1300, 800, 300]
        CapVei = [57, 57, 44, 25, 15]
    else:
        CustoVeiTrans = [10, 10, 8, 7, 3.5]#CUSTO POR KM DO TRAJETO
        CustoVeiDesl = [4.5, 4.5, 4, 3.5, 2]#CUSTO POR DESLOCAMENTO/KM EXTRA
        CustoDia = [1200, 1200, 800, 300, 200]
        CapVei = [57, 57, 44, 25, 15]


with col2:
    CidadeDest = st.selectbox("Destino", listCidads)
    DtVolta = st.date_input("Data de Volta")
passageiros = st.number_input('Nº de passageiros', min_value= 0, step= 1)
 
#col1, col2, col3, col4 = st.columns([1,0.5,1,0.5])
st.write("---")

col1, col2 = st.columns(2)
with col1:
    st.text(' ')
    st.subheader("Propostas")

with col2:
    cenarios = st.number_input("Nº Propostas",value=1, min_value= 0,  step= 1)

UserDados ={
            "Cliente": NomeCliente,
            "EmailCliet": EmailClient,
            "TelefCliet":telefClient,
            "cpf/cnpj":identiClient,
            "CidadeOri": CidadeOri,
            "DtIda": str(DtIda)    ,
            "CidadeDest": CidadeDest,
            "DtVolta": str(DtVolta),
            "passageiros": passageiros}

listOrcaments = []
for cen in range(cenarios):
    with st.expander(f'Proposta {cen + 1}'):
        col1, col2, col3 = st.columns(3)
        with col1:
            val_idaevolta = st.radio("Trajeto do Fretamento", ["Somente ida","Ida e volta"], key = f" val_idaevolta {cen}")
        
        with col2:
            st.text(' ')
            val_disposDes = st.checkbox("Veículo a disposição no local de destino?", key = f" val_disposDes {cen}")
            
        diaria = 0
        with col3:
            if val_disposDes:
                diaria = st.number_input("Nº Diárias", step= 1, min_value= 0, key = f" diaria {cen}")

        st.write('---')
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            v1 = st.number_input("Nº Leito Semi-Leito", step= 1, min_value= 0, key = f" v1 {cen}")
            Veic_1 = "Leito Semi-Leito"

        with col2:
            v2 = st.number_input("Nº Semi-Leito", step= 1, min_value= 0, key = f" v2 {cen}")
            Veic_2 = "Semi-Leito"

        with col3:
            v3 = st.number_input("Nº Convencional G7", step= 1, min_value= 0, key = f" v3 {cen}")
            Veic_3 = "Convencional G7"

        with col4:
            v4 = st.number_input("Nº Micro Ônibus", step= 1, min_value= 0, key = f" v4 {cen}")
            Veic_4 = "Micro Ônibus"

        with col5:
            v5 = st.number_input("Nº Van", step= 1, min_value= 0, key = f" v5 {cen}")
            Veic_5 = "Van"

        col1, col2, col3 = st.columns(3)
        with col1:
            kmCheio = st.number_input("KM Cheio", step= 1, min_value= 0, key = f" kmCheio {cen}")
            kmCheio = kmCheio * 2 if val_idaevolta == 'Ida e volta' else kmCheio

        with col2:
            kmExtra = st.number_input("KM Extra", step= 1, min_value= 0, key = f" kmExtra {cen}")
        
        with col3:
            kmDeslocamento = st.number_input("KM Deslocamento", step= 1, min_value= 0, key = f" kmDeslocamento {cen}")

        Frota = v1 * [Veic_1] +  v2 * [Veic_2] + v3 * [Veic_3] + v4 * [Veic_4] + v5 * [Veic_5]

        valorTotal = (calCusto(Frota), Frota)

        orcament = [
            [f'{Frota.count(y)} * {y}' for y in list(set([x for x in Frota]))],#QUANTIDADE DE VEÍCULOS
            {y: {w[4] for w in bd_carros if w[1] == y} for y in list(set([x for x in Frota]))},#COMENTÁRIOS
            {f'{y}':{'Valor KM':f'R$ {kmCheio * CustoVeiTrans[TipVei.index(y)]}',#VALOR POR CARRO
                     'valor Deslocamento': f'R$ {(kmDeslocamento + kmExtra) * CustoVeiDesl[TipVei.index(y)]}',
                     'Valor Diária': f'R$ {diaria * CustoDia[TipVei.index(y)]}'} for y in list(set([x for x in Frota]))},#CUSTO COM DIÁRIA POR CARRO            
            valorTotal[0]]
                    
        def limpaValor(orcament):
            text = '///'
            for a in orcament:
                text+=str(f'{a} = {orcament[2]} /// - ///').replace('{','').replace('}','').replace("'", "")
            
            return text
        
        listOrcaments.append(orcament)    
        st.divider()
        st.info(f"""
                    INFORMAÇÕES PROPOSTA {cen + 1}
                    ----------------------------------------------------------------
                    ----------------------------------------------------------------
                    

                    Cliente:  **{NomeCliente}**

                    Rota : **{CidadeOri} - {CidadeDest}**

                    Ida e Volta: **{'Sim' if val_idaevolta == 'Ida e volta' else 'Não'}**
                    
                    Data: **{DtIda.strftime("%d/%m/%Y")}{f" - {DtVolta.strftime('%d/%m/%Y')}" if val_idaevolta == "Ida e volta" else ""}**
                    
                    Passageiros: **{passageiros}**
                    
                    Veículo a Disposição: **{'Sim' if val_disposDes else 'Não'}**
                    
                    Diárias: **{diaria}**
                    
                    KM Cheio: **{kmCheio}**
                    
                    KM Deslocamento:  **{kmDeslocamento}**

                    KM Extra:  **{kmExtra}**

                    
                    ----------------------------------------------------------------
                    KM TOTAL: 
                    **{kmCheio + kmDeslocamento + kmExtra}** 

                    ----------------------------------------------------------------
                    VALOR TOTAL
                    **R${orcament[3]}**
                    ----------------------------------------------------------------
                    
                    ----------------------------------------------------------------
                    """)
       

st.download_button(label="Gerar Cotação", data=CreatePDF(listOrcaments, UserDados), file_name=f"cotacao{date.today()}.pdf", mime="application/pdf")
#st.download_button(label="Baixar PDF", data=pdf_data, file_name="exemplo.pdf", mime="application/pdf")

