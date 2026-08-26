# How OCR and Documents Works

Extract text and structure from PDFs and scans using OCR and document parsers.

![Detailed systems blueprint for OCR and Documents](../assets/system-blueprint.png)

## Stages

### 1. Inspect file type page count and quality

**Primary surface:** `PDF or scanned images`

Record the input, operation, observable output, and any decision that changes scope. Stop here if the output is missing, contradictory, or insufficient for the next stage.
### 2. Render pages at OCR-safe resolution

**Primary surface:** `Page rasterizer`

Record the input, operation, observable output, and any decision that changes scope. Stop here if the output is missing, contradictory, or insufficient for the next stage.
### 3. Detect text blocks tables and reading order

**Primary surface:** `OCR and layout detector`

Record the input, operation, observable output, and any decision that changes scope. Stop here if the output is missing, contradictory, or insufficient for the next stage.
### 4. Recognize text with confidence values

**Primary surface:** `Structured text normalizer`

Record the input, operation, observable output, and any decision that changes scope. Stop here if the output is missing, contradictory, or insufficient for the next stage.
### 5. Normalize headings paragraphs and tables

**Primary surface:** `Searchable export`

Record the input, operation, observable output, and any decision that changes scope. Stop here if the output is missing, contradictory, or insufficient for the next stage.
### 6. Export searchable text with page references

**Primary surface:** `Searchable export`

Record the input, operation, observable output, and any decision that changes scope. Stop here if the output is missing, contradictory, or insufficient for the next stage.

## Failure handling

- **Authorization failure:** do not probe credentials or broaden access; report the missing authority.
- **Target ambiguity:** stop before mutation and request the minimum identifying information.
- **Tool or service failure:** retain error evidence, retry only safe transient failures, and cap retries.
- **Verification failure:** classify the run as incomplete even when the preceding operation returned success.

## Completion evidence

The handoff should contain the original request, inspection state, preview or plan, exact execution result, direct verification, and a final receipt naming limitations and withheld actions.
