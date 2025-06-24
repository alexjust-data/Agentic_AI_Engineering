def build_prompt(user_input: str) -> list[dict]:
    return [
        {
            "role": "system",
            "content": "You are a helpful assistant. You can use tools if needed."
        },
        {
            "role": "user",
            "content": user_input
        }
    ]
