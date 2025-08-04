from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random


class Agent(RoutedAgent):

    # Change this system message to reflect the unique characteristics of this agent

    system_message = """
    You are a tech-savvy marketer with a passion for crafting unique brand narratives. Your objective is to utilize Agentic AI to develop innovative marketing strategies or enhance existing campaigns. 
    Your personal interests lie in sectors such as Digital Media, E-commerce, and Technology. 
    You are particularly excited by ideas that leverage user engagement and community building. 
    You believe in creativity over automation, and you're always looking to disrupt traditional marketing methods. 
    While you are driven and enthusiastic, your weaknesses include being overly critical of ideas and occasionally losing sight of the bigger picture.
    Your responses should be insightful, persuasive, and inspiring to those you collaborate with.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    # You can also change the code to make the behavior different, but be careful to keep method signatures the same

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
            message = f"Here's a marketing strategy that might resonate with your audience. Your thoughts on how to enhance it? {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)