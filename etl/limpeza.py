from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    trim,
    upper
)
from pyspark.sql.types import (
    FloatType,
    IntegerType
)

import os


# =========================================
# CONFIGURAÇÃO HADOOP
# =========================================

os.environ["HADOOP_HOME"] = "C:\\hadoop"
os.environ["hadoop.home.dir"] = "C:\\hadoop"


# =========================================
# INICIAR SPARK SESSION
# =========================================

spark = (
    SparkSession.builder
    .appName("ETL Escolar - Limpeza de Dados")

    # DESATIVA IO NATIVO DO WINDOWS
    .config("spark.hadoop.io.native.lib.available", "false")

    .getOrCreate()
)

print("\n=========================================")
print("SPARK INICIADO COM SUCESSO")
print("=========================================")


# =========================================
# LEITURA DO CSV
# =========================================

print("\n[ETAPA 1] LENDO ARQUIVO CSV...")

df = spark.read.csv(
    "data/dados_escolares.csv",
    header=True,
    inferSchema=True,
    encoding="UTF-8"
)

print("Arquivo carregado com sucesso.")


# =========================================
# EXIBIR COLUNAS ORIGINAIS
# =========================================

print("\nCOLUNAS ORIGINAIS:")
print(df.columns)


# =========================================
# PADRONIZAÇÃO DOS NOMES DAS COLUNAS
# =========================================

print("\n[ETAPA 2] PADRONIZANDO COLUNAS...")

df = (
    df.withColumnRenamed("ID Aluno", "id_aluno")
      .withColumnRenamed("Nome", "nome")
      .withColumnRenamed("Turma", "turma")
      .withColumnRenamed("Matéria", "materia")
      .withColumnRenamed("Nota AV1", "nota1")
      .withColumnRenamed("Nota AV2", "nota2")
      .withColumnRenamed("Frequência", "frequencia")
)

print("Colunas padronizadas com sucesso.")


# =========================================
# EXIBIR NOVAS COLUNAS
# =========================================

print("\nCOLUNAS PADRONIZADAS:")
print(df.columns)


# =========================================
# VISUALIZAÇÃO INICIAL
# =========================================

print("\n=========================================")
print("DADOS ORIGINAIS")
print("=========================================")

print(f"Total inicial: {df.count()} registros")


# =========================================
# AJUSTE DOS TIPOS DE DADOS
# =========================================

print("\n[ETAPA 3] AJUSTANDO TIPOS DE DADOS...")

df = (
    df.withColumn("nota1", col("nota1").cast(FloatType()))
      .withColumn("nota2", col("nota2").cast(FloatType()))
      .withColumn("frequencia", col("frequencia").cast(IntegerType()))
)

print("Tipos de dados ajustados.")


# =========================================
# REMOVER DUPLICADOS
# =========================================

print("\n[ETAPA 4] REMOVENDO DUPLICADOS...")

df = df.dropDuplicates()

print("Duplicados removidos.")


# =========================================
# REMOVER VALORES NULOS
# =========================================

print("\n[ETAPA 5] REMOVENDO VALORES NULOS...")

df = df.dropna()

print("Valores nulos removidos.")


# =========================================
# REMOVER ESPAÇOS EXTRAS
# =========================================

print("\n[ETAPA 6] REMOVENDO ESPAÇOS EXTRAS...")

df = (
    df.withColumn("nome", trim(col("nome")))
      .withColumn("turma", trim(col("turma")))
      .withColumn("materia", trim(col("materia")))
)

print("Espaços extras removidos.")


# =========================================
# PADRONIZAÇÃO DE TEXTO
# =========================================

print("\n[ETAPA 7] PADRONIZANDO TEXTO...")

df = (
    df.withColumn("nome", upper(col("nome")))
      .withColumn("materia", upper(col("materia")))
)

print("Texto padronizado.")


# =========================================
# REMOVER NOTAS INVÁLIDAS
# =========================================

print("\n[ETAPA 8] VALIDANDO NOTAS...")

df = df.filter(
    (col("nota1").isNotNull()) &
    (col("nota2").isNotNull()) &
    (col("nota1") >= 0) &
    (col("nota1") <= 10) &
    (col("nota2") >= 0) &
    (col("nota2") <= 10)
)

print("Notas inválidas removidas.")


# =========================================
# REMOVER FREQUÊNCIAS INVÁLIDAS
# =========================================

print("\n[ETAPA 9] VALIDANDO FREQUÊNCIAS...")

df = df.filter(
    (col("frequencia").isNotNull()) &
    (col("frequencia") >= 0) &
    (col("frequencia") <= 100)
)

print("Frequências inválidas removidas.")


# =========================================
# EXIBIR DADOS LIMPOS
# =========================================

print("\n=========================================")
print("DADOS LIMPOS")
print("=========================================")

df.show(10, truncate=False)


# =========================================
# SCHEMA FINAL
# =========================================

print("\n=========================================")
print("SCHEMA FINAL")
print("=========================================")

df.printSchema()


# =========================================
# RESULTADO FINAL
# =========================================

print("\n=========================================")
print("RESULTADO FINAL")
print("=========================================")

print(f"Total após limpeza: {df.count()} registros")


# =========================================
# CRIAR PASTA OUTPUT
# =========================================

os.makedirs("output", exist_ok=True)


# =========================================
# SALVAR DADOS LIMPOS
# =========================================

print("\n[ETAPA 10] SALVANDO DADOS LIMPOS...")

df.coalesce(1).toPandas().to_csv(
    "output/dados_escolares_limpos.csv",
    index=False
)

print("Dados limpos salvos com sucesso.")


# =========================================
# FINALIZAR SPARK
# =========================================

print("\n=========================================")
print("ETL FINALIZADA COM SUCESSO")
print("=========================================")

spark.stop()
