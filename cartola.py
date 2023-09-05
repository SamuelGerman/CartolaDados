import pandas as pd
import os


#define valor dos scouts
GOL = 8
ASS = 5
CA = -1
FS = 0.5
DS = 1.2
FC = -0.3
FF = 0.8
SG = 5.0
FD = 1.2
PS = 1

#Constantes e seus significados no EXCEL
GOLEIRO = 1
LAT = 2
ZAG = 3
MEI = 4
ATA = 5
TEC = 6
PROVAVEL = 7

cartoletas_restantes = 121.16
#Dicionario com o nome dos clubes do campeonato e seus IDS

clubes = {

    1371: 'Cuiaba',
    262: 'Flamengo',
    263: 'Botafogo',
    264: 'Corinthians',
    265: 'Bahia',
    266: 'Fluminense',
    267: 'Vasco da Gama',
    275: 'Palmeiras',
    276: 'Sao Paulo',
    277: 'Santos',
    280: 'Bragantino',
    282: 'Atletico MG',
    283: 'Cruzeiro',
    284: 'Gremio',
    285: 'Internacional',
    290: 'Goias',
    293: 'Athletico PR',
    294: 'Coritiba',
    327: 'America MG',
    356: 'Fortaleza'
}

#Constantes para o problema da escalação do time (representam a formação)
NUM_ATA = 3
NUM_MEI = 3
NUM_ZAG= 2
NUM_LAT = 2
NUM_TEC=1
NUM_GOL = 1


def lista_times_tec(dataframe, clubes):
    # Inicializa a lista para armazenar os valores de 'CASA GANHA' e 'FORA GANHA'
    ganhos_casa_fora = []
    
    # Itera sobre cada linha do DataFrame e adiciona os valores de 'CASA GANHA' e 'FORA GANHA' à lista
    for index, row in dataframe.iterrows():
        ganhos_casa = row['CASA GANHA']
        ganhos_fora = row['FORA GANHA']
        ganhos_casa_fora.extend([ganhos_casa, ganhos_fora])
    
    # Seleciona os cinco maiores valores da lista de 'CASA GANHA' e 'FORA GANHA'
    maiores_ganhos = sorted(ganhos_casa_fora, reverse=True)[:5]
    
    # Inicializa a lista final para armazenar os IDs dos times
    ids_times = []
    
    # Itera sobre os cinco maiores valores
    for valor in maiores_ganhos:
        # Verifica em qual coluna o valor se encontra ('CASA GANHA' ou 'FORA GANHA')
        if valor in dataframe['CASA GANHA'].values:
            # Se o valor estiver na coluna 'CASA GANHA', adiciona o ID do time presente na coluna 'TIME CASA'
            nome_time = dataframe[dataframe['CASA GANHA'] == valor]['TIME CASA'].values[0]
        elif valor in dataframe['FORA GANHA'].values:
            # Se o valor estiver na coluna 'FORA GANHA', adiciona o ID do time presente na coluna 'TIME FORA'
            nome_time = dataframe[dataframe['FORA GANHA'] == valor]['TIME FORA'].values[0]
        else:
            # Se o valor não estiver em nenhuma das colunas, ignora o valor
            continue
        
        # Converte o nome do time para o ID correspondente usando o dicionário 'clubes'
        id_time = next((id_time for id_time, nome in clubes.items() if nome == nome_time), None)
        if id_time is not None:
            # Adiciona o ID do time à lista final
            ids_times.append(id_time)
    
    # Retorna a lista com os IDs dos times
    return ids_times

def lista_times_ataque(dataframe, clubes):
   # Inicializa uma lista vazia para armazenar os IDs dos times
    ids_times = []
    
    # Itera sobre cada linha do DataFrame
    for index, row in dataframe.iterrows():
        # Verifica se o valor da coluna 'ESCALAR DEFESA CASA' é diferente de 'NÃO'
        if row['ESCALAR ATAQUE CASA'] != 'NÃO':
            # Se for diferente de 'NÃO', adiciona o ID do time presente na coluna 'TIME CASA' à lista
            nome_time = row['TIME CASA']
            id_time = [id for id, nome in clubes.items() if nome == nome_time][0]
            ids_times.append(id_time)
        
        # Verifica se o valor da coluna 'ESCALAR DEFESA FORA' é diferente de 'NÃO'
        if row['ESCALAR ATAQUE FORA'] != 'NÃO':
            # Se for diferente de 'NÃO', adiciona o ID do time presente na coluna 'TIME FORA' à lista
            nome_time = row['TIME FORA']
            id_time = [id for id, nome in clubes.items() if nome == nome_time][0]
            ids_times.append(id_time)
    
    # Retorna a lista com os IDs dos times
    return ids_times

def lista_times_defesa(dataframe):
    # Inicializa uma lista vazia para armazenar os IDs dos times
    ids_times = []
    
    # Itera sobre cada linha do DataFrame
    for index, row in dataframe.iterrows():
        # Verifica se o valor da coluna 'ESCALAR DEFESA CASA' é diferente de 'NÃO'
        if row['ESCALAR DEFESA CASA'] != 'NÃO':
            # Se for diferente de 'NÃO', adiciona o ID do time presente na coluna 'TIME CASA' à lista
            nome_time = row['TIME CASA']
            id_time = [id for id, nome in clubes.items() if nome == nome_time][0]
            ids_times.append(id_time)
        
        # Verifica se o valor da coluna 'ESCALAR DEFESA FORA' é diferente de 'NÃO'
        if row['ESCALAR DEFESA FORA'] != 'NÃO':
            # Se for diferente de 'NÃO', adiciona o ID do time presente na coluna 'TIME FORA' à lista
            nome_time = row['TIME FORA']
            id_time = [id for id, nome in clubes.items() if nome == nome_time][0]
            ids_times.append(id_time)
    
    # Retorna a lista com os IDs dos times
    return ids_times


def Pontuacao_Ofens_Med_Casa(row):
    return (row['FS.2']*FS + row['FF.2']*FF + row['G.2']*GOL + row['FD.2']*FD + row['A']*ASS)/((row['jogos_casa']+0.001)/2)

def Pontuacao_Ofens_Med_Fora(row):
    return (row['FS.3']*FS + row['FF.3']*FF + row['G.3']*GOL + row['FD.3']*FD + row['A']*ASS)/((row['jogos_fora']+0.001)/2) #df nao tem a.1 e a.2

def Pontuacao_Def_Casa(row):
    return (row['DS.2']*(DS+1) + row['FC.2']*FC + row['CA.2']*CA + row['SG']*SG)/((row['jogos_casa']+0.001)/2) #df n tem sg.2 e .3

def Pontuacao_Def_Fora(row):
    return (row['DS.3']*(DS+1) + row['FC.3']*FC + row['CA.3']*CA + row['SG']*SG)/((row['jogos_fora']+0.001)/2)

def Pontuacao_Scouts_Simples_Casa(row): #media
    return (row['FS.2']*FS + row['FF.2']*FF + row['FD.2']*FD + row['DS.2']*DS + row['FC.2']*FC +row['CA.2']*CA)/((row['jogos_casa']+0.001)/2)

def Pontuacao_Scouts_Simples_Fora(row): #media
    return (row['FS.3']*FS + row['FF.3']*FF + row['FD.3']*FD + row['DS.3']*DS + row['FC.3']*FC +row['CA.3']*CA)/((row['jogos_fora']+0.001)/2)

def rank_tec_provaveis(df, df_resumo, clubes):
    '''
    Esta função calcula o rank dos técnicos prováveis.

    Args:
        df: Um DataFrame contendo os dados da tabela resumida.
        df_resumo: Um DataFrame contendo os dados da tabela resumida.
        clubes: Um dicionário que mapeia os IDs dos clubes para os nomes dos clubes.

    Returns:
        Um DataFrame com as colunas `Rank_tec_casa` e `Rank_tec_fora` adicionadas.
    '''

    # Selecione as linhas do DataFrame em que o valor de `posicao_id` é igual à constante `TEC`.
    tecnicos_provaveis = df[df['posicao_id'] == TEC]

    # Para cada técnico, encontre o time do técnico na tabela resumida.
    for index, row in tecnicos_provaveis.iterrows():
        clube_id = row['clube_id']
        clube_nome = clubes[clube_id]

        # Se o clube estiver na coluna `TIME CASA`, o ranking do técnico será 2 * o valor da coluna `CASA GANHA`.
        if clube_nome in df_resumo['TIME CASA'].values:
            tecnicos_provaveis.loc[index, 'Rank_tec_casa'] =100* ((df_resumo[df_resumo['TIME CASA'] == clube_nome]['%SOFRE GOL FORA'].values[0] + df_resumo[df_resumo['TIME CASA'] == clube_nome]['CASA GANHA'].values[0]+ df_resumo[df_resumo['TIME CASA'] == clube_nome]['%SG CASA'].values[0])/3) 
        # Caso o time não esteja na coluna `TIME_CASA`, o ranking do técnico será 2 * o valor da coluna `FORA GANHA`.
        elif clube_nome in df_resumo['TIME FORA'].values:
            tecnicos_provaveis.loc[index, 'Rank_tec_fora'] = 100 * ((df_resumo[df_resumo['TIME FORA'] == clube_nome]['%SOFRE GOL CASA'].values[0] + df_resumo[df_resumo['TIME FORA'] == clube_nome]['FORA GANHA'].values[0]+ df_resumo[df_resumo['TIME FORA'] == clube_nome]['%SG FORA'].values[0]) /3) 

    # Retorne o DataFrame com as colunas `Rank_tec_casa` e `Rank_tec_fora` adicionadas.
    return tecnicos_provaveis



def rank_gol_provaveis(df, df_resumo, clubes):
    # Selecione as linhas do DataFrame em que o valor de `posicao_id` é igual à constante `GOLEIRO`.
    goleiros_provaveis = df[df['posicao_id'] == GOLEIRO]

    # Inicialize as colunas 'Rank_gol_casa' e 'Rank_gol_fora' com valor zero.
    goleiros_provaveis['Rank_gol_casa'] = 0
    goleiros_provaveis['Rank_gol_fora'] = 0

    # Para cada goleiro, encontre o time do goleiro na tabela resumida.
    for index, row in goleiros_provaveis.iterrows():
        clube_id = row['clube_id']
        clube_nome = clubes[clube_id]

        # Se o clube estiver na coluna `TIME CASA`, o ranking do goleiro será 50 * o valor da coluna `%SG CASA`.
        if clube_nome in df_resumo['TIME CASA'].values:
            goleiros_provaveis.loc[index, 'Rank_gol_casa'] = 100 * df_resumo[df_resumo['TIME CASA'] == clube_nome]['%SG CASA'].values[0] 

        # Caso o time não esteja na coluna `TIME_CASA`, o ranking do goleiro será 50 * o valor da coluna `%SG FORA`.
        elif clube_nome in df_resumo['TIME FORA'].values:
            goleiros_provaveis.loc[index, 'Rank_gol_fora'] = 100 * df_resumo[df_resumo['TIME FORA'] == clube_nome]['%SG FORA'].values[0] 

    # Retorne o DataFrame com as colunas `Rank_gol_casa` e `Rank_gol_fora` adicionadas.
    return goleiros_provaveis

def rank_ata_provaveis(df, df_resumo, clubes):
    """
    Esta função calcula o rank dos atacantes prováveis.

    Args:
        df: Um DataFrame contendo os dados da tabela resumida.
        df_resumo: Um DataFrame contendo os dados da tabela resumida.
        clubes: Um dicionário que mapeia os IDs dos clubes para os nomes dos clubes.

    Returns:
        Um DataFrame com as colunas `Rank_ata_casa` e `Rank_ata_fora` adicionadas.
    """

    # Selecione as linhas do DataFrame em que o valor de `posicao_id` é igual à constante `ATA`.
    atacantes_provaveis = df[(df['posicao_id'] ==ATA) & (df['jogos_casa'] > 0) & (df['jogos_fora'] > 0)]

    # Calcule o rank de cada atacante.
    atacantes_provaveis['Rank_ata_casa'] = (atacantes_provaveis['Pont.Ofens.Med.Casa']* 8.81 + atacantes_provaveis['Pont.DefMed.Casa']*2.2/2 + atacantes_provaveis['Pont.Scout.Basico.Casa']*2* 6.08+ atacantes_provaveis['G.2']/(atacantes_provaveis['jogos_casa']+0.01)* 3.95 + atacantes_provaveis['A.2']/(atacantes_provaveis['jogos_casa']+0.01) *0.93  + atacantes_provaveis['FF.2']/(atacantes_provaveis['jogos_casa']+0.01)*1.25 + atacantes_provaveis['FD.2']/(atacantes_provaveis['jogos_casa']+0.01)* 1.30 + atacantes_provaveis['FS.2'] /(atacantes_provaveis['jogos_casa']+0.01)* 1.34 + atacantes_provaveis['DS.2']/(atacantes_provaveis['jogos_casa']+0.01) * 2.20 + atacantes_provaveis['PS.2'] /(atacantes_provaveis['jogos_casa']+0.01)* 0.04)#*4.2
    atacantes_provaveis['Rank_ata_fora'] = (atacantes_provaveis['Pont.Ofens.Med.Fora'] * 9.11 + atacantes_provaveis['Pont.DefMed.Fora']*2.21/2 + atacantes_provaveis['Pont.Scout.Basico.Fora'] *2* 6.57+ atacantes_provaveis['G.3']/(atacantes_provaveis['jogos_fora']+0.01) * 3.72 + atacantes_provaveis['A.3']/(atacantes_provaveis['jogos_fora']+0.01) *0.96  + atacantes_provaveis['FF.3']/(atacantes_provaveis['jogos_fora']+0.01)*1.25 + atacantes_provaveis['FD.3']/(atacantes_provaveis['jogos_fora']+0.01) * 1.30 + atacantes_provaveis['FS.3'] /(atacantes_provaveis['jogos_fora']+0.01)* 1.81 + atacantes_provaveis['DS.3'] /(atacantes_provaveis['jogos_fora']+0.01)* 2.21 + atacantes_provaveis['PS.3'] /(atacantes_provaveis['jogos_fora']+0.01)*0.07)#*4.2

    for index, row in atacantes_provaveis.iterrows():
        clube_id = row['clube_id']
        clube_nome = clubes[clube_id]

        if clube_nome in df_resumo['TIME CASA'].values:
            atacantes_provaveis.loc[index, 'Rank_ata_casa'] *=df_resumo[df_resumo['TIME CASA'] == clube_nome]['%SOFRE GOL FORA'].values[0] #dar mais importancia para atacantes

        
        elif clube_nome in df_resumo['TIME FORA'].values:
            atacantes_provaveis.loc[index, 'Rank_ata_fora'] *=df_resumo[df_resumo['TIME FORA'] == clube_nome]['%SOFRE GOL CASA'].values[0] 


    return atacantes_provaveis


def rank_mei_provaveis(df,df_resumo,clubes):
  """
  Esta função calcula o rank dos meias

  Args:
    df: Um DataFrame contendo os dados da tabela resumida.

  Returns:
    Um DataFrame
  """

  # Selecione as linhas do DataFrame em que o valor de `posicao_id` é igual à constante `ATA`.
  meias_provaveis = df[(df['posicao_id'] ==MEI) & (df['jogos_casa'] > 0) & (df['jogos_fora'] > 0)]
  # Calcule o rank de cada atacante.
  meias_provaveis['Rank_mei_casa'] = (meias_provaveis['Pont.Ofens.Med.Casa'] *6.75*2 + meias_provaveis['Pont.DefMed.Casa']*4.95/2 + meias_provaveis['Pont.Scout.Basico.Casa'] *8.8*2 + meias_provaveis['G.2']/(meias_provaveis['jogos_casa']+0.01) * 1.83 + meias_provaveis['A.2']/(meias_provaveis['jogos_casa']+0.01) * 1.05 + meias_provaveis['FF.2']/(meias_provaveis['jogos_casa']+0.01)*1.16 + meias_provaveis['FD.2'] /(meias_provaveis['jogos_casa']+0.01)* 1 + meias_provaveis['FS.2']/(meias_provaveis['jogos_casa']+0.01) * 1.69  + meias_provaveis['DS.2'] /(meias_provaveis['jogos_casa']+0.01)*4.95 + meias_provaveis['PS.2']/(meias_provaveis['jogos_casa']+0.01) * 0.02)*3.3
  meias_provaveis['Rank_mei_fora'] = (meias_provaveis['Pont.Ofens.Med.Fora'] *6.35*2 + meias_provaveis['Pont.DefMed.Fora']*5.32/2 + meias_provaveis['Pont.Scout.Basico.Fora'] *8.93 *2+ meias_provaveis['G.3']/(meias_provaveis['jogos_fora']+0.01) *1.55  + meias_provaveis['A.3']/(meias_provaveis['jogos_fora']+0.01) * 1.17 + meias_provaveis['FF.3']/(meias_provaveis['jogos_fora']+0.01)*0.85 + meias_provaveis['FD.3'] /(meias_provaveis['jogos_fora']+0.01) *0.84 + meias_provaveis['FS.3'] /(meias_provaveis['jogos_fora']+0.01)* 1.93 + meias_provaveis['DS.3'] /(meias_provaveis['jogos_fora']+0.01)*5.32+ meias_provaveis['PS.3']/(meias_provaveis['jogos_fora']+0.01)* 0.01)*3.3
  
  for index, row in meias_provaveis.iterrows():
        clube_id = row['clube_id']
        clube_nome = clubes[clube_id]

        # Se o clube estiver na coluna `TIME CASA`, o ranking do goleiro será 50 * o valor da coluna `%SG CASA`.
        if clube_nome in df_resumo['TIME CASA'].values:
            meias_provaveis.loc[index, 'Rank_mei_casa'] *= (df_resumo[df_resumo['TIME CASA'] == clube_nome]['%SOFRE GOL FORA'].values[0]) 

        # Caso o time não esteja na coluna `TIME_CASA`, o ranking do goleiro será 50 * o valor da coluna `%SG FORA`.
        elif clube_nome in df_resumo['TIME FORA'].values:
            meias_provaveis.loc[index, 'Rank_mei_fora'] *= (df_resumo[df_resumo['TIME FORA'] == clube_nome]['%SOFRE GOL CASA'].values[0])
 
  # Retorne o DataFrame com a coluna `Rank_ata_casa` adicionada.
  return meias_provaveis

def rank_zag_provaveis(df,df_resumo,clubes):
  """
  Esta função calcula o rank dos zagueiros prováveis.

  Args:
    df: Um DataFrame contendo os dados da tabela resumida.

  Returns:
    Um DataFrame com as colunas `Rank_zag_casa` e `Rank_zag_fora` adicionadas.
  """

  # Selecione as linhas do DataFrame em que o valor de `posicao_id` é igual à constante `ZAG`.
  zagueiros_provaveis = df[(df['posicao_id'] ==ZAG) & (df['jogos_casa'] > 0) & (df['jogos_fora'] > 0)]

  # Calcule o rank de cada zagueiro em casa.
  zagueiros_provaveis['Rank_zag_casa'] = (zagueiros_provaveis['Pont.Ofens.Med.Casa'] * 3.11 + zagueiros_provaveis['Pont.DefMed.Casa'] *8.34 + zagueiros_provaveis['Pont.Scout.Basico.Casa'] * 5.25*2 + zagueiros_provaveis['G.2']/(zagueiros_provaveis['jogos_casa']+0.01) * 1.04+ zagueiros_provaveis['A.2'] /(zagueiros_provaveis['jogos_casa']+0.01)*0.32 + zagueiros_provaveis['FF.2']/(zagueiros_provaveis['jogos_casa']+0.01)*0.51 + zagueiros_provaveis['FD.2']/(zagueiros_provaveis['jogos_casa']+0.01) *0.42 + zagueiros_provaveis['FS.2']/(zagueiros_provaveis['jogos_casa']+0.01) * 0.82 + zagueiros_provaveis['DS.2']/(zagueiros_provaveis['jogos_casa']+0.01) * 2*3.51+ zagueiros_provaveis['PS.2']/(zagueiros_provaveis['jogos_casa']+0.01)* 0.01)
  zagueiros_provaveis['Rank_zag_fora'] = (zagueiros_provaveis['Pont.Ofens.Med.Fora'] * 2.87 + zagueiros_provaveis['Pont.DefMed.Fora'] *9.04 + zagueiros_provaveis['Pont.Scout.Basico.Fora'] * 6.28*2 + zagueiros_provaveis['G.3']/(zagueiros_provaveis['jogos_fora']+0.01) * 0.68+ zagueiros_provaveis['A.3'] /(zagueiros_provaveis['jogos_fora']+0.01)*0.33 + zagueiros_provaveis['FF.3']/(zagueiros_provaveis['jogos_fora']+0.01)*0.46 + zagueiros_provaveis['FD.3']/(zagueiros_provaveis['jogos_fora']+0.01) * 0.41 + zagueiros_provaveis['FS.3']/(zagueiros_provaveis['jogos_fora']+0.01) * 0.98+ zagueiros_provaveis['DS.3']/(zagueiros_provaveis['jogos_fora']+0.01) * 2*4.43+ zagueiros_provaveis['PS.3']/(zagueiros_provaveis['jogos_fora']+0.01)*0)
  for index, row in zagueiros_provaveis.iterrows():
        clube_id = row['clube_id']
        clube_nome = clubes[clube_id]

        # Se o clube estiver na coluna `TIME CASA`, o ranking do goleiro será 50 * o valor da coluna `%SG CASA`.
        if clube_nome in df_resumo['TIME CASA'].values:
            zagueiros_provaveis.loc[index, 'Rank_zag_casa'] *=(df_resumo[df_resumo['TIME CASA'] == clube_nome]['%SG CASA'].values[0])

        # Caso o time não esteja na coluna `TIME_CASA`, o ranking do goleiro será 50 * o valor da coluna `%SG FORA`.
        elif clube_nome in df_resumo['TIME FORA'].values:
            zagueiros_provaveis.loc[index, 'Rank_zag_fora'] *=(df_resumo[df_resumo['TIME FORA'] == clube_nome]['%SG FORA'].values[0])
   
  
  # Retorne o DataFrame com as colunas `Rank_zag_casa` e `Rank_zag_fora` adicionadas.
  return zagueiros_provaveis

def rank_lat_provaveis(df,df_resumo,clubes):
    """
    Esta função calcula o rank dos laterais prováveis.

    Args:
        df: Um DataFrame contendo os dados da tabela resumida.

    Returns:
        Um DataFrame
    """

    # Selecione as linhas do DataFrame em que o valor de `posicao_id` é igual à constante `LAT`.
    laterais_provaveis = df[(df['posicao_id'] ==LAT) & (df['jogos_casa'] > 0) & (df['jogos_fora'] > 0)]
    # Calcule o rank de cada lateral provável.
    laterais_provaveis['Rank_lat_casa'] = (laterais_provaveis['Pont.Ofens.Med.Casa'] * 3.42 + laterais_provaveis['Pont.DefMed.Casa'] * 7.69 + laterais_provaveis['Pont.Scout.Basico.Casa'] * 5.94*2 + laterais_provaveis['G.2']/(laterais_provaveis['jogos_casa']+0.01) * 0.68 + laterais_provaveis['A.2']/(laterais_provaveis['jogos_casa']+0.01) * 0.94 + laterais_provaveis['FF.2']/(laterais_provaveis['jogos_casa']+0.01)*0.44 + laterais_provaveis['FD.2'] /(laterais_provaveis['jogos_casa']+0.01)* 0.48 + laterais_provaveis['FS.2'] /(laterais_provaveis['jogos_casa']+0.01)* 0.87 + laterais_provaveis['DS.2'] /(laterais_provaveis['jogos_casa']+0.01)*2*4.15+ laterais_provaveis['PS.2']/(laterais_provaveis['jogos_casa']+0.01)* 0.01)
    laterais_provaveis['Rank_lat_fora'] = (laterais_provaveis['Pont.Ofens.Med.Fora'] * 3.09 + laterais_provaveis['Pont.DefMed.Fora'] * 8.22 + laterais_provaveis['Pont.Scout.Basico.Fora'] * 6.86*2 + laterais_provaveis['G.3']/(laterais_provaveis['jogos_fora']+0.01) * 0.48 + laterais_provaveis['A.3']/(laterais_provaveis['jogos_fora']+0.01) * 0.69 + laterais_provaveis['FF.3']/(laterais_provaveis['jogos_fora']+0.01)*0.47 + laterais_provaveis['FD.3']/(laterais_provaveis['jogos_fora']+0.01) * 0.29 + laterais_provaveis['FS.3']/(laterais_provaveis['jogos_fora']+0.01) * 1.16 + laterais_provaveis['DS.3'] /(laterais_provaveis['jogos_fora']+0.01)*2*4.94+ laterais_provaveis['PS.3']/(laterais_provaveis['jogos_fora']+0.01)*0.01)
     
    for index, row in laterais_provaveis.iterrows():
        clube_id = row['clube_id']
        clube_nome = clubes[clube_id]

        # Se o clube estiver na coluna `TIME CASA`, o ranking do goleiro será 50 * o valor da coluna `%SG CASA`.
        if clube_nome in df_resumo['TIME CASA'].values:
            laterais_provaveis.loc[index, 'Rank_lat_casa'] *=df_resumo[df_resumo['TIME CASA'] == clube_nome]['%SG CASA'].values[0] 
            

        # Caso o time não esteja na coluna `TIME_CASA`, o ranking do goleiro será 50 * o valor da coluna `%SG FORA`.
        elif clube_nome in df_resumo['TIME FORA'].values:
            laterais_provaveis.loc[index, 'Rank_lat_fora'] *=df_resumo[df_resumo['TIME FORA'] == clube_nome]['%SG FORA'].values[0] 
            
    # Retorne o DataFrame com as colunas `Rank_lat_casa` e `Rank_lat_fora` adicionadas.
    return laterais_provaveis

file_name = "Dados_CartolaCorreto.xlsx"
caminho_excel = os.path.abspath(os.path.join("E:\Gaming\Estudo\cartola", file_name))

Dados_Cartola = pd.read_excel(caminho_excel, sheet_name=1)

#pontuação ofensiva média em casa / fora, e pontuação defensiva média
#e pontuação de scouts simples média em casa/fora

Dados_Cartola['Pont.Ofens.Med.Casa'] = Dados_Cartola.apply(Pontuacao_Ofens_Med_Casa,axis=1)
Dados_Cartola['Pont.Ofens.Med.Fora'] = Dados_Cartola.apply(Pontuacao_Ofens_Med_Fora,axis=1)
Dados_Cartola['Pont.DefMed.Casa'] = Dados_Cartola.apply(Pontuacao_Def_Casa,axis=1)
Dados_Cartola['Pont.DefMed.Fora'] = Dados_Cartola.apply(Pontuacao_Def_Fora,axis=1)
Dados_Cartola['Pont.Scout.Basico.Casa'] = Dados_Cartola.apply(Pontuacao_Scouts_Simples_Casa,axis=1)
Dados_Cartola['Pont.Scout.Basico.Fora'] = Dados_Cartola.apply(Pontuacao_Scouts_Simples_Fora,axis=1)

Dados_Cartola=Dados_Cartola[Dados_Cartola['status_id']==PROVAVEL]
#print(Dados_Cartola.head())

#Definir melhores opções de times para defesa, ataque e meio campo.

Predic_Ult4 = pd.read_excel(caminho_excel,sheet_name='tabela com médias das predições')
Tabela_Resumida = Predic_Ult4.loc[0:9, 'PARTIDA':'ESCALAR TEC FORA']
del Tabela_Resumida['Coluna1']
del Tabela_Resumida['Coluna2']

equipes_defesa = lista_times_defesa(Tabela_Resumida)
equipes_ataque = lista_times_ataque(Tabela_Resumida,clubes)
equipes_tec = lista_times_tec(Tabela_Resumida,clubes)

df_rank_tec_provaveis = rank_tec_provaveis(Dados_Cartola,Tabela_Resumida,clubes)
df_rank_tec_provaveis=df_rank_tec_provaveis[df_rank_tec_provaveis['clube_id'].isin(equipes_tec)]


df_rank_gol_provaveis = rank_gol_provaveis(Dados_Cartola,Tabela_Resumida,clubes)
df_rank_gol_provaveis = df_rank_gol_provaveis[df_rank_gol_provaveis['clube_id'].isin(equipes_defesa)]



df_rank_ata_provaveis = rank_ata_provaveis(Dados_Cartola,Tabela_Resumida,clubes)
df_rank_ata_provaveis = df_rank_ata_provaveis[df_rank_ata_provaveis['clube_id'].isin(equipes_ataque)]
print(df_rank_ata_provaveis)

df_rank_meias_provaveis = rank_mei_provaveis(Dados_Cartola,Tabela_Resumida,clubes)

df_rank_meias_provaveis = df_rank_meias_provaveis[df_rank_meias_provaveis['clube_id'].isin(equipes_ataque)]


df_rank_zagueiros_provaveis = rank_zag_provaveis(Dados_Cartola,Tabela_Resumida,clubes)
df_rank_zagueiros_provaveis = df_rank_zagueiros_provaveis[df_rank_zagueiros_provaveis['clube_id'].isin(equipes_defesa)]


df_rank_laterais_provaveis = rank_lat_provaveis(Dados_Cartola,Tabela_Resumida,clubes)
df_rank_laterais_provaveis = df_rank_laterais_provaveis[df_rank_laterais_provaveis['clube_id'].isin(equipes_defesa)]


#df_rank_ata_provaveis=df_rank_ata_provaveis.to_excel('rank_ata_provaveis.xlsx')
#df_rank_laterais_provaveis=df_rank_laterais_provaveis.to_excel('rank_lat_provaveis.xlsx')
#df_rank_zagueiros_provaveis=df_rank_zagueiros_provaveis.to_excel('rank_zag_provaveis.xlsx')
#df_rank_meias_provaveis=df_rank_meias_provaveis.to_excel('rank_mei_provaveis.xlsx')

# Step 1: Concatenate the data frames of attackers, defenders, midfielders, and full-backs
df_rank_ata_provaveis['posicao'] = 'ata'  # Adding a column 'posicao' to identify attackers
df_rank_meias_provaveis['posicao'] = 'mei'  # Adding a column 'posicao' to identify midfielders
df_rank_zagueiros_provaveis['posicao'] = 'zag'  # Adding a column 'posicao' to identify defenders
df_rank_laterais_provaveis['posicao'] = 'lat'  # Adding a column 'posicao' to identify full-backs
df_rank_gol_provaveis['posicao']='gol'
df_rank_tec_provaveis['posicao']='tec'
# Concatenate the data frames of attackers, defenders, midfielders, and full-backs
df_aggregated_players = pd.concat([
    df_rank_ata_provaveis,
    df_rank_meias_provaveis,
    df_rank_zagueiros_provaveis,
    df_rank_laterais_provaveis,
    df_rank_gol_provaveis,
    df_rank_tec_provaveis
])

# Step 2: Determine if each player is playing at home or away
def get_ranking_utilizado(row):
    nome_time = clubes[row['clube_id']]  # Get the name of the team from 'clubes' dictionary
    if nome_time in Tabela_Resumida['TIME CASA'].values:
        return row['Rank_' + row['posicao'].lower() + '_casa']  # Use home ranking
    else:
        return row['Rank_' + row['posicao'].lower() + '_fora']  # Use away ranking

# Step 3: Create a new column 'ranking_utilizado' in the aggregated data frame
df_aggregated_players['ranking_utilizado'] = df_aggregated_players.apply(get_ranking_utilizado, axis=1)


# List of columns to be deleted from the aggregated data frame
columns_to_delete = ['CA', 'DS', 'FC', 'FF', 'FS', 'A', 'FD', 'G', 'PS', 'SG', 'rodada_id',
                     'posicao_id', 'status_id', 'pontos_num', 'variacao_num', 'media_num', 'jogos_num','minimo_para_valorizar',
                     'media_pontos_mandante', 'media_pontos_visitante',
                     'media_minutos_jogados', 'minutos_jogados', 'FS.1', 'DS.1', 'FC.1', 'CA.1', 'FF.1',
                     'SG.1', 'A.1', 'G.1', 'FD.1', 'PS.1', 'FS.2', 'DS.2', 'FC.2', 'CA.2', 'FF.2', 'SG.2',
                     'G.2', 'FD.2', 'PS.2', 'FS.3', 'DS.3', 'FC.3', 'CA.3', 'FF.3', 'A.2', 'G.3', 'FD.3',
                     'Pont.Ofens.Med.Casa', 'Pont.Ofens.Med.Fora', 'Pont.DefMed.Casa', 'Pont.DefMed.Fora',
                     'Pont.Scout.Basico.Casa', 'Pont.Scout.Basico.Fora', 'Rank_ata_casa', 'Rank_ata_fora',
                     'Rank_mei_casa', 'Rank_mei_fora', 'Rank_zag_casa', 'Rank_zag_fora', 'Rank_lat_casa',
                     'Rank_lat_fora','Rank_tec_casa','Rank_tec_fora','Rank_gol_casa','Rank_gol_fora','A.3','SG.3','PS.3','pontos_casa','pontos_fora','jogos_casa','jogos_fora']

# Drop the specified columns from the aggregated data frame
df_aggregated_players.drop(columns=columns_to_delete, inplace=True)

df_aggregated_players.to_excel('agregados.xlsx')

import pulp

import pulp

def solve_player_selection(jogadores, cartoletas_restantes):
    # Filter players by position
    jogadores_ata = jogadores[jogadores['posicao'] == 'ata']
    jogadores_mei = jogadores[jogadores['posicao'] == 'mei']
    jogadores_lat = jogadores[jogadores['posicao'] == 'lat']
    jogadores_zag = jogadores[jogadores['posicao'] == 'zag']
    jogadores_tec = jogadores[jogadores['posicao'] == 'tec']
    jogadores_gol = jogadores[jogadores['posicao'] == 'gol']

    # Create a binary variable for each player to indicate if they are selected or not
    player_vars = pulp.LpVariable.dicts("Player", jogadores.index, cat=pulp.LpBinary)

    # Define the LP problem
    prob = pulp.LpProblem("Player_Selection_Problem", pulp.LpMaximize)

    # Objective: Maximize the total ranking points
    prob += pulp.lpSum(jogadores.loc[player_id, 'ranking_utilizado'] * player_vars[player_id] for player_id in jogadores.index)

    # Constraint: The total number of selected players should be equal to 12
    prob += pulp.lpSum(player_vars[player_id] for player_id in jogadores.index) == 12

    # Constraint: The total cost of selected players should not exceed cartoletas_restantes
    prob += pulp.lpSum(jogadores.loc[player_id, 'preco_num'] * player_vars[player_id] for player_id in jogadores.index) <= cartoletas_restantes

    # Constraint: Select exactly 3 atacantes
    prob += pulp.lpSum(player_vars[player_id] for player_id in jogadores_ata.index) == 3

    # Constraint: Select exactly 3 meio-campistas
    prob += pulp.lpSum(player_vars[player_id] for player_id in jogadores_mei.index) == 3

    # Constraint: Select exactly 2 laterais
    prob += pulp.lpSum(player_vars[player_id] for player_id in jogadores_lat.index) == 2

    # Constraint: Select exactly 2 zagueiros
    prob += pulp.lpSum(player_vars[player_id] for player_id in jogadores_zag.index) == 2

    # Constraint: Select exactly 1 tecnico
    prob += pulp.lpSum(player_vars[player_id] for player_id in jogadores_tec.index) == 1

    # Constraint: Select exactly 1 goleiro
    prob += pulp.lpSum(player_vars[player_id] for player_id in jogadores_gol.index) == 1

    # Constraint: Limit the selection of defenders from the same team to at most 2
    for time in jogadores_mei['clube_id'].unique():
        prob += pulp.lpSum(player_vars[player_id] for player_id in jogadores_mei[jogadores_mei['clube_id'] == time].index) <= 1
    for time in jogadores_ata['clube_id'].unique():
        prob += pulp.lpSum(player_vars[player_id] for player_id in jogadores_ata[jogadores_ata['clube_id'] == time].index) <= 1
    for time in jogadores_zag['clube_id'].unique():
        prob += pulp.lpSum(player_vars[player_id] for player_id in jogadores_zag[jogadores_zag['clube_id'] == time].index) <= 1
    for time in jogadores_lat['clube_id'].unique():
        prob += pulp.lpSum(player_vars[player_id] for player_id in jogadores_lat[jogadores_lat['clube_id'] == time].index) <= 1
    for time in jogadores_gol['clube_id'].unique():
        prob += pulp.lpSum(player_vars[player_id] for player_id in jogadores_gol[jogadores_gol['clube_id'] == time].index) <= 1

    # Solve the problem
    prob.solve()

    best_players = [player_id for player_id in jogadores.index if pulp.value(player_vars[player_id]) == 1]
    best_pontuacao_total = pulp.value(prob.objective)

    return best_players, best_pontuacao_total


# Assuming you have a DataFrame 'df_players' containing player information, including 'ranking_utilizado' and 'preco_num'
# Call the function to get the best combination
best_players, best_pontuacao_total = solve_player_selection(df_aggregated_players, cartoletas_restantes)

print("Pontuação total do time:", best_pontuacao_total)
print("Melhores jogadores:")
print(df_aggregated_players.loc[best_players, ['apelido', 'ranking_utilizado', 'preco_num']])
print(equipes_ataque)
print(equipes_defesa)

df_aggregated_players.loc[best_players].to_excel('time_escalado.xlsx')