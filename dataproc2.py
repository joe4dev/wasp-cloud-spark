# Partially based on: https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/dataproc
import os
from google.cloud import dataproc_v1
from google.cloud import storage

client = dataproc_v1.ClusterControllerClient()
job_client = dataproc_v1.JobControllerClient()

# TODO: remove default value: os.environ['PROJECT_ID']
project_id = os.environ['PROJECT_ID']
region = 'global'

# Cluster settings
zone = 'us-east1-b'
cluster_name = 'wasp-cloud'
machine_type = 'n1-standard-1'
# Storage settings
bucket_name = 'wasp-bucket'
# Spark job
pyspark_file = 'multiply.py'


def list_clusters_with_details():
    """List the details of clusters in the region."""
    for cluster in client.list_clusters(project_id, region):
        print(('{} - {}'.format(cluster.cluster_name,
                                cluster.status.State.Name(
                                    cluster.status.state))))

def cluster_data(num_workers = 2):
    zone_uri = \
    'https://www.googleapis.com/compute/v1/projects/{}/zones/{}'.format(project_id, zone)
    cluster_data = {
        'project_id': project_id,
        'cluster_name': cluster_name,
        'config': {
            'gce_cluster_config': {
                'zone_uri': zone_uri
            },
            'master_config': {
                'num_instances': 1,
                'machine_type_uri': machine_type
            },
            'worker_config': {
                'num_instances': num_workers,
                'machine_type_uri': machine_type
            },
            'software_config': {
                'image_version': '1.4-ubuntu18'
            },
            'initialization_actions': [
                'gs://dataproc-initialization-actions/python/pip-install.shy'
            ]
        }
    }
    return cluster_data

def create_cluster():
    """Create the cluster."""
    print('Creating cluster...')
    metadata = [('PIP_PACKAGES', 'scipy==1.2.1 numpy==1.16.3')]
    cluster = client.create_cluster(project_id, region, cluster_data(), metadata=metadata)
    cluster.add_done_callback(callback)
    global waiting_callback
    waiting_callback = True

def update_cluster(num_workers):
    """Update the cluster."""
    print('Updating cluster...')
    update_mask = { 'paths': ['config.worker_config.num_instances'] }
    # metadata = [('PIP_PACKAGES', 'scipy==1.2.1')]
    metadata = [('x-goog-api-client', 'gl-python/2.7.14 grpc/1.21.1 gax/1.11.1 gapic/0.4.0')]
    cluster = client.update_cluster(project_id, region, cluster_name, cluster_data(num_workers), update_mask, metadata=metadata)
    print(cluster)
    cluster.add_done_callback(callback)
    global waiting_callback
    waiting_callback = True

def delete_cluster():
    """Delete the cluster."""
    print('Tearing down cluster.')
    result = client.delete_cluster(
        project_id=project_id, region=region, cluster_name=cluster)
    return result

def callback(operation_future):
    # Reset global when callback returns.
    global waiting_callback
    waiting_callback = False

def wait_for_cluster_operation():
    """Wait for cluster operation."""
    print('Waiting for cluster operation (create or update)...')

    while True:
        if not waiting_callback:
            print("Cluster created or updated.")
            break

def create_bucket(bucket_name):
    """Creates a new bucket."""
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)
    print('Bucket {} created'.format(bucket.name))

def get_pyspark_file(pyspark_file):
    f = open(pyspark_file, "rb")
    return f, os.path.basename(pyspark_file)

def upload_pyspark_file(project_id, bucket_name, filename, spark_file):
    """Uploads the PySpark file in this directory to the configured input
    bucket."""
    print('Uploading pyspark file to Cloud Storage.')
    storage_client = storage.Client(project=project_id)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_file(spark_file)

def download_output(project_id, cluster_id, output_bucket, job_id):
    """Downloads the output file from Cloud Storage and returns it as a
    string."""
    print('Downloading output file.')
    storage_client = storage.Client(project=project_id)
    bucket = storage_client.get_bucket(output_bucket)
    output_blob = (
        ('google-cloud-dataproc-metainfo/{}/jobs/{}/driveroutput.000000000'.
            format(cluster_id, job_id)))
    return bucket.blob(output_blob).download_as_string()

def get_cluster_id_by_name(dataproc, project_id, region, cluster_name):
    """Helper function to retrieve the ID and output bucket of a cluster by
    name."""
    for cluster in dataproc.list_clusters(project_id, region):
        if cluster.cluster_name == cluster_name:
            return cluster.cluster_uuid, cluster.config.config_bucket

def submit_pyspark_job(dataproc, project_id, region, cluster_name, bucket_name,
                       filename):
    """Submit the Pyspark job to the cluster (assumes `filename` was uploaded
    to `bucket_name."""
    job_details = {
        'placement': {
            'cluster_name': cluster_name
        },
        'pyspark_job': {
            'main_python_file_uri': 'gs://{}/{}'.format(bucket_name, filename)
        }
    }
    result = dataproc.submit_job(project_id=project_id, region=region, job=job_details)
    job_id = result.reference.job_id
    print('Submitted job ID {}.'.format(job_id))
    return job_id

def wait_for_job(dataproc, project_id, region, job_id):
    """Wait for job to complete or error out."""
    print('Waiting for job to finish...')
    while True:
        job = dataproc.get_job(project_id, region, job_id)
        # Handle exceptions
        if job.status.State.Name(job.status.state) == 'ERROR':
            raise Exception(job.status.details)
        elif job.status.State.Name(job.status.state) == 'DONE':
            print('Job finished.')
            return job

# Only first time (if not exists)
# create_bucket(bucket_name)

list_clusters_with_details()
spark_file, spark_filename = get_pyspark_file(pyspark_file)
# upload_pyspark_file(project_id, bucket_name, spark_filename, spark_file)

# create_cluster()
# wait_for_cluster_operation()

update_cluster(2)
wait_for_cluster_operation()

# (cluster_id, output_bucket) = (
#                 get_cluster_id_by_name(client, project_id,
#                                        region, cluster_name))
# job_id = submit_pyspark_job(job_client, project_id, region,
#                             cluster_name, bucket_name, spark_filename)
# wait_for_job(job_client, project_id, region, job_id)
# output = download_output(project_id, cluster_id, output_bucket, job_id)
# print('Received job output {}'.format(output))

# list_clusters_with_details()
# update_cluster(3)
# wait_for_cluster_operation()

# # TODO: use try/finally to kill resources on failure
# # delete_cluster()
# spark_file.close()
