import pandas as pd
import os
import glob
import json

# CONFIGURAÇÕES DE CAMINHOS
pasta_downloads = r"C:\Users\carol\Downloads"
padrao_arquivo = os.path.join(pasta_downloads, "BDT_export*.csv")
pasta_destino = r"C:\Users\carol\OneDrive\Área de Trabalho\Dandara\PRODUÇÃO DE CAMPO - GABI\BDT - Boletim Diário de Trabalho\Dados BDT para Power BI"
arquivo_final = os.path.join(pasta_destino, "bdt_consolidado_moderna.csv")

# FUNÇÕES DE AUXÍLIO
def extrair_litros(texto):
    """Soma insumos da lista JSON (Ex: Diesel + Óleo)"""
    try:
        dados = json.loads(texto.replace("''", '"'))
        return sum(float(item.get('quantidade', 0)) for item in dados)
    except: return 0

def conv_h(h_str):
    """Converte '3h 55min' ou '5h' para decimal (ex: 3.92)"""
    try:
        h_str = str(h_str).lower()
        if 'h' in h_str and 'min' in h_str:
            parts = h_str.replace('min', '').split('h ')
            return int(parts[0]) + (int(parts[1])/60)
        elif 'h' in h_str:
            return float(h_str.replace('h', ''))
        return 0.0
    except: return 0.0

def aplicar_metas(maquina_str):
    """Hierarquia 'Tipo - Modelo'"""
    maquina_str = str(maquina_str).upper()
    # Lógica baseada na aba VALORES da planilha Biocarbono
    if "GARRA" in maquina_str:
        if "MF2156" in maquina_str or "MF2246" in maquina_str:
            return 45.0  # Meta 40-50
        return 35.0      # Meta 30-40
    if "FELLER" in maquina_str or "SKIDDER" in maquina_str:
        return 70.0      # Meta 60-80
        
    return 25.0 # Padrão para outros

# PROCESSAMENTO PRINCIPAL

def processar_dados():
    arquivos = glob.glob(padrao_arquivo)
    if not arquivos:
        print("❌ Nenhum arquivo BDT_export encontrado em Downloads.")
        return
    
    # Arquivo mais recente
    arquivo_recente = max(arquivos, key=os.path.getmtime)
    print(f"🔄 Lendo: {arquivo_recente}")

    # Carrega os dados
    df = pd.read_csv(arquivo_recente, encoding='utf-8-sig')

    # 1. SEGURANÇA: Manter apenas registros enviados (Remove rascunhos)
    df = df[df['status'].str.lower() == 'enviado'].copy()

    # 2. CONVERSÃO DE NÚMEROS (Trata hodômetros quebrados)
    cols_numericas = ['hodometro_inicial', 'hodometro_final', 'hodometro_total', 'gps_latitude', 'gps_longitude']
    for col in cols_numericas:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # 3. IDENTIFICAÇÃO DE METAS E CÁLCULOS DE TEMPO
    df['meta_m3h'] = df['maquina_tipo'].apply(aplicar_metas)
    df['horas_decimais'] = df['total_horas'].apply(conv_h)
    df['diesel_litros'] = df['abastecimentos'].apply(extrair_litros)

    # 4. CÁLCULO DE VOLUME E BÔNUS
    df['volume_estimado'] = (df['horas_decimais'] * df['meta_m3h']).round(2)
    df['valor_bonus'] = (df['volume_estimado'] * 0.25).round(2)

    # 5. AUDITORIA DE ENVIO
    df['data_envio'] = pd.to_datetime(df['created_date'])
    df['data_fim_op'] = pd.to_datetime(df['data'] + ' ' + df['hora_fim'])
    
    # Diferença em minutos
    df['atraso_minutos'] = (df['data_envio'] - df['data_fim_op']).dt.total_seconds() / 60
    df['status_auditoria'] = df['atraso_minutos'].apply(
        lambda x: '🚨 Alerta' if x > 60 else ('⚠️ Atraso' if x > 30 else '✅ OK')
    )

    # 6. SALVAMENTO FINAL
    os.makedirs(pasta_destino, exist_ok=True)
    df.to_csv(arquivo_final, index=False, sep=';', encoding='utf-8-sig')
    
    print(f"✅ Sucesso! {len(df)} registros limpos e salvos em: {arquivo_final}")

if __name__ == "__main__":
    processar_dados()
