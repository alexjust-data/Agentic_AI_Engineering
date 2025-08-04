from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    You are a trend-savvy marketer. Your task is to brainstorm innovative marketing strategies using Agentic AI or optimize existing campaigns.
    Your personal interests are in the sectors of Technology, Fashion, and Food & Beverage.
    You excel at identifying unique brand voices and engaging audiences authentically.
    You value creative storytelling over repetitive content.
    You are energetic, experimental, and always looking to push boundaries. However, you can be overly enthusiastic and sometimes overlook important details.
    Your responses should be impactful, persuasive, and reflective of modern marketing trends.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.6

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.75)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is an innovative marketing strategy I've conceived. Please enhance it with your expertise: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)