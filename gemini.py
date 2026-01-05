# pip install google-genai

from google import genai
from google.genai import types

SYSTEM_PROMPT = """
Anda adalah chatbot khusus tentang Seni Ukir Jepara.
Anda boleh menjawab seluruh hal yang masih berkaitan dengan Seni Ukir Jepara, termasuk: sejarah, motif ukiran, teknik ukir, jenis kayu, alat ukir, proses pembuatan, nilai budaya, tokoh pengrajin, daerah penghasil ukiran, sentra industri ukir, dan informasi edukatif lain seputar seni ukir di Kabupaten Jepara.
Jika pertanyaan benar-benar tidak berkaitan dengan seni ukir Jepara, jawab dengan sopan bahwa Anda hanya bisa menjawab topik tersebut.
"""

def chat():
    # Ambil API Key
    with open("api_key.txt", "r") as f:
        api_key = f.read().strip()

    client = genai.Client(api_key=api_key)

    # Model gratis
    model = "gemini-2.0-flash"

    print("Chatbot Gemini (ketik 'selesai' / 'bye' / 'exit' untuk keluar)\n")

    while True:
        user_input = input("Anda: ")

        # Jika user mau keluar
        if user_input.lower() in ["selesai", "bye", "exit", "stop"]:
            print("\nChatbot: Sampai jumpa! 👋")
            break

        # Gabungkan system prompt + input user
        combined_prompt = f"{SYSTEM_PROMPT}\n\nPertanyaan pengguna: {user_input}"

        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=combined_prompt)],
            ),
        ]

        generate_config = types.GenerateContentConfig()

        print("Chatbot: ", end="")
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_config,
        ):
            if chunk.text:
                print(chunk.text, end="")

        print("\n")  # rapikan output

if __name__ == "__main__":
    chat()
