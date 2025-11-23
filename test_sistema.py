"""
Script de teste para verificar se todos os componentes do sistema estão funcionando
Execute: python test_sistema.py
"""

import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent))

def testar_imports():
    """Testa se todos os módulos podem ser importados"""
    print("🧪 Testando imports dos módulos...")
    
    try:
        from src.core.controller import FarmTechController
        print("  ✅ FarmTechController")
    except Exception as e:
        print(f"  ❌ FarmTechController: {e}")
        return False
    
    try:
        from src.core.config import Config
        print("  ✅ Config")
    except Exception as e:
        print(f"  ❌ Config: {e}")
        return False
    
    try:
        from src.fase1.calculo_plantio import CalculoPlantio
        from src.fase1.clima_service import ClimaService
        print("  ✅ Fase 1 (Cálculos e Clima)")
    except Exception as e:
        print(f"  ❌ Fase 1: {e}")
        return False
    
    try:
        from src.fase2.models import Base, Funcionarios, Insumos
        from src.fase2.database import DatabaseHandler
        print("  ✅ Fase 2 (Database e Models)")
    except Exception as e:
        print(f"  ❌ Fase 2: {e}")
        return False
    
    try:
        from src.fase3.sensor_handler import SensorHandler, SensorData
        print("  ✅ Fase 3 (Sensores IoT)")
    except Exception as e:
        print(f"  ❌ Fase 3: {e}")
        return False
    
    try:
        from src.fase4.ml_model import MLModel
        print("  ✅ Fase 4 (Machine Learning)")
    except Exception as e:
        print(f"  ❌ Fase 4: {e}")
        return False
    
    try:
        from src.fase6.yolo_detector import YOLODetector
        print("  ✅ Fase 6 (YOLO - Placeholder)")
    except Exception as e:
        print(f"  ❌ Fase 6: {e}")
        return False
    
    print("\n✅ Todos os imports funcionando!\n")
    return True


def testar_funcionalidades():
    """Testa funcionalidades básicas do sistema"""
    print("🧪 Testando funcionalidades básicas...")
    
    from src.core.controller import FarmTechController
    
    try:
        # Inicializar controlador
        print("\n1️⃣ Inicializando controlador...")
        controller = FarmTechController()
        print("  ✅ Controlador inicializado")
        
        # Testar Fase 1: Cálculo de Plantio
        print("\n2️⃣ Testando cálculo de plantio...")
        resultado_milho = controller.calcular_plantio_milho(100, 50)
        print(f"  ✅ Milho: {resultado_milho['area']:.2f} m², {resultado_milho['qnt_insumo']:.2f} L de {resultado_milho['tipo_insumo']}")
        
        resultado_soja = controller.calcular_plantio_soja(30)
        print(f"  ✅ Soja: {resultado_soja['area']:.2f} m², {resultado_soja['qnt_insumo']:.2f} L de {resultado_soja['tipo_insumo']}")
        
        # Testar Fase 2: Database
        print("\n3️⃣ Testando conexão com banco de dados...")
        db_ok = controller.testar_conexao_db()
        if db_ok:
            print("  ✅ Conexão com banco de dados OK")
        else:
            print("  ⚠️ Conexão com banco de dados com problemas")
        
        # Testar Fase 3: Sensores
        print("\n4️⃣ Testando sensores IoT...")
        controller.gerar_dados_sensores_simulados(5)
        ultima_leitura = controller.obter_ultima_leitura_sensor()
        print(f"  ✅ Sensores: Umidade={ultima_leitura.umidade:.1f}%, pH={ultima_leitura.ph:.2f}")
        
        stats = controller.obter_estatisticas_sensores()
        print(f"  ✅ Estatísticas: {stats['total_leituras']} leituras")
        
        # Testar Fase 4: ML
        print("\n5️⃣ Testando modelo de Machine Learning...")
        resultado_ml = controller.prever_irrigacao(35.0, 28.0, 150.0)
        if 'erro' in resultado_ml:
            print(f"  ⚠️ ML: {resultado_ml['erro']}")
            print("     (Copie o modelo da Fase 4 para 'models/modelo_irrigacao.pkl')")
        else:
            print(f"  ✅ ML: {resultado_ml['status']} (Confiança: {resultado_ml['confianca']})")
        
        # Testar status do sistema
        print("\n6️⃣ Verificando status geral do sistema...")
        status = controller.status_sistema()
        
        componentes_ok = sum([
            status['fase1_calculo'],
            status['fase1_clima'],
            status['fase2_database'],
            status['fase3_sensores'],
            status['fase4_ml'],
        ])
        
        print(f"  ✅ {componentes_ok}/5 componentes principais funcionando")
        
        if not status['fase4_ml']:
            print("  ⚠️ Modelo ML não carregado (esperado se não copiou o .pkl)")
        
        print("\n✅ Todos os testes básicos concluídos!\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()
        return False


def testar_analise_integrada():
    """Testa a análise integrada (clima + ML)"""
    print("🧪 Testando análise integrada...")
    
    from src.core.controller import FarmTechController
    
    try:
        controller = FarmTechController()
        
        # Nota: Este teste pode falhar se não houver internet ou API key inválida
        print("\n🌐 Testando análise integrada (requer internet)...")
        resultado = controller.analisar_necessidade_irrigacao_completa(
            cidade="São Paulo",
            umidade_solo=35.0,
            temperatura=28.0,
            nutrientes=150.0
        )
        
        print(f"  ✅ Decisão: {'IRRIGAR' if resultado['deve_irrigar'] else 'NÃO IRRIGAR'}")
        print(f"  📝 Motivo: {resultado['motivo']}")
        print(f"  🎯 Prioridade: {resultado['prioridade']}")
        
        return True
        
    except Exception as e:
        print(f"  ⚠️ Erro na análise integrada: {e}")
        print("     (Normal se não houver internet ou API key inválida)")
        return False


def main():
    """Função principal de testes"""
    print("=" * 60)
    print("🧪 TESTE DO SISTEMA FARMTECH SOLUTIONS - FASE 7")
    print("=" * 60)
    print()
    
    # Teste 1: Imports
    if not testar_imports():
        print("\n❌ Falha nos imports. Corrija os erros antes de continuar.")
        return
    
    # Teste 2: Funcionalidades
    if not testar_funcionalidades():
        print("\n❌ Falha nos testes de funcionalidades.")
        return
    
    # Teste 3: Análise Integrada (opcional)
    testar_analise_integrada()
    
    print("\n" + "=" * 60)
    print("✅ SISTEMA TESTADO COM SUCESSO!")
    print("=" * 60)
    print()
    print("📌 Próximos passos:")
    print("   1. Execute 'streamlit run app.py' para ver o dashboard")
    print("   2. Copie o modelo ML da Fase 4 para 'models/' (se disponível)")
    print("   3. Configure sua API key no arquivo .env")
    print()
    print("🎉 Sistema pronto para uso e expansão pelas outras pessoas!")
    print()


if __name__ == "__main__":
    main()

