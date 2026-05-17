"""
Pipeline ETL Completo - Sistema de Análise de Desempenho Escolar
Executa: Limpeza (Integrante 2) + Transformação (Integrante 3)
"""

import sys
import os
import subprocess

def executar_limpeza():
    """Executa o script de limpeza do Integrante 2"""
    print("="*60)
    print("🧹 ETAPA 1: LIMPEZA DOS DADOS (Integrante 2)")
    print("="*60)
    
    try:
        # Executa o script de limpeza como um processo separado
        resultado = subprocess.run(
            [sys.executable, 'etl/limpeza.py'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        print(resultado.stdout)
        
        if resultado.returncode == 0:
            print("✅ Limpeza concluída com sucesso!")
            return True
        else:
            print(f"❌ Erro na limpeza:")
            print(resultado.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erro ao executar limpeza: {e}")
        return False

def executar_transformacao():
    """Executa o script de transformação do Integrante 3"""
    print("\n" + "="*60)
    print("📊 ETAPA 2: TRANSFORMAÇÃO DOS DADOS (Integrante 3)")
    print("="*60)
    
    try:
        from etl.transformacao import TransformacaoDados
        transformador = TransformacaoDados()
        resultados = transformador.executar()
        print("\n✅ Transformação concluída com sucesso!")
        return True
        
    except ImportError:
        print("❌ Arquivo etl/transformacao.py não encontrado!")
        return False
    except Exception as e:
        print(f"❌ Erro na transformação: {e}")
        return False

def main():
    """Pipeline completo"""
    print("\n🎓 SISTEMA DE ANÁLISE DE DESEMPENHO ESCOLAR")
    print("🚀 Pipeline ETL Completo")
    print("="*60)
    
    # Etapa 1: Limpeza
    sucesso_limpeza = executar_limpeza()
    
    # Etapa 2: Transformação (só roda se limpeza funcionou)
    if sucesso_limpeza:
        sucesso_transformacao = executar_transformacao()
        
        if sucesso_transformacao:
            print("\n" + "="*60)
            print("🎯 PIPELINE COMPLETO CONCLUÍDO COM SUCESSO!")
            print("="*60)
            print("\n📁 Arquivos gerados em /output:")
            print("  - dados_escolares_limpos.csv (limpeza)")
            print("  - alunos_metricas.csv (transformação)")
            print("  - turmas_metricas.csv (transformação)")
            print("  - materias_metricas.csv (transformação)")
            print("  - indicadores_finais.csv (transformação)")
            print("  - relatorio_analise.txt (transformação)")
    else:
        print("\n❌ Pipeline interrompido devido a erro na limpeza.")

if __name__ == "__main__":
    main()