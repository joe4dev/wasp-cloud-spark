import pyspark
from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.mllib.linalg import Matrices
from pyspark.mllib.linalg.distributed import BlockMatrix
# from pyspark.mllib.linalg.distributed import *
import numpy

appName = "MultiplyApp"
local_parallel = "local[*]"
conf = SparkConf().setAppName(appName).setMaster("local")
sc = SparkContext(conf=conf)
spark = SparkSession(sc)

dm1 = Matrices.dense(3, 2, [1, 2, 3, 4, 5, 6])
dm2 = Matrices.dense(3, 2, [7, 8, 9, 10, 11, 12])
sm = Matrices.sparse(3, 2, [0, 1, 3], [0, 1, 2], [7, 11, 12])
blocks1 = sc.parallelize([((0, 0), dm1), ((1, 0), dm2)])
blocks2 = sc.parallelize([((0, 0), dm1), ((1, 0), dm2)])
blocks3 = sc.parallelize([((0, 0), sm), ((1, 0), dm2)])
mat1 = BlockMatrix(blocks1, 3, 2)
mat2 = BlockMatrix(blocks2, 3, 2)
mat3 = BlockMatrix(blocks3, 3, 2)

mat1.add(mat2).toLocalMatrix()

print("done")

# sc.stop()
