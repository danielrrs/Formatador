import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import chardet

# Função para substituir os caracteres especiais e transformar tudo em maiúsculas
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
        '°': '',  
        'ª': '',
        'º': '',
        '-': '',
    }
    # Substituir caracteres especiais
    texto_limpado = texto.translate(str.maketrans(substituicoes))
    # Transformar tudo em maiúsculas
    return texto_limpado.upper()

# Função para remover a palavra "#VALOR!" de todas as colunas
def remover_valor_excessivo(df):
    for coluna in df.columns:
        df[coluna] = df[coluna].apply(lambda x: str(x).replace('#VALOR!', '') if isinstance(x, str) else x)
    return df

# Função para detectar a codificação do arquivo
def detectar_codificacao(arquivo):
    with open(arquivo, 'rb') as f:
        resultado = chardet.detect(f.read())
        return resultado['encoding']

# Função para manter somente os 10 primeiros caracteres de colunas específicas
def manter_10_primeiros_caracteres(df, colunas):
    for coluna in colunas:
        if coluna in df.columns:
            df[coluna] = df[coluna].apply(lambda x: str(x)[:10] if isinstance(x, str) else x)
        else:
            messagebox.showwarning("Aviso", f"A coluna '{coluna}' não foi encontrada no arquivo.")
    return df

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

        # Limpar todas as colunas do DataFrame e transformar para maiúsculas
        for coluna in df.columns:
            df[coluna] = df[coluna].apply(lambda x: limpar_caracteres(str(x)))

        # Remover a palavra "#VALOR!" de todas as colunas
        df = remover_valor_excessivo(df)

        # Substituir os valores NaN por uma string vazia
        df = df.fillna('')

        # Salvar o arquivo CSV com os caracteres limpos e em maiúsculas
        caminho_salvar = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if caminho_salvar:  # Se o usuário escolher um local para salvar
            try:
                df.to_csv(caminho_salvar, index=False, sep=';', encoding='utf-8')
                messagebox.showinfo("Sucesso", "Arquivo CSV limpo e salvo com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar o arquivo: {e}")

# Função para remover colunas fixas
def remover_colunas(df):
    # Lista fixa de colunas que sempre serão removidas
    colunas_fixas = ['Cor (Pend)', 'Data Resolução Max', 'Prof. Call Center', 'Duração da chamada (minutos)', 'Tempo max resolução (horas)', 'Descrição / Comentários', '...']
    
    for coluna in colunas_fixas:
        if coluna in df.columns:
            df.drop(coluna, axis=1, inplace=True)
        else:
            messagebox.showwarning("Aviso", f"A coluna '{coluna}' não foi encontrada no arquivo.")
    return df

# Função para abrir e limpar o arquivo CSV com a remoção das colunas fixas, separação de dias e horas e remoção da coluna 'Tempo Decorrido'
def limpar_ocorrencias():
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

        # Limpar todas as colunas do DataFrame e transformar para maiúsculas
        for coluna in df.columns:
            df[coluna] = df[coluna].apply(lambda x: limpar_caracteres(str(x)))

        # Remover as colunas fixas
        df = remover_colunas(df)

        # Separar a coluna "Tempo Decorrido" (se existir) em Dias e Horas
        if 'Tempo Decorrido' in df.columns:
            # Separar a coluna "Tempo Decorrido" no formato "0 Dias 07:09:08"
            df[['DIASDECORRIDOS', 'HORASDECORRIDAS']] = df['Tempo Decorrido'].str.split(' DIAS ', expand=True)
            # Remover a coluna "Tempo Decorrido" depois de extrair os dias e horas
            df.drop('Tempo Decorrido', axis=1, inplace=True)

        # Exemplo de colunas que você pode querer modificar
        colunas_a_modificar = ['Data do Registro', 'Data da Ocorrência', 'Data Baixa', 'Data Máxima Resolução']  
        
        
        df = manter_10_primeiros_caracteres(df, colunas_a_modificar)

        # Remover a palavra "#VALOR!" de todas as colunas
        df = remover_valor_excessivo(df)

        # Salvar o arquivo CSV com os caracteres limpos, maiúsculas, colunas removidas e a coluna 'Tempo Decorrido' excluída
        caminho_salvar = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if caminho_salvar:  # Se o usuário escolher um local para salvar
            try:
                df.to_csv(caminho_salvar, index=False, sep=';', encoding='utf-8')
                messagebox.showinfo("Sucesso", "Arquivo CSV limpo, colunas removidas e salvo com sucesso!")
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

# botão para limpar o arquivo CSV
botao_limpar = tk.Button(root, text="Limpar e Salvar Arquivo CSV", command=verificar_arquivo_csv)
botao_limpar.pack(pady=10)

# botão "Limpar Ocorrências"
botao_limpar_ocorrencias = tk.Button(root, text="Limpar Ocorrências", command=limpar_ocorrencias)
botao_limpar_ocorrencias.pack(pady=10)

# Iniciar a interface
root.mainloop()
