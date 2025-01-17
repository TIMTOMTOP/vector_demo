[Anthropic home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/dark.svg)](/)

English

Search...

Ctrl K

Search...

Navigation

Build with Claude

PDF support

[Welcome](/en/home) [User Guides](/en/docs/welcome) [API Reference](/en/api/getting-started) [Prompt Library](/en/prompt-library/library) [Release Notes](/en/release-notes/overview) [Developer Newsletter](/en/developer-newsletter/overview)

You can now ask Claude about any text, pictures, charts, and tables in PDFs you provide. Some sample use cases:

- Analyzing financial reports and understanding charts/tables
- Extracting key information from legal documents
- Translation assistance for documents
- Converting document information into structured formats

## [​](\#before-you-begin)  Before you begin

### [​](\#check-pdf-requirements)  Check PDF requirements

Claude works with any standard PDF. However, you should ensure your request size meet these requirements when using PDF support:

| Requirement | Limit |
| --- | --- |
| Maximum request size | 32MB |
| Maximum pages per request | 100 |
| Format | Standard PDF (no passwords/encryption) |

Please note that both limits are on the entire request payload, including any other content sent alongside PDFs.

Since PDF support relies on Claude’s vision capabilities, it is subject to the same [limitations and considerations](/en/docs/build-with-claude/vision#limitations) as other vision tasks.

### [​](\#supported-platforms-and-models)  Supported platforms and models

PDF support is currently available on both Claude 3.5 Sonnet models ( `claude-3-5-sonnet-20241022`, `claude-3-5-sonnet-20240620`) via direct API access. This functionality will be supported on Amazon Bedrock and Google Vertex AI soon

* * *

## [​](\#process-pdfs-with-claude)  Process PDFs with Claude

### [​](\#send-your-first-pdf-request)  Send your first PDF request

Let’s start with a simple example using the Messages API:

Shell

Python

TypeScript

Copy

```bash
# First fetch the file
curl -s "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf" | base64 | tr -d '\n' > pdf_base64.txt

# Create a JSON request file using the pdf_base64.txt content
jq -n --rawfile PDF_BASE64 pdf_base64.txt '{
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 1024,
    "messages": [{\
        "role": "user",\
        "content": [{\
            "type": "document",\
            "source": {\
                "type": "base64",\
                "media_type": "application/pdf",\
                "data": $PDF_BASE64\
            }\
        },\
        {\
            "type": "text",\
            "text": "Which model has the highest human preference win rates across each use-case?"\
        }]\
    }]
}' > request.json

# Finally send the API request using the JSON file
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d @request.json

```

### [​](\#how-pdf-support-works)  How PDF support works

When you send a PDF to Claude, the following steps occur:

1

The system extracts the contents of the document.

- The system converts each page of the document into an image.
- The text from each page is extracted and provided alongside each page’s image.

2

Claude analyzes both the text and images to better understand the document.

- Documents are provided as a combination of text and images for analysis.
- This allows users to ask for insights on visual elements of a PDF, such as charts, diagrams, and other non-textual content.

3

Claude responds, referencing the PDF's contents if relevant.

Claude can reference both textual and visual content when it responds. You can further improve performance by integrating PDF support with:

- **Prompt caching**: To improve performance for repeated analysis.
- **Batch processing**: For high-volume document processing.
- **Tool use**: To extract specific information from documents for use as tool inputs.

### [​](\#estimate-your-costs)  Estimate your costs

The token count of a PDF file depends on the total text extracted from the document as well as the number of pages:

- Text token costs: Each page typically uses 1,500-3,000 tokens per page depending on content density. Standard API pricing applies with no additional PDF fees.
- Image token costs: Since each page is converted into an image, the same [image-based cost calculations](/en/docs/build-with-claude/vision#evaluate-image-size) are applied.

You can use [token counting](/en/docs/build-with-claude/token-counting) to estimate costs for your specific PDFs.

* * *

## [​](\#optimize-pdf-processing)  Optimize PDF processing

### [​](\#improve-performance)  Improve performance

Follow these best practices for optimal results:

- Place PDFs before text in your requests
- Use standard fonts
- Ensure text is clear and legible
- Rotate pages to proper upright orientation
- Use logical page numbers (from PDF viewer) in prompts
- Split large PDFs into chunks when needed
- Enable prompt caching for repeated analysis

### [​](\#scale-your-implementation)  Scale your implementation

For high-volume processing, consider these approaches:

#### [​](\#use-prompt-caching)  Use prompt caching

Cache PDFs to improve performance on repeated queries:

Shell

Python

TypeScript

Copy

```bash
# Create a JSON request file using the pdf_base64.txt content
jq -n --rawfile PDF_BASE64 pdf_base64.txt '{
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 1024,
    "messages": [{\
        "role": "user",\
        "content": [{\
            "type": "document",\
            "source": {\
                "type": "base64",\
                "media_type": "application/pdf",\
                "data": $PDF_BASE64\
            },\
            "cache_control": {\
              "type": "ephemeral"\
            }\
        },\
        {\
            "type": "text",\
            "text": "Which model has the highest human preference win rates across each use-case?"\
        }]\
    }]
}' > request.json

# Then make the API call using the JSON file
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d @request.json

```

#### [​](\#process-document-batches)  Process document batches

Use the Message Batches API for high-volume workflows:

Shell

Python

TypeScript

Copy

```bash
# Create a JSON request file using the pdf_base64.txt content
jq -n --rawfile PDF_BASE64 pdf_base64.txt '
{
  "requests": [\
      {\
          "custom_id": "my-first-request",\
          "params": {\
              "model": "claude-3-5-sonnet-20241022",\
              "max_tokens": 1024,\
              "messages": [\
                {\
                    "role": "user",\
                    "content": [\
                        {\
                            "type": "document",\
                            "source": {\
                                "type": "base64",\
                                "media_type": "application/pdf",\
                                "data": $PDF_BASE64\
                            }\
                        },\
                        {\
                            "type": "text",\
                            "text": "Which model has the highest human preference win rates across each use-case?"\
                        }\
                    ]\
                }\
              ]\
          }\
      },\
      {\
          "custom_id": "my-second-request",\
          "params": {\
              "model": "claude-3-5-sonnet-20241022",\
              "max_tokens": 1024,\
              "messages": [\
                {\
                    "role": "user",\
                    "content": [\
                        {\
                            "type": "document",\
                            "source": {\
                                "type": "base64",\
                                "media_type": "application/pdf",\
                                "data": $PDF_BASE64\
                            }\
                        },\
                        {\
                            "type": "text",\
                            "text": "Extract 5 key insights from this document."\
                        }\
                    ]\
                }\
              ]\
          }\
      }\
  ]
}
' > request.json

# Then make the API call using the JSON file
curl https://api.anthropic.com/v1/messages/batches \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d @request.json

```

## [​](\#next-steps)  Next steps

[**Try PDF examples** \\
\\
Explore practical examples of PDF processing in our cookbook recipe.](https://github.com/anthropics/anthropic-cookbook/tree/main/multimodal) [**View API reference** \\
\\
See complete API documentation for PDF support.](/en/api/messages)

Was this page helpful?

YesNo

[Message Batches](/en/docs/build-with-claude/message-batches) [Token counting](/en/docs/build-with-claude/token-counting)

On this page

- [Before you begin](#before-you-begin)
- [Check PDF requirements](#check-pdf-requirements)
- [Supported platforms and models](#supported-platforms-and-models)
- [Process PDFs with Claude](#process-pdfs-with-claude)
- [Send your first PDF request](#send-your-first-pdf-request)
- [How PDF support works](#how-pdf-support-works)
- [Estimate your costs](#estimate-your-costs)
- [Optimize PDF processing](#optimize-pdf-processing)
- [Improve performance](#improve-performance)
- [Scale your implementation](#scale-your-implementation)
- [Use prompt caching](#use-prompt-caching)
- [Process document batches](#process-document-batches)
- [Next steps](#next-steps)