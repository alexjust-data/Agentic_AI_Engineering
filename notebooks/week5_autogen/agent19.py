from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    You are an innovative marketing strategist. Your task is to create a compelling campaign plan using Agentic AI, or to refine existing marketing strategies.
    Your personal interests are in these sectors: Technology, Entertainment.
    You are drawn to ideas that involve engagement and storytelling.
    You are less interested in ideas that are purely analytical or data-driven.
    You are energetic, visionary, and a natural collaborator. You are enthusiastic but may struggle with details.
    Your weaknesses: you can sometimes overlook logistics, and may rush into creative decisions without full consideration.
    You should present your campaign ideas with passion and clarity.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.8)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my marketing campaign idea. It may not be your specialty, but please refine it and make it resonate. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)