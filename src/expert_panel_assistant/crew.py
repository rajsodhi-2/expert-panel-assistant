from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Dict
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@CrewBase
class ExpertPanelAssistant:
    """
    Expert Panel Assistant Crew for routing emails to relevant experts
    and synthesizing their responses into cohesive replies.
    """
    
    # Required attributes for @CrewBase
    agents: List[BaseAgent]
    tasks: List[Task]
    
    # Add paths to your YAML configuration files
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    selected_experts: List[str] = []
    expert_responses: Dict[str, str] = {}
    
    @staticmethod
    def get_llm_config() -> str:
        """
        Get LLM configuration from environment variable.
        Returns the LLM model string for CrewAI agents.
        """
        llm_model = os.getenv('LLM_MODEL', 'anthropic/claude-3-5-haiku-latest')
        print(f"🤖 Using LLM: {llm_model}")
        return llm_model

    @property
    def agent_map(self) -> Dict[str, Agent]:
        """Lazy-loaded agent mapping dictionary"""
        if not hasattr(self, '_agent_map'):
            self._agent_map = {
                "simon_sinek": self.simon_sinek(),
                "julie_zhuo": self.julie_zhuo(),
                "satya_nadella": self.satya_nadella(),
                "roger_martin": self.roger_martin(),
                "chris_voss": self.chris_voss()
            }
        return self._agent_map

    @agent
    def router(self) -> Agent:
        config = self.agents_config["router"].copy()  # type: ignore[index]
        config["llm"] = self.get_llm_config()
        return Agent(
            config=config,
            verbose=True
        )

    @agent
    def simon_sinek(self) -> Agent:
        config = self.agents_config["simon_sinek"].copy()  # type: ignore[index]
        config["llm"] = self.get_llm_config()
        return Agent(
            config=config,
            verbose=True
        )

    @agent
    def julie_zhuo(self) -> Agent:
        config = self.agents_config["julie_zhuo"].copy()  # type: ignore[index]
        config["llm"] = self.get_llm_config()
        return Agent(
            config=config,
            verbose=True
        )

    @agent
    def satya_nadella(self) -> Agent:
        config = self.agents_config["satya_nadella"].copy()  # type: ignore[index]
        config["llm"] = self.get_llm_config()
        return Agent(
            config=config,
            verbose=True
        )

    @agent
    def roger_martin(self) -> Agent:
        config = self.agents_config["roger_martin"].copy()  # type: ignore[index]
        config["llm"] = self.get_llm_config()
        return Agent(
            config=config,
            verbose=True
        )

    @agent
    def chris_voss(self) -> Agent:
        config = self.agents_config["chris_voss"].copy()  # type: ignore[index]
        config["llm"] = self.get_llm_config()
        return Agent(
            config=config,
            verbose=True
        )

    @task
    def route_task(self) -> Task:
        return Task(
            config=self.tasks_config["route_task"]  # type: ignore[index]
        )

    @task
    def expert_assessment_task(self) -> Task:
        return Task(
            config=self.tasks_config["expert_assessment_task"]  # type: ignore[index]
        )

    @task
    def expert_response_task(self) -> Task:
        return Task(
            config=self.tasks_config["expert_response_task"]  # type: ignore[index]
        )

    @task
    def synthesis_task(self) -> Task:
        return Task(
            config=self.tasks_config["synthesis_task"]  # type: ignore[index]
        )

    @task
    def quality_review_task(self) -> Task:
        return Task(
            config=self.tasks_config["quality_review_task"]  # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """
        Creates the full crew with all agents and tasks.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

    def get_expert_agent_by_name(self, name: str) -> Agent:
        """Helper method to get expert agent by name - reuses existing instances"""
        return self.agent_map.get(name)

    def _get_expert_emoji_and_title(self, expert_name: str) -> tuple:
        """Get emoji and title for each expert"""
        expert_formatting = {
            "simon_sinek": ("🧭", "Leadership & Vision"),
            "julie_zhuo": ("👥", "Team Dynamics & Scaling"),
            "satya_nadella": ("🚀", "Transformation & Innovation"),
            "roger_martin": ("📈", "Strategy & Market Positioning"),
            "chris_voss": ("🤝", "Negotiation & Persuasion")
        }
        return expert_formatting.get(expert_name, ("💡", "Expert Insights"))

    def create_dynamic_crew(self, selected_experts: List[str]) -> Crew:
        """
        Creates a dynamic crew with only the selected experts.
        This bypasses the routing task and directly engages the selected experts.
        """
        self.selected_experts = selected_experts
        
        # Create only the agents we need
        dynamic_agents = []
        dynamic_tasks = []

        # Add only the selected expert agents
        for expert_name in selected_experts:
            expert_agent = self.get_expert_agent_by_name(expert_name)
            if expert_agent:
                dynamic_agents.append(expert_agent)

                # Create assessment and response tasks for each expert
                # Use a simpler approach without accessing config directly
                assessment_task = Task(
                    description=f"""
                    Review the email content and determine if it falls within your area of expertise as {expert_name}. 
                    If yes, prepare to provide insights. If no, decline politely.
                    
                    Email Content:
                    {{email}}
                    """,
                    expected_output="Either 'RELEVANT' with a brief note on why this falls in your expertise, OR 'NOT RELEVANT - No insights to add.'",
                    agent=expert_agent
                )
                
                response_task = Task(
                    description=f"""
                    Provide a concise, actionable response to the email based on your expertise as {expert_name}. 
                    Focus on practical insights, strategic recommendations, or tactical guidance that directly 
                    addresses the sender's needs. Keep responses focused and implementable.
                    
                    Email Content:
                    {{email}}
                    """,
                    expected_output="A thoughtful, actionable paragraph (3-5 sentences) that provides specific value based on your expertise. Include concrete next steps or frameworks when applicable.",
                    agent=expert_agent,
                    context=[assessment_task]  # Response depends on assessment
                )
                dynamic_tasks.extend([assessment_task, response_task])

        # Add router agent for synthesis and quality control
        router_agent = self.router()
        dynamic_agents.append(router_agent)

        # Create synthesis task that uses all expert responses as context
        # Get just the response tasks (every second task starting from index 1)
        expert_response_tasks = [dynamic_tasks[i] for i in range(1, len(dynamic_tasks), 2)]
        
        synthesis_task = Task(
            description=f"""
            Compile all expert responses into a cohesive, well-structured reply email with enhanced formatting. 
            Organize insights by expert using clear markdown headers with relevant emojis. Create a professional 
            yet engaging response that maintains each expert's unique voice while ensuring the message flows naturally.
            
            Selected experts: {', '.join(selected_experts)}
            
            Use this structure:
            - Start with executive summary
            - Present each expert's insights with emoji headers
            - Include concrete next steps
            - End with collaborative summary
            
            Expert emoji mapping:
            - Simon Sinek: 🧭 (Leadership & Vision)
            - Julie Zhuo: 👥 (Team Dynamics & Scaling) 
            - Satya Nadella: 🚀 (Transformation & Innovation)
            - Roger Martin: 📈 (Strategy & Market Positioning)
            - Chris Voss: 🤝 (Negotiation & Persuasion)
            
            Original Email:
            {{email}}
            """,
            expected_output="""
            A professionally formatted markdown email response with:
            
            ## 🎯 Key Insights from Expert Panel
            
            **Executive Summary:** [Brief overview of main recommendations]
            
            ---
            
            ### [Emoji] [Expert Name] on [Expertise Area]
            *[Expert's main insight and recommendations]*
            
            **Key Actions:**
            - [Specific actionable item 1]
            - [Specific actionable item 2]
            
            ---
            
            [Repeat for each expert]
            
            ---
            
            ## 🎯 Integrated Recommendations
            
            **Immediate Actions (Next 30 Days):**
            1. [Priority action item]
            2. [Priority action item]
            
            **Strategic Initiatives (Next Quarter):**
            1. [Strategic initiative]
            2. [Strategic initiative]
            
            ---
            
            *This response was generated by our Expert Advisory Panel. For follow-up questions or deeper discussion on any of these areas, please let us know.*
            """,
            agent=router_agent,
            context=expert_response_tasks,  # Use all expert responses as context
            markdown=True,
            output_file="panel_response.md"  # Save synthesis output to file
        )
        
        quality_task = Task(
            description="""
            Review the synthesized response for clarity, completeness, and professionalism. 
            Ensure all key points from the original email are addressed and that the response 
            provides genuine value to the recipient.
            
            Original Email:
            {email}
            """,
            expected_output="Either 'APPROVED' if the response meets quality standards, OR specific recommendations for improvement focusing on clarity, completeness, or actionability.",
            agent=router_agent,
            context=[synthesis_task]  # Quality review the synthesis
        )

        dynamic_tasks.extend([synthesis_task, quality_task])

        return Crew(
            agents=dynamic_agents,
            tasks=dynamic_tasks,
            process=Process.sequential,
            verbose=True
        )
