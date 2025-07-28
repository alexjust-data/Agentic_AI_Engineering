## Microsoft Autogen 0.5.1: AI Agent Framework Explained for Beginners

Now, I know exactly what you’re thinking. “Another framework? Another week, another reset, another new thing to learn. I just want to get to MCP—that’s what all the hype is about! That’s week six. Why are we doing another framework now?”

But I’ve got plenty of good news for you. First, this week’s framework—**AutoGen**—will actually be really quick and simple to pick up, because it shares a lot in common with the others we’ve used so far. We’re going to move through it at a brisk pace. Secondly, the whole week itself is going to be much faster. I know, I said that last time, but last week I got so caught up in LineGraph, I couldn’t help myself. This time, I really mean it: this week will be nice and brisk, setting us up for the pinnacle of the course in week six.

And here’s a third piece of good news: we’ll actually get a preview of MCP *this* week as well. So, not only are we covering AutoGen, we’re also going to dip our toes into what’s coming next. With that, welcome to week five: understanding AutoGen concepts—specifically, **AutoGen from Microsoft**. Let’s dive in.

![](../img/66.png)

So, introducing AutoGen. You’ll recognize it by that ‘AG’ logo. AutoGen is Microsoft’s open-source agent framework. The major rewrite—version 0.4—was released in January, and it represents a ground-up overhaul. This new version is based on an asynchronous, event-driven architecture, aimed at addressing prior criticisms about observability (can you really see what’s happening in agent interactions?), as well as offering more flexibility, control, and scalability. This is a complete replacement for the old AutoGen 0.2, with a very different architecture and feel.

So, naturally, I faced a decision: should we use AutoGen 0.4 or stick with 0.2? I decided to… stick with 0.2? No, of course not—I’m joking. We’re using 0.4. Or actually, not even that—we’re going with **0.5.1**, which is the current version as of right now. They’ve moved beyond 0.4, but 0.5.1 isn’t radically different from 0.4. So yes, we’re using the latest, refreshed version of AutoGen released this year.

However, a word of caution: if you search for documentation, you *must* check whether you’re looking at docs for 0.4+ or the older 0.2 version—they’re very different in structure and usage.

![](../img/67.png)

But wait, there’s more—a bit of drama in the AutoGen world. Late last year, the original creator and several key co-founders of AutoGen left Microsoft, where it was being developed as open source, and branched off to create a fork: a different, community-led version. The original creator is now at Google and working on this new fork, called **AG2** (short for AutoGen 2, also known as AgentOS 2). Here’s where it gets even more confusing: AG2 started from the 0.2 codebase, so it’s both compatible and somewhat consistent with the *old* version of AutoGen, but it diverges completely from the new Microsoft path (post-fork, post-0.4).

In other words, AG2 is like a “throwback” to what AutoGen used to be, and this has made things pretty confusing. The rationale for the fork was to allow faster, more flexible development, free from the bureaucracy of Microsoft. On the flip side, being part of Microsoft has obvious advantages: the mainline AutoGen (Microsoft’s) is widely used in enterprises, has major adoption, and remains highly visible.

This split created some bizarre situations. For example, Microsoft also lost control of the official AutoGen Discord group, which is now managed by the AG2/AgentOS 2 team. As a result, a lot of community discussion is about AG2, not Microsoft’s AutoGen. So newcomers can get very confused: if you search for AutoGen documentation, you might end up looking at AG2 (which is based on 0.2) instead of the Microsoft-supported track.

Microsoft, for their part, have made it absolutely clear they’re not slowing down development on their AutoGen, especially as seen in the new architecture from 0.4 onward. Meanwhile, the AG2 camp argues they can move faster and more flexibly, and they have been releasing new versions at a rapid pace—they’re already up to AG2 version 0.8. Version numbers don’t always tell the whole story, but it does create the perception of rapid progress, which was one of their main motivations for the fork.

There’s one more spicy twist: the AG2 team has control of the official AutoGen package on PyPI. So, if you do a simple `pip install autogen`, you’ll get AG2—not Microsoft’s official version! This is more than a little amusing, but also confusing (and arguably problematic) for newcomers, who expect that a Microsoft project would “own” the official PyPI install. Instead, a `pip install autogen` gets you a version built by a group of former maintainers—important renegades, so to speak, whose “rebellion” has created something impressive but very different from what Microsoft now maintains.

So, bottom line: we’re going with the Microsoft track for this course. That’s where the largest community and the greatest current traction is. But I want you to be aware of this split, and stay alert for confusion in documentation, examples, or community chat—especially around AG2.

Now, since we’re using UV as our environment, I’ve already set up the correct projects for you. What’s installed will be the official Microsoft AutoGen, currently at version 0.5.1 (though that will likely move forward quickly). They’re not at 0.8—yet!

That’s the full story. I hope it makes sense.


## AutoGen vs Other Agent Frameworks: Features & Components Compared

![](../img/68.png)

So with that, let’s move on to talk about what Autogen actually is.

Let’s first remind you where we are: these are the frameworks we’ve been going through. Autogen is the last of the frameworks—since MCP isn’t really a framework in the strict sense.



### What is Autogen

Like the others, **Autogen** is a collection of different components all bundled under one umbrella. Here’s how it’s structured:

![](../img/63.png)

* **AutoGen Core** is the foundation.

  * It is *agnostic* to which agents or LLMs you use.
  * Think of it as a **general framework for building scalable, multi-agent systems**.
  * It manages messaging between agents, even if they’re distributed in different places.
  * It acts as a *fabric* or *runtime* for agents to run together.
  * While it shares some conceptual ground with something like LandGraph, it’s much, much simpler.
  * In essence, **AutoGen Core is an agent runtime.**

* On top of Core is **AutoGen AgentChat**.

  * The name is a bit of a mouthful!
  * This layer will be very familiar to you—it’s much like OpenAI Agents SDK and Crew.
  * It provides a **lightweight, simple abstraction for combining LLMs in an agent construct**, so they can use tools and interact with each other.
  * **AgentChat** is built directly on Core, making it the main way to construct conversational, multi-agent applications.

* Built on top of AgentChat are:

  * **Studio**:

    * A low-code/no-code visual app builder for constructing agent workflows.
  * **Magentic One CLI**:

    * A product you use from the command line—a ready-to-use application that can run an agent framework out-of-the-box.

![](../img/64.png)

All of these components are open source and maintained by Microsoft Research, but they have contributions from all over the world. There’s a key difference from frameworks like Crew and LangChain: with Microsoft, **AutoGen is positioned as a research project for the community**. There’s no commercial “push” shaping the roadmap here. Things like Studio and Magentic One are considered research environments—not ready for production (as they say very clearly in the docs). So, it’s a different positioning: this is a large open-source contribution through and through.

Of course, no surprise—our focus will be on **AutoGen Core** and especially **AutoGen AgentChat**, as these are the most relevant parts for us as coders. The low-code/no-code options are less interesting for now, and Magentic One CLI is cool but essentially like a packaged version of what we built ourselves last week with our “sidekick” or “coworker”.

One more point to highlight: **AutoGen AgentChat** is the direct analogue of Crew, OpenAI Agents SDK, and the agent interaction layer in LandGraph. We’ll also dip into Core for some interesting experiments, but most of our time will be spent with AgentChat.

### The Building Blocks of Autogen

So, what are the core concepts in the Autogen framework—especially in AgentChat? Here’s where it gets even more familiar.

![](../img/65.png)

* **Models**

  * In Autogen, “models” correspond to language models (LLMs), exactly as we’ve seen in other platforms.

* **Messages**

  * A key concept in Autogen. Messages can represent:

    * Communication between agents,
    * Events that happen inside an agent (like calling a tool),
    * Results from a model.
  * Whether it’s an agent-to-agent communication, an internal action, or an interaction with a model—these are all considered “messages”.

* **Agents**

  * Just as we’re used to: an agent is something with a model behind it, able to carry out tasks on behalf of a user or another agent.

* **Teams**

  * This is like a “crew” in Crew: a group of agents collaborating to achieve a goal.

There are other advanced concepts, but these are the most important to introduce right now. For today, we’ll be focusing on the first three—**models, messages, and agents**—as we quickly set up an example. And to make it even more practical, we’ll include some SQL in the example, since I know that’s valuable for many.

Let’s jump in!



