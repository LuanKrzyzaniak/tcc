import os
import glob
import sys

def main():

    # Consts
    PDF_SOURCE_DIR = "output/webscrapping"  # Use a distinct name for the directory path
    OUTPUT_FOLDER = "output/desired_output"

    try:
        if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)

        # Use a new variable for the list of files to avoid overwriting the path string
        pdf_files_list = glob.glob(os.path.join(PDF_SOURCE_DIR, '*.pdf'))
        pdf_files_list.extend(glob.glob(os.path.join(PDF_SOURCE_DIR, '*.PDF')))

        if not pdf_files_list:
            return

        for pdf_path in pdf_files_list: # Loop over the list of file paths
            base_name = os.path.basename(pdf_path)
            file_name_without_ext = os.path.splitext(base_name)[0]
            txt_file_name = file_name_without_ext + ".txt"
            txt_path = os.path.join(OUTPUT_FOLDER, txt_file_name)

            with open(txt_path, 'a+', encoding='utf-8') as f:
                f.seek(0)
                content = f.read(1)

                if not content:
                    f.write(f"Original PDF Path: {os.path.abspath(pdf_path)}\n\n")

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()