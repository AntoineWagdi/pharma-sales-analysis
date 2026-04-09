
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# --- CONFIG ---
sns.set_theme(style="whitegrid")
COLORS = ["#2ecc71","#3498db","#e74c3c","#f39c12","#9b59b6","#1abc9c","#e67e22","#34495e"]

DRUG_NAMES = {
    'M01AB': 'Anti-inflammatory (M01AB)',
    'M01AE': 'Anti-inflammatory (M01AE)',
    'N02BA': 'Analgesics (N02BA)',
    'N02BE': 'Analgesics (N02BE)',
    'N05B':  'Anxiolytics (N05B)',
    'N05C':  'Sedatives (N05C)',
    'R03':   'Respiratory (R03)',
    'R06':   'Antihistamines (R06)'
}

# --- LOAD DATA ---
monthly = pd.read_csv('/home/claude/pharma_data/salesmonthly.csv', parse_dates=['datum'])
daily   = pd.read_csv('/home/claude/pharma_data/salesdaily.csv',   parse_dates=['datum'])
weekly  = pd.read_csv('/home/claude/pharma_data/salesweekly.csv',  parse_dates=['datum'])

monthly['Year'] = monthly['datum'].dt.year
drugs = list(DRUG_NAMES.keys())

# ==============================================================
# FIGURE 1 — Total Sales by Drug Category
# ==============================================================
fig, ax = plt.subplots(figsize=(12, 6))
totals = monthly[drugs].sum().rename(DRUG_NAMES)
bars = ax.barh(totals.index, totals.values, color=COLORS, edgecolor='white', height=0.6)
ax.bar_label(bars, fmt='%.0f', padding=6, fontsize=10, fontweight='bold')
ax.set_xlabel('Total Units Sold', fontsize=12)
ax.set_title('Total Pharma Sales by Drug Category (2014–2019)', fontsize=15, fontweight='bold', pad=15)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
plt.tight_layout()
plt.savefig('/home/claude/fig1_total_sales.png', dpi=150)
plt.close()
print("✅ Figure 1 saved")

# ==============================================================
# FIGURE 2 — Monthly Sales Trend for Top 3 Drugs
# ==============================================================
top3 = monthly[drugs].sum().nlargest(3).index.tolist()
fig, ax = plt.subplots(figsize=(14, 6))
for i, drug in enumerate(top3):
    ax.plot(monthly['datum'], monthly[drug], label=DRUG_NAMES[drug], color=COLORS[i], linewidth=2)
ax.set_title('Monthly Sales Trend — Top 3 Drug Categories', fontsize=15, fontweight='bold', pad=15)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Units Sold', fontsize=12)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig('/home/claude/fig2_trend.png', dpi=150)
plt.close()
print("✅ Figure 2 saved")

# ==============================================================
# FIGURE 3 — Year-over-Year Growth
# ==============================================================
yearly = monthly.groupby('Year')[drugs].sum()
yearly_growth = yearly.pct_change() * 100

fig, ax = plt.subplots(figsize=(12, 6))
for i, drug in enumerate(drugs):
    ax.plot(yearly_growth.index[1:], yearly_growth[drug].iloc[1:],
            marker='o', label=DRUG_NAMES[drug], color=COLORS[i], linewidth=2)
ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
ax.set_title('Year-over-Year Sales Growth by Drug Category (%)', fontsize=15, fontweight='bold', pad=15)
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Growth (%)', fontsize=12)
ax.legend(fontsize=8, ncol=2)
plt.tight_layout()
plt.savefig('/home/claude/fig3_yoy_growth.png', dpi=150)
plt.close()
print("✅ Figure 3 saved")

# ==============================================================
# FIGURE 4 — Best Sales Day of the Week
# ==============================================================
daily_avg = daily.groupby('Weekday Name')[drugs].mean().reindex(
    ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
daily_avg['Total'] = daily_avg.sum(axis=1)

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(daily_avg.index, daily_avg['Total'], color=COLORS, edgecolor='white')
ax.bar_label(bars, fmt='%.1f', padding=4, fontsize=10, fontweight='bold')
ax.set_title('Average Daily Sales by Day of Week', fontsize=15, fontweight='bold', pad=15)
ax.set_ylabel('Avg Units Sold', fontsize=12)
plt.tight_layout()
plt.savefig('/home/claude/fig4_weekday.png', dpi=150)
plt.close()
print("✅ Figure 4 saved")

# ==============================================================
# FIGURE 5 — Sales Heatmap (Month vs Drug)
# ==============================================================
monthly['Month'] = monthly['datum'].dt.month
month_drug = monthly.groupby('Month')[drugs].mean()
month_drug.index = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
month_drug.columns = [DRUG_NAMES[d] for d in drugs]

fig, ax = plt.subplots(figsize=(14, 6))
sns.heatmap(month_drug.T, cmap='YlGn', annot=True, fmt='.0f',
            linewidths=0.5, ax=ax, cbar_kws={'label': 'Avg Units'})
ax.set_title('Average Monthly Sales Heatmap by Drug Category', fontsize=15, fontweight='bold', pad=15)
ax.set_xlabel('Month', fontsize=12)
plt.tight_layout()
plt.savefig('/home/claude/fig5_heatmap.png', dpi=150)
plt.close()
print("✅ Figure 5 saved")

print("\n🎉 All charts generated successfully!")
