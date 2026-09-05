# 111-Backend

A small web server built with **Flask**, a Python tool for making websites and APIs.

Right now it has one endpoint (one "address" you can visit) that just reports whether
the server is alive. It's called a *health check* — the same idea as a doctor taking
your pulse to confirm you're still breathing.

```
GET http://127.0.0.1:5000/api/health   →   200  {"status": "Ok"}
```

---

## What's in here

| File | What it does |
| --- | --- |
| `server.py` | The actual program. Defines the server and its routes. |
| `venv/` | A private folder holding this project's Python and its add-ons. |
| `notes.txt` | Class notes on the setup commands. |
| `README.md` | This file. |

---

## Setup (do this once)

**1. Create the virtual environment**

```bash
python3 -m venv venv
```

A *virtual environment* (venv) is a private toolbox for one project. Instead of
installing Flask onto your whole computer where every project shares it, you install
it into this folder only. That way this project can use Flask 3.1 while some other
project uses Flask 2.0, and neither one breaks the other.

> ⚠️ This command takes a few seconds. **Do not press Ctrl+C while it runs.**
> See Problem #1 below for what happens if you do.

**2. Activate it**

```bash
source venv/bin/activate
```

**3. Install Flask**

```bash
pip install Flask
```

---

## Running the server

Every time you open a new terminal:

```bash
source venv/bin/activate
python server.py
```

You'll see:

```
* Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

The terminal will look frozen. **That's normal** — the server is running and waiting
for requests. Leave that tab alone. Open a *second* terminal tab if you need to type
other commands.

To stop the server, click that terminal and press `Ctrl+C`.

---

## Testing it with Thunder Client

Thunder Client is a VS Code extension that sends requests to your server so you can
see what comes back.

1. Make sure the server is running (previous section).
2. Open Thunder Client → **New Request**
3. Method: `GET`
4. URL: `http://127.0.0.1:5000/api/health`
5. Hit **Send**

You should get **Status: 200 OK** and this body:

```json
{ "status": "Ok" }
```

---

## Troubleshooting: problems I hit, and the fixes

These are the real errors that came up while setting this up. If you see one again,
here's what it means in plain English.

### Problem 1 — `KeyboardInterrupt` while creating the venv

**What I saw:**

```
File ".../subprocess.py", line 1208, in communicate
KeyboardInterrupt
```

**What it means:** `python3 -m venv venv` was still working when it got cancelled
(that's what Ctrl+C does). It had already made the folder and copied Python in, but
it never got to the part that installs `pip` or writes the `activate` script.

So I *had* a `venv` folder — it just wasn't finished. That's worse than having none,
because everything looks fine at a glance but nothing works.

**The fix:** delete the half-built one and start over. Let it finish this time.

```bash
rm -rf venv
python3 -m venv venv
```

**Lesson:** a folder existing doesn't mean it's complete. When a setup step gets
interrupted, redo it from scratch rather than trying to patch it up.

---

### Problem 2 — `source: no such file or directory: venv/bin/Activate`

**What I saw:**

```
source venv/bin/Activate
source: no such file or directory: venv/bin/Activate
```

**What it means:** capital **A**. The real file is `activate`, all lowercase. Mac and
Linux treat `Activate` and `activate` as two completely different names, so the
computer went looking for a file that doesn't exist.

(My `notes.txt` had it capitalized, which is where the typo came from. The notes also
say `venv\Script\Activate` for Windows — that's missing an *s*; it's `Scripts`.)

**The fix:**

```bash
source venv/bin/activate
```

**Lesson:** on Mac, capitalization in filenames matters. Always.

---

### Problem 3 — `zsh: command not found: pip`

**What it means:** two things at once.

- The venv wasn't activated, so the `pip` that lives inside `venv/bin/` wasn't
  reachable.
- This Mac's system Python only provides `pip3`, never a plain `pip`.

**The fix:** activate first. Once you do, plain `pip` works, because activating puts
`venv/bin/` at the front of the list of places your terminal searches for commands.

```bash
source venv/bin/activate
pip install Flask
```

---

### Problem 4 — `ModuleNotFoundError: No module named 'flask'`

**What I saw:**

```
from flask import Flask, jsonify
ModuleNotFoundError: No module named 'flask'
```

...even though I had definitely installed Flask.

**What it means:** Flask *was* installed — into the venv. But I ran the program with
the **system** Python, which is a completely separate installation that has never
heard of Flask.

Here's the proof:

| Which Python | Has Flask? |
| --- | --- |
| system `python3` | ❌ `ModuleNotFoundError` |
| `venv/bin/python` | ✅ Flask 3.1.3 |

**How to spot it instantly:** look at the start of your terminal prompt.

```
jeylofton@Jeys-Mac-Studio 111-Backend %          ← NOT activated
(venv) jeylofton@Jeys-Mac-Studio 111-Backend %   ← activated
```

No `(venv)` means you're using the wrong Python.

**The fix:**

```bash
source venv/bin/activate
python server.py
```

**Important:** activation only lasts for that one terminal tab. New tab, or you
restarted VS Code? Activate again. This is the single most common thing to forget.

**Make VS Code do it for you:** press `Cmd+Shift+P`, type
**Python: Select Interpreter**, and choose the one inside `./venv/bin/python`.
Now VS Code activates the venv automatically in every terminal it opens.

---

### Problem 5 — `404 NOT FOUND` in Thunder Client

**What I saw:** Status `404 NOT FOUND`, and the terminal logged:

```
127.0.0.1 - - "GET /api/health HTTP/1.1" 404 -
```

**What it means:** 404 means "I'm here and I'm listening, but nothing lives at that
address." The server was working perfectly — I was just knocking on the wrong door.

My code said:

```python
@app.get("/app/health")   # app
```

My request said:

```
http://127.0.0.1:5000/api/health   # api
```

`app` vs `api`. One letter.

**The fix:** every other endpoint in this project uses `/api/...`, so the *route* was
the typo, not the request. Changed the code to match:

```python
@app.get("/api/health")
```

**Lesson:** a 404 is not a crash. It means the server is fine and the URL doesn't
match. Compare the two side by side, character by character.

---

### Problem 6 — Server restarts over and over by itself

**What I saw:**

```
* Detected change in '.../111-Backend/._server.py', reloading
```

**What it means:** this SSD is formatted as exFAT, which can't store the extra file
info macOS wants to keep. So macOS quietly creates a hidden twin file — `._server.py`
next to `server.py` — to hold that info.

Flask's debug mode watches your folder and restarts whenever a file changes. It sees
those hidden twins change and restarts for no real reason.

**The fix:** delete them.

```bash
find . -name '._*' -not -path './venv/*' -delete
```

They'll come back — they're harmless, just noisy. Formatting the drive as APFS would
stop it for good.

---

### Problem 7 — `Address already in use` (may hit you later)

Flask uses port 5000 by default. So does macOS, for AirPlay Receiver.

**Two fixes, pick either:**

- Turn off **System Settings → General → AirDrop & Handoff → AirPlay Receiver**
- Or use a different port:

  ```python
  app.run(debug=True, port=5001)
  ```

---

## Quick reference

```bash
# Set up (once)
python3 -m venv venv
source venv/bin/activate
pip install Flask

# Every time you work
source venv/bin/activate
python server.py

# Check what's installed
pip list

# Stop the server
Ctrl+C
```

---

## One note about the code

`server.py` ends like this:

```python
if __name__ == "__main__":
    app.run(debug=True)
```

That `if` line matters. Without it, the server would start up any time another file
*imports* this one — including tests. Importing would hang forever, because starting
a web server never finishes.

The line means: "only start the server if someone ran this file directly." Import it,
and it stays quiet.
