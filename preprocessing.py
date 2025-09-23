import utils as ut

folder = "output/webscrapping"

def main():

    pdf_files = ut.carregar_pdf(folder)
    ut.criar_dataset(pdf_files)

if __name__ == "__main__":
    main()