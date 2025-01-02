# BibTeX Converter

This Streamlit application converts BibTeX files into CSV, JSON, and extracts DOIs into a text file. It allows users to upload BibTeX files or paste BibTeX content directly, and then provides options to download the converted data and preview it.

## Features

-   **BibTeX Parsing:** Parses BibTeX content from uploaded files or pasted text.
-   **CSV Conversion:** Converts BibTeX entries to CSV format.
-   **JSON Conversion:** Converts BibTeX entries to JSON format.
-   **DOI Extraction:** Extracts DOIs from BibTeX entries into a text file.
-   **Download Options:** Provides download buttons for CSV, JSON, and DOI text files.
-   **Preview Options:** Allows users to preview CSV, JSON, and DOI data.
-   **Modal JSON Preview:** Displays formatted JSON in a modal for better readability.
-   **Handles Multiple Files:** Combines content from multiple uploaded BibTeX files.
-   **Error Handling:** Provides error messages for parsing and conversion issues.
-   **Logging:** Logs application events and errors to a file.

## How to Use

1.  **Upload BibTeX Files:**
    -   Drag and drop one or more BibTeX files (.bib) into the file uploader.
    -   The maximum file size is 50MB per file.
2.  **Paste BibTeX Content:**
    -   Alternatively, paste BibTeX content directly into the text area.
3.  **Process Preview:**
    -   Enter the number of entries to process for preview (default is 5).
    -   Click the "Process Preview" button to process a limited number of entries.
4.  **Process All:**
    -   Click the "Process All" button to process all entries.
5.  **Download Data:**
    -   Click the "Download CSV" button to download the data in CSV format.
    -   Click the "Download JSON" button to download the data in JSON format.
    -   Click the "Download DOIs txt" button to download the extracted DOIs in a text file.
6.  **Preview Data:**
    -   Enter the number of records to preview (max 50).
    -   The app will display a preview of the CSV data in a table.
    -   Click the "View Full JSON" button to view the JSON data in a modal.
    -   The app will display a preview of the extracted DOIs.

## Installation

1.  **Clone the Repository:**
    ```bash
    git clone [repository_url]
    cd [repository_directory]
    ```
2.  **Install Dependencies:**
    ```bash
    pip install streamlit bibtexparser pandas
    ```
3.  **Run the Application:**
    ```bash
    streamlit run bibtex_app.py
    ```

## Dependencies

-   [Streamlit](https://streamlit.io/): For creating the web application.
-   [Streamlit-Modal](https://pypi.org/project/streamlit-modal/): For displaying the JSON data in a popup modal.  
    Future: Consider [st.dialog](https://docs.streamlit.io/develop/api-reference/execution-flow/st.dialog)
-   [bibtexparser](https://pypi.org/project/bibtexparser/): For parsing BibTeX files.
-   [pandas](https://pandas.pydata.org/): For data manipulation and CSV conversion.

## Logging

The application logs events and errors to the `app.log` file.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

[MIT License]