

from flask import jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from llama_cpp import Llama
import os


def get_slm_summary(user_input, model_name, system_message, temperature, max_tokens, top_p, top_k):
    """
    This function extracts the slm summary.

    Parameters:
    user_input: str - User prompt.
    model_name: str - Model name.
    system_message: str - System orientation message.
    temperature: float - Model Temperature parameter.
    max_tokens: int - Limit of tokens in the model response.
    top_p: float - Model top_p parameter.
    top_k: float - Model top_k parameter.

    Returns:
        A string with model answer.
    """
    try:

        print("Loading model and tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )

        print("Setting up pipeline...")
        # Use the pipeline with explicitly loaded components
        generator = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer
        )

        # Generate text
        prompt = (
            f""" <|system|>\n
                {system_message}\n
                <|user|>\n
                {user_input}
                <|assistant|>\n"""
        )

        print("Generating summary...")
        result = generator(
            prompt,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            do_sample=True,
            return_full_text=False,
            max_new_tokens=max_tokens
        )

        print("\n" + "="*50)
        print("GENERATED SUMMARY:")
        print("="*50)
        print(result[0]['generated_text'])

        # Read DOCX file
        # doc = Document(file_path)
        # file_content = {}
        # for paragraph in doc.paragraphs:
        #     for run in paragraph.runs:
        #         file_content[run.text] = ''

        return result[0], 200
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500
    
def get_slm_summary_llama_cpp(user_input, model_name, system_message, temperature, max_tokens, top_p, top_k):
    """
    This function extracts the SLM summary using a local GGUF model (llama.cpp backend).

    Parameters:
    user_input: str - User prompt.
    model_path: str - Path to the local .gguf model.
    system_message: str - System prompt or orientation.
    temperature: float - Model temperature parameter.
    max_tokens: int - Limit of tokens in the model response.
    top_p: float - top_p for nucleus sampling.
    top_k: int - top_k for token filtering.

    Returns:
        A string with model answer.
    """
    try:
        print("Loading GGUF model...")

        model_path = os.path.join("model-api", "models", model_name)
        llm = Llama(
            model_path= os.path.abspath(model_path),
            n_ctx=4096,  # or increase depending on your GPU/CPU
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            verbose=False
        )

        # Phi-3 expects specific format with <|system|>, <|user|>, <|assistant|>
        prompt = (
            f"<|system|>\n{system_message}\n"
            f"<|user|>\n{user_input}\n"
            f"<|assistant|>\n"
        )

        print("Generating summary...")
        output = llm(prompt, max_tokens=max_tokens, stop=["<|user|>", "<|system|>", "<|end|>"])

        answer = output["choices"][0]["text"]

        print("\n" + "="*50)
        print("GENERATED SUMMARY:")
        print("="*50)
        print(answer)

        return answer, 200

    except Exception as e:
        return {"message": f"Error: {str(e)}"}, 500