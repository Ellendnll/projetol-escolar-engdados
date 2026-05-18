import pandas as pd
from sqlalchemy import create_engine

# =========================================
# CONEXÃO POSTGRESQL
# =========================================

usuario = "postgres"
senha = "123456"  # <-- SE MUDOU A SENHA NA INSTALAÇÃO, ALTERE AQUI!
host = "localhost"
porta = "5432"
banco = "escola"

# Cria a ponte de conexão com o banco de dados
engine = create_engine(
    f"postgresql://{usuario}:{senha}@{host}:{porta}/{banco}"
)

print("Conexão realizada com sucesso!")

# =========================================
# 1. ALUNOS MÉTRICAS
# =========================================
print("Lendo alunos_metricas.csv...")
df_alunos = pd.read_csv("output/alunos_metricas.csv")

# Envia para o banco de dados criando a tabela
df_alunos.to_sql(
    "alunos_metricas",
    engine,
    if_exists="replace",
    index=False
)
print("Tabela alunos_metricas enviada com sucesso!")

# =========================================
# 2. MATÉRIAS MÉTRICAS
# =========================================
print("Lendo materias_metricas.csv...")
df_materias = pd.read_csv("output/materias_metricas.csv")

# Envia para o banco de dados criando a tabela
df_materias.to_sql(
    "materias_metricas",
    engine,
    if_exists="replace",
    index=False
)
print("Tabela materias_metricas enviada com sucesso!")

# =========================================
# 3. INDICADORES FINAIS
# =========================================
print("Lendo indicadores_finais.csv...")
df_indicadores = pd.read_csv("output/indicadores_finais.csv")

# Envia para o banco de dados criando a tabela
df_indicadores.to_sql(
    "indicadores_finais",
    engine,
    if_exists="replace",
    index=False
)
print("Tabela indicadores_finais enviada com sucesso!")

print("\n--- SUCESSO TOTAL! ---")
print("Todos os dados foram enviados para o PostgreSQL com sucesso!")