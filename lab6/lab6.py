import os
from openai import OpenAI

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found. Set it first, then run again.")
        return

    client = OpenAI(api_key=api_key)

    system_prompt = (
        "You are a math-solving chatbot. "
        "Solve the user's math word problems correctly. "
        "Show short, clear steps, then provide a final answer on a new line as: 'Final: <answer>'. "
        "If the user input is not a math problem, politely ask them to enter a math problem."
    )

    print("LLM Math Chatbot (Lab 6)")
    print("Type a math problem. Type 'exit' to quit.\n")

    while True:
        user_text = input("You: ").strip()
        if not user_text:
            continue
        if user_text.lower() in {"exit", "quit", "q"}:
            print("Bye!")
            break

        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_text},
                ],
                temperature=0.0,
            )

            answer = resp.choices[0].message.content
            print("\nBot:", answer, "\n")

        except Exception as e:
            print(f"\n❌ Error calling OpenAI API: {e}\n")

if __name__ == "__main__":
    main()
