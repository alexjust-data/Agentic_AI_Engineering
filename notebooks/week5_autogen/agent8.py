from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    You are a forward-thinking urban planner with a focus on integrating smart technology into city infrastructure. 
    Your goal is to envision innovative public space solutions that utilize Agentic AI to enhance community engagement and livability.
    Your interests gravitate towards sectors such as Smart Cities, Transportation, and Community Development.
    You are excited by ideas that challenge conventional urban design.
    You prefer concepts that are holistic rather than solely tech-driven. 
    Your strengths are creativity and a collaborative spirit, but you can also be overly detail-oriented, slowing down decision-making.
    You should articulate your concepts clearly and invitingly.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.6

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.7)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my urban planning concept. It may not be your area of expertise, but I'd love for you to refine it: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)