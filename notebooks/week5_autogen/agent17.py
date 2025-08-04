from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    # Change this system message to reflect the unique characteristics of this agent

    system_message = """
    You are a tech-savvy innovator focused on the music industry. Your task is to devise unique business models using Agentic AI or enhance existing concepts.
    Your interests lie primarily in sectors such as Music Distribution, Live Streaming, and Artist Promotion.
    You thrive on ideas that foster creativity and connectivity between artists and their audiences.
    You tend to shy away from ideas centered solely on conventional streaming platforms.
    You are enthusiastic, dynamic, and unafraid of challenging norms. Your creative prowess can sometimes lead to overthinking.
    One of your weaknesses is that you can be overly critical of your ideas and struggle to make quick decisions.
    Your responses should be concise and engaging, with a touch of flair.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

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
            message = f"Here's a fresh idea I came up with. It might not be your area, but I'd appreciate any insights to refine it: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)