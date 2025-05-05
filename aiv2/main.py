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
from aiv2.agent.agent_factory import create_agent
from aiv2.tools.dynamic_tool_loader import load_default_tools

# Setup logging
logger = setup_logging()

def main():
    """
    Fungsi utama untuk menjalankan asisten AI
    """
    try:
        # Load tools & buat agent
        load_default_tools()
        agent = create_agent()
        
        logger.info("AI Assistant siap digunakan!")
        print("\n" + "="*50)
        print(" 🤖 AI Assistant Indonesia 🤖 ".center(50))
        print("="*50)
        print("Ketik 'keluar' atau 'quit' untuk keluar.")
        print("Tips: Gunakan bahasa Indonesia yang jelas untuk hasil terbaik.")
        print("="*50 + "\n")
        
        # Loop interaksi
        while True:
            try:
                user_input = input("\nPertanyaan Anda: ")
                
                # Periksa apakah user ingin keluar
                if user_input.lower() in ['keluar', 'quit', 'exit']:
                    print("Terima kasih telah menggunakan AI Assistant. Sampai jumpa!")
                    break
                
                # Kosongkan input
                if not user_input.strip():
                    continue
                
                # Jalankan agent
                print("\nSedang memikirkan jawaban...")
                response = agent.invoke({"input": user_input})
                
                # Periksa apakah response adalah dict dan memiliki 'output'
                if isinstance(response, dict) and "output" in response:
                    response_text = response["output"]
                else:
                    # Jika bukan dict, pastikan response adalah string
                    response_text = str(response)

                # Format output agar lebih rapi
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