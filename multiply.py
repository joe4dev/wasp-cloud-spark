import pyspark
from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.mllib.linalg import Matrices
from pyspark.mllib.linalg.distributed import BlockMatrix
from pyspark.mllib.linalg.distributed import IndexedRowMatrix
# from pyspark.mllib.linalg.distributed import *
import numpy
from scipy.io import mmread
from scipy.sparse import coo_matrix
# download example matrix
import urllib

appName = "MultiplyApp"
local = "local"
local_parallel = "local[*]"
nRowsPerBlock = 5 # Need to set this to something useful
nColumnsPerBlock = 5 # Need to set this to something useful
conf = SparkConf().setAppName(appName).setMaster(local)
sc = SparkContext(conf=conf)
spark = SparkSession(sc)

matrix_file = urllib.URLopener()
matrix_file.retrieve("https://vanrooij.se/index.php/s/absHJm46dG6MDg5/download", "rel3.mtx")
mat = mmread("rel3.mtx")

indexed_rows = sc.parallelize(enumerate(mat.toarray()))
indexed_row_matrix = IndexedRowMatrix(indexed_rows)
block_matrix = indexed_row_matrix.toBlockMatrix(nRowsPerBlock,nColumnsPerBlock)

print(block_matrix.add(block_matrix).toLocalMatrix())


print("done")

# sc.stop()
