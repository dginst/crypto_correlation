import numpy as np
import matplotlib.pyplot as plt
from kneed import KneeLocator
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from btc_analysis.mongo_func import query_mongo


reg_df = query_mongo("btc_analysis", "S2F_source")
reg_df = reg_df[["S2F ratio", "Market Cap"]]
reg_array = np.array(reg_df)


scaler = StandardScaler()
scaled_reg = scaler.fit_transform(reg_array)

kmeans = KMeans(n_clusters=4)
kmeans.fit(scaled_reg)
print(kmeans.labels_)
print(kmeans.cluster_centers_)
plt.plot(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1])
plt.show()

kmeans.fit(reg_array)
print(kmeans.labels_)
print(kmeans.cluster_centers_)
plt.plot(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1])
plt.show()

kmeans_kwargs = {
    "init": "random",
    "n_init": 10,
    "max_iter": 300,
    "random_state": 42,
}
# A list holds the SSE values for each k
sse = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
    kmeans.fit(scaled_reg)
    sse.append(kmeans.inertia_)


plt.style.use("fivethirtyeight")
plt.plot(range(1, 11), sse)
plt.xticks(range(1, 11))
plt.xlabel("Number of Clusters")
plt.ylabel("SSE")
plt.show()

kl = KneeLocator(
    range(1, 11), sse, curve="convex", direction="decreasing"
)
print(kl.elbow)

# A list holds the silhouette coefficients for each k
silhouette_coefficients = []
# Notice you start at 2 clusters for silhouette coefficient
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
    kmeans.fit(scaled_reg)
    score = silhouette_score(scaled_reg, kmeans.labels_)
    silhouette_coefficients.append(score)

plt.style.use("fivethirtyeight")
plt.plot(range(2, 11), silhouette_coefficients)
plt.xticks(range(2, 11))
plt.xlabel("Number of Clusters")
plt.ylabel("Silhouette Coefficient")
plt.show()
