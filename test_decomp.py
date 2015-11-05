
# pre load bigdf

# ------------------

# count # shot attempts by team, per second

temp = bigdf.groupby(['Tm', 'Time2'])['points'].count()

tm_time_shots = temp.unstack(level=1)

tm_time_shots.head(3)

pca = PCA(n_components=3)
pca.fit(tm_time_shots.reset_index(drop=True).values)


