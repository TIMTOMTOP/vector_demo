[Anthropic home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/dark.svg)](/)

English

Search...

Ctrl K

Search...

Navigation

Build with Claude

Vision

[Welcome](/en/home) [User Guides](/en/docs/welcome) [API Reference](/en/api/getting-started) [Prompt Library](/en/prompt-library/library) [Release Notes](/en/release-notes/overview) [Developer Newsletter](/en/developer-newsletter/overview)

This guide describes how to work with images in Claude, including best practices, code examples, and limitations to keep in mind.

* * *

## [​](\#how-to-use-vision)  How to use vision

Use Claude’s vision capabilities via:

- [claude.ai](https://claude.ai/). Upload an image like you would a file, or drag and drop an image directly into the chat window.
- The [Console Workbench](https://console.anthropic.com/workbench/). If you select a model that accepts images (Claude 3 models only), a button to add images appears at the top right of every User message block.
- **API request**. See the examples in this guide.

* * *

## [​](\#before-you-upload)  Before you upload

### [​](\#basics-and-limits)  Basics and Limits

You can include multiple images in a single request (up to 20 for [claude.ai](https://claude.ai/) and 100 for API requests). Claude will analyze all provided images when formulating its response. This can be helpful for comparing or contrasting images.

If you submit an image larger than 8000x8000 px, it will be rejected. If you submit more than 20 images in one API request, this limit is 2000x2000 px.

### [​](\#evaluate-image-size)  Evaluate image size

For optimal performance, we recommend resizing images before uploading if they are too large. If your image’s long edge is more than 1568 pixels, or your image is more than ~1,600 tokens, it will first be scaled down, preserving aspect ratio, until it’s within the size limits.

If your input image is too large and needs to be resized, it will increase latency of [time-to-first-token](/en/docs/resources/glossary), without giving you any additional model performance. Very small images under 200 pixels on any given edge may degrade performance.

To improve [time-to-first-token](/en/docs/resources/glossary), we recommend
resizing images to no more than 1.15 megapixels (and within 1568 pixels in
both dimensions).

Here is a table of maximum image sizes accepted by our API that will not be resized for common aspect ratios. With the Claude 3.5 Sonnet model, these images use approximately 1,600 tokens and around $4.80/1K images.

| Aspect ratio | Image size |
| --- | --- |
| 1:1 | 1092x1092 px |
| 3:4 | 951x1268 px |
| 2:3 | 896x1344 px |
| 9:16 | 819x1456 px |
| 1:2 | 784x1568 px |

### [​](\#calculate-image-costs)  Calculate image costs

Each image you include in a request to Claude counts towards your token usage. To calculate the approximate cost, multiply the approximate number of image tokens by the [per-token price of the model](https://anthropic.com/pricing) you’re using.

If your image does not need to be resized, you can estimate the number of tokens used through this algorithm: `tokens = (width px * height px)/750`

Here are examples of approximate tokenization and costs for different image sizes within our API’s size constraints based on Claude 3.5 Sonnet per-token price of $3 per million input tokens:

| Image size | \# of Tokens | Cost / image | Cost / 1K images |
| --- | --- | --- | --- |
| 200x200 px(0.04 megapixels) | ~54 | ~$0.00016 | ~$0.16 |
| 1000x1000 px(1 megapixel) | ~1334 | ~$0.004 | ~$4.00 |
| 1092x1092 px(1.19 megapixels) | ~1590 | ~$0.0048 | ~$4.80 |

### [​](\#ensuring-image-quality)  Ensuring image quality

When providing images to Claude, keep the following in mind for best results:

- **Image format**: Use a supported image format: JPEG, PNG, GIF, or WebP.
- **Image clarity**: Ensure images are clear and not too blurry or pixelated.
- **Text**: If the image contains important text, make sure it’s legible and not too small. Avoid cropping out key visual context just to enlarge the text.

* * *

## [​](\#prompt-examples)  Prompt examples

Many of the [prompting techniques](/en/docs/build-with-claude/prompt-engineering/overview) that work well for text-based interactions with Claude can also be applied to image-based prompts.

These examples demonstrate best practice prompt structures involving images.

Just as with document-query placement, Claude works best when images come
before text. Images placed after text or interpolated with text will still
perform well, but if your use case allows it, we recommend an image-then-text
structure.

### [​](\#about-the-prompt-examples)  About the prompt examples

These prompt examples use the [Anthropic Python SDK](/en/api/client-sdks), and fetch images from Wikipedia using the `httpx` library. You can use any image source.

The example prompts use these variables.

Python

```Python
import base64
import httpx

image1_url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
image1_media_type = "image/jpeg"
image1_data = base64.standard_b64encode(httpx.get(image1_url).content).decode("utf-8")

image2_url = "https://upload.wikimedia.org/wikipedia/commons/b/b5/Iridescent.green.sweat.bee1.jpg"
image2_media_type = "image/jpeg"
image2_data = base64.standard_b64encode(httpx.get(image2_url).content).decode("utf-8")

```

To utilize images when making an API request, you can provide images to Claude as a base64-encoded image in `image` content blocks. Here is simple example in Python showing how to include a base64-encoded image in a Messages API request:

Python

```Python
import anthropic

client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[\
        {\
            "role": "user",\
            "content": [\
                {\
                    "type": "image",\
                    "source": {\
                        "type": "base64",\
                        "media_type": image1_media_type,\
                        "data": image1_data,\
                    },\
                },\
                {\
                    "type": "text",\
                    "text": "Describe this image."\
                }\
            ],\
        }\
    ],
)
print(message)

```

See [Messages API examples](/en/api/messages) for more example code and parameter details.

Example: One image

It’s best to place images earlier in the prompt than questions about them or instructions for tasks that use them.

Ask Claude to describe one image.

| Role | Content |
| --- | --- |
| User | \[Image\] Describe this image. |

Here is the corresponding API call using the Claude 3.5 Sonnet model.

Python

```Python
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[\
        {\
            "role": "user",\
            "content": [\
                {\
                    "type": "image",\
                    "source": {\
                        "type": "base64",\
                        "media_type": image1_media_type,\
                        "data": image1_data,\
                    },\
                },\
                {\
                    "type": "text",\
                    "text": "Describe this image."\
                }\
            ],\
        }\
    ],
)

```

Example: Multiple images

In situations where there are multiple images, introduce each image with `Image 1:` and `Image 2:` and so on. You don’t need newlines between images or between images and the prompt.

Ask Claude to describe the differences between multiple images.

| Role | Content |
| --- | --- |
| User | Image 1: \[Image 1\] Image 2: \[Image 2\] How are these images different? |

Here is the corresponding API call using the Claude 3.5 Sonnet model.

Python

```Python
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[\
        {\
            "role": "user",\
            "content": [\
                {\
                    "type": "text",\
                    "text": "Image 1:"\
                },\
                {\
                    "type": "image",\
                    "source": {\
                        "type": "base64",\
                        "media_type": image1_media_type,\
                        "data": image1_data,\
                    },\
                },\
                {\
                    "type": "text",\
                    "text": "Image 2:"\
                },\
                {\
                    "type": "image",\
                    "source": {\
                        "type": "base64",\
                        "media_type": image2_media_type,\
                        "data": image2_data,\
                    },\
                },\
                {\
                    "type": "text",\
                    "text": "How are these images different?"\
                }\
            ],\
        }\
    ],
)

```

Example: Multiple images with a system prompt

Ask Claude to describe the differences between multiple images, while giving it a system prompt for how to respond.

| Content |  |
| --- | --- |
| System | Respond only in Spanish. |
| User | Image 1: \[Image 1\] Image 2: \[Image 2\] How are these images different? |

Here is the corresponding API call using the Claude 3.5 Sonnet model.

Python

```Python
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system="Respond only in Spanish.",
    messages=[\
        {\
            "role": "user",\
            "content": [\
                {\
                    "type": "text",\
                    "text": "Image 1:"\
                },\
                {\
                    "type": "image",\
                    "source": {\
                        "type": "base64",\
                        "media_type": image1_media_type,\
                        "data": image1_data,\
                    },\
                },\
                {\
                    "type": "text",\
                    "text": "Image 2:"\
                },\
                {\
                    "type": "image",\
                    "source": {\
                        "type": "base64",\
                        "media_type": image2_media_type,\
                        "data": image2_data,\
                    },\
                },\
                {\
                    "type": "text",\
                    "text": "How are these images different?"\
                }\
            ],\
        }\
    ],
)

```

Example: Four images across two conversation turns

Claude’s vision capabilities shine in multimodal conversations that mix images and text. You can have extended back-and-forth exchanges with Claude, adding new images or follow-up questions at any point. This enables powerful workflows for iterative image analysis, comparison, or combining visuals with other knowledge.

Ask Claude to contrast two images, then ask a follow-up question comparing the first images to two new images.

| Role | Content |
| --- | --- |
| User | Image 1: \[Image 1\] Image 2: \[Image 2\] How are these images different? |
| Assistant | \[Claude’s response\] |
| User | Image 1: \[Image 3\] Image 2: \[Image 4\] Are these images similar to the first two? |
| Assistant | \[Claude’s response\] |

When using the API, simply insert new images into the array of Messages in the `user` role as part of any standard [multiturn conversation](/en/api/messages-examples#multiple-conversational-turns) structure.

* * *

## [​](\#limitations)  Limitations

While Claude’s image understanding capabilities are cutting-edge, there are some limitations to be aware of:

- **People identification**: Claude [cannot be used](https://www.anthropic.com/legal/aup) to identify (i.e., name) people in images and will refuse to do so.
- **Accuracy**: Claude may hallucinate or make mistakes when interpreting low-quality, rotated, or very small images under 200 pixels.
- **Spatial reasoning**: Claude’s spatial reasoning abilities are limited. It may struggle with tasks requiring precise localization or layouts, like reading an analog clock face or describing exact positions of chess pieces.
- **Counting**: Claude can give approximate counts of objects in an image but may not always be precisely accurate, especially with large numbers of small objects.
- **AI generated images**: Claude does not know if an image is AI-generated and may be incorrect if asked. Do not rely on it to detect fake or synthetic images.
- **Inappropriate content**: Claude will not process inappropriate or explicit images that violate our [Acceptable Use Policy](https://www.anthropic.com/legal/aup).
- **Healthcare applications**: While Claude can analyze general medical images, it is not designed to interpret complex diagnostic scans such as CTs or MRIs. Claude’s outputs should not be considered a substitute for professional medical advice or diagnosis.

Always carefully review and verify Claude’s image interpretations, especially for high-stakes use cases. Do not use Claude for tasks requiring perfect precision or sensitive image analysis without human oversight.

* * *

## [​](\#faq)  FAQ

What image file types does Claude support?

Claude currently supports JPEG, PNG, GIF, and WebP image formats, specifically:

- image/jpeg
- image/png
- image/gif
- image/webp

Can Claude read image URLs?

No, Claude cannot read image URLs on any interface, including on claude.ai.
Our API does not currently support adding URLs in either the text or image
blocks. Adding image URLs (or URLs of any sort) in the text block might cause
Claude to hallucinate, as Claude is currently unable to retrieve information
from that URL.

Is there a limit to the image file size I can upload?

Yes, there are limits:

- API: Maximum 5MB per image
- claude.ai: Maximum 10MB per image

Images larger than these limits will be rejected and return an error when using our API.

How many images can I include in one request?

The image limits are:

- Messages API: Up to 100 images per request
- claude.ai: Up to 20 images per turn

Requests exceeding these limits will be rejected and return an error.

Does Claude read image metadata?

No, Claude does not parse or receive any metadata from images passed to it.

Can I delete images I've uploaded?

No. Image uploads are ephemeral and not stored beyond the duration of the API
request. Uploaded images are automatically deleted after they have been
processed.

Where can I find details on data privacy for image uploads?

Please refer to our privacy policy page for information on how we handle
uploaded images and other data. We do not use uploaded images to train our
models.

What if Claude's image interpretation seems wrong?

If Claude’s image interpretation seems incorrect:

1. Ensure the image is clear, high-quality, and correctly oriented.
2. Try prompt engineering techniques to improve results.
3. If the issue persists, flag the output in claude.ai (thumbs up/down) or contact our support team.

Your feedback helps us improve!

Can Claude generate or edit images?

No, Claude is an image understanding model only. It can interpret and analyze images, but it cannot generate, produce, edit, manipulate, or create images.

* * *

## [​](\#dive-deeper-into-vision)  Dive deeper into vision

Ready to start building with images using Claude? Here are a few helpful resources:

- [Multimodal cookbook](https://github.com/anthropics/anthropic-cookbook/tree/main/multimodal): This cookbook has tips on [getting started with images](https://github.com/anthropics/anthropic-cookbook/blob/main/multimodal/getting%5Fstarted%5Fwith%5Fvision.ipynb) and [best practice techniques](https://github.com/anthropics/anthropic-cookbook/blob/main/multimodal/best%5Fpractices%5Ffor%5Fvision.ipynb) to ensure the highest quality performance with images. See how you can effectively prompt Claude with images to carry out tasks such as [interpreting and analyzing charts](https://github.com/anthropics/anthropic-cookbook/blob/main/multimodal/reading%5Fcharts%5Fgraphs%5Fpowerpoints.ipynb) or [extracting content from forms](https://github.com/anthropics/anthropic-cookbook/blob/main/multimodal/how%5Fto%5Ftrascribe%5Ftext.ipynb).
- [API reference](/en/api/messages): Visit our documentation for the Messages API, including example [API calls involving images](/en/api/messages-examples).

If you have any other questions, feel free to reach out to our [support team](https://support.anthropic.com/). You can also join our [developer community](https://www.anthropic.com/discord) to connect with other creators and get help from Anthropic experts.

Was this page helpful?

YesNo

[Google Sheets add-on](/en/docs/build-with-claude/claude-for-sheets) [Tool use (function calling)](/en/docs/build-with-claude/tool-use)

On this page

- [How to use vision](#how-to-use-vision)
- [Before you upload](#before-you-upload)
- [Basics and Limits](#basics-and-limits)
- [Evaluate image size](#evaluate-image-size)
- [Calculate image costs](#calculate-image-costs)
- [Ensuring image quality](#ensuring-image-quality)
- [Prompt examples](#prompt-examples)
- [About the prompt examples](#about-the-prompt-examples)
- [Limitations](#limitations)
- [FAQ](#faq)
- [Dive deeper into vision](#dive-deeper-into-vision)