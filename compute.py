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
from datetime import datetime
# download example matrix
import urllib

appName = "MultiplyApp"
local = "local"
local_parallel = "local[2]"
nRowsPerBlock = 1024 # Need to set this to something useful
nColumnsPerBlock = 1024 # Need to set this to something useful
#conf = SparkConf().setAppName(appName).setMaster(local_parallel)
sc = SparkContext()
spark = SparkSession(sc)

matrix_file = urllib.URLopener()
matrix_file.retrieve("https://vanrooij.se/index.php/s/wBPCCoygzXccJg8/download", "psmigr_1.mtx")
mat = mmread("psmigr_1.mtx")

startTimestamp_block = datetime.now()
indexed_rows = sc.parallelize(enumerate(mat.toarray()), numSlices=512)
indexed_row_matrix = IndexedRowMatrix(indexed_rows)
block_matrix = indexed_row_matrix.toBlockMatrix(nRowsPerBlock,nColumnsPerBlock)
endTimestamp_block = datetime.now()
duration = (endTimestamp_block - startTimestamp_block).total_seconds()
print("PARALLELIZE_DURATION:{duration}".format(duration=duration))


startTimestamp_calc = datetime.now()
#indexed_row_matrix.computeSVD(10)
block_matrix.multiply(block_matrix)
endTimestamp_calc = datetime.now()
duration = (endTimestamp_calc - startTimestamp_calc).total_seconds()
total_duration = (endTimestamp_calc - startTimestamp_block).total_seconds()

print("CALCULATION_DURATION:{duration}".format(duration=duration))


# sc.stop()
