# 🏏 IPL Crunch '26 — Cricket Analytics Dashboard

> **A production-grade IPL analytics platform built for national-level hackathon competition.**  
> Powered by ball-by-ball historical data, interactive Plotly charts, and a premium Streamlit UI.

---

## 🚀 Live Features

| Tab | What It Answers |
|-----|-----------------|
| 🪙 **Q1 — Toss Advantage** | Does winning the toss actually help you win the match? Season-by-season trend included. |
| 📈 **Q2 — Decisive Phase** | Which chapter (Powerplay / Middle / Death) is most linked to winning? Over-by-over run-rate chart included. |
| 🏆 **Q3 — Player Leaderboards** | Top batters & bowlers ranked by Runs, Strike Rate, Average, Wickets, Economy & more. Bubble scatter charts. |
| 💡 **Q4 — Surprise Insights** | The genuinely counter-intuitive finding + season-wise scoring evolution trend. |

---

## 📊 Dataset

- **Ball-by-ball IPL data** — 280,000+ deliveries across 1,200+ matches (2008–2026)
- Place the CSV at one of the repository-relative paths below, or upload it when you run the app:
  - `./att_0_1778303821_c3a907.csv`
  - `./data/att_0_1778303821_c3a907.csv`
  - `%USERPROFILE%\Downloads\att_0_1778303821_c3a907.csv`
  - `c:\Users\VICTUS\Downloads\att_0_1778303821_c3a907.csv`
  *(not committed to repo due to file size)*

---

## 🛠️ Setup & Run

```bash
# 1. Install dependencies
pip install streamlit pandas numpy plotly openpyxl

# 2. Run the dashboard
streamlit run app.py
```

---

## 🧠 Key Insights Discovered

- **Toss win rate ≈ 50%** — the toss is essentially a coin flip for match outcomes
- **Fielding first wins slightly more** — likely due to evening dew aiding chase
- **Middle Overs dominate** — winning overs 7–14 correlates with ~65%+ match wins
- **Death Overs are overrated** — only ~50% correlation despite the drama
- **IPL scoring has risen** — average team totals have increased significantly since 2008

---

## 📁 Project Structure

```
cricke1234567/
├── app.py               # Main Streamlit dashboard
├── phase_analysis.py    # Phase correlation analysis module
├── generate_assets.py   # Asset generation helpers
├── ipl_trophy.png       # Hero banner image
├── ipl_logo.png         # Sidebar logo image
├── ipl_stadium.png      # Stadium strip image
└── README.md
```

---

## 👨‍💻 Developer

**Pushpraj Patel**  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://www.linkedin.com/in/pushpraj-patel-16a2843b4/)
[![GitHub](https://img.shields.io/badge/GitHub-Repo-black?logo=github)](https://github.com/patelpushpraj35-cell/cricket_ipl26)

---

*Built with ❤️ using Python · Streamlit · Plotly · Pandas*
