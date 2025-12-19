# Gemini Claude Skills

Claude Code skills for integrating Google's Gemini 3 Pro models into your workflow. For more context, see [this blog post](https://quesma.com/blog/claude-skills-not-antigravity/).

## Skills Included

### 1. Nano Banana Pro (`nano-banana-pro`)

Generate images using Google's advanced Nano Banana Pro model (`gemini-3-pro-image-preview`).

**Capabilities:**

- Accurate infographics with real data (uses Google Search grounding)
- Text rendering in images
- Cartographic visualizations and maps
- Detailed instruction following
- Multiple aspect ratios: `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`
- Resolutions: `1K`, `2K`, `4K`

### 2. Gemini Consultant (`gemini-consultant`)

Get a second opinion from Gemini 3 Pro (`gemini-3-pro-preview`) with Google Search grounding and vision.

**Capabilities:**

- Real-time web information via Google Search grounding
- Image analysis (single or multiple images)
- Configurable thinking depth (`low` for speed, `high` for complex reasoning)
- Context passing for detailed questions

## Prerequisites

You need a Google AI API key with access to Gemini 3 Pro models.

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Get your API key from [Google AI Studio](https://aistudio.google.com/).

## Installation

```bash
# In Claude Code, add the marketplace
/plugin marketplace add stared/gemini-claude-skills

# Install the plugin
/plugin install gemini-skills@gemini-claude-skills
```

## Usage Examples

Once installed, Claude will automatically use these skills when appropriate. You can also explicitly request them:

### Image Generation

> "Generate an infographic showing the water cycle"

> "Create a 16:9 landscape image of a futuristic city at 4K resolution"

### AI Consultation

> "Ask Gemini what the latest React 19 features are"

> "Get a second opinion on this code architecture from Gemini"

> "Have Gemini analyze this screenshot" (attach image)

## Dependencies

The scripts use [uv](https://docs.astral.sh/uv/) with inline script dependencies - no manual package installation required. Dependencies are declared in each script:

```python
# /// script
# dependencies = ["google-genai"]
# ///
```

## Author

Piotr Migdał ([@pmigdal](https://github.com/stared))

## License

MIT

## Links

- [Nano Banana Pro Blog Post](https://p.migdal.pl/blog/nano-banana-pro/)
- [Google AI Gemini Documentation](https://ai.google.dev/gemini-api/docs)
- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)
