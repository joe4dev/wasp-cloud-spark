# WASP Cloud Spark Assignment

* Task: https://docs.google.com/document/d/1D6xGA-gf5tV6njvIIySMIDXnS7Ay0YAI2eoepXWoX8c/edit
* Deadline: June 6th
* Github repository: https://github.com/joe4dev/wasp-cloud-spark

## Project 1

* Evaluate the Spark library LINALG
* LINALG
  * [Reference](https://spark.apache.org/docs/1.5.1/api/java/org/apache/spark/mllib/linalg/package-frame.html)
  * [Paper](https://shivaram.org/publications/matrix-spark-kdd.pdf)
    * [TFOCS for Spark Implementation + Examples](https://github.com/databricks/spark-tfocs)
    * [Sparse Matrix support (CCS) and additional native BLAS](https://github.com/apache/spark/pull/2294)
  * [MLib (parent lib) Docs Example with linalg.Vectors](https://spark.apache.org/docs/1.0.1/mllib-linear-methods.html#linear-least-squares-lasso-and-ridge-regression)
* [Spark 2.4.2 docs](https://spark.apache.org/docs/2.4.2/)
  * [Distributed linalg Matrix API (Scala)](https://spark.apache.org/docs/2.4.2/api/scala/index.html#org.apache.spark.mllib.linalg.distributed.package)
  * [Distributed linalg Matrix API (Java)](https://spark.apache.org/docs/2.4.2/api/java/index.html)
  * [(+best docs) Distributed linalg Matrix API (Python)](https://spark.apache.org/docs/2.4.2/api/python/pyspark.mllib.html#module-pyspark.mllib.linalg.distributed)
  * Latest Spark version available on Google Dataproc [see Changelog](https://cloud.google.com/dataproc/docs/release-notes#may_9_2019)
* [Dataset](https://sparse.tamu.edu/)
  * "you will find multiple matrices in different formats from many applications, including, control and optimization, networking, and privacy data"
  * "choose two of the available methods in the library, and one of the matrices available in the datasets"
  * "evaluate the speedup when using Spark with a low number of nodes, versus a large number of nodes for each of the methods"
* Report
  * "describe your setup, and your conclusion"
  * "e.g., by showing performance speedup graphs or slowdowns"
  * "if it is linear in the amount of resources, sublinear, or something else, or if the CPU was the bottleneck, or the Memory, etc?"

## Dataset Selection

Source: Paper

* "The library targets large-scale matrices that benefit from row, column, entry, or block sparsity to store and operate on distributed and local matrices."
  * => row, column, entry, or block sparsity matrix dataset
* "MLlib has specialized implementations for performing Sparse Matrix × Dense Matrix, and Sparse Matrix × Dense Vec- tor multiplications, where matrices can be optionally transposed." Example benchmark graphs for [SparseMatrix](https://github.com/apache/spark/pull/2294)
* "linalg includes Java, Scala, and Python APIs" and itself is "Written in Scala and using na- tive (C++ and fortran based)"
  * => choose one of these languages, JVM seems common, maybe Scala is a goot fit then (or Python for such a small example)
* "Most of the time GPU is less effective due to overhead of copying matrices to/from GPU. However, when multiplying sufficiently large matrices, i.e. starting from 10000×10000 by 10000×1000, the overhead becomes negligible with re- spect to the computation complexity. At that point GPU is several times more effective than CPU. Interestingly, adding more GPUs speeds up the computation almost linearly for big matrices."
  * => focus on CPU

* What matrix size?
* What dataset?

* [Spreadsheet with Matrix multiplication benchmark (Figure 2 in paper)](https://docs.google.com/spreadsheets/d/1lWdVSuSragOobb0A_oeouQgHUMx378T9J5r7kwKSPkY/edit#gid=0)
  * maybe around 100 to 1000 (no idea?, probably need to try out starting with small sizes?)

### Dataset Filter

Hint: We can use filters (e.g., by matrix structure) to search for a suitable dataset.

* keyword: Linear Programming (?)
* sorted by: Date (Recent First) (?)
* Matrix Size and Shape: (?)
* Matrix Structure and Entry Type: Maybe special structure to symmetric (?)

## Implementation

* We are allowed to use [Cloud Dataproc](https://cloud.google.com/dataproc/) "A faster, easier, more cost-effective way to run Apache Spark and Apache Hadoop"
  * => automated cluster management etc, seems smart to use that one
  * [Docs](https://cloud.google.com/dataproc/docs/quickstarts)
* The *Distributed linalg Matrix API* has the best API documentation in Python, probably the best choice to go with Python then
  * [(+best docs) Distributed linalg Matrix API (Python)](https://spark.apache.org/docs/2.4.2/api/python/pyspark.mllib.html#module-pyspark.mllib.linalg.distributed)

* Which operations?
  * [add(other)](https://spark.apache.org/docs/2.4.2/api/python/pyspark.mllib.html#pyspark.mllib.linalg.distributed.BlockMatrix.add): "The matrices must have the same size and matching rowsPerBlock and colsPerBlock values."
  * [multiply(other)](https://spark.apache.org/docs/2.4.2/api/python/pyspark.mllib.html#pyspark.mllib.linalg.distributed.BlockMatrix.multiply): "The colsPerBlock of this matrix must equal the rowsPerBlock of other." Better no SparseMatrix blocks because they have to be converted to DenseMatrix blocks, which may lead to performance issues due to lacking support for multiplying two sparse matrices.
  * [subtract(other)](https://spark.apache.org/docs/2.4.2/api/python/pyspark.mllib.html#pyspark.mllib.linalg.distributed.BlockMatrix.subtract): "The matrices must have the same size and matching rowsPerBlock and colsPerBlock values."
  * [computeSVD(k, computeU=False, rCond=1e-09)](https://spark.apache.org/docs/2.4.2/api/python/pyspark.mllib.html#pyspark.mllib.linalg.distributed.IndexedRowMatrix.computeSVD): "Computes the singular value decomposition of the IndexedRowMatrix."
  * [multiply(matrix)](https://spark.apache.org/docs/2.4.2/api/python/pyspark.mllib.html#pyspark.mllib.linalg.distributed.IndexedRowMatrix.multiply): "Multiply this matrix by a local dense matrix on the right."
  * [columnSimilarities(threshold=0.0)](https://spark.apache.org/docs/2.4.2/api/python/pyspark.mllib.html#pyspark.mllib.linalg.distributed.RowMatrix.columnSimilarities): "Compute similarities between columns of this matrix."
  * [tallSkinnyQR(computeQ=False)](https://spark.apache.org/docs/2.4.2/api/python/pyspark.mllib.html#pyspark.mllib.linalg.distributed.RowMatrix.tallSkinnyQR): "Compute the QR decomposition of this RowMatrix. The implementation is designed to optimize the QR decomposition (factorization) for the RowMatrix of a tall and skinny shape."

### Chosen Operations

* `multiply` => Matrix multiplication seems to be a standard benchmark operation used in practice (see Figure 2 + Benchmark in PR)
  * SparseMatrix vs DenseMatrix !? ()
* ???
