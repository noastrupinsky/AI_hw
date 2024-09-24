import matplotlib.pyplot as plt
import numpy as np

# Generate some test data
data = np.random.rand(10, 10)

# Display the data as an image
plt.imshow(data, cmap='binary', interpolation='nearest')
plt.show()
