# Caikit custom model profiles

----------------------------------
----- **UNDER CONSTRUCTION** -----
----------------------------------

## 1. Objective

The objective of the project is to add a custom model to `caikit==v0.4.1` and use `grpcurl` to invoke a text generation command.

The project contains a `client/server` example for using GRPC. 

## 2. Environment setup

* Clone the project

```sh
git clone https://github.com/thomassuedbroecker/caikit-custom-model-protofiles.git
```

* Create virtual environment

```sh
cd code

python3.10 -m venv caikit-env-3.10
source ./caikit-env-3.10/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip install grpcio
python3 -m pip install grpcio-tools
python3 -m pip install grpcio-health-checking
python3 -m pip install grpcio-reflection
python3 -m pip install prometheus_client
python3 -m pip install py_grpc_prometheus
python3 -m pip install caikit.runtime.service_factory
#python3 -m caikit.runtime.dump_services protos
```

## 3. Start the `server/client` example

* Simplified dependences of the `client/server` architecture of the example

![](/images/caikit-simplifed-dependencies-overview-2023-05-25-example-client-server-depencencies.drawio.png)

* Start the server in the first terminal

```sh
source ./caikit-env-3.10/bin/activate
python start_runtime.py
```

Output:

```sh
...
2023-08-06T11:28:10.609698 [2PCVR:DBUG] Message name: TrainingStatusResponse
2023-08-06T11:28:10.609997 [2PCVR:DBUG] Creating FileDescriptorProto
2023-08-06T11:28:10.610045 [2PCVR:DBUG] Adding Descriptors to DescriptorPool
{"channel": "SERVR-GRPC", "exception": null, "level": "info", "message": "Serving prometheus metrics on port 8086", "num_indent": 0, "thread_id": 140704560412224, "timestamp": "2023-08-06T11:28:10.623832"}
...
```

* Start the client in the second terminal

```sh
source ./caikit-env-3.10/bin/activate
python client.py
```

## 3. Create `protos`

Execute the following command in the third terminal.
The command will create a folder with the proto files on your local computer.

```sh
source ./caikit-env-3.10/bin/activate
export CONFIG_FILES=text_generation/config.yml
python3 -m caikit.runtime.dump_services protos
```

## Use `grpcurl`

* List the services

```sh
grpcurl -import-path ./protos -proto textgenerationservice.proto list
```

Example output:

```sh
caikit.runtime.TextGeneration.TextGenerationService
```

* List the services with the grpc-server

```sh
grpcurl -import-path ./protos -proto textgenerationservice.proto -plaintext localhost:8085 list
```

Example output:

```sh
caikit.runtime.TextGeneration.TextGenerationService
```

* Describe the service

```sh
grpcurl -import-path ./protos -proto textgenerationservice.proto -plaintext localhost:8085 describe caikit.runtime.TextGeneration.TextGenerationService
```

Example output:

```sh
service TextGenerationService {
  rpc HfModulePredict ( .caikit.runtime.TextGeneration.HfModuleRequest ) returns ( .text_generation.data_model.TextOutput );
}
```

```sh
grpcurl -import-path ./protos -proto hfmodulerequest.proto -plaintext localhost:8085 describe caikit.runtime.TextGeneration.HfModuleRequest
```

Example output:

```sh
message HfModuleRequest {
  //-- fields --
  .text_generation.data_model.TextInput text_input = 1;
}
```

* Invoke a method of the service

```sh
MM_MODEL_ID=text_generation
grpcurl -d '{"text_input":{"text":"This is"}}' -H "mm-model-id:$MM_MODEL_ID" -import-path ./protos -proto textgenerationservice.proto -plaintext localhost:8085 caikit.runtime.TextGeneration.TextGenerationService/HfModulePredict
```

## Container

* Build a container image and execute a container image

```sh
docker build -f Dockerfile -t caikit-server-proto-export:v1 .
docker run -it caikit-server-proto-export:v1
```

* Verify the created `protos`

Navigate inside the container to the `protos` folder.

```sh
cd protos
ls
```

* Example output

```sh
hfmodulerequest.proto                textoutput.proto
modelpointer.proto                   traininginforequest.proto
producerid.proto                     traininginforesponse.proto
producerpriority.proto               trainingjob.proto
textgenerationservice.proto          trainingmanagement.proto
textgenerationtrainingservice.proto  trainingstatus.proto
textinput.proto
```

