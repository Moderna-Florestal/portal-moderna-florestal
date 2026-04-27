import pandas as pd
import os
import glob
import json

# CONFIGURAÇÕES DE CAMINHO
pasta_downloads = r"C:\Users\carol\Downloads"
padrao_arquivo = os.path.join(pasta_downloads, "BDT_export*.csv")
pasta_destino = r"C:\Users\carol\OneDrive\Área de Trabalho\Dandara\PRODUÇÃO DE CAMPO - GABI\BDT - Boletim Diário de Trabalho\Dados BDT para Power BI"
arquivo_final = os.path.join(pasta_destino, "bdt_producao_limpo.csv")

def extrair_litros(texto):
    try:
        dados = json.loads(texto.replace("''", '"'))
        return sum(float(item.get('quantidade', 0)) for item in dados)
    except: return 0

def conv_h(h_str):
    try:
        parts = h_str.replace('min', '').split('h ')
        return int(parts[0]) + (int(parts[1])/60)
    except: return 0

def processar_dados():
    arquivos = glob.glob(padrao_arquivo)
    if not arquivos: return print("❌ Arquivo não encontrado.")
    
    df = pd.read_csv(max(arquivos, key=os.path.getmtime), encoding='utf-8-sig')

    # 1. Tratamento de Horas e Insumos
    df['horas_decimais'] = df['total_horas'].apply(conv_h)
    df['diesel_litros'] = df['abastecimentos'].apply(extrair_litros)

    # 2. Lógica de Metas (Planilha VALORES - Biocarbono)
    def aplicar_metas(row):
        maquina = str(row['maquina_tipo']).upper()
        modelo = str(row['mf']).upper()
        
        if "GARRA" in maquina:
            if modelo in ["MF2156", "MF2246"]: return 45.0 # Meta 40-50
            return 35.0 # Meta 30-40
        if "FELLER" in maquina or "SKIDDER" in maquina: return 70.0 # Meta 60-80
        return 25.0

    df['meta_produtividade_m3h'] = df.apply(aplicar_metas, axis=1)

    # 3. Cálculos de Produção e Bônus
    df['volume_estimado'] = df['horas_decimais'] * df['meta_produtividade_m3h']
    df['valor_bonus'] = df['volume_estimado'] * 0.25

    # 4. Auditoria de Envio
    df['data_envio'] = pd.to_datetime(df['created_date'])
    df['data_fim_op'] = pd.to_datetime(df['data'] + ' ' + df['hora_fim'])
    df['atraso_minutos'] = (df['data_envio'] - df['data_fim_op']).dt.total_seconds() / 60
    df['status_auditoria'] = df['atraso_minutos'].apply(lambda x: '🚨 Alerta' if x > 60 else '✅ OK')

    # 5. Exportação
    os.makedirs(pasta_destino, exist_ok=True)
    df.to_csv(arquivo_final, index=False, sep=';', encoding='utf-8-sig')
    print(f"✅ Sucesso! Dados salvos em: {arquivo_final}")

if __name__ == "__main__": processar_dados()