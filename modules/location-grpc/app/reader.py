import grpc
import location_pb2
import location_pb2_grpc

"""
Sample implementation of a getter-or reader from gRPC.
"""

print("Reading a location")

channel = grpc.insecure_channel("127.0.0.1:30006", options=(('grpc.enable_http_proxy', 0),))
stub = location_pb2_grpc.LocationServiceStub(channel)

request = location_pb2.MessageRequest(id=51)
response = stub.Retrieve(request)
print("Location retrieved: ...", response)
