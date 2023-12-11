from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd

years = [1949, 1949, 1949, 1949, 1949,  1948, 1948, 1948, 1948, 1948, 1947, 1947, 1947, 1947, 1947]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jan", "Feb", "Mar", "Apr", "May", "Jan", "Feb", "Mar", "Apr", "May"]
passe = [112,118,132,129,121, 129,121,129,121,129, 132,129,132,129,132]

points = {"years": years, "months": months, "passengers": passe}
points = pd.DataFrame(points, columns=["years", "months", "passengers"])
sns.barplot(
    data=points, x="years", y="passengers", hue='months',
    errorbar="se", capsize=.3
    )
plt.show()