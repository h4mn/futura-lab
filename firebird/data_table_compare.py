import fdb
import pprint

# Enumerador para tipo de dicionario: Simples e Colunas Separadas
class TipoDicionario:
  Simples = 0
  ColunasSeparadas = 1

class ConexaoFirebird:
  def __init__(self, 
    host='serverimport', 
    database=r'D:\_hads\_tarefas\LIMPA.FDB', 
    user='sysdba', 
    password='sbofutura'):
    self.host = host
    self.database = database
    self.user = user
    self.password = password
    self.conexao = self.conectar()

  def conectar(self):
    return fdb.connect(
      host=self.host,
      database=self.database,
      user=self.user,
      password=self.password
    )
  
  def sql(self, sql):
    cursor = self.conexao.cursor()
    cursor.execute(sql)
    self.cursor = cursor
    self.linhas = cursor.fetchall()
    self.colunas = [column[0] for column in cursor.description]
    return self.linhas

  # def colunas(self):
  #   return [column[0] for column in self.cursor.description]

  def dicionario(self, tipo=TipoDicionario.Simples, index=0):
    dict = {}
    for linha in self.linhas:
      if tipo == TipoDicionario.Simples:
        dict[linha[index]] = linha
      elif tipo == TipoDicionario.ColunasSeparadas:
        dict[linha[index]] = {self.colunas[i]: value for i, value in enumerate(linha)}
      else:
        raise Exception('Tipo de dicionário não suportado')     
    return dict

  def fechar(self):
    self.conexao.close()

def main():
  # Dicionario com os dados
  dados = {
    #FTP-80CH
    'limpa': {
      'path': 'D:\\_hads\\_tarefas\\LIMPA.FDB',
      'fk_layout': 7,
    },
    #NOVO NOVO
    'teste': {
      'path': 'D:\\_hads\\_tarefas\\TESTE.FDB',
      'fk_layout': 1401,
    },
  }
  sql = """--sql
    select i.id, i.fk_layout, i.descricao, i.campo, i.tipocampo, i.secao, i.linha, i.coluna, i.tamanho_maximo
    from layout_item i 
    where 1=1
      and i.fk_layout = {fk_layout}
      and i.imprime = 'S'
    ;
  """

  # Conexão com o banco de dados
  fb1 = ConexaoFirebird(database=dados['limpa']['path'])
  fb2 = ConexaoFirebird(database=dados['teste']['path'])

  # Executar o comando SQL e recuperar as linhas retornadas
  fb1.sql(sql.format(fk_layout=dados['limpa']['fk_layout']))
  fb2.sql(sql.format(fk_layout=dados['teste']['fk_layout']))

  # Imprimir o resultado
  #pprint.pprint( fb1.dicionario(TipoDicionario.ColunasSeparadas) )
  #pprint.pprint( fb2.dicionario(TipoDicionario.ColunasSeparadas) )
  teste1 = fb1.dicionario(TipoDicionario.ColunasSeparadas, index=2)
  print( teste1['SALDO DE LINHAS PARA CORTE']['CAMPO'] )
  teste2 = fb2.dicionario(TipoDicionario.ColunasSeparadas, index=2)
  print( teste2['SALDO DE LINHAS PARA CORTE']['CAMPO'] )

  # Comparar os dicionários
  if 1==0:
    dict1 = fb1.dicionario(TipoDicionario.ColunasSeparadas)
    dict2 = fb2.dicionario(TipoDicionario.ColunasSeparadas)
    for key in set(dict1.keys()).intersection(dict2.keys()):
      if dict1[key] != dict2[key]:
        print(f"Valores diferentes para a chave {key}: {dict1[key]} (dict1), {dict2[key]} (dict2)")

  if 1==1:
    dict1 = fb1.dicionario(TipoDicionario.ColunasSeparadas)
    dict2 = fb2.dicionario(TipoDicionario.ColunasSeparadas)

    # Para cada campo presente nos dois dicionários
    for campo in set(dict1.keys()).intersection(dict2.keys()):
        # Se os valores associados ao campo são diferentes nos dois dicionários
        if dict1[campo] != dict2[campo]:
            print(f"Valores diferentes para o campo {campo}: {dict1[campo]} (dict1), {dict2[campo]} (dict2)")


  # Fechar a conexão com o banco de dados
  fb1.fechar()
  fb2.fechar()

if __name__ == '__main__':
  main()