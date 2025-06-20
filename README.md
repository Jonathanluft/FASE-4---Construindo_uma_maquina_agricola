# Sistema de Sensores e Controle com ESP32

# FIAP - Inteligência artificial e data science

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

## Nome do grupo
25

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/company/inova-fusca">Guilherme Campos Hermanowski </a>
- <a href="https://www.linkedin.com/company/inova-fusca">Gabriel Viel </a>
- <a href="https://www.linkedin.com/company/inova-fusca"> Matheus Alboredo Soares</a> 
- <a href="https://www.linkedin.com/company/inova-fusca">Jonathan Willian Luft </a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/company/inova-fusca">Leonardo Ruiz Orabona</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/company/inova-fusca">ANDRÉ GODOI CHIOVATO</a>


# Projeto de Monitoramento de Solo com ESP32

Este projeto simula a leitura de sensores de **umidade**, **temperatura**, **pH**, **fósforo** e **potássio** em um ambiente de cultivo, utilizando um ESP32. A lógica de controle foi desenvolvida em C++ e pode ser simulada no ambiente Wokwi. Com a adição do LCD podemos observar as atualizações de temperatura, umidade, ph e fosforo.
---

## ⚙️ Componentes e Conexões

- **Sensor Fosforo - Botão Vermelho**:
  - Conexão: pino 23
- **Sensor Potassio - Botão Verde**:  
  - Conexão: pino 22
- **Sensor Ph - Sensor LDR**: 
  - Conexão: 35
  - Responsável por simular a coleta do PH.
- **Sensor Temperatura e Umidade - Sensor DHT22**: 
  - Conexão: 15
  - Responsável por coleta de temperatura e umidade.
- **Sensor Bomba Irrigação - LED (Vermelho e Verde) (Relé simulado)**: 
  - Conexão: pino 2
  - Utilizado como atuador da bomba de irrigação.
- **Display lcd1602**
  - LCD SDA -> PIN 21
  - LCD SCL -> PIN 22
  - LCD VCC -> 5V 


  ![Screenshot_1](https://github.com/user-attachments/assets/d6f58ae6-32e6-4e19-b348-29ee8e9a5210)


---

## 🧠 Lógica de Funcionamento


- **Observações:**
  - Segundo a liberdade e criatividade da lógica de coleta dos sensores, definimos que o para a simulação, o sistema evita logs repetitivos: só gera nova saída quando há mudança no estado dos sensores **LDR (Ph), Botões (Fosforo e Potassio)**.
  - A coleta do sensor de Temperatura e Umidade é mostrado toda vez que há alterações em alguns desses sensores (para não poluir o monitor e também facilitar validação da avaliação.
  - A coleta do sensor do Relé, simulando a bomba de irrigação é feita automaticamente só com a alteração de umidade no sensor DTH22.
  - O valor de pH é tratado com `fabs()` para considerar desvios mínimos.
  - Ao final do Loop com alteração de parametros do sensor LDR ou botão, o log é gerado coletando de todos os sensores (até os que não foram alterados, para gerar carga na cópia para execução do entregável 2) - Simulando uma Trigger para disparo de log / coleta

- O sistema lê os botões de **fósforo** e **potássio**. Quando pressionados, gera valores aleatórios simulando a presença em mol desses nutrientes.
- O valor de **pH** é calculado com base em um valor analógico lido pelo sensor LDR
- O sensor DHT22 fornece leitura de **temperatura** e **umidade**.
- A **bomba de irrigação (LED)** é acionada ou desligada conforme o valor da umidade:
  - **≥ 40%**: bomba desligada (LED Vermelho Ligado)
  - **< 40%**: bomba ligada (LED Verde Ligado)
- Todos os dados são exibidos no monitor serial, com um bloco especialmente formatado para facilitar a cópia e posterior uso em scripts Python.
- Além de serem exibidos no monitor serial, temos o uso do LCD, que também exibe as atualizações dos dados.
---

## 📤 Exemplo de Saída no Serial

```
Presença Fosforo: 68.32
Presença Potassio: 92.14
Ph: 0.22
Temp (°C): 12.7
Humidity (%): 17

============================================ COPIAVEL PARA SCRIPT PYTHON ============================================

log,68.32,92.14,5.89,23.55,35.7

**Sendo (seria a data no projeto real por exemplo), (Fosforo), (Potassio), (Ph), (Temp), (Umidade)

=====================================================================================================================
```
![image](https://github.com/user-attachments/assets/9e3022dd-ff9a-43b7-8d92-0143f319051f)

![Screenshot_2](https://github.com/user-attachments/assets/c44f34e9-e222-4df8-bea1-1b8ee6678ad9)

Ph: 0.24
Temp (°C): 12.7
Humidity (%): 17

**====================== DATA BASE ===============================**
Nosso data base foi inteiramente simulado, porém desta vez foram feitas relações com os sensores.

**==================== 1. pH do Solo =============================**
Efeito no Fósforo (P):
Em solos com pH alto (alcalinos, >7), o fósforo tende a se precipitar com cálcio (Ca), reduzindo sua disponibilidade para as plantas.
Em solos com pH baixo (ácidos, <6), o fósforo torna-se mais solúvel, porém pode ser fixado por alumínio (Al) ou ferro (Fe).

Equação:
Fósforo (mg/kg) = 50.0 - (pH - 5.5) * 5 + ruído 

Efeito no Potássio (K):
Solos ácidos (pH baixo) aumentam a solubilidade do potássio, mas também elevam o risco de lixiviação (perda por água).
Solos alcalinos (pH alto) reduzem a disponibilidade de K devido à competição com íons como Ca²⁺ e Mg²⁺.

Equação:
Potássio (mg/kg) = 300.0 - (pH - 5.5) * 15 - (Umidade - 50) * 0.2 + ruído  

**==================== 2. Temperatura (°C) ==========================**
Relação com a Umidade:
Temperaturas mais altas aceleram a evaporação, reduzindo a umidade do solo.

Equação:
Umidade (%) ≈ 70.0 → 50.0 (quando Temperatura aumenta de 22°C → 28°C)  

**==================== 3. Umidade do Solo (%) ========================**
Impacto no Potássio (K):
Solos com umidade elevada facilitam a lixiviação do potássio (arraste pela água), reduzindo sua concentração.

Termo na equação do Potássio:
- (Umidade - 50) * 0.2

**================== 4. Nutrientes: Fósforo (P) vs. Potássio (K) =====**
Solos com alto teor de P podem inibir a absorção de K (e vice-versa), especialmente em pH extremos.
Quando P > 45 mg/kg, o K geralmente fica abaixo de 270 mg/kg (para pH ~6.0).

**=================== Como as Relações Foram Implementadas ============**
As equações usadas para gerar os dados incorporam:

Variações naturais: Adição de ruído (np.random.normal) para simular flutuações reais.
Tendências lineares: Relações diretas/inversas entre pH, umidade e nutrientes.

**================== Limites realistas: ===============================**
pH entre 5.5 e 7.5 (solos agrícolas típicos).
Potássio entre 200–350 mg/kg (solos férteis).

**=================== BANCO DE DADOS: ==================================**
# FarmTech-Solutions-Data-Base – Modelo Entidade-Relacionamento (MER)

## Visão Geral
Este documento apresenta o modelo entidade-relacionamento (MER) para o banco de dados da fase 2 do projeto FarmTech, 
detalhando entidades, atributos e relacionamentos necessários para suportar o gerenciamento de culturas, áreas de plantio, sensores e coletas de dados ambientais.  
Fonte: Documentação FarmTech (MER) :contentReference[oaicite:0]{index=0}&#8203;:contentReference[oaicite:1]{index=1}

---

## Entidades

### Culturas
- **Chave Primária:** `ID_cultura`  
- **Resumo:** Armazena dados referentes à aquisição de culturas para plantio futuro.  
| Coluna         | Tipo             | Descrição                                             | Obrigatório |
|----------------|------------------|-------------------------------------------------------|-------------|
| `ID_cultura`   | INTEGER          | Código de registro único da cultura adquirida         | Sim         |
| `Nome_cultura` | VARCHAR(50)      | Nome da cultura adquirida (ex.: café, cana, milho…)   | Sim         |
| `Quantidade`   | DECIMAL(10,2)    | Quantidade adquirida da cultura para plantio         | Sim         |
| `Unidade`      | VARCHAR(20)      | Unidade de medida da cultura (grão, Kg, Toneladas)    | Não         |

### Áreas de Plantio
- **Chave Primária:** `ID_area`  
- **Resumo:** Registra as áreas disponíveis e suas dimensões.  
| Coluna      | Tipo             | Descrição                                               | Obrigatório |
|-------------|------------------|---------------------------------------------------------|-------------|
| `ID_area`   | INTEGER          | Código de registro único da área de plantio             | Sim         |
| `Geometria` | VARCHAR(50)      | Formato descritivo da área (Retângulo, Triângulo…)      | Sim         |
| `Base`      | DECIMAL(10,2)    | Valor numérico da base                                  | Sim         |
| `Altura`    | DECIMAL(10,2)    | Valor numérico da altura                                | Sim         |
| `Area`      | DECIMAL(10,2)    | Cálculo da área total dessa local                       | Não         |
| `Unidade`   | VARCHAR(20)      | Unidade das métricas de base e altura (cm, m², …)       | Sim         |

### Cultivos
- **Chave Primária:** `ID_cultivo`  
- **Chaves Estrangeiras:** `ID_area` → Áreas de Plantio, `ID_cultura` → Culturas  
- **Resumo:** Registra quais culturas estão sendo cultivadas em quais áreas e em que quantidade.  
| Coluna               | Tipo             | Descrição                                               | Obrigatório |
|----------------------|------------------|---------------------------------------------------------|-------------|
| `ID_cultivo`         | INTEGER          | Código de registro único do cultivo                     | Sim         |
| `ID_area`            | INTEGER          | Código da área em que está sendo cultivado              | Sim         |
| `ID_cultura`         | INTEGER          | Código da cultura cultivada nessa área                  | Sim         |
| `Quantidade_plantio` | DECIMAL(10,2)    | Quantidade de cultura utilizada para o plantio         | Sim         |
| `Unidade`            | VARCHAR(20)      | Unidade da cultura cultivada (grão, Kg, Toneladas)      | Sim         |

### Quadrantes
- **Chave Primária:** `ID_quadra`  
- **Chaves Estrangeiras:** `ID_area` → Áreas de Plantio, `ID_cultivo` → Cultivos  
- **Resumo:** Divide um cultivo em sub-áreas para maior precisão nas métricas de monitoramento.  
| Coluna             | Tipo             | Descrição                                                     | Obrigatório |
|--------------------|------------------|---------------------------------------------------------------|-------------|
| `ID_quadra`        | INTEGER          | Código de registro único do quadrante                         | Sim         |
| `ID_area`          | INTEGER          | Código da área em que está o quadrante                        | Sim         |
| `ID_cultivo`       | INTEGER          | Código da cultura cultivada nesse quadrante                   | Sim         |
| `Descricao_quadra` | VARCHAR(100)     | Descrição livre do quadrante                                  | Não         |
| `Acesso`           | VARCHAR(100)     | Método de acesso ao quadrante (ex.: pelas ruas X e Y)         | Não         |

### Produtos
- **Chave Primária:** `ID_produto`  
- **Resumo:** Armazena produtos adquiridos para uso no plantio e manutenção.  
| Coluna               | Tipo             | Descrição                                           | Obrigatório |
|----------------------|------------------|-----------------------------------------------------|-------------|
| `ID_produto`         | INTEGER          | Código de registro único do produto                 | Sim         |
| `Nome_produto`       | VARCHAR(100)     | Nome do produto adquirido                           | Sim         |
| `Marca`              | VARCHAR(100)     | Marca do produto                                    | Sim         |
| `Modelo`             | VARCHAR(100)     | Modelo do produto                                   | Sim         |
| `Quantidade`         | INTEGER          | Quantidade adquirida/possuída                       | Sim         |
| `Responsável_Técnico`| VARCHAR(100)     | Responsável técnico pelo produto                    | Sim         |
| `Observação`         | VARCHAR(100)     | Anotações ou observações adicionais                 | Não         |

### Sensores
- **Chave Primária:** `ID_sensor`  
- **Chaves Estrangeiras:** `ID_produto` → Produtos, `ID_area` → Áreas de Plantio, `ID_quadra` → Quadrantes  
- **Resumo:** Controle patrimonial e de manutenção de cada unidade de sensor instalada.  
| Coluna          | Tipo          | Descrição                                                     | Obrigatório |
|-----------------|---------------|---------------------------------------------------------------|-------------|
| `ID_sensor`     | INTEGER       | Código de registro único do sensor                            | Sim         |
| `ID_produto`    | INTEGER       | Código do produto associado ao sensor                         | Sim         |
| `ID_area`       | INTEGER       | Código da área de plantio onde está instalado                 | Sim         |
| `ID_quadra`     | INTEGER       | Código do quadrante onde o sensor está instalado              | Sim         |
| `Dt_aquisicao`  | DATE          | Data e hora de cadastro do sensor                             | Sim         |
| `Dt_manutencao` | DATE          | Data da última manutenção realizada                           | Não         |

### Coletas de Umidade
- **Chave Primária:** `ID_coleta_umidade`  
- **Chaves Estrangeiras:** `ID_sensor`, `ID_cultura`, `ID_area`, `ID_quadra`  
- **Resumo:** Logs de coletas de umidade e temperatura do solo.  
| Coluna       | Tipo             | Descrição                                             | Obrigatório |
|--------------|------------------|-------------------------------------------------------|-------------|
| `ID_coleta_umidade` | INTEGER    | Código de registro único da coleta                   | Sim         |
| `ID_sensor`         | INTEGER    | Sensor responsável pela coleta                       | Sim         |
| `ID_cultura`        | INTEGER    | Cultura relacionada à coleta                         | Sim         |
| `ID_area`           | INTEGER    | Área relacionada à coleta                            | Sim         |
| `ID_quadra`         | INTEGER    | Quadrante relacionado à coleta                       | Sim         |
| `Dt_log`            | DATE       | Data da coleta                                       | Sim         |
| `Tipo_desc`         | VARCHAR(100)| Descrição ou observação                              | Não         |
| `Umidade`           | DECIMAL(10,2)| Umidade do solo coletada                            | Sim         |
| `Temperatura`       | DECIMAL(10,2)| Temperatura do solo coletada                        | Sim         |
| `Unidades`          | VARCHAR(150)| Unidades de medida dos registros                    | Sim         |

### Coletas de pH
- **Chave Primária:** `ID_coleta_ph`  
- **Chaves Estrangeiras:** `ID_sensor`, `ID_cultura`, `ID_area`, `ID_quadra`  
- **Resumo:** Logs de coletas de pH e outras métricas do solo.  
| Coluna         | Tipo             | Descrição                                               | Obrigatório |
|----------------|------------------|---------------------------------------------------------|-------------|
| `ID_coleta_ph` | INTEGER          | Código de registro único da coleta                      | Sim         |
| `ID_sensor`    | INTEGER          | Sensor responsável pela coleta                          | Sim         |
| `ID_cultura`   | INTEGER          | Cultura relacionada à coleta                            | Sim         |
| `ID_area`      | INTEGER          | Área relacionada à coleta                               | Sim         |
| `ID_quadra`    | INTEGER          | Quadrante relacionado à coleta                          | Sim         |
| `Dt_log`       | DATE             | Data da coleta                                          | Sim         |
| `Tipo_desc`    | VARCHAR(100)     | Descrição ou observação                                 | Não         |
| `Ph`           | DECIMAL(10,2)    | Nível de pH registrado                                  | Sim         |
| `Temperatura`  | DECIMAL(10,2)    | Temperatura no momento da coleta                        | Sim         |
| `NTU`          | DECIMAL(10,2)    | Métrica de turbidez (NTU)                               | Sim         |
| `Condutividade`| DECIMAL(10,2)    | Condutividade elétrica registrada                       | Sim         |
| `Unidades`     | VARCHAR(150)     | Unidades de medida dos registros                       | Sim         |

### Coletas de NPK
- **Chave Primária:** `ID_coleta_nutriente`  
- **Chaves Estrangeiras:** `ID_sensor`, `ID_cultura`, `ID_area`, `ID_quadra`  
- **Resumo:** Logs de coletas de elementos químicos (N, P, K) do solo.  
| Coluna                 | Tipo             | Descrição                                                  | Obrigatório |
|------------------------|------------------|------------------------------------------------------------|-------------|
| `ID_coleta_nutriente`  | INTEGER          | Código de registro único da coleta                        | Sim         |
| `ID_sensor`            | INTEGER          | Sensor responsável pela coleta                            | Sim         |
| `ID_cultura`           | INTEGER          | Cultura relacionada à coleta                              | Sim         |
| `ID_area`              | INTEGER          | Área relacionada à coleta                                 | Sim         |
| `ID_quadra`            | INTEGER          | Quadrante relacionado à coleta                            | Sim         |
| `Dt_log`               | DATE             | Data da coleta                                            | Sim         |
| `Tipo_desc`            | VARCHAR(100)     | Descrição ou observação                                   | Não         |
| `Nitrogenio`           | DECIMAL(10,2)    | Nível de nitrogênio registrado                            | Sim         |
| `Fosforo`              | DECIMAL(10,2)    | Nível de fósforo registrado                               | Sim         |
| `Potassio`             | DECIMAL(10,2)    | Nível de potássio registrado                              | Sim         |
| `Unidades`             | VARCHAR(150)     | Unidades de medida dos registros                          | Sim         |

---

## Relacionamentos

| Entidades Envolvidas      | Relacionamento     | Cardinalidade    | Descrição                                                                        |
|---------------------------|--------------------|------------------|----------------------------------------------------------------------------------|
| Culturas → Cultivos       | Cultiva            | 1:0..N           | Uma cultura pode ser cultivada várias vezes. Cada cultivo deve referenciar uma cultura.          |
| Áreas_plantio → Cultivos  | Ocupa              | 1:0..N           | Uma área de plantio pode conter diversos cultivos ao longo do tempo.                              |
| Cultivos → Quadrantes     | Pertence           | 1:1..N           | Um cultivo pode ser dividido em vários quadrantes.                                               |
| Áreas_plantio → Quadrantes| Contém             | 1:1..N           | Todo quadrante deve estar em uma área. Uma área possui um ou mais quadrantes.                   |
| Produtos → Sensores       | Pode conter        | 1:0..N           | Um produto pode ter vários sensores associados.                                                    |
| Áreas_plantio → Sensores  | Está alocado       | 1:0..N           | Sensores precisam estar em uma área, mas uma área não precisa ter sensores.                       |
| Quadrantes → Sensores     | Posicionado em     | 0..1:0..N        | Sensores podem ou não estar posicionados em um quadrante.                                         |
| Sensores → Umidade_coleta | Coleta_umidade     | 1:0..N           | Um sensor pode gerar várias coletas de umidade.                                                  |
| Sensores → PH_coleta      | Coleta_pH         | 1:0..N           | Um sensor pode gerar várias coletas de pH.                                                         |
| Sensores → NPK_coleta     | Coleta_nutriente  | 1:0..N           | Um sensor pode gerar várias coletas de NPK.                                                        |
# FarmTech-Solutions-Data-Base


## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
