import os
import subprocess
import json
import openai

# Ensure AI Proxy Token is set
openai.api_key = os.environ.get("AIPROXY_TOKEN")

def execute_task(task: str):
    """Parses and executes a given task."""
    if "install uv" in task:
        return subprocess.run(["pip", "install", "uv"], capture_output=True, text=True).stdout
    
    elif "run datagen.py" in task:
        return subprocess.run(["python", "datagen.py", os.environ["USER_EMAIL"]], capture_output=True, text=True).stdout

    elif "format markdown" in task:
        return subprocess.run(["npx", "prettier@3.4.2", "--write", "/data/format.md"], capture_output=True, text=True).stdout

    elif "count Wednesdays" in task:
        with open("/data/dates.txt", "r") as file:
            dates = file.readlines()
        count = sum(1 for date in dates if "Wed" in date)
        with open("/data/dates-wednesdays.txt", "w") as file:
            file.write(str(count))
        return f"Counted {count} Wednesdays."

    elif "sort contacts" in task:
        with open("/data/contacts.json", "r") as file:
            contacts = json.load(file)
        contacts.sort(key=lambda c: (c["last_name"], c["first_name"]))
        with open("/data/contacts-sorted.json", "w") as file:
            json.dump(contacts, file, indent=4)
        return "Sorted contacts successfully."

    elif "fetch email sender" in task:
        with open("/data/email.txt", "r") as file:
            email_content = file.read()
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "Extract sender email address"},
                      {"role": "user", "content": email_content}]
        )
        email_address = response["choices"][0]["message"]["content"]
        with open("/data/email-sender.txt", "w") as file:
            file.write(email_address)
        return f"Extracted email: {email_address}"

    else:
        raise ValueError("Unsupported task.")

def read_file(path: str):
    """Reads the content of a file and returns it."""
    if not path.startswith("/data/"):
        raise HTTPException(status_code=403, detail="Access denied to non-data paths.")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found.")
    with open(path, "r") as file:
        return {"content": file.read()}
 
