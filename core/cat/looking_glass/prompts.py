
from typing import List

from langchain.agents.tools import BaseTool
from langchain.prompts import StringPromptTemplate

# TODO: get by hook
DEFAULT_TOOL_TEMPLATE = """Answer the following question: `{input}`
You can only reply using these tools:

{tools}

If you want to use tools, use the following format:
Action: the name of the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
...
Action: the name of the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action

When you have a final answer respond with:
Final Answer: the final answer to the original input question (or "?" if no tool is adapt)

Begin!

Question: {input}
{agent_scratchpad}"""


class ToolPromptTemplate(StringPromptTemplate):
    # The template to use
    template: str = DEFAULT_TOOL_TEMPLATE
    # The list of tools available
    tools: List[BaseTool]

    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\n"
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])

        return self.template.format(**kwargs)