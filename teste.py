# code
import numpy

A_n2 = numpy.array(numpy.ones((1000000, 1)), float)
A_max = 0
A_min = 10000000

A_min_base = input("Digite a altura mínima do terreno em metros: ")
print("\n Altura mínima selecionada para", A_min_base, "m\n")
print("---------------------------------------------\n")

e = "0"
m = "0"
i = 0

while e == "0":
    A_n = input("Digite a altura a ser corrigida: ")
    A_n = round(float(A_n), 2)
    A_n2_atual = A_n - float(A_min_base)
    print(
        "\n Altura deve ser corrigida de",
        A_n,
        "m para",
        round(float(A_n2_atual), 2),
        "m\n",
    )

    A_n2[i] = A_n2_atual
    i += 1
    if ((i > 0) and (A_max < A_n2_atual)):
        A_max = A_n2_atual
    if ((i > 0) and (A_min > A_n2_atual)):
        A_min = A_n2_atual

    print("---------------------------------------------\n")
    e = input("Deseja ajustrar outra medida? 0(Sim) 1(Não): ")
    print("---------------------------------------------\n")

else:
    m = input(
        "Deseja saber a media das alturas máxima e mínima do terreno? 0(Sim) 1(Não): "
    )
    if m == "0":
        A_med = 0.5 * (A_max)
        print("A altura média do terreno é:", round(A_med, 2))
        print("---------------------------------------------\n")
    m = input("Digite 0 para sair")
    if m == "0":
        print("---------------------------------------------\n")
