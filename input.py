import chatbot
import subprocess
import os
import shlex

APPS_DIR = "applications"

def _discover_apps():
    if not os.path.isdir(APPS_DIR):
        return set()
    return {f for f in os.listdir(APPS_DIR) if f.endswith(".py")}

def _maybe_extract_command(line: str):
    """
    Returns a (python_exec, path) tuple if the line looks like:
    'python3 applications/some_app.py'
    otherwise returns None.
    """
    try:
        parts = shlex.split(line.strip())
    except ValueError:
        return None

    if len(parts) < 2:
        return None
    py, path = parts[0], parts[1]
    if py not in ("python3", "python"):
        return None
    # Require it to be inside applications/
    if not path.startswith(f"{APPS_DIR}/") or not path.endswith(".py"):
        return None
    return py, path

def user_prompt():
    client = chatbot.loadAI()
    memory = []
    allowed_apps = _discover_apps()

    print("Retro console online. Type 'stop' to exit.")

    try:
        while True:
            prompt = input("> ").strip()
            if prompt.lower() == "stop":
                print("Shutting down. Goodbye.")
                break

            

            # Get the assistant's response and emotion
            resp = chatbot.response(client, prompt, memory)
            emo = chatbot.emotion(client, resp)
            print(f"[emotion: {emo}]")
            print(resp)

            # Update memory with both user and assistant turns
            memory.append({"role": "user", "content": prompt})
            memory.append({"role": "assistant", "content": resp})

            # Scan for runnable line(s)
            for raw_line in resp.splitlines():
                maybe = _maybe_extract_command(raw_line)
                if not maybe:
                    continue
                py, path = maybe

                # Safety: ensure the referenced app actually exists
                fname = os.path.basename(path)
                if fname not in allowed_apps:
                    print(f"[blocked: {fname} not in installed apps]")
                    continue

                choice = input(f"Run '{py} {path}'? [y/N] ").strip().lower()
                if choice != "y":
                    print("[cancelled]")
                    continue

                try:
                    # Use absolute path to be explicit
                    abs_path = os.path.join(os.getcwd(), path)
                    subprocess.run([py, abs_path], check=False)
                except Exception as e:
                    print(f"[error running command: {e}]")

    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye.")

if __name__ == "__main__":
    user_prompt()
