# Welcome to the Qiskit Hackathon at World of QUANTUM

## 🏠 Running Locally

To run these Qiskit exercises on your local machine:

### Quick Start
```bash
# 1. Install dependencies and setup environment
python3 setup_local.py

# 2. Start Jupyter notebooks
./start_local.sh
```

### Manual Setup
If you prefer manual setup:

```bash
# Option 1: Using virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
jupyter nbextension enable --py widgetsnbextension

# Option 2: System-wide install (if allowed)
pip install -r requirements.txt --user
jupyter nbextension enable --py widgetsnbextension

# Start Jupyter in the Exercises directory
cd Exercises
jupyter notebook
```

### Requirements
- Python 3.8 or higher
- pip (Python package installer)

### What's Included
- **Easy Exercises**: `Easy_Single_Qubit_Gates.ipynb`, `Easy_Multiple_Qubit_Gates.ipynb`
- **Medium Exercises**: `Medium_Single_Qubit_Gates.ipynb`, `Medium_Multiple_Qubit_Gates.ipynb`
- **Validation Functions**: Automatic checking of your solutions
- **Visualization**: Bloch sphere and circuit diagrams

### IBM Quantum Access
For real quantum hardware access:
1. Create account at [IBM Quantum](https://quantum-computing.ibm.com/)
2. Get your API token
3. Use `IBMQ.save_account('your_token_here')` in a notebook

---

## 📄  [Click here to download the In-Person Attendee Guide](https://github.com/qiskit-community/Qiskit-Hackathon-at-World-of-QUANTUM/raw/main/Attendee%20Guide%20In-Person.pdf)

### About

The Qiskit Hackathon@World of QUANTUM is the first Qiskit event happening in person in Germany hosted by the Federal Ministry of Education and Research (BMBF), IBM Quantum's Community Team and Messe München GmbH.

The hackathon will kickoff with an opening presentation and guideline review.

Participants will then form teams of 4-5 people and work on a challenge for the next 24 hours.

Mentors will be available to support and help the teams during the hackathon.

After the 24 hours, a committee of experts will evaluate the outcome and select the winners.


### Timeline

#### Tuesday 26 April
11:55 – 12:15 - Welcome note at the Forum World of QUANTUM

12:15 - 14:30 - Guidelines, lunch, and team formation in the Hackathon Space

14:30 - Start of the Hacking Phase in the Hackathon Space

*Between 20:00 (26 April) and 08:00 (27 April) you may ask questions in the dedicated Qiskit Event
Slack Channel [#hackathon-woq-support](https://qiskit.slack.com/archives/C03BJNQ0S15) for remote assistance. [[Click here to join
Qiskit Slack](https://ibm.co/joinqiskitslack), if needed.]

#### Tuesday 26 April
14:00 - End of the Hacking Phase and start of the Judging Phase

14:30 - 16:00 - Optional Project Presentation & Community Choice Award

16:00 - 16:30 - Closing Ceremony at the Forum World of QUANTUM

### Projects

Please find full details on the Hackathon Project format, team formation, and project submission in the [In-Person Attendee Guide](https://github.com/qiskit-community/Qiskit-Hackathon-at-World-of-QUANTUM/blob/main/Attendee%20Guide%20In-Person.pdf). 

Here is an [example of an Education Hackathon Project Submission](https://github.com/TigrisCallidus/Education-Hackathon-Template) for your review.

### Questions

If you have any questions, please ask the team of Qiskit Mentors at the event or post them in the dedicated Qiskit Event
Slack Channel [#hackathon-woq-support](https://qiskit.slack.com/archives/C03BJNQ0S15).




