from ocr_service import OCRService


def main():
    ocr_service = OCRService()

    # Example usage
    file_path = input("Enter the path to your image or PDF file: ")
    extracted_text = ocr_service.extract_text(file_path)

    if extracted_text:
        print("\nExtracted Text:")
        print("=" * 50)
        print(extracted_text)
        print("=" * 50)
        with open("extracted_text.txt", "w", encoding="utf-8") as f:
            f.write(extracted_text)
    else:
        print("Failed to extract text from the file.")


if __name__ == "__main__":
    main()
