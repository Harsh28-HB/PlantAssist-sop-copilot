
# BiztelAI Assignment: Manufacturing SOP AI Copilot

## 1. Understand the User

### Who is the user?

The primary user is a shop-floor supervisor working at a manufacturing plant. The supervisor needs to access information related to quality inspection, machine maintenance, and workplace safety.

For this assignment, I am assuming the supervisor coordinates with machine operators, quality inspectors, and maintenance technicians during daily operations.

### What are they trying to do?

The supervisor wants to find accurate information from company SOPs, manuals, and procedures without manually searching through multiple PDF documents.

Typical information needs include:

- Understanding machine alarms and operating parameters.
- Checking preventive maintenance procedures.
- Finding incoming material inspection requirements.
- Verifying safety procedures such as Lockout/Tagout (LOTO).
- Identifying the correct document revision before acting on information.

### What frustrates them today?

The following are my assumptions about the challenges faced by a shop-floor supervisor:

- Searching through multiple PDF documents can take time.
- Finding the correct and latest document revision can be confusing.
- Technical information may be difficult to locate during a busy shift.
- Important instructions may be missed when documents are lengthy.
- Answers without clear references are difficult to verify.
- Incorrect or outdated safety and maintenance instructions could create operational risks.

### Assumptions

- The supervisor has access to a laptop, tablet, or smartphone connected to the plant network.
- The company has a collection of digital SOPs and equipment manuals.
- Supervisors need short, direct answers supported by official documents.
- The AI copilot is an information assistant and does not replace approved procedures, training, or supervisor authorization.
- The supervisor should be able to verify the original document and page before acting.

## 2. User Journey

### Step-by-step journey


1. **Open the application:** The supervisor opens the AI copilot using a mobile phone, tablet, or laptop connected to the plant network.

2. **Enter a question:** The supervisor types a question in simple language. For example, they might ask what to do when a TX-200 CNC machine displays alarm AL-104.

3. **Search the documents:** The application searches the available manufacturing SOPs and manuals to find information related to the question.

4. **Retrieve relevant information:** The system identifies the most relevant document sections and uses them to prepare an answer.

5. **Display the answer:** The copilot provides a short and understandable response along with the document name, revision number, and page number.

6. **Verify the information:** The supervisor can check the cited document and confirm that the information is relevant before taking action. For important safety and maintenance activities, they must continue to follow the approved plant procedures.

7. **Handle missing information:** If the requested information is not available in the supplied documents, the copilot clearly says that it could not find a reliable answer instead of guessing.

8. **Handle conflicting information:** If different document revisions contain different instructions, the application should identify the revision difference and prioritize the applicable current revision. The supervisor should verify the latest controlled copy in the QMS before acting.


### Possible Problems and Risks

- **Outdated document retrieval:** The application might retrieve information from an older SOP revision instead of the latest revision. For example, QC-SOP-014 Rev 03 and Rev 04 have different sampling requirements.

- **Incorrect answers:** The AI might misunderstand a question or generate information that is not supported by the source documents.

- **Missing information:** A supervisor might ask a question that the available PDFs cannot answer. The application should not invent an answer.

- **Incorrect source references:** The application might display an answer with the wrong document name, revision, or page number.

- **PDF extraction problems:** Important information in tables, technical values, or formatting might not be extracted correctly.

- **Network or application failure:** The supervisor might be unable to access the copilot because of a network problem or application error.

- **Safety risks:** A supervisor might depend entirely on an AI-generated response without checking the official safety procedure or confirming that they are authorized to perform the activity.

To reduce these risks, the application should provide source references, identify document revisions, avoid unsupported answers, and remind users to verify safety-critical instructions against the latest approved procedures.



## 3. AI Challenge

### AI Tool Used
ChatGPT

### Key Points from the AI Critique

I asked ChatGPT to review my proposed user journey from the perspective of a skeptical product manager.

The following concerns were highlighted:

1. **Document revision handling:** How will the application identify the correct document revision and avoid retrieving outdated instructions?

2. **Ambiguous questions:** What happens when a supervisor asks an unclear question, such as "The machine pressure is low"? The application should ask for clarification instead of providing a potentially incorrect answer.

3. **Safety and reliability:** How can supervisors verify safety-related answers before acting on them? Source citations alone may not prevent incorrect interpretation.

4. **Network availability:** What happens if the supervisor loses Wi-Fi connectivity while using the application?

5. **Source transparency:** Answers should include the document name, revision number, page number, and supporting information so that supervisors can verify them.

### My Reflection

I agreed with most of the feedback, especially the concerns about outdated documents, source verification, and safety.

The feedback helped me realise that retrieving information is not enough. The application must also identify the correct document revision and provide evidence for its answers.

I had not considered ambiguous questions in sufficient detail. A question about low pressure could refer to different machine parameters, so the application should avoid making assumptions when the question is unclear.

I also understood that the AI copilot should support the supervisor rather than replace approved procedures or human authorization.

Based on this feedback, I decided to prioritise revision-aware document retrieval, clear source references, and a fallback response when information is unavailable.



## 4. Improvement Added and Why I Chose It

### Revision-Aware Retrieval and Source References

The improvement I selected was revision-aware document retrieval combined with source references.

While reviewing the supplied documents, I noticed that QC-SOP-014 had two different versions: Revision 03 and Revision 04. These versions contain different inspection requirements.

To reduce the risk of retrieving outdated information, I added logic to identify the highest revision available for each document number. For normal operational questions, older revisions are excluded from retrieval when a higher revision is available.

I also improved the answer presentation to display:

- Source document name and document number.
- Document revision.
- Page number.
- Relevant supporting passages.
- A clear response when sufficient evidence is unavailable.

I chose this improvement because manufacturing supervisors need to verify where information comes from, especially when dealing with quality, maintenance, and safety procedures.

The system only compares revisions among the supplied PDFs. It cannot independently verify whether a document is the latest officially approved version in the plant's QMS.

### Why This Improvement Matters

This improvement makes the application more transparent and reduces the possibility of relying on outdated instructions. It also allows supervisors to verify the original document instead of depending entirely on an AI-generated response.

## 5. Final Reflection

### What I Would Build Next

If I continued developing this application, I would work on semantic search using embedding-based retrieval, document upload and automatic indexing, conversation history, and improved support for tables and scanned PDFs.

I would also explore offline document access because shop-floor supervisors may not always have a reliable network connection.

### What I Am Unsure About

I would like to understand how frequently the manufacturing plant updates its SOPs and who is responsible for approving new revisions.

I am also unsure about the expected response time, the level of detail supervisors prefer, and whether different employees should have different access permissions.

### Questions I Would Ask the Customer

1. How are approved SOP revisions maintained and distributed across the plant?
2. Should the application support different access levels for operators, supervisors, and maintenance technicians?
3. What is the acceptable response time for questions during a shift?
4. Should the copilot support offline access when the plant network is unavailable?
5. How should the system handle tables, images, scanned documents, and conflicting procedures?

### Biggest Challenge I Faced

One of the biggest challenges was connecting the language model to the document retrieval pipeline.

I initially used the OpenAI API, but I encountered an API authentication issue followed by an exhausted-credit error. I then switched to Google Gemini to continue development without depending on additional OpenAI API credits.

I also encountered a retrieval issue where the application could not initially find the correct information about rejected material storage. I reviewed the retrieval threshold and adjusted it from 0.08 to 0.02, which allowed the relevant document passage to be retrieved.

Another challenge was handling document revisions and making sure the answers displayed useful source references. I addressed this by retaining revision and page metadata throughout PDF processing and retrieval.

### Testing and Deployment

I tested the application using the five questions provided in the assignment and five additional questions of my own.

The tests covered machine maintenance, quality inspection, safety procedures, document revision handling, and a question that the supplied documents could not answer.

The application currently runs locally using FastAPI and Uvicorn. It has been tested through a desktop browser. Local network access from a second device is a remaining demonstration step.

### What I Learned

This assignment helped me understand how document-based AI assistants work beyond simply sending a question to an LLM.

I gained practical experience with PDF processing, text chunking, TF-IDF retrieval, cosine similarity, API integration, prompt design, source references, and frontend-backend integration.

Most importantly, I learned that a useful AI assistant should not only provide answers but also communicate uncertainty and avoid generating unsupported information.

