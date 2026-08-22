# Evaluation & Sample Questions

This document contains sample questions to test the RAG system's capabilities, including its ability to retrieve specific facts and gracefully reject unanswerable questions (hallucination prevention).

## Answerable Questions (Simple Retrieval)

### 1. Paid Time Off
**Question**: How many days of paid time off do employees accrue?
**Expected Behavior**: Retrieve the PTO section from the Employee Handbook and state 21 days or 1.75 days/month.
**Actual Answer**: Full-time employees accrue 1.75 days of PTO per month.
**Sources**: `Employee_Handbook.pdf` (Page 2, Chunk: `Employee_Handbook.pdf_p2_c0`), `Onboarding_Guide.pdf` (Page 3, Chunks: `Onboarding_Guide.pdf_p3_c2`, `Onboarding_Guide.pdf_p3_c1`)

### 2. API Authentication
**Question**: How do I authenticate API requests?
**Expected Behavior**: State that a Bearer token is required in the Authorization header.
**Actual Answer**: All API requests require a Bearer token in the Authorization header. Tokens are issued via the /oauth/token endpoint.
**Sources**: `API_Reference.pdf` (Page 2, Chunk: `API_Reference.pdf_p2_c0`)

### 3. File Deletion
**Question**: How long do deleted files stay in the trash via the API?
**Expected Behavior**: State 30 days.
**Actual Answer**: Deleted files remain recoverable via /v2/trash for 30 days.
**Sources**: `API_Reference.pdf` (Page 3, Chunk: `API_Reference.pdf_p3_c0`), `Security_Policy.pdf` (Page 3, Chunk: `Security_Policy.pdf_p3_c0`), `API_Reference.pdf` (Page 2, Chunk: `API_Reference.pdf_p2_c1`)

### 4. Company Name
**Question**: What is the name of the company?
**Expected Behavior**: State Atman Cloud Consultancy.
**Actual Answer**: "I couldn't find enough relevant information in the provided documents to answer this question." *(Note: Failed due to `TOP_K=3` restricting retrieval spread for this highly generalized query)*
**Sources**: None (Filtered by similarity threshold).

### 5. Onboarding
**Question**: What happens on the first day of onboarding?
**Expected Behavior**: Retrieve the first-day schedule from the Onboarding Guide.
**Actual Answer**: On the first day of onboarding, which is a Monday, company-wide orientation takes place.
**Sources**: `Onboarding_Guide.pdf` (Page 3, Chunk: `Onboarding_Guide.pdf_p3_c0`), `Onboarding_Guide.pdf` (Page 1, Chunk: `Onboarding_Guide.pdf_p1_c0`), `Onboarding_Guide.pdf` (Page 2, Chunk: `Onboarding_Guide.pdf_p2_c0`)

### 6. Support SLAs
**Question**: What is the guaranteed uptime in the SLA?
**Expected Behavior**: Retrieve uptime percentage from the Pricing and SLA document.
**Actual Answer**: The guaranteed uptime in the SLA is:
*   **Free:** Best effort, no guarantee
*   **Standard:** 99.5% monthly uptime
*   **Enterprise:** 99.95% monthly uptime
**Sources**: `Pricing_and_SLA.pdf` (Page 2, Chunks: `Pricing_and_SLA.pdf_p2_c1`, `Pricing_and_SLA.pdf_p2_c0`), `Onboarding_Guide.pdf` (Page 3, Chunk: `Onboarding_Guide.pdf_p3_c2`)

---

## Complex Retrieval (Requires careful chunk matching)

### 7. API Permanent Deletion
**Question**: How do I bypass the trash and permanently delete a file using the API?
**Expected Behavior**: State that you must append `?permanent=true` to the delete request.
**Actual Answer**: To bypass the trash and permanently delete a file, use the `DELETE /v2/files/{file_id}` endpoint and pass `?permanent=true`.
**Sources**: `API_Reference.pdf` (Page 3, Chunk: `API_Reference.pdf_p3_c0`), `API_Reference.pdf` (Page 2, Chunks: `API_Reference.pdf_p2_c1`, `API_Reference.pdf_p2_c0`)

### 8. PTO Accrual Start
**Question**: Does PTO accrue immediately when I start working?
**Expected Behavior**: State that it accrues from the first day of employment.
**Actual Answer**: PTO accrual begins on the employee's start date.
**Sources**: `Employee_Handbook.pdf` (Page 2, Chunk: `Employee_Handbook.pdf_p2_c0`), `Onboarding_Guide.pdf` (Page 3, Chunks: `Onboarding_Guide.pdf_p3_c2`, `Onboarding_Guide.pdf_p3_c0`)

---

## Unanswerable Questions (Testing Hallucination Prevention)

### 9. Out-of-Scope Fact
**Question**: What is the capital of Japan?
**Expected Behavior**: The system must reject the question because the Atman documents do not state this, even though the Gemini model inherently knows the answer.
**Actual Answer**: "I couldn't find enough relevant information in the provided documents to answer this question."
**Sources**: None (Filtered by similarity threshold).

### 10. Irrelevant Geography
**Question**: What is the weather in Pune today?
**Expected Behavior**: The system must reject the question immediately.
**Actual Answer**: "I couldn't find enough relevant information in the provided documents to answer this question."
**Sources**: None (Filtered by similarity threshold).
