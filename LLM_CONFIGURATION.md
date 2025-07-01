# LLM Configuration Guide

## Overview

The Expert Panel Assistant now supports centralized LLM configuration through a single environment variable. All expert agents will use the same LLM model specified in your `.env` file.

## Quick Setup

1. **Edit your `.env` file:**
   ```bash
   # Change this single line to switch LLM providers/models:
   LLM_MODEL=anthropic/claude-3-5-haiku-latest
   ```

2. **Restart your application** - The new LLM will be used for all agents.

## Supported LLM Formats

### Anthropic Models
```bash
# Fast and cost-effective (recommended for development)
LLM_MODEL=anthropic/claude-3-5-haiku-latest

# More powerful for complex reasoning
LLM_MODEL=anthropic/claude-3-5-sonnet-20240620

# Most capable model (higher cost)
LLM_MODEL=anthropic/claude-3-opus-20240229
```

### OpenAI Models
```bash
# Latest GPT-4 model
LLM_MODEL=openai/gpt-4

# GPT-4 Turbo (faster)
LLM_MODEL=openai/gpt-4-turbo

# More cost-effective option
LLM_MODEL=openai/gpt-3.5-turbo
```

## Testing Different Models

You can easily test different models for your specific use case:

1. **Development/Testing:** Use `anthropic/claude-3-5-haiku-latest` for fast, cost-effective testing
2. **Production:** Use `anthropic/claude-3-5-sonnet-20240620` for balanced performance and cost
3. **Complex Analysis:** Use `anthropic/claude-3-opus-20240229` or `openai/gpt-4` for sophisticated reasoning

## Performance Considerations

| Model | Speed | Cost | Quality | Best For |
|-------|-------|------|---------|----------|
| Claude 3.5 Haiku | ⚡⚡⚡ | 💰 | ⭐⭐⭐ | Development, Simple emails |
| Claude 3.5 Sonnet | ⚡⚡ | 💰💰 | ⭐⭐⭐⭐ | Production, Most use cases |
| Claude 3 Opus | ⚡ | 💰💰💰 | ⭐⭐⭐⭐⭐ | Complex strategic analysis |
| GPT-4 | ⚡ | 💰💰💰 | ⭐⭐⭐⭐⭐ | Alternative to Opus |
| GPT-3.5 Turbo | ⚡⚡⚡ | 💰 | ⭐⭐⭐ | Budget-conscious option |

## Example: Switching to OpenAI GPT-4

1. Update your `.env` file:
   ```bash
   LLM_MODEL=openai/gpt-4
   OPENAI_API_KEY=your_openai_api_key_here
   ```

2. Run the system:
   ```bash
   python -m expert_panel_assistant.main sample
   ```

3. You'll see: `🤖 Using LLM: openai/gpt-4` in the output

## Troubleshooting

- **Invalid Model Error:** Check the model name format matches the examples above
- **API Key Error:** Ensure you have the correct API key for your chosen provider
- **Rate Limits:** Some models have different rate limits - consider switching to a different model if you hit limits

## What Changed

- ✅ **Single Configuration Point:** Change `LLM_MODEL` in `.env` to affect all agents
- ✅ **Dynamic Loading:** LLM is loaded from environment variable at runtime
- ✅ **Backward Compatible:** Existing functionality remains unchanged
- ✅ **Easy Testing:** Switch models instantly without code changes

The system will display which LLM is being used when you run it:
```
🤖 Using LLM: anthropic/claude-3-5-haiku-latest
```
