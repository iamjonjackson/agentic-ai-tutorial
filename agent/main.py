import os

from openai import OpenAI

from agent import rag, tools_fs, tools_gmail
from agent.scrub import scrub

client = OpenAI(
    api_key=os.environ["MISTRAL_API_KEY"],
    base_url="https://api.mistral.ai/v1",
)

SYSTEM_MESSAGE = "You are a terminal assistant. Be concise."
TOOLS = tools_fs.TOOLS + rag.RAG_TOOLS + tools_gmail.GMAIL_TOOLS

dispatch = tools_fs.dispatch
tools_fs.TOOL_IMPLS.update(rag.RAG_TOOL_IMPLS)
tools_fs.TOOL_IMPLS.update(tools_gmail.GMAIL_TOOL_IMPLS)
from agent import policy
policy.ASK.add("send_mail")


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
                {"role": "tool", "tool_call_id": call.id, "content": scrub(result)}
            )
    print("(max turns reached)")


def load_project_memory(cwd):
    for name in ("AGENT.md", "CLAUDE.md"):
        path = os.path.join(cwd, name)
        if os.path.isfile(path):
            with open(path) as f:
                return f.read(4000)
    return ""


def main():
    messages = [{"role": "system", "content": SYSTEM_MESSAGE}]
    memory = load_project_memory(os.getcwd())
    if memory:
        messages.append({"role": "user", "content": memory})
    while True:
        user_input = input("> ")
        if user_input.strip().lower() in ("exit", "quit"):
            break
        messages.append({"role": "user", "content": user_input})
        run_agent(messages)


if __name__ == "__main__":
    main()
