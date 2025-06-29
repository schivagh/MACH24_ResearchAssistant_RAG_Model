import os
import subprocess
import sys
import venv

def create_virtualenv(env_dir="venv"):
    if not os.path.exists(env_dir):
        print("🔧 Creating virtual environment...")
        venv.create(env_dir, with_pip=True)
    else:
        print("✅ Virtual environment already exists.")

def install_requirements(env_dir="venv"):
    pip_path = os.path.join(env_dir, "bin", "pip") if os.name != "nt" else os.path.join(env_dir, "Scripts", "pip.exe")
    print("📦 Installing required libraries...")

    output = subprocess.check_output(["python", "-c", "import os, sys; print(os.path.dirname(sys.executable))"])
    pythonpath = output.decode().strip()

    python_exe = os.path.join(pythonpath, "python.exe")

    subprocess.check_call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])    
    
    subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])

def run_streamlit_app(env_dir="venv"):
    os.environ["STREAMLIT_WATCHER_TYPE"] = "none"
    python_path = os.path.join(env_dir, "bin", "python") if os.name != "nt" else os.path.join(env_dir, "Scripts", "python.exe")
    print("🚀 Launching Streamlit app...")
    subprocess.run([python_path, "-m", "streamlit", "run", "streamlit_app.py"])



if __name__ == "__main__":
    env_dir = "venv"

    create_virtualenv(env_dir)
    install_requirements(env_dir)
    run_streamlit_app(env_dir)
