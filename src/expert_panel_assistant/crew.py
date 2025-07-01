from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Dict, Any

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
        return Agent(
            config=self.agents_config["router"],  # Changed from **self.agents_config
            verbose=True
        )

    @agent
    def simon_sinek(self) -> Agent:
        return Agent(
            config=self.agents_config["simon_sinek"],  # Changed from **self.agents_config
            verbose=True
        )

    # Expert Agents - Fixed
    @agent
    def julie_zhuo(self) -> Agent:
        return Agent(
            config=self.agents_config["julie_zhuo"],  # Changed from **self.agents_config
            verbose=True
        )

    @agent
    def satya_nadella(self) -> Agent:
        return Agent(
            config=self.agents_config["satya_nadella"],  # Changed from **self.agents_config
            verbose=True
        )

    @agent
    def roger_martin(self) -> Agent:
        return Agent(
            config=self.agents_config["roger_martin"],  # Changed from **self.agents_config
            verbose=True
        )

    @agent
    def chris_voss(self) -> Agent:
        return Agent(
            config=self.agents_config["chris_voss"],  # Changed from **self.agents_config
            verbose=True
        )

    # Core Workflow Tasks - Fixed
    @task
    def route_task(self) -> Task:
        return Task(
            config=self.tasks_config["route_task"]  # Changed from **self.tasks_config
            # Removed agent assignment - let it be handled by config or dynamically
        )

    @task
    def expert_assessment_task(self) -> Task:
        return Task(
            config=self.tasks_config["expert_assessment_task"]  # Changed from **self.tasks_config
            # Removed agent assignment - will be handled dynamically
        )

    @task
    def expert_response_task(self) -> Task:
        return Task(
            config=self.tasks_config["expert_response_task"]  # Changed from **self.tasks_config
            # Removed agent assignment - will be handled dynamically
        )

    @task
    def synthesis_task(self) -> Task:
        return Task(
            config=self.tasks_config["synthesis_task"]  # Changed from **self.tasks_config
            # Removed agent assignment - let it be handled by config or dynamically
        )

    @task
    def quality_review_task(self) -> Task:
        return Task(
            config=self.tasks_config["quality_review_task"]  # Changed from **self.tasks_config
            # Removed agent assignment - let it be handled by config or dynamically
        )

    @crew
    def crew(self) -> Crew:
        """
        Creates the full crew with all agents and tasks.
        The process will be dynamically managed based on routing decisions.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            output_file="panel_response.md"
        )

    def get_expert_agent_by_name(self, name: str) -> Agent:
        """Helper method to get expert agent by name - reuses existing instances"""
        return self.agent_map.get(name)  # Now uses the property

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
        """
        router_agent = self.router()
        dynamic_agents = [router_agent]
        dynamic_tasks = [self.route_task()]

        self.selected_experts = selected_experts

        for expert_name in selected_experts:
            expert_agent = self.get_expert_agent_by_name(expert_name)
            if expert_agent:
                dynamic_agents.append(expert_agent)

                # Create new task instances with proper config
                assessment_task = Task(
                    config=self.tasks_config["expert_assessment_task"],
                    agent=expert_agent
                )
                response_task = Task(
                    config=self.tasks_config["expert_response_task"],
                    agent=expert_agent
                )
                dynamic_tasks.extend([assessment_task, response_task])

        # Create synthesis and quality tasks with proper agent assignment
        synthesis_task = Task(
            config=self.tasks_config["synthesis_task"],
            agent=router_agent
        )
        quality_task = Task(
            config=self.tasks_config["quality_review_task"],
            agent=router_agent
        )

        dynamic_tasks.extend([synthesis_task, quality_task])

        return Crew(
            agents=dynamic_agents,
            tasks=dynamic_tasks,
            process=Process.sequential,
            verbose=True,
            output_file="panel_response.md"
        )
