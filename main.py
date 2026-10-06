import argparse
import os
import sys

from dotenv import load_dotenv  # pyright: ignore[reportMissingImports]
from openai import OpenAI  # pyright: ignore[reportMissingImports]

import prompts
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("No API key found")

client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=api_key,
)


def main():



    parser = argparse.ArgumentParser(description="Tilino Code Chat")
    parser.add_argument("user_prompt", type=str, help="Prompt del usuario")
    parser.add_argument("--verbose", action="store_true", help="Habilita el output verbose")
    args = parser.parse_args()

    messages=[
        {"role": "system", "content": prompts.system_prompt},
        {"role":"user", "content": args.user_prompt},
    ]

    for i in range(20):
        response = client.chat.completions.create(
            model="gemini-3.1-flash-lite",
            messages=messages,
            tools=available_functions,
        )

        if response.usage.prompt_tokens == None or response.usage.completion_tokens == None:
            raise RuntimeError("Prompt tokens or Response tokens missing")
        if args.verbose:
            print(f"User prompt: {args.user_prompt}\n")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}\n")

        message = response.choices[0].message
        messages.append(message)
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, args.verbose)
                if not result_message['content']:
                    raise RuntimeError("Error: empty function content")
                if args.verbose:
                    print(f"-> {result_message['content']}")
                messages.append(result_message)
        else:
            print(message.content)
            break
        if message.tool_calls and i==19:
            print("\n\nThe LLM has exceeded the maximum allowed number of calls before a final message.")
            sys.exit(1)






if __name__ == "__main__":
    main()
