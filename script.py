import pandas as pd
import json
import uuid
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

print("🔄 Carregando dados de treino...")

# Suponha que você já tenha um DataFrame chamado df_treino
df_treino = pd.read_csv('dados_treino.csv')  # exemplo, se necessário

# Lê os dados do JSON
print("📂 Lendo dados do JSON externo...")
with open('dados_usuarios.json', 'r', encoding='utf-8') as f:
    novos_dados = json.load(f)
df_novos = pd.DataFrame(novos_dados)

# Adiciona um ID único para rastreamento
df_novos['prediction_id'] = [str(uuid.uuid4()) for _ in range(len(df_novos))]

# Prepara os encoders
print("📊 Realizando encoding robusto para 'location' e 'last_action'...")
df_temp = pd.concat([df_treino.drop(columns='label'), df_novos], ignore_index=True)

le_action = LabelEncoder()
le_location = LabelEncoder()

le_action.fit(df_temp['last_action'])
le_location.fit(df_temp['location'])

df_treino['last_action'] = le_action.transform(df_treino['last_action'])
df_treino['location'] = le_location.transform(df_treino['location'])
df_novos['last_action'] = le_action.transform(df_novos['last_action'])
df_novos['location'] = le_location.transform(df_novos['location'])

# Prepara os dados para treino
X = df_treino[['view_time_seconds', 'in_cart', 'cart_time_minutes', 'last_action', 'location']]
y = df_treino['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

print("🤖 Treinando modelo RandomForest...")
model = RandomForestClassifier()
model.fit(X_train, y_train)
joblib.dump(model, 'modelo_compra.pkl')

# Faz previsões com os novos dados
print("🧠 Fazendo previsões com novos dados...")
X_novos = df_novos[['view_time_seconds', 'in_cart', 'cart_time_minutes', 'last_action', 'location']]
df_novos['probabilidade'] = model.predict_proba(X_novos)[:, 1]

# Define threshold de ação logística
threshold = 0.85
df_novos['compra_provavel'] = (df_novos['probabilidade'] > threshold).astype(int)

# Traduções mais legíveis
df_novos['decisao'] = df_novos['compra_provavel'].map({1: 'Compraria', 0: 'Não compraria'})
df_novos['probabilidade (%)'] = (df_novos['probabilidade'] * 100).map(lambda x: f"{x:.2f}%")

# 🔄 Lógica de ações logísticas
def acao_logistica(prob, in_cart):
    if prob > 0.95 and in_cart == 1:
        return 'Enviar imediatamente'
    elif prob > 0.85:
        return 'Pré-reservar em hub'
    else:
        return 'Aguardar'

df_novos['acao_logistica'] = df_novos.apply(lambda row: acao_logistica(row['probabilidade'], row['in_cart']), axis=1)

# 🔄 Mapeamento fictício de localização para centro logístico
mapa_hubs = {
    0: "Centro SP",
    1: "Centro RJ",
    2: "Centro MG",
    3: "Centro Sul",
    4: "Centro Norte",
}
df_novos['hub_destino'] = df_novos['location'].map(mapa_hubs)

# 🔄 Nível de prioridade
def prioridade(row):
    if row['probabilidade'] > 0.95 and row['in_cart'] == 1:
        return 'Alta'
    elif row['probabilidade'] > 0.85:
        return 'Média'
    else:
        return 'Baixa'

df_novos['prioridade_envio'] = df_novos.apply(prioridade, axis=1)

# 📁 Exporta resultado principal
saida_csv = 'resultados_predicoes.csv'
colunas_exportar = [
    'prediction_id',
    'item_id',
    'item_name',
    'decisao',
    'probabilidade (%)',
    'acao_logistica',
    'prioridade_envio',
    'hub_destino',
    'view_time_seconds',
    'in_cart',
    'cart_time_minutes',
    'last_action',
    'location'
]
df_novos[colunas_exportar].to_csv(saida_csv, index=False, sep=';', encoding='utf-8-sig')
print("✅ Arquivo CSV salvo com previsões!")

# 📦 Exporta apenas as ações logísticas reais
df_logistica = df_novos[df_novos['acao_logistica'] != 'Aguardar']
df_logistica.to_csv('acoes_logisticas.csv', index=False, sep=';', encoding='utf-8-sig')
print("🚚 Arquivo CSV com ações logísticas salvo!")
