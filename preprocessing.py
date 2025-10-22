import pipeline as pipe

folder = "output/webscrapping"

def main():

    arquivos = pipe.carregar_pdf(folder)
    arquivos_tratados = pipe.tratar_arquivos(arquivos)
    pipe.criar_dataset(arquivos_tratados)

if __name__ == "__main__":
    main()