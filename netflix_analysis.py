import warnings; warnings.filterwarnings("ignore")
import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt, seaborn as sns, json
sns.set_theme(style="whitegrid", font_scale=1.0)
RED="#E50914"; DARK="#221f1f"
df = pd.read_csv("netflix_titles.csv")
S = {}
S["rows"], S["cols"] = df.shape
S["missing"] = df.isna().sum().to_dict()
S["dups"] = int(df.duplicated().sum())

# cleaning
df["rating"] = df["rating"].fillna("Unknown")
df["country"] = df["country"].fillna("Unknown")
df["date_added"] = pd.to_datetime(df["date_added"].str.strip(), errors="coerce")
df["year_added"] = df["date_added"].dt.year
df["decade"] = (df["release_year"]//10*10)
df["genres"] = df["listed_in"].str.split(", ")
S["type_counts"] = df["type"].value_counts().to_dict()

# 1 type
fig, ax = plt.subplots(figsize=(6,4))
sns.countplot(data=df, x="type", palette=[RED, DARK], ax=ax)
for p in ax.patches:
    ax.annotate(int(p.get_height()), (p.get_x()+p.get_width()/2, p.get_height()), ha="center", va="bottom", fontsize=10)
ax.set_title("Movies vs TV Shows on Netflix"); ax.set_xlabel(""); ax.set_ylabel("Number of titles")
plt.tight_layout(); plt.savefig("f1_type.png", dpi=170); plt.close()

# genres
g = df.explode("genres").reset_index(drop=True)
gc = g["genres"].value_counts()
S["n_genres"] = int(gc.shape[0])
S["top_genres"] = gc.head(10).to_dict()
fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(x=gc.head(10).values, y=gc.head(10).index, palette="Reds_r", ax=ax)
for i,v in enumerate(gc.head(10).values): ax.text(v+15, i, str(v), va="center", fontsize=9)
ax.set_title("Top 10 Genres (Listed In)"); ax.set_xlabel("Number of titles"); ax.set_ylabel("")
plt.tight_layout(); plt.savefig("f2_genres.png", dpi=170); plt.close()

# genres per type
gm = g[g.type=="Movie"]["genres"].value_counts().head(8)
gt = g[g.type=="TV Show"]["genres"].value_counts().head(8)
S["top_movie_genres"] = gm.to_dict(); S["top_tv_genres"] = gt.to_dict()
fig, axs = plt.subplots(1,2, figsize=(11,4.5))
sns.barplot(x=gm.values, y=gm.index, palette="Reds_r", ax=axs[0]); axs[0].set_title("Top Movie Genres")
sns.barplot(x=gt.values, y=gt.index, palette="Greys_r", ax=axs[1]); axs[1].set_title("Top TV Show Genres")
for a in axs: a.set_xlabel("Number of titles"); a.set_ylabel("")
plt.tight_layout(); plt.savefig("f3_genres_type.png", dpi=170); plt.close()

# ratings
rc = df["rating"].value_counts()
S["rating_counts"] = rc.to_dict()
order = rc.index.tolist()
fig, ax = plt.subplots(figsize=(9,4.5))
sns.barplot(x=rc.index, y=rc.values, order=order, palette="Reds_r", ax=ax)
ax.set_title("Distribution of Content Ratings"); ax.set_xlabel("Rating"); ax.set_ylabel("Number of titles")
plt.xticks(rotation=45, ha="right"); plt.tight_layout(); plt.savefig("f4_ratings.png", dpi=170); plt.close()

# rating by type
ct = pd.crosstab(df["rating"], df["type"])
top_r = rc.head(8).index
fig, ax = plt.subplots(figsize=(8,4.5))
ct.loc[top_r].plot(kind="bar", color=[RED, DARK], ax=ax)
ax.set_title("Top 8 Ratings by Content Type"); ax.set_xlabel("Rating"); ax.set_ylabel("Number of titles")
plt.xticks(rotation=0); plt.tight_layout(); plt.savefig("f5_rating_type.png", dpi=170); plt.close()

# maturity group
mp = {"TV-MA":"Adults","R":"Adults","NC-17":"Adults","TV-14":"Teens","PG-13":"Teens","TV-PG":"Older Kids","PG":"Older Kids","TV-Y7":"Kids","TV-Y7-FV":"Kids","TV-Y":"Kids","TV-G":"Kids","G":"Kids"}
df["audience"] = df["rating"].map(mp).fillna("Other/Unrated")
S["audience"] = df["audience"].value_counts().to_dict()

# release years
ry = df["release_year"]
S["ry_min"], S["ry_max"] = int(ry.min()), int(ry.max())
S["ry_mean"] = round(float(np.mean(ry)),1); S["ry_median"] = float(np.median(ry))
yc = ry.value_counts().sort_index()
S["peak_year"] = int(yc.idxmax()); S["peak_count"] = int(yc.max())
S["share_since_2015"] = round(float((ry>=2015).mean()*100),1)
S["decade_counts"] = df["decade"].value_counts().sort_index().to_dict()
yt = df[df.release_year>=1995].groupby(["release_year","type"]).size().unstack(fill_value=0)
fig, ax = plt.subplots(figsize=(9,4.5))
ax.plot(yt.index, yt["Movie"], color=RED, lw=2.2, marker="o", ms=3, label="Movie")
ax.plot(yt.index, yt["TV Show"], color=DARK, lw=2.2, marker="o", ms=3, label="TV Show")
ax.set_title("Titles by Release Year (1995 onwards)"); ax.set_xlabel("Release year"); ax.set_ylabel("Number of titles"); ax.legend()
plt.tight_layout(); plt.savefig("f6_release.png", dpi=170); plt.close()

# decade bar
dc = df["decade"].value_counts().sort_index()
dc = dc[dc.index>=1940]
fig, ax = plt.subplots(figsize=(8,4))
sns.barplot(x=dc.index.astype(int).astype(str)+"s", y=dc.values, color=RED, ax=ax)
ax.set_title("Titles by Release Decade"); ax.set_xlabel("Decade"); ax.set_ylabel("Number of titles")
plt.tight_layout(); plt.savefig("f7_decade.png", dpi=170); plt.close()

# heatmap genre x decade
top8 = gc.head(8).index
g2 = g[g["genres"].isin(top8) & (g.release_year>=1990)].copy()
g2["decade"] = g2["decade"].astype(int).astype(str)+"s"
hm = pd.crosstab(g2["genres"], g2["decade"]).loc[top8]
fig, ax = plt.subplots(figsize=(8,4.8))
sns.heatmap(hm, annot=True, fmt="d", cmap="Reds", linewidths=.5, ax=ax)
ax.set_title("Top 8 Genres by Release Decade (1990s onwards)"); ax.set_xlabel("Decade"); ax.set_ylabel("")
plt.tight_layout(); plt.savefig("f8_heatmap.png", dpi=170); plt.close()

# movie duration (NumPy)
mv = df[df.type=="Movie"].copy()
mv["mins"] = mv["duration"].str.extract(r"(\d+)").astype(float)
d = mv["mins"].dropna().values
S["dur_mean"]=round(float(np.mean(d)),1); S["dur_median"]=float(np.median(d)); S["dur_std"]=round(float(np.std(d)),1)
S["dur_min"]=int(d.min()); S["dur_max"]=int(d.max()); S["dur_p25"],S["dur_p75"]=[float(x) for x in np.percentile(d,[25,75])]
fig, ax = plt.subplots(figsize=(8,4))
sns.histplot(d, bins=30, color=RED, ax=ax); ax.axvline(np.mean(d), color=DARK, ls="--", label=f"Mean = {np.mean(d):.0f} min")
ax.set_title("Distribution of Movie Duration"); ax.set_xlabel("Duration (minutes)"); ax.legend()
plt.tight_layout(); plt.savefig("f9_duration.png", dpi=170); plt.close()
ts = df[df.type=="TV Show"]["duration"].str.extract(r"(\d+)")[0].astype(int)
S["tv_seasons"] = ts.value_counts().sort_index().head(6).to_dict()
S["tv_one_season_pct"] = round(float((ts==1).mean()*100),1)

# added per year
ya = df["year_added"].dropna().astype(int).value_counts().sort_index()
ya = ya[ya.index>=2008]
S["added_per_year"] = ya.to_dict()
fig, ax = plt.subplots(figsize=(8,4))
sns.barplot(x=ya.index, y=ya.values, color=RED, ax=ax)
ax.set_title("Titles Added to Netflix per Year"); ax.set_xlabel("Year added"); ax.set_ylabel("Number of titles")
plt.xticks(rotation=45); plt.tight_layout(); plt.savefig("f10_added.png", dpi=170); plt.close()

# countries
cc = df[df.country!="Unknown"]["country"].str.split(", ").explode().value_counts().head(5)
S["top_countries"] = cc.to_dict()
print(json.dumps(S, indent=1, default=str))
json.dump(S, open("stats.json","w"), default=str)
