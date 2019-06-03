from google.cloud import dataproc_v1

client = dataproc_v1.ClusterControllerClient()

project_id = 'direct-volt-240011'
# region = 'us-east1-b'
region = 'global'


# Iterate over all results
for element in client.list_clusters(project_id, region):
    # process element
    pass

# Or iterate over results one page at a time
for page in client.list_clusters(project_id, region).pages:
    for element in page:
        # process element
        pass
