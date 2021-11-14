from clarifai_grpc.grpc.api import service_pb2, resources_pb2, service_pb2_grpc
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api.status import status_code_pb2

import base64

stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())

def detect(filename):
    # This is how you authenticate.
    secret_key = 'ca98524a0b8047feb6ef2453e1c5f010'
    metadata = (('authorization', f'Key {secret_key}'),)


    # Insert here the initialization code as outlined on this page:
    # https://docs.clarifai.com/api-guide/api-overview/api-clients#client-installation-instructions

    with open(filename, "rb") as f:
        file_bytes = f.read()

        post_model_outputs_response = stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                model_id='aaa03c23b3724a16a56b629203edc62c',
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            image=resources_pb2.Image(
                                base64=file_bytes
                            )
                        )
                    )
                ]
            ),
            metadata=metadata
        )

        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            print("There was an error with your request!")
            print("\tCode: {}".format(post_model_outputs_response.outputs[0].status.code))
            print("\tDescription: {}".format(post_model_outputs_response.outputs[0].status.description))
            print("\tDetails: {}".format(post_model_outputs_response.outputs[0].status.details))
            raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

        # Since we have one input, one output will exist here.
        output = post_model_outputs_response.outputs[0]

        print("Predicted concepts:")
        print(output.data)
        for concept in output.data.concepts:
            print("%s %.2f" % (concept.name, concept.value))