#-----------------------------------------------------------------------------
# Copyright 2011 Andrés Mantecon Ribeiro Martano
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#-----------------------------------------------------------------------------

texto =\
'''AEIOU-Unicel: 7900 a 7949 
Claro: 6168 a 6181, 6300 a 6339, 6570 a 6650, 6914 a 6931, 7052 a 7086, 7968 a 7970, 76xx, 88xx, 89xx, 91xx, 92xx, 93xx , 94xx 
Nextel: 77xx , 78xx 
Oi: 5400 a 5419, 5700 a 5768, 6011 a 6056, 6086 a 6167, 6500 a 6569, 6651 a 6699, 6800 a 6826, 6867 a 6899, 6932 a 6999, 7971 a 7999, 62xx, 67xx, 80xx 
Tim: 5200 a 5211, 5214 a 5224, 5420 a 5458, 5475 a 5499, 5787 a 5799, 6061 a 6085, 6340 a 6369, 6420 a 6469, 6827 a 6839, 7011 a 7051, 7950 a 7967, 81xx, 82xx, 83xx, 84xx, 85xx, 86xx, 87xx 
Vivo: 5472 a 5474, 5769 a 5786, 6057 a 6060, 6182 a 6199, 6370 a 6419, 6470 a 6499, 6840 a 6866, 6900 a 6913, 7087 a 7099, 71xx, 72xx, 73xx, 74xx, 75xx, 95xx, 96xx, 97xx, 98xx, 99xx'''

# Retorna um dicionario com operadoras e seus numeros correspondentes
def carregar_dados():
    dados = {}
    for linha in texto.split("\n"):
        operadora, numeros = linha.split(":")
        dados[operadora] = []
        intervalos = []
        for intervalo in numeros.split(","):
            intervalo = intervalo.strip()
            if len(intervalo) == 4 and intervalo.find("xx") != -1:
                x1 = int(intervalo[0:2]+"00")
                x2 = int(intervalo[0:2]+"99")
                intervalos += xrange(x1,x2)
                dados[operadora] = intervalos
            elif intervalo.find("a") != -1:
                x1, x2 = intervalo.split("a")
                intervalos += xrange(int(x1), int(x2))
                dados[operadora] = intervalos
            else:
                print("ERRO! Formato desconhecido: "+intervalo)
    return dados


# Dado o dicionario correto e um numero, retorna a operadora do numero
def descobrir_operadora(dados, numero):
    for operadora in dados.keys():
        try:
            n = int(numero)
            if n in dados[operadora]:
                return operadora
        except:
            return None
    return None

d = carregar_dados()

import contacts
db = contacts.open()
ids =  db.keys()
cont = 0

# Passa por todos os contatos identificando as operadoras
for id in ids:
    cont += 1
    contato = db[id]
    ops = ""
    for tipo in ['mobile_number', 'phone_number']:
        num_inteiro = contato.find(tipo)
        if len(num_inteiro) > 0:
            num = num_inteiro[0].value[-8:-4]
            if len(num) == 4:
                oper = descobrir_operadora(d, num) 
                if oper != None:
                    if len(ops) == 0:
                        ops = oper
                    else:
                        ops += "/"+oper
    # Caso alguma operadora foi identificada, salva o nome dela no campo empresa
    if len(ops):
        empresa = contato.find('company_name')
        contato.begin()
        if len(empresa):
            empresa[0].value = ops
        else:
            contato.add_field('company_name', ops)
        contato.commit()

print("Feito para %s contatos." % cont)
