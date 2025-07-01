#!/bin/bash
# Git commit script for LLM configuration centralization

echo "🔍 Checking git status..."
git status

echo ""
echo "📦 Adding all changes..."
git add .

echo ""
echo "💬 Committing with descriptive message..."
git commit -m "🎯 Centralize LLM Configuration - Single Environment Variable

✨ Features Added:
- Single LLM_MODEL environment variable controls all expert agents
- Dynamic LLM loading from .env configuration
- Support for multiple providers (Anthropic, OpenAI)
- Easy model switching without code changes

🔧 Technical Changes:
- Updated crew.py with get_llm_config() method
- Modified all agent methods to use dynamic LLM configuration
- Cleaned agents.yaml to remove hardcoded LLM settings
- Enhanced .env with clear LLM configuration options

📚 Documentation:
- Added LLM_CONFIGURATION.md with usage guide
- Updated README.md with new configuration instructions
- Enhanced .env_example with LLM options
- Created test_llm_config.py for validation

🚀 Benefits:
- Cost optimization through easy model switching
- Development flexibility (Haiku) vs production quality (Sonnet)
- Provider independence (Anthropic ↔ OpenAI)
- Instant configuration changes without code deployment

Ready for production testing with Keysight emails! 🎉"

echo ""
echo "🚀 Pushing to GitHub..."
git push origin main

echo ""
echo "✅ LLM Configuration centralization complete!"
echo "🎯 Ready to test with: python -m expert_panel_assistant.main sample"
