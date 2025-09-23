# 🎲 Customizable Randomizer (Streamlit App)

The BEST randomized on Streamlit. A powerful, interactive, and customizable randomizer built with [Streamlit](https://streamlit.io).  
This app allows you to create weighted random selections, draft lists, lottery-style selections, and even generate Power Ball numbers — all in one place!  

👉 [Subscribe to the Guide](https://www.youtube.com/@TheBOLGuide) for tutorials!

---

## 📖 Overview

The **Customizable Randomizer** lets you:
- Add, import, and customize options (like games, names, tasks, etc.)
- Assign **weights** using percentages or whole numbers
- Choose different randomization modes:
  - **Pick a Single Winner** – pick one random item (like a raffle or “What game should we play?”).
  - **Create a Draft List** – generate a random order for playing games, assigning turns, etc.
  - **Lottery Draft** – simulate a suspenseful lottery draft (great for fantasy leagues, presentations, or turn-taking).
  - **Power Ball** – generate random Power Ball numbers with white and red balls.

---

## 🗂️ Index

1. [Installation](#-installation)  
2. [Requirements](#-requirements)  
3. [Running the App](#-running-the-app)  
4. [User Guide](#-user-guide)  
   - [Pick One](#pick-one)  
   - [Draft List](#draft-list)  
   - [Lottery Draft](#lottery-draft)  
   - [Power Ball](#power-ball)  
   - [Importing Options from File](#importing-options-from-file)  
5. [Examples](#-examples)  
6. [Contributing](#-contributing)  
7. [License](#-license)

---

## 💻 Installation

Clone this repository:

```
git clone https://github.com/yourusername/customizable-randomizer.git
cd customizable-randomizer
```

Set up a Python environment (recommended with `venv` or `conda`) and install the dependencies:

```
pip install -r requirements.txt
```
---

## 📦 Requirements

Your `requirements.txt` should look like this:

```
altair==5.5.0
attrs==25.3.0
blinker==1.9.0
cachetools==6.2.0
certifi==2025.8.3
charset-normalizer==3.4.3
click==8.3.0
colorama==0.4.6
gitdb==4.0.12
GitPython==3.1.45
idna==3.10
Jinja2==3.1.6
jsonschema==4.25.1
jsonschema-specifications==2025.9.1
MarkupSafe==3.0.2
narwhals==2.5.0
numpy==2.3.3
packaging==25.0
pandas==2.3.2
pillow==11.3.0
protobuf==6.32.1
pyarrow==21.0.0
pydeck==0.9.1
python-dateutil==2.9.0.post0
pytz==2025.2
referencing==0.36.2
requests==2.32.5
rpds-py==0.27.1
six==1.17.0
smmap==5.0.2
streamlit==1.49.1
tenacity==9.1.2
toml==0.10.2
tornado==6.5.2
typing_extensions==4.15.0
tzdata==2025.2
urllib3==2.5.0
watchdog==6.0.0
```

---

## ▶️ Running the App

From the project folder, run:

```
streamlit run app.py
```

This will open the app in your browser at [Local Host](http://localhost:8501).

---

## 📘 User Guide

### Pick One
- Use this mode when you need a single random selection. Example: *“Which game should we play tonight?”*
- Percentages or whole numbers weight options.

---

### Draft List
- Generate a randomized order of your items. Example: *A group of friends wants a turn order for board games.*
- You can choose drafting with or without replacement:
  - With replacement → options can repeat.
  - Without replacement → each option appears once.

---

### Lottery Draft
- Adds **suspense** by revealing draft picks one at a time with a delay.
- Perfect for:
  - Fantasy sports league drafts 🏈
  - Presentation order in class 👩‍🏫
  - Group activities where the reveal matters 🎉

---

### Power Ball
- Simulates a Power Ball drawing:
  - 5 random white balls (1–69)
  - 1 random red ball (1–26)
- Great for fun lottery-style games.

---

### Importing Options from File

- Upload a `.csv` or `.txt` file with one option per line.
Example `.txt` file:
<!-- START_TXT_CONTENT -->
Call of Duty
Mario Kart
Smash Bros
<!-- END_TXT_CONTENT -->

---

## 🧾 Examples

- **Pick One:** Randomly select a game from a list of 10.
- **Draft List:** Create a random order to decide presentation order in class.
- **Lottery Draft:** Run a fantasy football draft with dramatic reveals.
- **Power Ball:** Generate a fun lottery simulation for a group event.

---

##🤝 Contributing

Contributions are welcome!
- Fork the repo
- Create a new branch (`feature/new-mode`)
- Submit a pull request 🚀

---

👉 Don’t forget to check out my tutorials and live demos on YouTube:
- [The BOL Guide](https://www.youtube.com/@TheBOLGuide)
- [The BOL Broadcast](https://www.youtube.com/@TheBOLBroadcast)
