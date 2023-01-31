import matplotlib.pyplot as plt

print("matplotlib backend : ", plt.get_backend())
# Simple plt example
x = [1, 2, 3, 4]
y = [1, 4, 9, 16]
plt.plot(x, y)
a, b = plt.subplots()
print(a, b)
plt.show()
