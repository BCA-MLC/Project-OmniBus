import numpy as np
m = np.load("competition_data/graph_cache/time_matrix.npy")
print("shape", m.shape, "max", m.max(), "1e6", (m >= 1e5).sum())
