#################################################
# main.py
#################################################
"""
AI Assistant berbasis Ollama dengan beragam kemampuan
"""
import sys
import logging
import textwrap
from aiv2.utils.logging_setup import setup_logging
from aiv2.agent.agent_factory import create_agent, run_agent_with_history
from aiv2.tools.dynamic_tool_loader import load_default_tools

# Setup logging
logger = setup_logging()

def main():
    """
    Fungsi utama untuk menjalankan asisten AI
    """
    try:
        load_default_tools()
        agent = create_agent()

        logger.info("AI Assistant siap digunakan!")
        print("\n" + "="*50)
        print(" 🤖 AI Assistant Indonesia 🤖 ".center(50))
        print("="*50)
        print("Ketik 'keluar' atau 'quit' untuk keluar.")
        print("Tips: Gunakan bahasa Indonesia yang jelas untuk hasil terbaik.")
        print("="*50 + "\n")

        chat_history = ""

        while True:
            try:
                user_input = input("\nPertanyaan Anda: ")
                
                if user_input.lower() in ['keluar', 'quit', 'exit']:
                    print("Terima kasih telah menggunakan AI Assistant. Sampai jumpa!")
                    break

                if not user_input.strip():
                    continue

                print("\nSedang memikirkan jawaban...")

                response = run_agent_with_history(agent, user_input, chat_history)

                if isinstance(response, dict) and "output" in response:
                    response_text = response["output"]
                else:
                    response_text = str(response)

                # Tambahkan ke chat history
                chat_history += f"Human: {user_input}\nAI: {response_text}\n"

                formatted_response = "\n".join(
                    textwrap.fill(line, width=80)
                    for line in response_text.split('\n')
                )

                print("\nJawaban:")
                print(formatted_response)

            except KeyboardInterrupt:
                print("\nProses dihentikan.")
                break
            except Exception as e:
                logger.error(f"Error while processing query: {e}")
                print(f"\nMaaf, terjadi kesalahan: {str(e)}")
                print("Silakan coba pertanyaan lain.")

    except Exception as e:
        logger.error(f"Failed to initialize AI Assistant: {e}")
        print(f"Gagal menginisialisasi AI Assistant: {str(e)}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
