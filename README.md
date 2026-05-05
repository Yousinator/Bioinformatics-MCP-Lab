# 🏥 Bioinformatics Lab: Clinical AI Assistant with MCP

Welcome to the Clinical AI Assistant Lab. In this session, you will explore **Agentic AI**, **Model Context Protocol (MCP)**, and **AI Observability**.

## 🚀 Lab Overview

You will run a local "Client" agent that connects to a "Central Lab Server" hosted by the instructor. The agent has access to real-time clinical tools:

- **FDA Drug Lookup**: Real warnings and usage data.
- **NIH RxNorm**: Real drug-drug interaction checking.
- **NCBI PubMed**: Peer-reviewed medical literature.
- **Hospital DB**: Patient records (P001, P002, P003).

---

## 🛠️ Step 1: Setup & API Keys

You need personal keys for the "Brain" and the "Observer":

1. **Groq API (The Brain)**:
   - Go to [console.groq.com](https://console.groq.com/).
   - Create an API Key.
2. **Langfuse (The Observer)**:
   - Go to [cloud.langfuse.com](https://cloud.langfuse.com/).
   - Create a project called "Bio-Lab".
   - Go to **Settings -> API Keys** and copy your Public and Secret keys.

---

## ⚙️ Step 2: Configuration

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to a new file named `.env`.
3. Paste your API keys into the `.env` file.
4. **CRITICAL**: Ask the instructor for the **ngrok URL** (https://3140-5-45-131-33.ngrok-free.app/sse) and paste it as `MCP_SERVER_URL`.

---

## 🧠 Step 3: Writing the System Prompt (Student Task)

Open `agent.py`. Locate the `SYSTEM_PROMPT` variable.
You must write the **Clinical Guidelines** for your agent. Consider:

- How should it identify itself?
- What are the rules for chest pain or emergencies?
- How should it handle drug interaction warnings?
- Should it ever prescribe specific doses?

**You must experiment with 3 different versions of this prompt.**

---

## 🏃 Step 4: Run & Observe

1. Start the lab:
   ```bash
   streamlit run app.py
   ```
2. Run these 3 queries and check **Langfuse** for the trace:
   - "I am patient P001. Is it safe for me to take Ibuprofen with my current meds?"
   - "What are the latest clinical findings on Metformin for kidney patients?" (PubMed check)
   - "Book an appointment for P003 in Cardiology tomorrow."

---

## 📝 Submission Requirements

Create a Word document with the following:

### Part A: Experimentation

1. **System Prompt Table**: Paste the three versions of the System Prompt you tried.
2. **Analysis**: Which prompt performed best? Why?

### Part B: Trace Evidence (Screenshots)

Include **at least 3 screenshots** from Langfuse showing the "Trace" (the internal thinking steps) for:

- A drug interaction check.
- A PubMed search.
- A patient history lookup.

### Part C: Research Questions

1. **Observability**: Based on the Langfuse trace, did the agent call the FDA tool before or after checking the patient's history? Why is this order important for safety?
2. **Bioinformatics**: How does connecting an AI to a real-time source like **RxNorm** compare to a standard LLM like ChatGPT (which only has data up to its training cutoff)?
3. **Clinical Safety**: Describe one scenario where the agent might give a dangerous answer. How did you try to prevent this in your System Prompt?
4. **MCP Architecture**: If the instructor adds a "Genomics" tool to the central server, do you need to change your code to use it? Explain why.

---

**Submission Format**: PDF or Word Document.
**Deadline**: End of Lab Session.
