#
#-----------------------------------------------------------------------------------------------

# Código para geração da curva de carga e curva de duração de carga - Geração de Energia Elétrica
# 22/08/2025

#-----------------------------------------------------------------------------------------------
#

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Carrega os dados do arquivo CSV
try:
    df = pd.read_csv('./perfis_de_carga.csv')
except FileNotFoundError:
    print("Arquivo 'perfis_de_carga.csv' não encontrado. Certifique-se de que o arquivo está no mesmo diretório.")
    exit()

# Calcula a carga total (soma dos consumidores A e B)
df['Carga Total (kW)'] = df['Consumidor A (kW)'] + df['Consumidor B (kW)']

# Configura o gráfico
plt.figure(figsize=(12, 7))

# Plota as curvas de carga
plt.plot(df['Hora'], df['Consumidor A (kW)'], label='Consumidor A', color='blue')
plt.plot(df['Hora'], df['Consumidor B (kW)'], label='Consumidor B', color='red')
plt.plot(df['Hora'], df['Carga Total (kW)'], label='Carga Total', color='green', linewidth=2.5, linestyle='--')

# Adiciona títulos e legendas
plt.title('Curvas de Carga Diária e Fator de Diversidade')
plt.xlabel('Hora do Dia')
plt.ylabel('Demanda (kW)')
plt.legend()
plt.grid(True)
plt.xticks(range(0, 25, 2))  # Define os marcadores do eixo x para melhor visualização
plt.margins(x=0)

# Mostra o gráfico
plt.show()

# Salva o gráfico em um arquivo de imagem
plt.savefig('fig_fator_diversidade_gerado.png')

# Configura o gráfico
plt.figure(figsize=(12, 7))

# Plota a curva de carga do Consumidor A
plt.plot(df['Hora'], df['Consumidor A (kW)'], label='Consumidor A', color='blue', marker='o')

# Adiciona títulos e legendas
plt.title('Curva de Carga Diária - Consumidor A')
plt.xlabel('Hora do Dia')
plt.ylabel('Demanda (kW)')
plt.legend()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.xticks(range(0, 25, 2)) # Melhora a visualização do eixo das horas
plt.margins(x=0) # Remove as margens brancas nas extremidades do eixo x

# Mostra o gráfico
plt.show()

# Salva o gráfico em um arquivo de imagem
plt.savefig('curva_carga_consumidor_a.png')

# Extrai os dados de carga do Consumidor A e ordena em ordem decrescente
carga_consumidor_a = df['Consumidor A (kW)'].sort_values(ascending=False).reset_index(drop=True)

# Cria o eixo de duração (em horas)
duracao_horas = np.arange(1, 25)

# Configura o gráfico
plt.figure(figsize=(12, 7))

# Plota a Curva de Duração de Carga
plt.plot(duracao_horas, carga_consumidor_a, label='Consumidor A', color='purple', marker='o')

# Adiciona títulos e legendas
plt.title('Curva de Duração de Carga (CDC) - Consumidor A')
plt.xlabel('Duração (Horas)')
plt.ylabel('Demanda (kW)')
plt.legend()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.xticks(range(1, 25)) # Define os marcadores do eixo x para cada hora
plt.margins(x=0)

# Mostra o gráfico
plt.show()

# Salva o gráfico em um arquivo de imagem
plt.savefig('cdc_consumidor_a.png')