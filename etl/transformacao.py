"""
Integrante 3 - Transformação dos Dados Escolares
Responsável por calcular indicadores e aplicar regras de negócio
"""

import pandas as pd
import os

class TransformacaoDados:
    """
    Transforma dados limpos em indicadores analíticos
    """
    
    def __init__(self):
        self.input_file = 'output/dados_escolares_limpos.csv'
        self.output_dir = 'output'
        
    def carregar_dados(self):
        """Carrega os dados limpos do Integrante 2"""
        print("📂 Carregando dados limpos...")
        df = pd.read_csv(self.input_file)
        print(f"✅ {len(df)} registros carregados")
        print(f"Colunas: {list(df.columns)}")
        return df
    
    def calcular_media_aluno(self, df):
        """Calcula média por aluno e status"""
        print("\n📊 Calculando métricas por aluno...")
        
        df['media_materia'] = (df['nota1'] + df['nota2']) / 2
        
        aluno_metrics = df.groupby(['id_aluno', 'nome', 'turma']).agg({
            'media_materia': 'mean',
            'frequencia': 'mean'
        }).round(2)
        
        aluno_metrics.columns = ['media_geral', 'frequencia_media']
        aluno_metrics = aluno_metrics.reset_index()
        
        aluno_metrics['status'] = aluno_metrics['media_geral'].apply(
            lambda x: 'Aprovado' if x >= 7 else ('Recuperação' if x >= 5 else 'Reprovado')
        )
        
        print("✅ Métricas por aluno calculadas")
        print(f"Alunos aprovados: {len(aluno_metrics[aluno_metrics['status'] == 'Aprovado'])}")
        print(f"Alunos em recuperação: {len(aluno_metrics[aluno_metrics['status'] == 'Recuperação'])}")
        print(f"Alunos reprovados: {len(aluno_metrics[aluno_metrics['status'] == 'Reprovado'])}")
        
        return aluno_metrics
    
    def calcular_media_turma(self, aluno_metrics):
        """Calcula indicadores por turma"""
        print("\n📚 Calculando métricas por turma...")
        
        turma_metrics = aluno_metrics.groupby('turma').agg({
            'media_geral': 'mean',
            'frequencia_media': 'mean',
            'id_aluno': 'count'
        }).round(2)
        
        turma_metrics.columns = ['media_geral_turma', 'frequencia_media_turma', 'total_alunos']
        
        status_count = aluno_metrics.groupby(['turma', 'status']).size().unstack(fill_value=0)
        turma_metrics = turma_metrics.join(status_count)
        
        turma_metrics['perc_aprovacao'] = ((turma_metrics.get('Aprovado', 0) / turma_metrics['total_alunos']) * 100).round(2)
        turma_metrics['perc_reprovacao'] = ((turma_metrics.get('Reprovado', 0) / turma_metrics['total_alunos']) * 100).round(2)
        turma_metrics['perc_recuperacao'] = ((turma_metrics.get('Recuperação', 0) / turma_metrics['total_alunos']) * 100).round(2)
        
        turma_metrics = turma_metrics.reset_index()
        
        print("✅ Métricas por turma calculadas")
        return turma_metrics
    
    def calcular_media_materia(self, df):
        """Calcula indicadores por matéria"""
        print("\n📖 Calculando métricas por matéria...")
        
        df['media_materia'] = (df['nota1'] + df['nota2']) / 2
        df['status_materia'] = df['media_materia'].apply(
            lambda x: 'Aprovado' if x >= 7 else ('Recuperação' if x >= 5 else 'Reprovado')
        )
        
        materia_metrics = df.groupby('materia').agg({
            'media_materia': 'mean',
            'frequencia': 'mean',
            'id_aluno': 'count'
        }).round(2)
        
        materia_metrics.columns = ['media_materia', 'frequencia_media', 'total_avaliacoes']
        
        reprovacoes = df[df['status_materia'] == 'Reprovado'].groupby('materia').size()
        materia_metrics['total_reprovacoes'] = reprovacoes.fillna(0)
        materia_metrics['perc_reprovacao'] = ((materia_metrics['total_reprovacoes'] / materia_metrics['total_avaliacoes']) * 100).round(2)
        
        materia_metrics['nivel_dificuldade'] = materia_metrics['perc_reprovacao'].apply(
            lambda x: 'Alta Dificuldade' if x > 30 else ('Média Dificuldade' if x > 15 else 'Baixa Dificuldade')
        )
        
        materia_metrics = materia_metrics.reset_index()
        
        print("✅ Métricas por matéria calculadas")
        return materia_metrics
    
    def identificar_melhores_piores(self, aluno_metrics):
        """Identifica melhores e piores alunos"""
        print("\n🏆 Identificando destaques...")
        
        top5 = aluno_metrics.nlargest(5, 'media_geral')[['id_aluno', 'nome', 'turma', 'media_geral', 'frequencia_media']]
        bottom5 = aluno_metrics.nsmallest(5, 'media_geral')[['id_aluno', 'nome', 'turma', 'media_geral', 'frequencia_media']]
        
        print("\n🏅 TOP 5 MELHORES ALUNOS:")
        print(top5.to_string(index=False))
        
        print("\n⚠️ TOP 5 PIORES ALUNOS:")
        print(bottom5.to_string(index=False))
        
        return top5, bottom5
    
    def salvar_resultados(self, aluno_metrics, turma_metrics, materia_metrics):
        """Salva todos os resultados"""
        print("\n💾 Salvando resultados...")
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        aluno_metrics.to_csv(f'{self.output_dir}/alunos_metricas.csv', index=False)
        turma_metrics.to_csv(f'{self.output_dir}/turmas_metricas.csv', index=False)
        materia_metrics.to_csv(f'{self.output_dir}/materias_metricas.csv', index=False)
        
        indicadores = aluno_metrics.merge(
            turma_metrics[['turma', 'media_geral_turma', 'frequencia_media_turma']], 
            on='turma'
        )
        indicadores.to_csv(f'{self.output_dir}/indicadores_finais.csv', index=False)
        
        print("✅ Arquivos salvos:")
        print("  - output/alunos_metricas.csv")
        print("  - output/turmas_metricas.csv")
        print("  - output/materias_metricas.csv")
        print("  - output/indicadores_finais.csv")
    
    def gerar_relatorio(self, aluno_metrics, turma_metrics, materia_metrics):
        """Gera relatório resumido"""
        print("\n" + "="*60)
        print("📊 RELATÓRIO DE ANÁLISE DE DESEMPENHO ESCOLAR")
        print("="*60)
        
        total = len(aluno_metrics)
        aprovados = len(aluno_metrics[aluno_metrics['status'] == 'Aprovado'])
        recuperacao = len(aluno_metrics[aluno_metrics['status'] == 'Recuperação'])
        reprovados = len(aluno_metrics[aluno_metrics['status'] == 'Reprovado'])
        
        print(f"\n📈 VISÃO GERAL:")
        print(f"Total de alunos: {total}")
        print(f"Aprovados: {aprovados} ({(aprovados/total*100):.1f}%)")
        print(f"Recuperação: {recuperacao} ({(recuperacao/total*100):.1f}%)")
        print(f"Reprovados: {reprovados} ({(reprovados/total*100):.1f}%)")
        
        print(f"\n📚 POR TURMA:")
        for _, row in turma_metrics.iterrows():
            print(f"Turma {row['turma']}: Média {row['media_geral_turma']} | "
                  f"Aprovação: {row['perc_aprovacao']}% | "
                  f"Reprovação: {row['perc_reprovacao']}%")
        
        print(f"\n📖 MATÉRIAS MAIS DIFÍCEIS:")
        dificeis = materia_metrics.nsmallest(3, 'media_materia')
        for _, row in dificeis.iterrows():
            print(f"{row['materia']}: Média {row['media_materia']} "
                  f"({row['perc_reprovacao']}% reprovação)")
        
        print("="*60)
        
        with open(f'{self.output_dir}/relatorio_analise.txt', 'w', encoding='utf-8') as f:
            f.write(f"RELATÓRIO DE ANÁLISE\n")
            f.write(f"Total alunos: {total}\n")
            f.write(f"Aprovados: {aprovados} ({(aprovados/total*100):.1f}%)\n")
            f.write(f"Recuperação: {recuperacao} ({(recuperacao/total*100):.1f}%)\n")
            f.write(f"Reprovados: {reprovados} ({(reprovados/total*100):.1f}%)\n")
        
        print(f"\n📄 Relatório salvo em: {self.output_dir}/relatorio_analise.txt")
    
    def executar(self):
        """Executa todo o pipeline de transformação"""
        print("🚀 INICIANDO TRANSFORMAÇÃO DOS DADOS ESCOLARES")
        print("="*60)
        
        df = self.carregar_dados()
        aluno_metrics = self.calcular_media_aluno(df)
        turma_metrics = self.calcular_media_turma(aluno_metrics)
        materia_metrics = self.calcular_media_materia(df)
        self.identificar_melhores_piores(aluno_metrics)
        self.salvar_resultados(aluno_metrics, turma_metrics, materia_metrics)
        self.gerar_relatorio(aluno_metrics, turma_metrics, materia_metrics)
        
        print("\n✅ TRANSFORMAÇÃO CONCLUÍDA COM SUCESSO!")
        
        return {
            'alunos': aluno_metrics,
            'turmas': turma_metrics,
            'materias': materia_metrics
        }

if __name__ == "__main__":
    transformador = TransformacaoDados()
    resultados = transformador.executar()