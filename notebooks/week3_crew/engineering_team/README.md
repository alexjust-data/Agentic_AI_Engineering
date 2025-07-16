
## Building AI Teams: Configure Crew AI for Collaborative Development

```sh
(agents) ➜  my_agents git:(main) cd notebooks/week3_crew 
(agents) ➜  week3_crew git:(main) crewai create crew engineering_team
Creating folder engineering_team...
Cache expired or not found. Fetching provider data from the web...
Downloading  [####################################]  577286/26936
Select a provider to set up:
1. openai
2. anthropic
3. gemini
4. nvidia_nim
5. groq
6. huggingface
7. ollama
8. watson
9. bedrock
10. azure
11. cerebras
12. sambanova
13. other
q. Quit
Enter the number of your choice or 'q' to quit: 1
Select a model to use for Openai:
1. gpt-4
2. gpt-4.1
3. gpt-4.1-mini-2025-04-14
4. gpt-4.1-nano-2025-04-14
5. gpt-4o
6. gpt-4o-mini
7. o1-mini
8. o1-preview
q. Quit
Enter the number of your choice or 'q' to quit: 3
Enter your OPENAI API key (press Enter to skip): 
API keys and model saved to .env file
Selected model: gpt-4.1-mini-2025-04-14
  - Created engineering_team/.gitignore
  - Created engineering_team/pyproject.toml
  - Created engineering_team/README.md
  - Created engineering_team/knowledge/user_preference.txt
  - Created engineering_team/src/engineering_team/__init__.py
  - Created engineering_team/src/engineering_team/main.py
  - Created engineering_team/src/engineering_team/crew.py
  - Created engineering_team/src/engineering_team/tools/custom_tool.py
  - Created engineering_team/src/engineering_team/tools/__init__.py
  - Created engineering_team/src/engineering_team/config/agents.yaml
  - Created engineering_team/src/engineering_team/config/tasks.yaml
Crew engineering_team created successfully!
(agents) ➜  week3_crew git:(main) ✗ 
```