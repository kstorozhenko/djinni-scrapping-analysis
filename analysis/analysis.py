import pandas as pd
import matplotlib.pyplot as plt
import os

from config import TECHNOLOGIES

df = pd.read_csv("vacancies.csv")

df = df[df["Requirements"].notna()]

df["Requirements"] = df["Requirements"].str.split(", ")
tech_counts = {
    tech: df["Requirements"].apply(lambda reqs: tech in reqs).sum()
    for tech in TECHNOLOGIES
}

tech_counts = {tech: count for tech, count in tech_counts.items() if count > 0}

sorted_tech_counts = dict(
    sorted(tech_counts.items(), key=lambda item: item[1], reverse=True)
)

plt.bar(sorted_tech_counts.keys(), sorted_tech_counts.values())

for i, (tech, count) in enumerate(sorted_tech_counts.items()):
    plt.text(i, count, str(count), ha="center", va="bottom")

plt.xticks(rotation="vertical", fontsize=5)

os.makedirs("plots", exist_ok=True)
plt.savefig("plots/tech_counts.png")

plt.show()
