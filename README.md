# PlantAssist 2.0 – Manufacturing SOP AI Copilot

An AI-powered manufacturing knowledge assistant that helps shop-floor supervisors quickly find reliable information from Standard Operating Procedures (SOPs), maintenance manuals, and safety documents.

**Built for:** BiztelAI Technologies – Full Stack Engineer Internship Assignment

**Repository:** https://github.com/Harsh28-HB/PlantAssist-sop-copilot

---

## 1. Project Overview

Manufacturing shop-floor supervisors regularly need to refer to multiple PDF documents to find information about machine maintenance, quality inspections, and workplace safety procedures.

Searching through lengthy documents during a busy shift can be time-consuming. It can also be difficult to identify the correct document revision and verify whether an instruction is supported by an official source.

PlantAssist addresses this problem through a simple AI-powered interface where supervisors can ask questions in natural language and receive answers based on the supplied manufacturing documents.

The application uses Retrieval-Augmented Generation (RAG) to retrieve relevant document passages and Google Gemini to generate answers using the retrieved context.

When the supplied documents do not contain sufficient information, the application is designed to communicate that limitation rather than invent an answer.

## 2. Key Features

- **Natural-language question answering:** Ask questions about manufacturing procedures in everyday language.
- **PDF processing:** Extract text from manufacturing SOPs and manuals.
- **RAG-based retrieval:** Find relevant document passages using TF-IDF and cosine similarity.
- **AI-powered responses:** Generate document-grounded answers using Google Gemini.
- **Source references:** Display document name, revision, page number, and supporting passages.
- **Revision awareness:** Identify the highest available revision for each document number among the supplied PDFs.
- **Unsupported-question handling:** Provide a fallback when sufficient supporting information cannot be found.
- **Responsive interface:** Designed for desktop, tablet, and mobile browsers.
- **Expandable source cards:** Allow users to inspect the retrieved document excerpts.
- **Safety reminders:** Reinforce that AI answers do not replace approved manufacturing procedures or authorization.

## 3. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend Framework | FastAPI |
| Application Server | Uvicorn |
| PDF Processing | PyMuPDF |
| Text Retrieval | Scikit-learn TF-IDF |
| Similarity Measurement | Cosine Similarity |
| AI Model | Google Gemini |
| AI SDK | Google GenAI SDK |
| Frontend | HTML5, CSS3, JavaScript |
| Configuration | Python-dotenv |
| Version Control | Git and GitHub |

## 4. Project Architecture

The application follows a document-retrieval and answer-generation workflow.

1. **Document ingestion:** The PDF processor reads the supplied manufacturing documents.
2. **Text extraction:** Text is extracted page by page using PyMuPDF.
3. **Text chunking:** Extracted text is divided into smaller overlapping chunks.
4. **Metadata extraction:** Document numbers, revision information, filenames, and page numbers are retained.
5. **Document retrieval:** TF-IDF converts document passages into searchable numerical representations.
6. **Similarity search:** Cosine similarity identifies passages relevant to the user's question.
7. **Answer generation:** Retrieved passages are provided to Gemini as supporting context.
8. **Source presentation:** The frontend displays the generated answer with supporting document references.

### Architecture Flow

```text
             Shop-floor Supervisor
                      |
                      v
             PlantAssist Web UI
                HTML / CSS / JS
                      |
                      v
                 FastAPI
                      |
                      v
              RAG Retrieval Engine
                      |
              TF-IDF + Cosine
                      |
                      v
              Relevant PDF Chunks
                      |
                      v
              Google Gemini API
                      |
                      v
              Generated Answer
                      |
                      v
            Answer + Source Cards
```

## 5. Project Structure

```text
PlantAssist-sop-copilot/
|
|-- app/
|   |-- __init__.py
|   |-- main.py
|   |-- rag.py
|   |-- pdf_processor.py
|
|-- documents/
|   |-- MNT-MAN-CNC-02_TX-200_Preventive_Maintenance.pdf
|   |-- QC-SOP-014_Rev03_Incoming_Material_Inspection.pdf
|   |-- QC-SOP-014_Rev04_Incoming_Material_Inspection.pdf
|   |-- SAF-SOP-003_Lockout_Tagout_Procedure.pdf
|
|-- templates/
|   |-- index.html
|
|-- static/
|   |-- style.css
|   |-- favicon.svg
|
|-- README.md
|-- THINKING.md
|-- requirements.txt
|-- .env.example
|-- .gitignore
```

## 6. Installation and Setup

### Prerequisites

- Python 3.11 or later
- Visual Studio Code
- Git
- Google Gemini API key
- Internet connectivity for Gemini API requests

### Step 1: Clone the repository

```bash
git clone https://github.com/Harsh28-HB/PlantAssist-sop-copilot.git

cd PlantAssist-sop-copilot
```

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

### Step 3: Activate the virtual environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 4: Install the dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 5: Configure environment variables

Create a `.env` file in the root project directory.

Add:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

Obtain an API key from:

https://aistudio.google.com/api-keys

**Security:** Never upload your actual `.env` file or API key to GitHub.

### Step 6: Run the application

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Wait for the following message:

```text
Application startup complete.
```

### Step 7: Open PlantAssist

Application:

http://localhost:8000

Health check:

http://localhost:8000/health

## 7. Sample Questions and Test Results

The application was evaluated using the five sample questions provided in the assignment and five additional questions.

### A. Questions Provided by BiztelAI

**Question 1: What is the recommended coolant concentration for the TX-200 CNC turning centre?**

Expected answer: The recommended coolant concentration is **6–8%**, checked using a refractometer with a 1.0 factor.

Source: MNT-MAN-CNC-02, Revision 02, Page 1.

**Question 2: The machine is showing alarm AL-104. What does it mean and what should the operator do?**

Expected answer: AL-104 indicates low way lube oil level. Top up using ISO VG 68 oil to the MAX mark and press RESET. The manual states that the machine can continue after reset.

Source: MNT-MAN-CNC-02, Revision 02, Page 2.

**Question 3: Who is allowed to remove a lockout lock from a machine?**

Expected answer: Each authorised person must remove only their own personal lock. Another person's lock must not be removed outside the documented special absence procedure.

Source: SAF-SOP-003, Revision 05, Page 1.

**Question 4: What is the outer diameter tolerance for the BH-220 bearing housing?**

Expected answer: The nominal outer diameter is 90.000 mm with a tolerance of ±0.050 mm.

Source: QC-SOP-014, Revision 04, Page 2.

**Question 5: How often should spindle runout be checked, and who does it?**

Expected answer: Spindle runout should be checked monthly by a maintenance technician.

Source: MNT-MAN-CNC-02, Revision 02, Page 1.

### B. Five Additional Questions

**Question 6: What should happen if the supplier's Material Test Certificate (MTC) is missing?**

Expected answer: The incoming material lot must be placed on HOLD and must not be inspected or accepted until the mandatory MTC is received.

Source: QC-SOP-014, Revision 04, Page 2.

**Question 7: How many samples should be inspected for a lot size of 1,000 pieces?**

Expected answer: 32 samples must be inspected. A lot size of 1,000 falls within the 501–3,200 sampling range.

Source: QC-SOP-014, Revision 04, Page 1.

**Question 8: What is the warranty period for the TX-200 CNC machine?**

Expected answer: The supplied documents do not contain enough information to answer this question.

Expected system behaviour: The copilot should communicate that the information is unavailable rather than generating an unsupported warranty period.

**Question 9: Where should rejected incoming materials be stored?**

Expected answer: Rejected incoming materials must be tagged with a RED tag and moved to Quarantine Cage Q1, Stores Bay 3.

The cage is locked, and the key is held by the Shift QC Supervisor.

Source: QC-SOP-014, Revision 04, Page 2.

**Question 10: What is the procedure if an authorised person leaves the plant without removing their lock?**

Expected answer:

1. The Shift Supervisor makes reasonable efforts to contact the lock owner.
2. If the owner cannot be reached, both the Production Manager and Safety Officer must authorize removal.
3. The machine must be physically inspected to confirm that it is safe to re-energise.
4. The removal must be recorded on form SF-12.
5. The lock owner must be informed before resuming work on their next shift.

Source: SAF-SOP-003, Revision 05, Pages 1–2.

## 8. Revision-Aware Document Retrieval

One important issue identified during document analysis was that two versions of QC-SOP-014 were supplied:

- QC-SOP-014 Revision 03
- QC-SOP-014 Revision 04

The two versions contain different inspection requirements.

PlantAssist includes logic to identify the highest revision available for each document number and exclude older revisions from normal operational retrieval when a higher revision is present.

The application retains the document revision and page information for source verification.

**Limitation:** The application compares only the supplied documents. It cannot independently verify whether a document is the latest officially approved version in the manufacturing plant's Quality Management System (QMS).

## 9. Reliability and Safety

The application is designed to provide supporting information rather than replace human decision-making.

Important reliability considerations include:

- Answers should be based on retrieved document passages.
- Unsupported questions should receive an explicit fallback response.
- Source documents and page references should remain visible.
- Older revisions should not be used for normal operational retrieval when a newer supplied revision is available.
- Safety-related instructions must be verified against the latest approved controlled procedure.
- The copilot does not provide authorization to perform maintenance or safety-related activities.

## 10. Limitations

- Retrieval currently uses TF-IDF and cosine similarity rather than semantic embedding-based search.
- PDF extraction primarily handles selectable text. Scanned documents and complex layouts may require additional processing.
- Tables and technical formatting may not always be extracted perfectly.
- Revision selection is based on the available supplied files and does not connect to the plant's QMS.
- Answer generation depends on Gemini API availability and internet connectivity.
- The application does not currently provide offline AI answer generation.
- AI-generated responses require verification against the original manufacturing documents.

## 11. Future Improvements

Possible future enhancements include:

- Semantic retrieval using embedding-based search.
- Support for scanned PDFs and OCR.
- Automatic document upload, indexing, and revision management.
- Integration with an organization's QMS.
- Offline access to approved reference documents.
- User authentication and role-based access control.
- Conversation history and follow-up questions.
- Improved retrieval evaluation and answer-quality monitoring.
- More detailed source highlighting and document navigation.

## 12. Screenshots and Demonstration

Application screenshots and the final demonstration recording will be added here.

**Demo video:** To be added.

## 13. Disclaimer

PlantAssist is an internship assignment prototype built using fictional manufacturing documents.

It is an information assistant and does not replace official manufacturing procedures, approved safety instructions, formal training, or authorization.

Users must verify safety-critical information against the latest approved controlled documents before taking action.

---

**Developed by:** Harsh Biradar  
**Project:** PlantAssist – Manufacturing SOP AI Copilot  
**Assignment:** BiztelAI Technologies – Full Stack Engineer Internship
