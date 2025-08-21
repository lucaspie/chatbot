import pytesseract
from PIL import Image
import re
import pandas as pd

# 1. Caminho do executável Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 2. Caminho da tessdata (se precisar)
#tessdata_dir = r'C:\\Program Files\\Tesseract-OCR\\tessdata'
#tess_config = f'--tessdata-dir "{tessdata_dir}"'

# Caminho da imagem
caminho_da_imagem = 'teste.jpeg'

try:
    # Extrair texto
    imagem = Image.open(caminho_da_imagem)
    texto_extraido = pytesseract.image_to_string(imagem)

    # Quebrar em linhas
    linhas = texto_extraido.splitlines()

    # Regex para pegar itens no formato "código descrição"
    # Aceita códigos com £, letras, números, hífens
    padrao = re.compile(r"^([£A-Za-z0-9\-]+)\s+(.*)$")

    dados = []
    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue
        match = padrao.match(linha)
        if match:
            codigo = match.group(1)
            descricao = match.group(2)
            dados.append([codigo, descricao])

    # Criar DataFrame e salvar em Excel
    df = pd.DataFrame(dados, columns=["Código", "Descrição"])
    df.to_excel("itens_extraidos.xlsx", index=False)

    print("Itens extraídos e salvos em 'itens_extraidos.xlsx'")
    print(df)

except FileNotFoundError:
    print(f"Erro: O arquivo de imagem em '{caminho_da_imagem}' não foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
