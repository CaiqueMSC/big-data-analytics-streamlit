# --------------------------------------------------------------
# Projeto: Trabalho Espaço Terapêutico neuro 7 vidas - Big Data em Python (Estácio)
# Empresa fictícia: Espaço Terapêutico Neuro 7 Vidas
# Autor: Caique Mariano, Joaquim Oliveira, Pedro Henrique.
# Data: 12/11/2025


import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import random
import os
 
# 1. GERAR CSV FICTÍCIO
if not os.path.exists('dados_clientes.csv'):
    random.seed(42)

    # Tipos de serviço oferecidos pela terapeuta
    servicos = [
        'Terapia Integrativa - Individual',
        'Terapia Integrativa - Casal',
        'Terapia Integrativa - Online'
    ]

    # Distribuição de gênero 
    generos_base = ['Feminino', 'Masculino', 'Não-binário', 'Outro']
    generos_restantes = random.choices(
        ['Feminino', 'Masculino', 'Não-binário', 'Outro'],
        weights=[0.5, 0.4, 0.07, 0.03], 
        k=26  # total 30 (26 + 4 garantidos)
    )
    generos = generos_base + generos_restantes
    random.shuffle(generos)

    #  Feedbacks possíveis 
    feedbacks = [
        "Excelente atendimento e ambiente acolhedor",
        "Senti muita melhora nas sessões",
        "Profissional muito atenciosa e competente",
        "Ótimo custo-benefício, recomendo!",
        "Ambiente tranquilo e energia positiva",
        "Me senti ouvido e compreendido",
        "Voltarei com certeza",
        "Resultados transformadores desde a primeira sessão",
        "A experiência foi única e enriquecedora",
        "Espaço que transmite paz e confiança"
    ]

    #  Geração dos dados 
    dados = []
    for i in range(30):
        dados.append({
            'id_cliente': i + 1,
            'idade': random.randint(18, 65),
            'gênero': generos[i],
            'tipo_serviço': random.choice(servicos),
            'valor_atendimento': round(random.uniform(120, 250), 2),
            'data_atendimento': f"2025-{random.randint(1, 9):02d}-{random.randint(1, 28):02d}",
            'feedback': random.choice(feedbacks)
        })

    #  Cria o CSV 
    df = pd.DataFrame(dados)
    df.to_csv('dados_clientes.csv', index=False, encoding='utf-8-sig')
    print("✅ Arquivo 'dados_clientes.csv' criado com sucesso!")

#  2. LER O ARQUIVO CSV 
df = pd.read_csv('dados_clientes.csv')

#  3. GRÁFICO DE BARRAS 
valor_medio = df.groupby('tipo_serviço')['valor_atendimento'].mean().sort_values()
plt.figure(figsize=(8,5))
valor_medio.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Valor médio gasto por tipo de serviço')
plt.xlabel('Tipo de Serviço')
plt.ylabel('Valor médio (R$)')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig('grafico_barras.png')
plt.show()

#  4. GRÁFICO DE PIZZA 
genero_counts = df['gênero'].value_counts()
plt.figure(figsize=(6,6))
plt.pie(genero_counts, labels=genero_counts.index, autopct='%1.1f%%', startangle=90)
plt.title('Distribuição de clientes por gênero')
plt.tight_layout()
plt.savefig('grafico_pizza.png')
plt.show()

#  5. WORD CLOUD 
texto_feedbacks = " ".join(df['feedback'].dropna())
nuvem = WordCloud(width=800, height=400, background_color='white', colormap='plasma').generate(texto_feedbacks)
plt.figure(figsize=(10,5))
plt.imshow(nuvem, interpolation='bilinear')
plt.axis('off')
plt.title('Palavras mais citadas nos feedbacks')
plt.tight_layout()
plt.savefig('grafico_wordcloud.png')
plt.show()

#  6. GRÁFICO COMPARATIVO 
df['mês'] = pd.to_datetime(df['data_atendimento']).dt.month
evolucao = df.groupby(['mês', 'tipo_serviço']).size().unstack(fill_value=0)
evolucao.plot(kind='bar', figsize=(10,6))
plt.title('Evolução mensal dos atendimentos por tipo de serviço')
plt.xlabel('Mês')
plt.ylabel('Quantidade de atendimentos')
plt.legend(title='Tipo de Serviço')
plt.tight_layout()
plt.savefig('grafico_comparativo.png')
plt.show()

print("✅ Todos os gráficos foram gerados com sucesso!")


#bibliotecas utilizadas
'''
pandas

matplotlib

wordcloud

random

os

'''