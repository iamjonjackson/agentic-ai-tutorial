import os

from openai import OpenAI

client = OpenAI(
    api_key=os.environ["MISTRAL_API_KEY"],
    base_url="https://api.mistral.ai/v1",
)

SYSTEM_MESSAGE = "You are a terminal assistant. Be concise."


def main():
    messages = [{"role": "system", "content": SYSTEM_MESSAGE}]
    while True:
        user_input = input("> ")
        if user_input.strip().lower() in ("exit", "quit"):
            break
        messages.append({"role": "user", "content": user_input})
        reply = client.chat.completions.create(
            model="mistral-small-latest",
            messages=messages,
        )
        messages.append(reply.choices[0].message)
        print(reply.choices[0].message.content)


if __name__ == "__main__":
    main()
