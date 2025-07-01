# Expert Panel Assistant Crew

Welcome to the Expert Panel Assistant Crew project, powered by [crewAI](https://crewai.com). This intelligent system routes incoming emails to a panel of expert AI agents who provide specialized insights based on their areas of expertise, then synthesizes their responses into cohesive, actionable replies.

## 🎯 What It Does

The Expert Panel Assistant intelligently analyzes incoming emails and routes them to the most relevant experts from a panel of renowned thought leaders:

- **🧭 Simon Sinek** - Leadership & Vision Expert
- **👥 Julie Zhuo** - Team Dynamics & Scaling Expert
- **🚀 Satya Nadella** - Transformation & Innovation Expert
- **📈 Roger Martin** - Strategic Market Positioning Expert
- **🤝 Chris Voss** - Negotiation & Persuasion Expert

The system uses a router agent to select up to 3 most relevant experts, collects their insights, and synthesizes them into a professional, markdown-formatted response.

## 🏗️ System Architecture

The crew consists of:

1. **Router Agent** - Analyzes emails and selects relevant experts (max 3)
2. **Expert Agents** - Provide specialized insights in their domains
3. **Dynamic Task Flow** - Assessment → Response → Synthesis → Quality Review
4. **Markdown Output** - Professional formatted responses with expert attribution
## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

```bash
crewai install
```

### Environment Setup
**Add your `OPENAI_API_KEY` into the `.env` file**

```bash
# .env
OPENAI_API_KEY=your_openai_api_key_here
```

## 🚀 Running the Project

### Quick Test with Sample Email

```bash
crewai run sample
```

### Interactive Mode

```bash
crewai run
```

### Available Commands

- `crewai run` - Interactive mode for processing emails
- `crewai run sample` - Test with sample email
- `crewai train <iterations> <filename>` - Train the crew
- `crewai replay <task_id>` - Replay from specific task
- `crewai test <iterations> <eval_llm>` - Test crew performance

## 📁 Project Structure
