import os
import time
import json
import pdfplumber
import ollama
import openpyxl
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ================= CONFIGURAÇÕES =================
PASTA_MONITORADA = r"C:\Users\vinic\OneDrive\Docs_Pessoal\Pagamentos"
ARQUIVO_EXCEL = r"C:\Users\vinic\OneDrive\Docs_Pessoal\Pagamentos\Pasta_ref.xlsx"

# ================= FUNÇÕES NUCLEARES =================

def extrair_texto_pdf(caminho_pdf):
    """Extrai todo o texto de um arquivo PDF."""
    texto_completo = ""
    try:
        with pdfplumber.open(caminho_pdf) as pdf:
            for pagina in pdf.pages:
                texto_completo += pagina.extract_text() + "\n"
        return texto_completo
    except Exception as e:
        print(f"Erro ao ler PDF {caminho_pdf}: {e}")
        return None

def processar_com_ia_local(texto_comprovante):
    """Envia o texto para a IA rodando no Ollama e retorna um dicionário (JSON)."""
    prompt_sistema = (
        "Você é um assistente financeiro de extração de dados. "
        "Leia o texto do comprovante e identifique o tipo de documento, se é um comprovante, ou um boleto com código de barras e extraia as seguintes informações: "
        "No caso de comprovante: tipo de documento,  Data do Pagamento (formato DD/MM/AAAA), Valor (apenas números e vírgula), Recebedor (Nome ou Razão Social), Descrição (resumo curto do pagamento) e conta utilizada para pagamento."
        "No caso de boleto: tipo de documento, Data do Vencimento (formato DD/MM/AAAA), Valor (apenas números e vírgula), Beneficiário (Nome ou Razão Social), Descrição (resumo curto do pagamento) e conta e banco utilizados para pagamento."
        "Retorne ESTRITAMENTE um objeto JSON válido com as chaves: 'tipo de documento', 'data', 'valor', 'conta', 'banco', 'pagador', 'recebedor', 'descrição'. "
        "Em tipo de documento indique 'comprovante' ou 'boleto'. Se alguma informação não puder ser extraída, deixe a chave correspondente com valor vazio (''). "
        "Não inclua nenhum texto adicional além do JSON."
    )

    print("Processando dados localmente com o Ollama (Llama 3)...")
    
    try:
        response = ollama.chat(
            model='llama3', 
            format='json',
            messages=[
                {'role': 'system', 'content': prompt_sistema},
                {'role': 'user', 'content': f"Extraia os dados deste comprovante:\n\n{texto_comprovante}"}
            ],
            options={
                'temperature': 0.1 # Deixa a IA mais precisa e menos criativa
            }
        )
        
        conteudo_resposta = response['message']['content']
        dados_json = json.loads(conteudo_resposta)
        
        return dados_json
    
    except Exception as e:
        print(f"Erro ao processar na IA Local: {e}")
        return None
    
def salvar_json(dados, caminho_original_pdf):
    """Salva os dados extraídos em um arquivo .json na mesma pasta."""
    try:
        # Troca a extensão de .pdf para .json
        caminho_json = caminho_original_pdf.replace('.pdf', '.json').replace('.PDF', '.json')
        
        # Cria e salva o arquivo JSON
        with open(caminho_json, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
            
        print(f"💾 Arquivo JSON salvo: {os.path.basename(caminho_json)}")
        
    except Exception as e:
        print(f"Erro ao salvar o arquivo JSON: {e}")

def inserir_no_excel(dados):
    """Adiciona uma nova linha com os dados na planilha Excel."""
    try:
        workbook = openpyxl.load_workbook(ARQUIVO_EXCEL)
        sheet = workbook.active
        
        # A ordem aqui reflete as colunas A, B, C e D do seu Excel
        nova_linha = [
            dados.get('tipo', ''),
            dados.get('data', ''),
            dados.get('recebedor', ''),
            dados.get('pagador', ''),
            dados.get('valor', ''),
            dados.get('descrição', ''),
            dados.get('conta', ''),
            dados.get('banco', '')
        ]
        
        sheet.append(nova_linha)
        workbook.save(ARQUIVO_EXCEL)
        print(f"✅ Dados inseridos com sucesso: {nova_linha}")
        
    except Exception as e:
        print(f"Erro ao salvar no Excel: {e}")

# ================= MONITORAMENTO (WATCHDOG) =================

class MonitorDeComprovantes(FileSystemEventHandler):
    def on_created(self, event):
        nome_arquivo = os.path.basename(event.src_path)
        
        # Ignora pastas, arquivos que não são PDF e arquivos temporários do Windows (~ ou ~~)
        if event.is_directory or not event.src_path.lower().endswith('.pdf') or nome_arquivo.startswith('~'):
            return
        
        caminho_arquivo = event.src_path
        print(f"\n📄 Novo comprovante detectado: {nome_arquivo}")
        
        # Aguarda 2 segundos para o Windows liberar o arquivo
        time.sleep(2) 
        
        # 1. Extrai o texto fisicamente do PDF
        print("Lendo conteúdo do PDF...")
        texto = extrair_texto_pdf(caminho_arquivo)
        
        if texto:
            # 2. Envia o texto extraído para o Llama 3 formatar
            dados_extraidos = processar_com_ia_local(texto)
            
            if dados_extraidos:
                # 3. Chama a nova função para salvar o .json
                salvar_json(dados_extraidos, caminho_arquivo)
                
                # 4. Salva no Excel
                inserir_no_excel(dados_extraidos)

if __name__ == "__main__":
    if not os.path.exists(PASTA_MONITORADA):
        print(f"Erro: A pasta {PASTA_MONITORADA} não existe.")
        exit()
        
    if not os.path.exists(ARQUIVO_EXCEL):
        print(f"Erro: O arquivo Excel {ARQUIVO_EXCEL} não foi encontrado.")
        exit()

    event_handler = MonitorDeComprovantes()
    observer = Observer()
    observer.schedule(event_handler, PASTA_MONITORADA, recursive=False)
    
    print(f"👀 Monitorando a pasta: {PASTA_MONITORADA}")
    print("Pressione Ctrl+C para encerrar.")
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nMonitoramento encerrado.")
    
    observer.join()