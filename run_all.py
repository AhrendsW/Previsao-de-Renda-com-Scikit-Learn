import subprocess
import sys
import os
from threading import Thread

def run_api():
    if sys.platform.startswith('win'):
        os.system('start cmd /k ".venv\\Scripts\\activate && uvicorn src.api.api:app --reload"')
    else:
        os.system('gnome-terminal -- bash -c "source .venv/bin/activate && uvicorn src.api.api:app --reload; exec bash"')

def run_streamlit():
    if sys.platform.startswith('win'):
        os.system('start cmd /k ".venv\\Scripts\\activate && streamlit run src/ui/app.py"')
    else:
        os.system('gnome-terminal -- bash -c "source .venv/bin/activate && streamlit run src/ui/app.py; exec bash"')

if __name__ == "__main__":
    print("Iniciando API e Streamlit em terminais separados...")
    
    api_thread = Thread(target=run_api)
    streamlit_thread = Thread(target=run_streamlit)
    
    api_thread.start()
    streamlit_thread.start()
    
    print("\n✅ API e Streamlit iniciados com sucesso!")
    print("📌 API disponível em: http://localhost:8000")
    print("📌 Interface Streamlit disponível em: http://localhost:8501")
    print("\n⚠️ Para encerrar a aplicação:")
    print("   1. Feche manualmente as janelas dos terminais abertos, ou")
    print("   2. Em cada terminal, pressione Ctrl+C para interromper o processo.") 