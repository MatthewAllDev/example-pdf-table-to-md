# PDF to Markdown Table Export with Translation Example

This repository contains an example of extracting tables from PDF files, converting them to Markdown, and performing text translation.

## Description

The example provides:
- Reading tables from PDF.
- Converting tables to Markdown format.
- Translating text using various translators.

### Supported Translators:
1. **GoogleTranslator**.
2. **ArgosTranslator**.
3. **[LibreTranslator](https://github.com/LibreTranslate/LibreTranslate)** (default - requires setup).

## Installation

1. Clone the repository:
   ```bash
   git clone {URL}
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   - **ArgosTranslator**: to use it, install `argostranslate`.
   - **GoogleTranslator**: to use it, install `googletrans` and `httpx`.
   - **LangDetector**: to use it, install `fasttext`.
