import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import chardet

# Função para substituir os caracteres especiais
def limpar_caracteres(texto):
    substituicoes = {
        'ç': 'c',
        'Ç': 'C',
        'ê': 'e',
        'Ê': 'E',
        'é': 'e',
        'É': 'E',
        'í': 'i',
        'Í': 'I',
        'ó': 'o',
        'Ó': 'O',
        'ô': 'o',
        'Ô': 'O',
        'ú': 'u',
        'Ú': 'U',
        'à': 'a',
        'À': 'A',
        'â': 'a',
        'Â': 'A',
        'ã': 'a',
        'Ã': 'A',
        'õ': 'o',
        'Õ': 'O',
        'ü': 'u',
        'Ü': 'U',
        'à': 'a',
        'á': 'a',
        'Á': 'A',
        '°': '',  # Remover símbolo de grau
    }
    return texto.translate(str.maketrans(substituicoes))

# Função para detectar a codificação do arquivo
def detectar_codificacao(arquivo):
    with open(arquivo, 'rb') as f:
        resultado = chardet.detect(f.read())
        return resultado['encoding']

# Função para abrir e limpar o arquivo CSV
def limpar_csv():
    # Abrir caixa de diálogo para escolher o arquivo CSV
    arquivo_csv = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    
    if arquivo_csv:  # Se um arquivo for selecionado
        try:
            # Detectar a codificação do arquivo
            codificacao = detectar_codificacao(arquivo_csv)
            
            # Tentar ler o arquivo CSV com o delimitador ';' e codificação detectada
            df = pd.read_csv(arquivo_csv, encoding=codificacao, delimiter=';')  

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar o arquivo: {e}")
            return

        # Limpar todas as colunas do DataFrame
        for coluna in df.columns:
            df[coluna] = df[coluna].apply(lambda x: limpar_caracteres(str(x)))

        # Salvar o arquivo CSV com os caracteres limpos
        caminho_salvar = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if caminho_salvar:  # Se o usuário escolher um local para salvar
            try:
                df.to_csv(caminho_salvar, index=False, sep=';', encoding='utf-8')
                messagebox.showinfo("Sucesso", "Arquivo CSV limpo e salvo com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar o arquivo: {e}")

# Função principal para verificar o formato do arquivo
def verificar_arquivo_csv():
    # Abrir caixa de diálogo para escolher o arquivo CSV
    arquivo_csv = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if arquivo_csv:
        if not arquivo_csv.lower().endswith('.csv'):
            messagebox.showerror("Erro", "Por favor, selecione um arquivo CSV válido.")
            return
        limpar_csv()

# Criando a janela principal
root = tk.Tk()
root.title("Limpeza de CSV")

# Definir o tamanho da janela como 300x150 pixels
root.geometry("300x150")

# Impedir o redimensionamento da janela
root.resizable(False, False)

# Adicionar um botão para limpar o arquivo CSV
botao_limpar = tk.Button(root, text="Limpar e Salvar Arquivo CSV", command=verificar_arquivo_csv)
botao_limpar.pack(pady=20)

# Iniciar a interface
root.mainloop()
