import streamlit as st
import bibtexparser
import pandas as pd
import json
import io
import logging
import re
import base64
from streamlit_modal import Modal

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

log_handler = logging.FileHandler('app.log', mode='w')
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger = logging.getLogger(__name__)
logger.addHandler(log_handler)

# Function to parse BibTeX data
def parse_bibtex(bibtex_content):
    """Parses BibTeX content and returns a list of entries."""
    logger.debug("Starting BibTeX parsing")
    try:
        bib_database = bibtexparser.loads(bibtex_content)
        logger.debug("BibTeX parsing successful")
        return bib_database.entries
    except Exception as e:
        logger.error(f"Error parsing BibTeX: {e}")
        st.error(f"Error parsing BibTeX: {e}")
        return None

# Function to extract DOIs
def extract_dois(entries):
    """Extracts DOIs from BibTeX entries."""
    logger.debug("Starting DOI extraction")
    try:
        #dois = [entry.get('doi', None) for entry in entries]
        #dois = [doi for doi in dois if doi]
        #logger.debug(f"Extracted DOIs: {dois}")
        #return dois
        return [entry.get("doi") for entry in entries if entry.get("doi")]
    except Exception as e:
        logger.error(f"Error extracting DOIs: {e}")
        st.error(f"Error extracting DOIs: {e}")
        return []
    logger.debug(f"Extracted DOIs: {dois}")

# Function to convert to CSV
def to_csv(entries):
    """Converts BibTeX entries to CSV format."""
    logger.debug("Starting CSV conversion")
    try:
        df = pd.DataFrame(entries)
        # Ensure year is an integer
        if 'year' in df.columns:
            df['year'] = pd.to_numeric(df['year'], errors='coerce').fillna(0).astype(int)
        csv_data = df.to_csv(index=False, float_format='%.0f').encode('utf-8')
        logger.debug("CSV conversion successful")
        return csv_data
    except Exception as e:
        logger.error(f"Error converting to CSV: {e}")
        st.error(f"Error converting to CSV: {e}")
        return None

# Function to convert to JSON
def to_json(entries):
    """Converts BibTeX entries to JSON format."""
    logger.debug("Starting JSON conversion")
    try:
        json_data = json.dumps(entries, indent=4).encode('utf-8')
        logger.debug("JSON conversion successful")
        return json_data
    except Exception as e:
        logger.error(f"Error converting to JSON: {e}")
        st.error(f"Error converting to JSON: {e}")
        return None

# Function to create a download button
def download_button(file_data, file_name, button_label, mime_type):
    logger.debug(f"Creating download button for {file_name}")
    st.download_button(
        label=button_label,
        data=file_data,
        file_name=file_name,
        mime=mime_type
    )
    logger.debug(f"Download button created for {file_name}")

# Function to display JSON in a modal
#def show_json_modal(json_data):
#def show_json_modal(json_data, key_prefix=None):
#def ModalComponent(json_data, json_preview_entries_count, key_prefix=None): # this all component is handled and passed json string including default styling. Also fixes state via function arguments and will reuse all those functions as  pure methods, where all  code can follow using standard procedural coding-style from component's own logic using helper methods. That is way a UI/rendering has better reliability in apps
#def ModalComponent(json_data, json_preview_entries_count=2, key_prefix=None):
#def show_json_modal(json_data, json_preview_entries_count=2 ,key_prefix=None):  # UI state , all  local + callback (where python UI does session) by html component UI methods + proper data handling format (also edge handling of bad json/string) including their type format checking via these all method scopes.
#def show_json_modal(json_data, json_preview_entries_count=2, key_prefix=None): # Component (function  type) based local state variable management and  UI styles handling (from that all layout + string parsing type formatting using that scopes via method /function calls via methods.
def show_json_modal(json_data, json_preview_entries_count=2, key_prefix=None):
    """Displays formatted parsed JSON in a modal using streamlit_modal."""

    if key_prefix is None:
        key_prefix = str(hash(json_data))
    modal_key = f"modal_{key_prefix}"
    show_button_key = f"show_button_{key_prefix}"
    close_button_key = f"close_button_{key_prefix}"
    is_modal_open_key = f"is_modal_open_{key_prefix}"

    if is_modal_open_key not in st.session_state:
        st.session_state[is_modal_open_key] = False

    def format_json_content(json_data_text, count_from_component_var):
        """Formats JSON data for display, handling errors and escaping"""
        try:
            json_obj = json.loads(json_data_text)
            if isinstance(json_obj, list):
                return json.dumps(json_obj[:count_from_component_var], indent=4).replace('\\', '\\\\')
            elif isinstance(json_obj, dict):
                return json.dumps(json_obj, indent=4).replace('\\', '\\\\')
            else:
                return f"Invalid JSON format. Type: {type(json_data_text)}. Check data and layout."
        except (json.JSONDecodeError, TypeError) as e:
            return f"Error formatting JSON. Raw Input: {repr(json_data_text)}, Reason: {str(e)}"

    if not st.session_state[is_modal_open_key]:
        st.button("View Full JSON", key=show_button_key, on_click=lambda: st.session_state.__setitem__(is_modal_open_key, True))
    else:
        modal = Modal(title="JSON Preview", key=modal_key)
        with modal.container():
            '''st.markdown(
                f"""
                <div style="max-height:60vh; overflow-y:auto;">
                    <pre style="white-space:pre-wrap; word-break:break-word; color:var(--text-color);">
                        {format_json_content(json_data, json_preview_entries_count)}
                    </pre>
                </div>
                """,
                unsafe_allow_html=True,
            )'''
            st.code(
                format_json_content(json_data, json_preview_entries_count),
                language='json')
        if modal.is_open():
            st.session_state[is_modal_open_key] = True
        else:
            st.session_state[is_modal_open_key] = False



def extract_bibtex_entries(bibtex_content, preview_entries_count):
    """
    Extracts a specified number of BibTeX entries from a string.

    Args:
        bibtex_content (str): The BibTeX content string.
        preview_entries_count (int): The number of entries to extract.

    Returns:
        str: A string containing the extracted BibTeX entries, or an empty string if no entries are found.
    """
    #entry_pattern = re.compile(r'(@[a-zA-Z]+\{[^}]*?\}(?:},|},\\n|$))', re.DOTALL)
    regex_p = r'(@[^@]*?)(?=@[^@]|$)'
    entry_pattern = re.compile(regex_p, re.DOTALL)
    entries = entry_pattern.findall(bibtex_content)
    logger.debug(f"[extract_bibtex_entries]: entries: {entries}")
    logger.debug(f"[extract_bibtex_entries]: entries: {entries[:2]}")
    
    if not entries:
        return ""
    
    limited_entries = entries[:preview_entries_count]
    #logger.debug(f"[extract_bibtex_entries]: limited_entries: {"\n".join(limited_entries)}")
    logger.debug(f"[extract_bibtex_entries]: limited_entries:")
    return "\n".join(limited_entries)

# Function to process BibTeX data and update session state
def process_bibtex_data(bibtex_content, preview_entries_count=None):
    with st.spinner("Processing BibTeX data..."):
        try:
            #entries = parse_bibtex(bibtex_content)
            if preview_entries_count:
                limited_bibtex_content = extract_bibtex_entries(bibtex_content, preview_entries_count)
                #logger.debug(f"[Process Preview] limited_bibtex_content: {limited_bibtex_content}") #{limited_bibtex_content[:100]}")  # Show first 100 characters
                logger.debug(f"[Process Preview] limited_bibtex_content count: {len(limited_bibtex_content)}")
                entries = parse_bibtex(limited_bibtex_content)
                #logger.debug(f"[Process Preview] entries: {entries}")  #{entries[:1]}")
                logger.debug(f"[Process Preview] entries count: {len(entries)}")
            else:
                entries = parse_bibtex(bibtex_content)
                logger.debug(f"[Process All] entries: {entries[:1]}")
                logger.debug(f"[Process All] entries count: {len(entries)}")
            if entries:
                csv_data = to_csv(entries)
                json_data = to_json(entries)
                doi_list = extract_dois(entries)
                logger.info("Download options displayed")
                return entries, csv_data, json_data, doi_list
            else:
                return None, None, None, None
        except Exception as e:
            logger.error(f"Error processing BibTeX data: {e}")
            st.error(f"Error processing BibTeX data: {e}")
            return None, None, None, None

# Function to display download and preview options
def display_results(entries, csv_data, json_data, doi_list, preview_entries_count):
    if entries:
        # Download options
        st.header("Download")
        col1, col2, col3 = st.columns(3)
        with col1:
            if csv_data:
                download_button(csv_data, "bibtex_output.csv", "Download CSV", "text/csv")
        with col2:
            if json_data:
                download_button(json_data, "bibtex_output.json", "Download JSON", "application/json")
        with col3:
            if doi_list:
                doi_text = "\n".join(doi_list).encode('utf-8')
                download_button(doi_text, "dois.txt", "Download DOIs txt", "text/plain")

        # Preview options
        st.header("Preview")
        preview_count = st.number_input("Enter number of records to preview (max 50)", min_value=1, max_value=50, value=2, step=1)

        # Preview CSV
        st.subheader("CSV Preview")
        if csv_data:
            df_preview = pd.read_csv(io.BytesIO(csv_data))
            # Format year column for display
            if 'year' in df_preview.columns:
                #assist: https://stackoverflow.com/a/76236399/20107918 | https://discuss.streamlit.io/t/date-format-mm-dd-yy-to-yy-mm-dd/34334
                #df_preview['year'] = df_preview['year'].astype(int)
                df_preview['year'] = pd.to_datetime(df_preview['year'], format="%Y").dt.strftime("%Y")                
            st.dataframe(df_preview.head(preview_count))

        # Preview JSON
        st.subheader("JSON Preview")
        if json_data:
            show_json_modal(json_data, preview_count)
            #show_json_modal(json_data[:preview_count])

        # Preview DOI
        st.subheader("DOI Preview")
        if doi_list:
            st.text("\n".join(doi_list[:preview_count]))

# Main Streamlit app
def main():
    st.title("BibTeX Converter")
    logger.info("App started")

    st.markdown("""
        <p>
            This app converts BibTeX files into CSV, JSON, and extracts DOIs into a text file.
            You can upload one or more BibTeX files, or paste the BibTeX content directly.
            The app will combine all the content into a single dataset.
        </p>
    """, unsafe_allow_html=True)

    # Initialize session state
    if 'all_bibtex_content' not in st.session_state:
        st.session_state['all_bibtex_content'] = ""
    if 'preview_entries' not in st.session_state:
        st.session_state['preview_entries'] = None
    if 'preview_csv_data' not in st.session_state:
        st.session_state['preview_csv_data'] = None
    if 'preview_json_data' not in st.session_state:
        st.session_state['preview_json_data'] = None
    if 'preview_doi_list' not in st.session_state:
        st.session_state['preview_doi_list'] = None
    if 'all_entries' not in st.session_state:
        st.session_state['all_entries'] = None
    if 'all_csv_data' not in st.session_state:
        st.session_state['all_csv_data'] = None
    if 'all_json_data' not in st.session_state:
        st.session_state['all_json_data'] = None
    if 'all_doi_list' not in st.session_state:
        st.session_state['all_doi_list'] = None
    if 'preview_count' not in st.session_state:
        st.session_state['preview_count'] = 2

    uploaded_files = st.file_uploader(
        "Drag and drop BibTeX file(s) here. Limit 50MB per file .BIB",
        type=["bib"],
        accept_multiple_files=True,
        help="Upload one or more BibTeX files (.bib). Maximum 50MB per file.",
    )
    bibtex_text = st.text_area("Or paste BibTeX content here")

    if uploaded_files or bibtex_text:
        if uploaded_files:
            for uploaded_file in uploaded_files:
                st.session_state['all_bibtex_content'] += uploaded_file.read().decode('utf-8')
        if bibtex_text:
            st.session_state['all_bibtex_content'] += bibtex_text
        logger.info("BibTeX content received")

    if st.session_state['all_bibtex_content']:
        # Option to process a limited number of entries
        preview_entries_count = st.number_input("Process a limited number of entries for preview (default 5)", min_value=1, value=5, step=1)

        if st.button("Process Preview"):
            st.session_state['preview_entries'], st.session_state['preview_csv_data'], st.session_state['preview_json_data'], st.session_state['preview_doi_list'] = process_bibtex_data(st.session_state['all_bibtex_content'], preview_entries_count)
            #display_results(st.session_state['preview_entries'], st.session_state['preview_csv_data'], st.session_state['preview_json_data'], st.session_state['preview_doi_list'], preview_entries_count)
        if st.session_state['preview_entries']:
            display_results(st.session_state['preview_entries'], st.session_state['preview_csv_data'], st.session_state['preview_json_data'], st.session_state['preview_doi_list'], preview_entries_count)

        if st.button("Process All"):
            st.session_state['all_entries'], st.session_state['all_csv_data'], st.session_state['all_json_data'], st.session_state['all_doi_list'] = process_bibtex_data(st.session_state['all_bibtex_content'])
            display_results(st.session_state['all_entries'], st.session_state['all_csv_data'], st.session_state['all_json_data'], st.session_state['all_doi_list'], preview_entries_count)

if __name__ == "__main__":
    main()