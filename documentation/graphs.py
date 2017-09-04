import numpy as np
import scipy.stats as sps
import matplotlib.pyplot as plt

fig, ax = plt.subplots(3,1, figsize=(10,6))
# plt.tight_layout()
fig.subplots_adjust(hspace=0.4)
# plt.xticks(fontsize=16)
# plt.yticks(fontsize=16)
for i in range(3):
    ax[i].set_ylim(0.5, 1.1)
    ax[i].set_xlim(-4,4)
    ax[i].tick_params(labelsize=16)

for i in range(2):
    ax[i].tick_params(axis='x', which='both', bottom='off', labelbottom='off')

x_ticks = np.linspace(sps.norm.ppf(0.01), sps.norm.ppf(0.99), 100)
y_std = sps.norm.pdf(x_ticks, scale=0.85)
y_max = max(y_std)
y_norm = [y/y_max for y in y_std]

points = [(x, y) for x, y in zip(x_ticks, y_norm) if y > 0.5]

x_vals = [p[0] for p in points]
y_vals = [p[1] for p in points]

ax[0].set_title('Base Model (1-CNN with N-Labels)', fontsize=20)
colors = ['g-', 'c-']
for n in range(-2, 3, 2):
    x_vals_n = [x + n for x in x_vals]
    ax[0].plot(x_vals_n, y_vals, 'g-', )

ax[2].set_title('Complementary (2-CNN with N-Labels)', fontsize=20)
colors = ['g-', 'c-']
for n in range(-2, 3):
    x_vals_n = [x + n for x in x_vals]
    ax[2].plot(x_vals_n, y_vals, colors[n%2])

x_ticks = np.linspace(sps.norm.ppf(0.01), sps.norm.ppf(0.99), 100)
y_std = sps.norm.pdf(x_ticks, scale=0.425)
y_max = max(y_std)
y_norm = [y/y_max for y in y_std]

points = [(x, y) for x, y in zip(x_ticks, y_norm) if y > 0.5]

x_vals = [p[0] for p in points]
y_vals = [p[1] for p in points]

ax[1].set_title('Doubled Base Model (1-CNN with 2N-Labels)', fontsize=20)
colors = ['g-', 'c-']
for n in range(-3, 4):
    x_vals_n = [x + n for x in x_vals]
    ax[1].plot(x_vals_n, y_vals, 'g-')


# plt.show()
plt.savefig('Complemntary.png', edgecolor='b')
