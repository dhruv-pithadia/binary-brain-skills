import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np, os
OUT = os.path.join(os.path.dirname(__file__), "fig"); os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.family": "Inter", "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#6B7A90", "axes.labelcolor": "#1F2A3C", "xtick.color": "#33415C", "ytick.color": "#33415C",
                     "svg.fonttype": "none", "axes.titleweight": "bold", "axes.titlesize": 12.5})
NAVY, BLUE, TEAL, ORANGE, RED, PURPLE, GREY = "#1F3A5F", "#2E6FD8", "#0F9D8A", "#E07B26", "#C8483B", "#7A5AC8", "#9AA7B8"

def save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".svg"), bbox_inches="tight", transparent=False, facecolor="white")
    plt.close(fig)

# 1. Investment waves (KPMG, King Fig 1.1)
yrs = list(range(2008, 2023))
val = [18.9, 3.7, 9.6, 15.6, 8.6, 18.9, 51.2, 64.9, 73.7, 54.4, 148.6, 216.8, 124.9, 238.9, 164.1]
fig, ax = plt.subplots(figsize=(8.2, 3.4))
cols = [GREY]*len(yrs)
for i, y in enumerate(yrs):
    if y == 2016: cols[i] = BLUE
    if y == 2019: cols[i] = TEAL
    if y == 2021: cols[i] = ORANGE
ax.bar([str(y) for y in yrs], val, color=cols, width=0.7)
for i, v in enumerate(val):
    if yrs[i] in (2016, 2019, 2021, 2022):
        ax.text(i, v + 5, f"${v:.0f}B", ha="center", fontsize=10, fontweight="bold", color="#1F2A3C")
ax.set_ylabel("Global FinTech investment (US$ bn)")
ax.tick_params(axis="x", rotation=45)
ax.annotate("Wave 1 peak\n2,173 deals", xy=(8, 74), xytext=(4.2, 150), fontsize=9.5, color=BLUE, arrowprops=dict(arrowstyle="->", color=BLUE))
ax.annotate("Wave 2 >$200B\n4,379 deals", xy=(11, 216), xytext=(7.6, 205), fontsize=9.5, color=TEAL, arrowprops=dict(arrowstyle="->", color=TEAL))
ax.annotate("Wave 3 record\n7,321 deals", xy=(13, 239), xytext=(10.2, 250), fontsize=9.5, color=ORANGE, arrowprops=dict(arrowstyle="->", color=ORANGE))
ax.set_ylim(0, 285)
ax.set_title("FinTech investment waves, 2008–2022 (KPMG)", loc="left")
save(fig, "invest_waves")

# 2. Christensen disruption
fig, ax = plt.subplots(figsize=(7.4, 4))
t = np.linspace(0, 10, 100)
ax.plot(t, 3 + 0.55*t, color=NAVY, lw=2.6, label="Incumbent performance (sustaining innovation)")
ax.plot(t, 0.6 + 0.62*t, color=ORANGE, lw=2.6, label="Entrant / disruptor performance")
ax.fill_between(t, 2.2 + 0.18*t, 4.2 + 0.25*t, color=TEAL, alpha=0.15)
ax.plot(t, 3.2 + 0.215*t, color=TEAL, lw=1.6, ls="--", label="What mainstream customers need")
ax.scatter([1], [1.22], color=ORANGE, zorder=5, s=50)
ax.annotate("① Foothold: low-end /\nnon-consumers, cheaper & simpler", xy=(1, 1.22), xytext=(1.7, 0.1), fontsize=9.5, arrowprops=dict(arrowstyle="->"))
ax.annotate("② Upmarket march:\ngood enough for the mainstream", xy=(6.4, 4.57), xytext=(6.6, 2.0), fontsize=9.5, arrowprops=dict(arrowstyle="->"))
ax.annotate("Incumbent over-serves\n(features nobody pays for)", xy=(8.5, 7.68), xytext=(4.6, 9.3), fontsize=9.5, arrowprops=dict(arrowstyle="->"))
ax.set_xlabel("Time →"); ax.set_ylabel("Performance →"); ax.set_xticks([]); ax.set_yticks([])
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=1, fontsize=9, frameon=False)
ax.set_ylim(0, 10)
ax.set_title("Christensen's disruptive innovation", loc="left")
save(fig, "christensen")

# 3. Five dimensions pentagon
fig, ax = plt.subplots(figsize=(5.4, 5.0)); ax.axis("off"); ax.set_aspect("equal")
labs = ["Information\nasymmetry", "Transaction\ncosts", "Risk\nsharing", "TRUST", "Liquidity\ncreation"]
colsP = [BLUE, TEAL, PURPLE, NAVY, ORANGE]
ang = np.deg2rad(90 + np.arange(5)*72)[[0, 4, 3, 2, 1]]
ang = np.deg2rad(np.array([126, 54, -18, -90, 198]))
xs, ys = np.cos(ang), np.sin(ang)
ax.fill(np.append(xs, xs[0]), np.append(ys, ys[0]), color="#EEF2F8", ec=NAVY, lw=2)
ax.text(0, 0.05, "Financial\nintermediation", ha="center", va="center", fontsize=12, fontweight="bold", color=NAVY)
for x, y, l, c in zip(xs, ys, labs, colsP):
    ax.add_patch(plt.Circle((x, y), 0.33, color=c, zorder=3))
    ax.text(x, y, l, ha="center", va="center", color="white", fontsize=9.6, fontweight="bold", zorder=4)
ax.set_xlim(-1.45, 1.45); ax.set_ylim(-1.45, 1.4)
save(fig, "five_dims")

# 4. Accuracy vs explainability
fig, ax = plt.subplots(figsize=(6.4, 3.9))
models = [("Logistic regression", 9, 3, BLUE), ("Decision tree", 7.6, 4.4, TEAL), ("Gradient-boosted trees\n(XGBoost) + SHAP", 5.3, 7.2, ORANGE), ("Deep neural network\n(“black box”)", 1.5, 9, RED)]
for n, x, y, c in models:
    ax.scatter(x, y, s=260, color=c, zorder=3)
    ax.annotate(n, (x, y), xytext=(10, -4), textcoords="offset points", fontsize=9.5)
ax.annotate("Recommended\nsweet spot", xy=(5.3, 7.2), xytext=(2.4, 5.4), fontsize=9.5, color=ORANGE, fontweight="bold", arrowprops=dict(arrowstyle="->", color=ORANGE))
ax.set_xlabel("Explainability →"); ax.set_ylabel("Predictive accuracy →")
ax.set_xlim(0, 12); ax.set_ylim(1.5, 10.5); ax.set_xticks([]); ax.set_yticks([])
ax.set_title("The accuracy vs explainability trade-off", loc="left")
save(fig, "xai_tradeoff")

# 5. Halving
eras = ["2009–12", "2012–16", "2016–20", "2020–24", "2024–28"]
rew = [50, 25, 12.5, 6.25, 3.125]
issued = [10.5, 5.25, 2.625, 1.3125, 0.656]
cum = np.cumsum(issued)
fig, ax = plt.subplots(figsize=(7.2, 3.4))
b = ax.bar(eras, rew, color=[NAVY, BLUE, TEAL, ORANGE, GREY])
for i, r in enumerate(rew):
    ax.text(i, r + 1.2, f"{r:g} BTC/block", ha="center", fontsize=9.6, fontweight="bold")
ax.set_ylabel("Block reward (BTC)"); ax.set_ylim(0, 62)
ax2 = ax.twinx(); ax2.plot(eras, cum, color=RED, marker="o", lw=2); ax2.set_ylim(0, 22.5)
ax2.axhline(21, color=RED, ls=":", lw=1.3); ax2.text(4.35, 21.3, "21M cap", color=RED, fontsize=9.5, ha="right")
ax2.set_ylabel("Cumulative supply (M BTC)", color=RED); ax2.spines["right"].set_visible(True); ax2.tick_params(axis="y", colors=RED)
ax.set_title("Halving every 210,000 blocks (~4 yrs)", loc="left")
save(fig, "halving")

# 6. $100 card fee waterfall (King Table 9.1)
steps = [("Customer pays", 100, NAVY), ("Interchange\n→ Issuer", -1.75, ORANGE), ("Surcharge\n→ Acquirer", -0.25, TEAL),
         ("Assessment\n→ Network", -0.11, PURPLE), ("Processing\n→ Gateway", -0.50, RED), ("Merchant gets", 97.39, BLUE)]
fig, ax = plt.subplots(figsize=(8, 3.6))
level = 100
for i, (n, v, c) in enumerate(steps):
    if i == 0 or i == len(steps) - 1:
        ax.bar(i, v - 96, bottom=96, color=c, width=0.6)
        ax.text(i, v + 0.06, f"\\${v:.2f}", ha="center", fontweight="bold", fontsize=10.5)
    else:
        ax.bar(i, v, bottom=level, color=c, width=0.6)
        ax.text(i, level + 0.06, f"−\\${-v:.2f}\n({-v:.2f}%)", ha="center", fontsize=9.5, fontweight="bold", color=c)
        level += v
ax.set_xticks(range(len(steps))); ax.set_xticklabels([s[0] for s in steps], fontsize=9.5)
ax.set_ylim(96, 100.75); ax.set_ylabel("US\\$ (axis starts at \\$96)")
ax.set_title("Where \\$100 goes: total drag \\$2.61 (2.61%)  ·  MDR = 1.75% + 0.25% = 2.00%", loc="left")
save(fig, "card_waterfall")

# 7. Alternative finance split
fig, ax = plt.subplots(figsize=(7.6, 1.9))
parts = [("Debt / P2P lending  ~90%", 90, TEAL), ("Equity ~3%", 3, BLUE), ("Donation + Reward ~7%", 7, ORANGE)]
left = 0
for n, v, c in parts:
    ax.barh(0, v, left=left, color=c, height=0.55)
    left += v
ax.text(45, 0, "Debt crowdfunding / P2P lending ≈ 90%", ha="center", va="center", color="white", fontweight="bold")
ax.annotate("Equity ≈ 3%", xy=(91.5, 0.27), xytext=(80, 0.62), fontsize=9.5, color=BLUE, fontweight="bold", arrowprops=dict(arrowstyle="->", color=BLUE))
ax.annotate("Donation + Reward ≈ 7%", xy=(96.5, -0.27), xytext=(73, -0.75), fontsize=9.5, color=ORANGE, fontweight="bold", arrowprops=dict(arrowstyle="->", color=ORANGE))
ax.plot([0, 93], [0.42, 0.42], color=NAVY, lw=1.5); ax.text(46.5, 0.5, "INVESTMENT crowdfunding 93%", ha="center", fontsize=9.5, color=NAVY, fontweight="bold")
ax.set_xlim(0, 100); ax.set_ylim(-0.95, 0.85); ax.axis("off")
save(fig, "altfin_split")

# 8. Wealth fees comparison
fig, ax = plt.subplots(figsize=(6.6, 2.8))
labs = ["Full-service advisor", "Mutual fund (MER)", "Wealthsimple", "Typical robo-advisor"]
lo = [1.0, 1.5, 0.35, 0.25]; hi = [2.0, 2.5, 0.50, 0.50]
y = np.arange(len(labs))[::-1]
for yi, l, h, c in zip(y, lo, hi, [RED, RED, TEAL, TEAL]):
    ax.barh(yi, h - l, left=l, color=c, height=0.5)
    ax.text(h + 0.05, yi, f"{l:g}–{h:g}%", va="center", fontsize=10, fontweight="bold")
ax.set_yticks(y); ax.set_yticklabels(labs); ax.set_xlim(0, 3)
ax.set_xlabel("Annual fee as % of assets (AUM)")
ax.set_title("Robo-advisors cut fees by ~75%", loc="left")
save(fig, "robo_fees")

# 9. Crypto vs stocks Sharpe
fig, axs = plt.subplots(1, 3, figsize=(8, 2.7))
data = [("Avg monthly return", [20.44, 0.94], "%"), ("Monthly volatility (σ)", [70.80, 3.42], "%"), ("Sharpe ratio (μ/σ)", [0.29, 0.27], "")]
for a, (t, v, u) in zip(axs, data):
    a.bar(["Crypto", "US stocks"], v, color=[ORANGE, BLUE], width=0.6)
    for i, x in enumerate(v): a.text(i, x * 1.02, f"{x}{u}", ha="center", fontweight="bold", fontsize=10)
    a.set_title(t, fontsize=10.5); a.set_yticks([]); a.spines["left"].set_visible(False)
    a.set_ylim(0, max(v) * 1.2)
fig.suptitle("Crypto 2011–18 (Liu & Tsyvinski): huge return, huge risk → similar Sharpe", x=0.01, ha="left", fontweight="bold", fontsize=11.5)
fig.tight_layout()
save(fig, "sharpe")

print("charts ok")
