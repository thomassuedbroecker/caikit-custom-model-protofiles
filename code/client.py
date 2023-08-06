# Copyright The Caikit Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Standard
import json

# Third Party
import grpc
import requests

# Local
from caikit.config.config import get_config
from caikit.runtime.service_factory import ServicePackageFactory
from text_generation.data_model import TextInput
import caikit


caikit.config.configure(
        config_dict={
            "merge_strategy": "merge",
            "runtime": {
                "library": "text_generation",
                "grpc": {"enabled": True},
                "http": {"enabled": False},
            },
        }
)

inference_service = ServicePackageFactory().get_service_package(
        ServicePackageFactory.ServiceType.INFERENCE,
)

model_id = "text_generation"

if get_config().runtime.grpc.enabled:
        # Setup the client
        port = 8085
        channel = grpc.insecure_channel(f"localhost:{port}")
        client_stub = inference_service.stub_class(channel)
        print(f"\n*** \n Client stub:\n--\n {client_stub}\n--\n")
        print(f"\n*** \n Verify if the with grpc command is available:\n--\n {dir(client_stub)}\n--\n")

        for text in ["This is "]:
            input_text_proto = TextInput(text=text).to_proto()
            print(f"\n*** \n Input text proto: '{input_text_proto}'\n*** \n ")

            request = inference_service.messages.HuggingFaceGenerationTaskRequst(text_input=input_text_proto)
            response = client_stub.HfModulePredict(
                request, metadata=[("mm-model-id", "text_generation")]
            )
            print("Text:", text)
            print("RESPONSE:", response)
