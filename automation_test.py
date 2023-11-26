
import psycopg2.extras

import re
import queries
import pandas as pd


conn = psycopg2.connect(database = "matb09",
                        user = "postgres",
                        host= '192.168.15.5',
                        password = "postgres",
                        port = 5432)

cur = conn.cursor()

tempos = []

tempos_cenario1 = []

tempos_cenario2 = []

tempos_cenario3 = []

query_executada = []


def pegar_tempo(queries, indexes, drop_indexes):
    for index, item in enumerate(indexes):
        cur.execute(item)
        conn.commit()
        for query in queries:
            cur.execute('EXPLAIN ANALYSE ' + query)
            rows = cur.fetchall()
            string_tempo = rows[rows.__len__()-1].__str__()
            match = re.search(r'(\d+\.\d+)', string_tempo)
            numero_extraido = match.group(1)
            query_executada.append(query)
            tempos.append(numero_extraido)
        cur.execute(drop_indexes[index])
        conn.commit()

pegar_tempo(queries.queries, queries.indexes, queries.drop_indexes)

print(query_executada)
print("tamanho QUERY EXECUTADA:" + query_executada.__len__().__str__())
print(tempos)
print(tempos.__len__())
conn.commit()
conn.close()

def splitar_array(lista):
    #tempos_cenario1 = lista[:16]
    tempos_cenario1.append(lista[:16])
    #tempos_cenario2 = lista[16:32]
    tempos_cenario2.append(lista[16:32])
    #tempos_cenario3 = lista[32:]
    tempos_cenario3.append(lista[32:])
    print('------ CENARIOS -------')
    print(tempos_cenario1, "tamanho:" + tempos_cenario1.__len__().__str__())
    print(tempos_cenario2,"tamanho:" + tempos_cenario2.__len__().__str__())
    print(tempos_cenario3,"tamanho:" + tempos_cenario3.__len__().__str__())

splitar_array(tempos)

queries_label_planilha = [
"CCA1",
"CCA2",
"CCA3",
"CCA4",
"CCA5",
"CCA6",
"CCA7",
"CCA8",
"CCA9",
"CCA10",
"CCA11",
"CCA12",
"CCA13",
"CCA14",
"CCA15",
"CCA16",
]
print("TAMANHO QUERY PLANILHA", tempos_cenario1.__len__())
# Criar um DataFrame
data = {'Queries': queries_label_planilha, 'cenario_index_1': tempos[:16], 'cenario_index_2': tempos[16:32], 'cenario_index_3': tempos[32:]}
df = pd.DataFrame(data)

# Salvar para um arquivo CSV
df.to_csv('tunning3.csv', index=False)
