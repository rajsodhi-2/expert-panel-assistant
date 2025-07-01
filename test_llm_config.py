#!/usr/bin/env python
"""
Quick test script to verify LLM configuration is working correctly.
"""
import os
import sys
sys.path.append('src')

from dotenv import load_dotenv
from expert_panel_assistant.crew import ExpertPanelAssistant

def test_llm_config():
    """Test that LLM configuration is loaded correctly from environment."""
    load_dotenv()
    
    print("🧪 Testing LLM Configuration")
    print("=" * 50)
    
    # Test environment variable loading
    llm_model = os.getenv('LLM_MODEL', 'not_found')
    print(f"📋 LLM_MODEL from .env: {llm_model}")
    
    # Test ExpertPanelAssistant LLM config method
    expert_panel = ExpertPanelAssistant()
    configured_llm = expert_panel.get_llm_config()
    print(f"🤖 Configured LLM: {configured_llm}")
    
    # Test agent creation with dynamic LLM
    try:
        print("\n🔧 Testing Agent Creation...")
        router = expert_panel.router()
        print(f"✅ Router agent created successfully")
        
        simon = expert_panel.simon_sinek()
        print(f"✅ Simon Sinek agent created successfully")
        
        print(f"\n🎯 All agents will use: {configured_llm}")
        print("✅ LLM configuration test passed!")
        
    except Exception as e:
        print(f"❌ Error creating agents: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_llm_config()
    if success:
        print("\n🚀 Ready to run the Expert Panel Assistant!")
        print("   To test with sample: python -m expert_panel_assistant.main sample")
    else:
        print("\n❌ Configuration test failed. Please check your setup.")
        sys.exit(1)
