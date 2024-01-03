#!/usr/bin/python3
 
from flask import Flask, send_file, request
from azure.storage.blob import BlobServiceClient
 
app = Flask(__name__)
 
@app.route('/')
def hello():
    return "Hello, World!"
 
@app.route('/test/<path:filename>')
def serve_static_content(filename):
    print(request.path)  # Print the URL path received by the route
    # Connection string needs to move to Azure Key Vault in future build. Should not be hardcoded here.
    connection_string = "REDACTED"
    container_name = "webapptest"
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(filename)
    blob_data = blob_client.download_blob().readall()
    return send_file(blob_data, mimetype='application/octet-stream')
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
