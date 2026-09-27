import os

from openai import OpenAI

client = OpenAI(
    api_key=os.environ["MISTRAL_API_KEY"],
    base_url="https://api.mistral.ai/v1",
)

SYSTEM_MESSAGE = "You are a terminal assistant. Be concise."
TOOLS = []


def dispatch(call):
    return f"error: unknown tool {call.function.name}"


def run_agent(messages, max_turns=25):
    for _ in range(max_turns):
        reply = client.chat.completions.create(
            model="mistral-small-latest",
            messages=messages,
            tools=TOOLS,
        )
        message = reply.choices[0].message
        messages.append(message)
        if not message.tool_calls:
            print(message.content)
            return
        for call in message.tool_calls:
            result = dispatch(call)
            messages.append(
                {"role": "tool", "tool_call_id": call.id, "content": result}
            )
    print("(max turns reached)")


def main():
    messages = [{"role": "system", "content": SYSTEM_MESSAGE}]
    while True:
        user_input = input("> ")
        if user_input.strip().lower() in ("exit", "quit"):
            break
        messages.append({"role": "user", "content": user_input})
        run_agent(messages)


if __name__ == "__main__":
    main()
