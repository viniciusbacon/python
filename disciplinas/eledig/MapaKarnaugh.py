import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 1. Definição das variáveis do problema
variables = ['T', 'M', 'E', 'P']

# 2. Geração da Tabela-Verdade para AC = (T ou M) e (não P) ou E
truth_table_list = []
for t in [0, 1]:
    for m in [0, 1]:
        for e in [0, 1]:
            for p in [0, 1]:
                ac_output = ((t or m) and (not p)) or e
                truth_table_list.append(str(int(ac_output)))
truth_table_string = "".join(truth_table_list)

print(f"Variáveis (MSB para LSB): {variables}")
print(f"String da Tabela-Verdade gerada: {truth_table_string}")

# 3. Mapeamento da Tabela-Verdade para a estrutura do K-Map (Ordem Gray)
# Ordem binária (índice da lista): 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
# Ordem K-Map (posição na matriz): 0  1  3  2  4  5  7  6 12 13 15 14  8  9 11 10
map_order = [0, 1, 3, 2, 4, 5, 7, 6, 12, 13, 15, 14, 8, 9, 11, 10]
kmap_values = [truth_table_list[i] for i in map_order]
kmap_matrix = [kmap_values[i:i+4] for i in range(0, 16, 4)]

# 4. Geração do Gráfico com Matplotlib
fig, ax = plt.subplots(figsize=(6, 6))

# Esconde os eixos
ax.axis('off')
ax.set_aspect('equal')

# Desenha a grade e preenche com os valores
table = ax.table(cellText=kmap_matrix,
                 rowLabels=['00', '01', '11', '10'],
                 colLabels=['00', '01', '11', '10'],
                 loc='center',
                 cellLoc='center')
table.scale(1, 1.5)
table.set_fontsize(14)

# Adiciona os nomes das variáveis nos eixos
ax.text(-0.25, 0.5, 'TM', va='center', ha='center', fontsize=14, transform=ax.transAxes, rotation='vertical')
ax.text(0.5, 0.9, 'EP', va='center', ha='center', fontsize=14, transform=ax.transAxes)

# 5. Desenha os laços (grupos) que representam a simplificação
# As coordenadas são (coluna, linha) e a origem (0,0) é no canto superior esquerdo
# A largura/altura é em unidades de células (1 célula = 0.25 de largura/altura)

# Grupo para o termo 'E' (colunas EP=11 e EP=10)
# Um retângulo de 2 células de largura e 4 de altura, começando na coluna 2
rect_E = patches.Rectangle((2/4, 0), 2/4, 4/4, linewidth=2, edgecolor='r', facecolor='r', alpha=0.3, transform=ax.transAxes)
ax.add_patch(rect_E)

# Grupo para o termo 'M*P'' (linhas TM=01,11 e colunas EP=00,10 - wrap-around)
# Dois retângulos, um para cada lado do wrap-around
rect_MP_1 = patches.Rectangle((0, 1/4), 1/4, 2/4, linewidth=2, edgecolor='g', facecolor='g', alpha=0.3, transform=ax.transAxes)
rect_MP_2 = patches.Rectangle((3/4, 1/4), 1/4, 2/4, linewidth=2, edgecolor='g', facecolor='g', alpha=0.3, transform=ax.transAxes)
ax.add_patch(rect_MP_1)
ax.add_patch(rect_MP_2)

# Grupo para o termo 'T*P'' (linhas TM=11,10 e colunas EP=00,10 - wrap-around)
rect_TP_1 = patches.Rectangle((0, 2/4), 1/4, 2/4, linewidth=2, edgecolor='b', facecolor='b', alpha=0.3, transform=ax.transAxes)
rect_TP_2 = patches.Rectangle((3/4, 2/4), 1/4, 2/4, linewidth=2, edgecolor='b', facecolor='b', alpha=0.3, transform=ax.transAxes)
ax.add_patch(rect_TP_1)
ax.add_patch(rect_TP_2)

# Adiciona título e a expressão simplificada
plt.title('Mapa de Karnaugh para o Problema do Ar Condicionado', fontsize=16, y=1.08)
simplified_expression = "AC = E + T·P' + M·P'"
plt.figtext(0.5, 0.01, simplified_expression, ha="center", fontsize=14, bbox={"facecolor":"white", "alpha":0.5, "pad":5})

# Salva a imagem
output_filename = 'mapa_karnaugh_ar_condicionado.png'
plt.savefig(output_filename, bbox_inches='tight', dpi=150)

print(f"\nO Mapa de Karnaugh foi gerado com sucesso e salvo como '{output_filename}'")