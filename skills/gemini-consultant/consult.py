# /// script
# dependencies = ["google-genai"]
# ///
"""
Gemini Consultant - Get a second opinion from Gemini 3 Pro with Google Search grounding and vision.

Usage:
    uv run consult.py "your question here"
    uv run consult.py "your question" -c "additional context"
    uv run consult.py "What's in this image?" -i image.png
"""

import argparse
import mimetypes
import sys
from pathlib import Path

from google import genai
from google.genai import types


def get_mime_type(file_path: str) -> str:
    """Get MIME type for an image file."""
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type and mime_type.startswith("image/"):
        return mime_type
    # Default fallback based on extension
    ext = Path(file_path).suffix.lower()
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".heic": "image/heic",
        ".heif": "image/heif",
    }
    return mime_map.get(ext, "image/jpeg")


def main():
    parser = argparse.ArgumentParser(
        description="Consult Gemini 3 Pro with Google Search grounding and vision"
    )
    parser.add_argument("question", help="The question to ask Gemini")
    parser.add_argument(
        "-c", "--context", help="Additional context to include with the question"
    )
    parser.add_argument(
        "-i",
        "--image",
        action="append",
        dest="images",
        help="Image file(s) to analyze (can be used multiple times)",
    )
    parser.add_argument(
        "--media-resolution",
        choices=["low", "medium", "high", "ultra_high"],
        default="medium",
        help="Image resolution for analysis: low (280 tokens), medium (560), high (1120), ultra_high (default: medium)",
    )
    parser.add_argument(
        "--no-search",
        action="store_true",
        help="Disable Google Search grounding (use pure model knowledge)",
    )
    parser.add_argument(
        "--thinking",
        choices=["low", "high"],
        default="high",
        help="Thinking level: 'low' for faster responses, 'high' for deeper reasoning (default: high)",
    )
    args = parser.parse_args()

    client = genai.Client()

    # Build the contents list
    contents = []

    # Add images if provided
    if args.images:
        for image_path in args.images:
            path = Path(image_path)
            if not path.exists():
                print(f"Error: Image file not found: {image_path}", file=sys.stderr)
                sys.exit(1)
            with open(path, "rb") as f:
                image_bytes = f.read()
            mime_type = get_mime_type(image_path)
            contents.append(
                types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
            )
            print(f"Including image: {image_path} ({mime_type})")

    # Build the text prompt
    if args.context:
        text_prompt = f"Context:\n{args.context}\n\nQuestion: {args.question}"
    else:
        text_prompt = args.question

    contents.append(text_prompt)

    # Configure options
    config_kwargs = {
        "thinking_config": types.ThinkingConfig(thinking_level=args.thinking)
    }
    if not args.no_search:
        config_kwargs["tools"] = [{"google_search": {}}]

    print(f"Consulting Gemini 3 Pro (thinking: {args.thinking})...")
    if not args.no_search:
        print("(with Google Search grounding enabled)")
    print("-" * 50)

    response = client.models.generate_content(
        model="gemini-3-pro-preview",
        contents=contents,
        config=types.GenerateContentConfig(**config_kwargs),
    )

    # Extract and print the response
    if response.candidates and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if hasattr(part, "text") and part.text:
                print(part.text)
    else:
        print("No response received from the model.", file=sys.stderr)
        sys.exit(1)

    # Print grounding metadata if available
    if hasattr(response, "candidates") and response.candidates:
        candidate = response.candidates[0]
        if hasattr(candidate, "grounding_metadata") and candidate.grounding_metadata:
            metadata = candidate.grounding_metadata
            if hasattr(metadata, "search_entry_point") and metadata.search_entry_point:
                print("\n" + "-" * 50)
                print("Sources:")
                if hasattr(metadata, "grounding_chunks") and metadata.grounding_chunks:
                    for chunk in metadata.grounding_chunks:
                        if hasattr(chunk, "web") and chunk.web:
                            print(f"  - {chunk.web.title}: {chunk.web.uri}")


if __name__ == "__main__":
    main()
