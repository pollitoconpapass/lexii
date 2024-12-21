import os
import json
from utils.pdf_reading import read_pdf
from utils.llm_analysis import azure_chunk_analysis_4_translation, parse_llm_output


def main_process(pdf_path: str, start_page: int = 0, final_page: int = None):
    # === Checking the PDF exists ===
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file {pdf_path} not found.")
        return
    
    # === Read it and get the chunks ===
    chunks = read_pdf(pdf_path, start_page, final_page)
    print(f"Number of chunks: {len(chunks)}\n")

    # === Analyze the whole file ===
    count = 0
    all_results = []
    for chunk in chunks:
        try:
            result = azure_chunk_analysis_4_translation(chunk)
            result = parse_llm_output(result)

            all_results.extend(result)

            count += 1
            print(f"Chunk {count} of {len(chunks)}")

        except Exception as e:
            print(f"Error in chunk {count}:", e)
            continue


    # === Generate the JSON file ===
    json_name = pdf_path.split("/")[-1].split(".")[0]
    output_directory = f"./jsons/{json_name}.json"
    os.makedirs(os.path.dirname(output_directory), exist_ok=True) 

    with open(output_directory, "w", encoding="utf-8") as f: 
        json.dump(all_results, f, ensure_ascii=False, indent=4)

    print("\nAll done! Check the JSON file in the jsons folder.")


if __name__ == "__main__":
    main_process("./PDFs/diccionario-qeswa-academia-mayor-cuzco.pdf", 16, 400) # -> change according to your needs