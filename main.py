import numpy as np
from skfuzzy import control as ctrl, trimf

# Definindo as variáveis de entrada e saída
direcao_norte = ctrl.Antecedent(np.arange(0, 201, 1), 'direcao_norte')
direcao_sul = ctrl.Antecedent(np.arange(0, 201, 1), 'direcao_sul')
tempo_verde = ctrl.Consequent(np.arange(0, 101, 1), 'tempo_verde')

# Funções de pertinência para direcao_norte
direcao_norte['muito_baixo'] = trimf(direcao_norte.universe, [1, 10, 20])
direcao_norte['baixo'] = trimf(direcao_norte.universe, [15, 35, 50])
direcao_norte['medio'] = trimf(direcao_norte.universe, [40, 70, 90])
direcao_norte['alto'] = trimf(direcao_norte.universe, [80, 115, 140])
direcao_norte['muito_alto'] = trimf(direcao_norte.universe, [135, 165, 200])

# Funções de pertinência para direcao_sul
direcao_sul['muito_baixo'] = trimf(direcao_sul.universe, [1, 10, 20])
direcao_sul['baixo'] = trimf(direcao_sul.universe, [15, 35, 50])
direcao_sul['medio'] = trimf(direcao_sul.universe, [40, 70, 90])
direcao_sul['alto'] = trimf(direcao_sul.universe, [80, 115, 140])
direcao_sul['muito_alto'] = trimf(direcao_sul.universe, [135, 165, 200])

# Funções de pertinência para tempo_verde
tempo_verde['curto'] = trimf(tempo_verde.universe, [10, 18, 40])
tempo_verde['medio'] = trimf(tempo_verde.universe, [35, 50, 60])
tempo_verde['longo'] = trimf(tempo_verde.universe, [55, 70, 85])
tempo_verde['muito_longo'] = trimf(tempo_verde.universe, [75, 88, 100])

# Definindo as regras fuzzy
regras = [
    ctrl.Rule(direcao_norte['muito_baixo'] & direcao_sul['muito_baixo'], tempo_verde['curto']),
    ctrl.Rule(direcao_norte['muito_baixo'] & direcao_sul['baixo'], tempo_verde['curto']),
    ctrl.Rule(direcao_norte['muito_baixo'] & direcao_sul['medio'], tempo_verde['curto']),
    ctrl.Rule(direcao_norte['muito_baixo'] & direcao_sul['alto'], tempo_verde['medio']),
    ctrl.Rule(direcao_norte['muito_baixo'] & direcao_sul['alto'], tempo_verde['medio']),

    ctrl.Rule(direcao_norte['baixo'] & direcao_sul['muito_baixo'], tempo_verde['curto']),
    ctrl.Rule(direcao_norte['baixo'] & direcao_sul['baixo'], tempo_verde['curto']),
    ctrl.Rule(direcao_norte['baixo'] & direcao_sul['medio'], tempo_verde['medio']),
    ctrl.Rule(direcao_norte['baixo'] & direcao_sul['alto'], tempo_verde['medio']),
    ctrl.Rule(direcao_norte['baixo'] & direcao_sul['muito_alto'], tempo_verde['longo']),

    ctrl.Rule(direcao_norte['medio'] & direcao_sul['muito_baixo'], tempo_verde['curto']),
    ctrl.Rule(direcao_norte['medio'] & direcao_sul['baixo'], tempo_verde['curto']),
    ctrl.Rule(direcao_norte['medio'] & direcao_sul['medio'], tempo_verde['medio']),
    ctrl.Rule(direcao_norte['medio'] & direcao_sul['alto'], tempo_verde['longo']),
    ctrl.Rule(direcao_norte['medio'] & direcao_sul['muito_alto'], tempo_verde['longo']),

    ctrl.Rule(direcao_norte['alto'] & direcao_sul['muito_baixo'], tempo_verde['medio']),
    ctrl.Rule(direcao_norte['alto'] & direcao_sul['baixo'], tempo_verde['medio']),
    ctrl.Rule(direcao_norte['alto'] & direcao_sul['medio'], tempo_verde['longo']),
    ctrl.Rule(direcao_norte['alto'] & direcao_sul['alto'], tempo_verde['longo']),
    ctrl.Rule(direcao_norte['alto'] & direcao_sul['muito_alto'], tempo_verde['muito_longo']),

    ctrl.Rule(direcao_norte['muito_alto'] & direcao_sul['muito_baixo'], tempo_verde['medio']),
    ctrl.Rule(direcao_norte['muito_alto'] & direcao_sul['baixo'], tempo_verde['longo']),
    ctrl.Rule(direcao_norte['muito_alto'] & direcao_sul['medio'], tempo_verde['longo']),
    ctrl.Rule(direcao_norte['muito_alto'] & direcao_sul['alto'], tempo_verde['muito_longo']),
    ctrl.Rule(direcao_norte['muito_alto'] & direcao_sul['muito_alto'], tempo_verde['muito_longo']),
]

# Criando o sistema de controle
sistema_controle = ctrl.ControlSystem(regras)
simulador = ctrl.ControlSystemSimulation(sistema_controle)

# Função para simular o tempo do sinal verde
def calcular_tempo_verde(direcao_norte_valor, direcao_sul_valor):
    simulador.input['direcao_norte'] = direcao_norte_valor
    simulador.input['direcao_sul'] = direcao_sul_valor

    simulador.compute()
    return simulador.output['tempo_verde']

# Exemplo de simulação
direcao_norte = 140
direcao_sul =  50

tempo_verde_calculado = calcular_tempo_verde(direcao_norte, direcao_sul)
print(f"Tempo do sinal verde para a via principal: {tempo_verde_calculado:.2f} segundos")
