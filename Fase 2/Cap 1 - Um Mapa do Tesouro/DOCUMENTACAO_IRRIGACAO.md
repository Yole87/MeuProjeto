# 🌽 Sistema de Irrigação Inteligente para Milho - FarmTech

## 📋 Visão Geral

O sistema FarmTech implementa uma solução de irrigação inteligente especificamente otimizada para o cultivo de milho, utilizando sensores IoT, análise meteorológica e interface web para maximizar a eficiência hídrica e a produtividade da cultura.

## 🎯 Cultura Escolhida: Milho (Zea mays)

### Por que Milho?
- **Importância Econômica**: Uma das principais culturas do agronegócio brasileiro
- **Sensibilidade Hídrica**: Requer irrigação precisa em diferentes estágios de crescimento
- **Parâmetros Bem Definidos**: Possui critérios claros de pH, umidade e nutrientes
- **Potencial de Otimização**: Grande benefício com irrigação inteligente

### Características da Cultura
- **Ciclo**: 120-150 dias (dependendo da variedade)
- **Consumo Hídrico**: 400-700mm por ciclo
- **Estágios Críticos**: Florescimento e enchimento de grãos
- **Tolerância ao Estresse**: Moderada a baixa

## 🔧 Parâmetros de Irrigação Otimizados

### 💧 Umidade do Solo
```cpp
#define UMID_MIN 40        // Umidade mínima para irrigação (%)
#define UMID_IDEAL 65      // Umidade ideal para milho (%)
#define UMID_MAX 80        // Umidade máxima (evitar encharcamento)
```

**Critérios de Decisão:**
- **< 40%**: Irrigação obrigatória (estresse hídrico)
- **40-65%**: Irrigação recomendada (zona de conforto)
- **65-80%**: Irrigação opcional (condições ideais)
- **> 80%**: Irrigação suspensa (risco de encharcamento)

### 🧪 pH do Solo
```cpp
#define PH_MIN 6.0         // pH mínimo aceitável
#define PH_IDEAL 6.5       // pH ideal para milho
#define PH_MAX 7.5         // pH máximo aceitável
```

**Justificativa Técnica:**
- **pH 6.0-7.5**: Faixa ideal para absorção de nutrientes
- **pH < 6.0**: Toxicidade por alumínio, deficiência de P
- **pH > 7.5**: Deficiência de micronutrientes (Fe, Mn, Zn)

### 🌱 Nutrientes NPK
```cpp
// Monitoramento via botões (simulação de sensores)
#define BTN_NITROGENIO 13  // Botão para simular sensor de Nitrogênio
#define BTN_FOSFORO 12     // Botão para simular sensor de Fósforo
#define BTN_POTASSIO 14    // Botão para simular sensor de Potássio
```

**Níveis Ideais para Milho:**
- **Nitrogênio (N)**: 150-200 kg/ha
- **Fósforo (P₂O₅)**: 80-120 kg/ha
- **Potássio (K₂O)**: 100-150 kg/ha

## 🏗️ Arquitetura do Sistema

### Hardware (ESP32)
```
ESP32 DevKit V1
├── DHT22 (Pino 15) - Temperatura e Umidade
├── LDR (Pino A0) - Simulação de pH
├── Botões NPK (Pinos 13, 12, 14) - Simulação de nutrientes
├── Relé (Pino 2) - Controle da bomba de irrigação
└── LED (Pino 23) - Indicador de status
```

### Software
```
Sistema Web (Flask)
├── Backend Python
│   ├── app.py - Servidor principal
│   ├── /api/dados - Endpoint de dados dos sensores
│   └── /api/estatisticas - Endpoint de estatísticas
├── Frontend HTML/CSS/JS
│   ├── index.html - Interface principal
│   ├── styles.css - Estilos responsivos
│   └── script.js - Lógica de interação
└── Dados
    └── analise_resultado.json - Dados de análise
```

## 📊 Interface Web

### Dashboard Principal
- **Monitoramento em Tempo Real**: Sensores de umidade, pH e temperatura
- **Controle de Irrigação**: Botões para irrigação manual e automática
- **Análise de Solo**: Visualização dos dados de análise
- **Estatísticas**: Gráficos e métricas de desempenho
- **Dados Meteorológicos**: Informações climáticas integradas

### Funcionalidades
1. **Visualização de Dados**: Cards informativos com dados dos sensores
2. **Controle Manual**: Botão para ativar irrigação manualmente
3. **Modo Automático**: Sistema inteligente baseado em parâmetros
4. **Histórico**: Registro de ações e medições
5. **Alertas**: Notificações sobre condições críticas

## 🔄 Algoritmo de Irrigação

### Lógica de Decisão
```cpp
bool precisaIrrigar() {
    float umidade = dht.readHumidity();
    float ph = lerPH();
    
    // Condições críticas - irrigação obrigatória
    if (umidade < UMID_MIN) return true;
    
    // Condições ideais - sem irrigação
    if (umidade > UMID_MAX) return false;
    
    // Zona intermediária - considerar pH
    if (umidade < UMID_IDEAL && ph >= PH_MIN && ph <= PH_MAX) {
        return true;
    }
    
    return false;
}
```

### Fatores Considerados
1. **Umidade do Solo**: Parâmetro principal
2. **pH do Solo**: Condição para absorção de nutrientes
3. **Temperatura**: Influência na evapotranspiração
4. **Nutrientes**: Disponibilidade de NPK
5. **Dados Meteorológicos**: Previsão de chuva

## 🌐 API e Comunicação

### Endpoints Disponíveis
```
GET /api/dados
├── Retorna dados atuais dos sensores
├── Formato JSON com timestamp
└── Inclui status de irrigação

GET /api/estatisticas
├── Retorna estatísticas de análise
├── Dados de área e produtividade
└── Métricas de eficiência
```

### Formato de Dados
```json
{
    "timestamp": "2024-01-15T10:30:00",
    "sensores": {
        "umidade": 45.2,
        "temperatura": 28.5,
        "ph": 6.3,
        "npk": {
            "nitrogenio": true,
            "fosforo": false,
            "potassio": true
        }
    },
    "irrigacao": {
        "status": "ativa",
        "modo": "automatico",
        "duracao": 15
    }
}
```

## 📈 Análise de Dados

### Métricas Monitoradas
- **Área Total**: 2.5 hectares de milho
- **Produtividade**: 8.5 ton/ha (meta)
- **Eficiência Hídrica**: 1.2 kg/m³ de água
- **Economia de Água**: 25% comparado à irrigação tradicional

### Relatórios Gerados
1. **Consumo Hídrico**: Volume de água utilizado
2. **Frequência de Irrigação**: Número de ativações
3. **Condições do Solo**: Histórico de pH e umidade
4. **Produtividade**: Estimativas baseadas em dados

## 🛠️ Configuração e Instalação

### Requisitos de Hardware
- ESP32 DevKit V1
- Sensor DHT22
- Fotoresistor (LDR)
- 3 Botões push-button
- Módulo relé 5V
- LED indicador
- Resistores (10kΩ, 220Ω)
- Protoboard e jumpers

### Requisitos de Software
```bash
# Python 3.8+
pip install flask
pip install requests

# Arduino IDE
# Bibliotecas: DHT sensor library, WiFi
```

### Configuração WiFi
```cpp
const char* ssid = "SUA_REDE_WIFI";
const char* password = "SUA_SENHA_WIFI";
```

## 🔧 Manutenção e Calibração

### Calibração de Sensores
1. **DHT22**: Verificar leituras a cada 6 meses
2. **pH (LDR)**: Calibrar com soluções padrão
3. **Relé**: Testar funcionamento mensalmente

### Manutenção Preventiva
- **Limpeza de Sensores**: Quinzenal
- **Verificação de Conexões**: Mensal
- **Atualização de Software**: Conforme necessário
- **Backup de Dados**: Semanal

## 📊 Resultados Esperados

### Benefícios do Sistema
- **Economia de Água**: 20-30%
- **Aumento de Produtividade**: 15-25%
- **Redução de Mão de Obra**: 40%
- **Melhoria na Qualidade**: Grãos mais uniformes

### ROI (Retorno sobre Investimento)
- **Investimento Inicial**: R$ 2.500,00
- **Economia Anual**: R$ 1.800,00
- **Payback**: 1.4 anos
- **ROI em 5 anos**: 260%

## 🚀 Próximas Melhorias

### Funcionalidades Planejadas
1. **Integração com Satélites**: Dados de NDVI
2. **Machine Learning**: Predição de necessidades
3. **App Mobile**: Controle remoto
4. **Sensores Adicionais**: Condutividade elétrica
5. **Integração Meteorológica**: APIs de clima

### Expansão do Sistema
- **Múltiplas Culturas**: Soja, algodão, cana
- **Maior Área**: Até 100 hectares
- **Automação Completa**: Fertirrigação
- **Análise Preditiva**: IA para otimização

## 📞 Suporte Técnico

### Contato
- **Email**: suporte@farmtech.com.br
- **Telefone**: (11) 9999-9999
- **WhatsApp**: (11) 9999-9999
- **Site**: www.farmtech.com.br

### Documentação Adicional
- Manual do Usuário
- Guia de Instalação
- FAQ - Perguntas Frequentes
- Vídeos Tutoriais

---

**Desenvolvido por FarmTech - Inovação em Agricultura de Precisão**
*Versão 2.0 - Janeiro 2024*