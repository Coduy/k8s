from hdfs import InsecureClient

client = InsecureClient('http://hdfs-release-datanode-0.hdfs-release-datanode.default.svc.cluster.local:50075', user='hdfs')

# Example: Upload a file
client.upload('/tmp/train01.csv', '/data/train01.csv')
