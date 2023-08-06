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
import os

# Third Party
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, PreTrainedTokenizer

# Local
from caikit.core import ModuleBase, ModuleLoader, ModuleSaver, module

from text_generation.data_model.text_generation import (
    TextOutput,
    TextInput
)

DEFAULT_MODEL = "google/flan-t5-small"
DEFAULT_MODEL_REVISION = "f6b63ff"

@module("9E42606B-34A8-4D4C-9B6C-6F66DAD8EC5A", "HuggingFaceTextGenerationModule", "0.0.1")
class HuggingFaceTextGenerationModule(ModuleBase):
    """Class to wrap AutoModelForSeq2SeqLM models from HuggingFace"""

    tokenizer: PreTrainedTokenizer
    model: any

    def __init__(self, model_path, whatever) -> None:
        super().__init__()
        #loader = ModuleLoader(model_path)
        #config = loader.config


    def run(self, text_input: TextInput) -> TextOutput:
       
        print("---------------------")
        print("- run model invoked")
        print("---------------------")
                   
        input_str: str
        input_str = text_input.text

        print("---------------------")
        print("- Input")
        print("---------------------")
        print(f"Input string: {input_str}")

        input_ids = HuggingFaceTextGenerationModule.tokenizer(input_str, return_tensors="pt")["input_ids"]
        output_ids = HuggingFaceTextGenerationModule.model.generate(input_ids)[0]
        result = HuggingFaceTextGenerationModule.tokenizer.decode(output_ids, skip_special_tokens=True)
        
        print("---------------------")
        print("- Result")
        print("---------------------")
        print(f"Result : {result}")

        return TextOutput(result)


    @classmethod
    def load(cls, model_path):

        #model_name, model_revision = ModuleBase.read_config(
        #    model_path, DEFAULT_MODEL, DEFAULT_MODEL_REVISION
        #)

        model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")
        HuggingFaceTextGenerationModule.model = model
        tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
        HuggingFaceTextGenerationModule.tokenizer = tokenizer
        print("---------------------")
        print("- model loaded")
        print(f"  model path: {model_path}")
        print("---------------------")

        return cls(model, tokenizer)


    def save(self, model_path, **kwargs):
        module_saver = ModuleSaver(
            self,
            model_path=model_path,
        )

        with module_saver:
            rel_path, _ = module_saver.add_dir("hf_model")
            save_path = os.path.join(model_path, rel_path)
            self.sentiment_pipeline.save_pretrained(save_path)
            module_saver.update_config({"hf_artifact_path": rel_path})

    @classmethod
    def bootstrap(cls, model_path="google/flan-t5-small"):
        print("---------------------")
        print("- bootstrap start")
        print("---------------------")

        model = AutoModelForSeq2SeqLM.from_pretrained(DEFAULT_MODEL)
        tokenizer = AutoTokenizer.from_pretrained(DEFAULT_MODEL)
        
        print("---------------------")
        print("- bootstrap end")
        print("---------------------")

        return cls(model_path)