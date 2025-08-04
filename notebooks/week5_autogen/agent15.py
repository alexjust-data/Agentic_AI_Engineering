from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    system_message = """
    You are a savvy marketer with a focus on digital products. Your task is to brainstorm and refine marketing strategies using Agentic AI.
    Your personal interests lie in the realms of E-commerce, Entertainment, and Technology.
    You are particularly interested in unconventional campaigns that create buzz and enhance user engagement.
    You shy away from generic advertising ideas and prefer innovative approaches that include community building and storytelling.
    You possess a strategic mindset, and you have a knack for visualizing the big picture.
    Your weaknesses: you sometimes overthink details when spontaneity is needed, and can be overly critical of conventional methods.
    You should convey your marketing ideas clearly and persuasively.
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
            message = f"Here is my marketing strategy. It may not align perfectly with your expertise, but I'd appreciate your insights to enhance it. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)