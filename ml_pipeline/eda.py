import polars as pl 

df= pl.read_csv("data/simulated/iris_simulated.csv")







print(
df.group_by("date")\
.agg([
    pl.count().alias("nrows"), 
    pl.col("species").value_counts().alias("class_distribution")
])
)






