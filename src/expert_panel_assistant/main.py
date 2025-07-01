#!/usr/bin/env python
import sys
import warnings
import os
import re
from datetime import datetime
from typing import Dict, Any, List

from expert_panel_assistant.crew import ExpertPanelAssistant

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.

def parse_expert_names(router_result: str) -> List[str]:
    """
    Parse expert names from the router result output.
    Expected format: Contains expert names like "simon_sinek", "julie_zhuo", etc.
    """
    # Define all possible expert names
    expert_names = ["simon_sinek", "julie_zhuo", "satya_nadella", "roger_martin", "chris_voss"]
    
    # Convert result to lowercase for matching
    result_lower = str(router_result).lower()
    
    selected_experts = []
    for name in expert_names:
        # Check for various formats: "simon_sinek", "Simon Sinek", "simon sinek"
        name_variants = [
            name,
            name.replace("_", " "),
            name.replace("_", "").replace(" ", ""),
            " ".join(word.capitalize() for word in name.split("_"))
        ]
        
        if any(variant.lower() in result_lower for variant in name_variants):
            selected_experts.append(name)
    
    # Fallback: if no experts found, try regex pattern matching
    if not selected_experts:
        # Look for patterns like "Selected experts: name1, name2, name3"
        patterns = [
            r'selected[^:]*:\s*([^.]+)',
            r'experts?[^:]*:\s*([^.]+)',
            r'recommend[^:]*:\s*([^.]+)',
            r'relevant[^:]*:\s*([^.]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, result_lower, re.IGNORECASE)
            if match:
                matched_text = match.group(1)
                for name in expert_names:
                    if any(variant.lower() in matched_text for variant in [
                        name,
                        name.replace("_", " "),
                        " ".join(word.capitalize() for word in name.split("_"))
                    ]):
                        if name not in selected_experts:
                            selected_experts.append(name)
                break
    
    # Limit to maximum 3 experts as per requirements
    selected_experts = selected_experts[:3]
    
    # If still no experts found, default to a reasonable selection
    if not selected_experts:
        print("⚠️  Could not parse expert selection from router output. Using default experts.")
        selected_experts = ["simon_sinek", "julie_zhuo", "roger_martin"]
    
    return selected_experts

def get_email_input() -> str:
    """
    Get email content from user input with better UX.
    """
    print("\n" + "="*60)
    print("EXPERT PANEL ASSISTANT")
    print("="*60)
    print("Available experts: Simon Sinek, Julie Zhuo, Satya Nadella, Roger Martin, Chris Voss")
    print("Maximum 3 experts will be selected based on relevance.")
    print("-"*60)
    
    print("\nEnter the email content (press Enter twice when finished):")
    print("-"*40)
    
    lines = []
    empty_line_count = 0
    
    while True:
        line = input()
        if line.strip() == "":
            empty_line_count += 1
            if empty_line_count >= 2:
                break
            lines.append(line)
        else:
            empty_line_count = 0
            lines.append(line)
    
    email_content = "\n".join(lines).strip()
    
    if not email_content:
        print("No email content provided. Exiting...")
        sys.exit(1)
    
    return email_content

def display_routing_results(selected_experts: List[str]) -> None:
    """
    Display which experts were selected by the router.
    """
    expert_display_names = {
        "simon_sinek": "Simon Sinek (Leadership & Vision)",
        "julie_zhuo": "Julie Zhuo (Team Dynamics & Scaling)",
        "satya_nadella": "Satya Nadella (Transformation & Innovation)",
        "roger_martin": "Roger Martin (Strategy & Market Positioning)",
        "chris_voss": "Chris Voss (Negotiation & Persuasion)"
    }
    
    print("\n🎯 EXPERT ROUTING RESULTS")
    print("-"*40)
    print(f"Selected {len(selected_experts)} expert(s):")
    
    for i, expert in enumerate(selected_experts, 1):
        display_name = expert_display_names.get(expert, expert)
        print(f"  {i}. {display_name}")
    
    print("-"*40)

def display_results(result: Any) -> None:
    """
    Display the results in a formatted way.
    """
    print("\n" + "="*60)
    print("EXPERT PANEL RESPONSE")
    print("="*60)
    
    if os.path.exists("panel_response.md"):
        print("✅ Full response saved to: panel_response.md")
        
        # Display a preview of the response
        try:
            with open("panel_response.md", "r", encoding="utf-8") as f:
                content = f.read()
                print("\nResponse Preview:")
                print("-"*40)
                # Show first 500 characters
                preview = content[:500]
                if len(content) > 500:
                    preview += "..."
                print(preview)
        except Exception as e:
            print(f"Could not read response file: {e}")
    else:
        print("⚠️  Response file not found")
    
    print(f"\nRaw Result:\n{result}")
    print("\n" + "="*60)

def run():
    """
    Run the expert panel crew with dynamic routing based on router task output.
    """
    try:
        # Get email content from user
        email_content = get_email_input()
        
        print(f"\n📧 Processing email ({len(email_content)} characters)...")
        
        # Prepare inputs
        inputs = {
            'email': email_content,
            'timestamp': datetime.now().isoformat(),
            'current_year': str(datetime.now().year)
        }
        
        # Step 1: Run routing task to determine which experts to engage
        print("🔍 Analyzing content and selecting relevant experts...")
        expert_panel = ExpertPanelAssistant()
        
        # Create a minimal crew with just the router for initial analysis
        router_agent = expert_panel.router()
        route_task = expert_panel.route_task()
        
        # Run the routing task
        print("🧠 Router analyzing email content...")
        router_result = route_task.execute_sync(agent=router_agent, context=inputs)
        
        # Parse the router output to get selected experts
        selected_experts = parse_expert_names(router_result)
        
        # Display routing results
        display_routing_results(selected_experts)
        
        # Step 2: Create dynamic crew with only selected experts
        print("🚀 Creating dynamic expert panel...")
        dynamic_crew = expert_panel.create_dynamic_crew(selected_experts)
        
        # Step 3: Run the full analysis with selected experts
        print("💬 Expert panel providing insights...")
        result = dynamic_crew.kickoff(inputs=inputs)
        
        # Display results
        display_results(result)
        
        return result
        
    except KeyboardInterrupt:
        print("\n\n❌ Process interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred while running the crew: {e}")
        print(f"Error type: {type(e).__name__}")
        if hasattr(e, '__traceback__'):
            import traceback
            print("Full traceback:")
            traceback.print_exc()
        sys.exit(1)

def run_with_sample():
    """
    Run with sample email using dynamic routing.
    """
    inputs = {
        'email': """Subject: Strategic Team Restructuring and Leadership Alignment
        
        Hi Expert Panel,
        
        We're facing a critical decision about restructuring our 150-person engineering team while maintaining momentum on our key product initiatives. The challenge involves:
        
        1. Leadership alignment across multiple product lines
        2. Scaling team communication and decision-making processes  
        3. Negotiating resource allocation between competing priorities
        4. Maintaining innovation velocity during organizational change
        
        Looking for strategic guidance on approach and timing.
        
        Best regards,
        Sarah Johnson
        VP Engineering""",
        'timestamp': datetime.now().isoformat(),
        'current_year': str(datetime.now().year)
    }
    
    try:
        print("🧪 Running with sample email using dynamic routing...")
        
        # Create the expert panel instance
        expert_panel = ExpertPanelAssistant()
        
        # For demo purposes, select some experts
        # In a real implementation, you'd run the router first to determine this
        selected_experts = ["simon_sinek", "julie_zhuo", "roger_martin"]
        
        print(f"🎯 Selected experts: {selected_experts}")
        
        # Create dynamic crew with selected experts
        print("🚀 Creating dynamic crew...")
        dynamic_crew = expert_panel.create_dynamic_crew(selected_experts)
        
        # Run the workflow
        print("🏃 Running expert panel workflow...")
        result = dynamic_crew.kickoff(inputs=inputs)
        
        print("✅ Expert panel analysis complete!")
        print(f"📄 Full response saved to: panel_response.md")
        print(f"🎯 Result: {result}")
        
    except Exception as e:
        print(f"❌ An error occurred while running the sample: {e}")
        raise

def train():
    """
    Train the crew for a given number of iterations.
    """
    if len(sys.argv) < 3:
        print("Usage: python main.py train <n_iterations> <filename>")
        sys.exit(1)
    
    training_inputs = {
        'email': "Sample training email about leadership and team dynamics...",
        'timestamp': datetime.now().isoformat(),
        'current_year': str(datetime.now().year)
    }
    
    try:
        print(f"🎯 Training crew for {sys.argv[1]} iterations...")
        ExpertPanelAssistant().crew().train(
            n_iterations=int(sys.argv[1]), 
            filename=sys.argv[2], 
            inputs=training_inputs
        )
        print("✅ Training completed successfully!")
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    if len(sys.argv) < 2:
        print("Usage: python main.py replay <task_id>")
        sys.exit(1)
    
    try:
        print(f"🔄 Replaying from task: {sys.argv[1]}")
        ExpertPanelAssistant().crew().replay(task_id=sys.argv[1])
        print("✅ Replay completed successfully!")
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    if len(sys.argv) < 3:
        print("Usage: python main.py test <n_iterations> <eval_llm>")
        sys.exit(1)
    
    test_inputs = {
        'email': "Test email for evaluation purposes focusing on strategic decisions and team management...",
        'timestamp': datetime.now().isoformat(),
        'current_year': str(datetime.now().year)
    }
    
    try:
        print(f"🧪 Testing crew with {sys.argv[1]} iterations using {sys.argv[2]} LLM...")
        ExpertPanelAssistant().crew().test(
            n_iterations=int(sys.argv[1]), 
            eval_llm=sys.argv[2], 
            inputs=test_inputs
        )
        print("✅ Testing completed successfully!")
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def main():
    """
    Main entry point with command routing.
    """
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == "train":
            train()
        elif command == "replay":
            replay()
        elif command == "test":
            test()
        elif command == "sample":
            run_with_sample()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: train, replay, test, sample")
            print("Or run without arguments for interactive mode")
            sys.exit(1)
    else:
        run()

if __name__ == "__main__":
    main()
