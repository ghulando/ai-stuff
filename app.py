import gradio as gr
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
import os

class ModelManager:
    def __init__(self):
        self.models = {}
        self.current_model = None
        self.device = "cpu"
        # Using smaller, more efficient models
        self.available_models = {
            "gpt2": "gpt2",  # 124M parameters
            "distilgpt2": "distilgpt2",  # 82M parameters
            "bloom-560m": "bigscience/bloom-560m",  # 560M parameters
            "tiny-llama": "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # 1.1B parameters
        }

    def load_model(self, model_name):
        if model_name not in self.models:
            print(f"Loading {model_name}...")
            model_path = self.available_models[model_name]
            
            # Optimize tokenizer loading
            tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                trust_remote_code=True,
                local_files_only=True  # Use cached files if available
            )
            
            # Configure 8-bit quantization
            quantization_config = BitsAndBytesConfig(
                load_in_8bit=True,
                llm_int8_threshold=6.0
            )
            
            # Load model with optimizations
            model = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.float32,
                device_map=self.device,
                low_cpu_mem_usage=True,
                trust_remote_code=True,
                quantization_config=quantization_config
            )
            
            # Enable model optimization
            model.eval()  # Set to evaluation mode
            torch.set_num_threads(os.cpu_count())  # Use all CPU cores
            
            self.models[model_name] = (model, tokenizer)
        
        self.current_model = model_name
        return "Model loaded successfully!"

    def generate_response(self, prompt):
        if not self.current_model:
            return "Please select a model first!"
        
        model, tokenizer = self.models[self.current_model]
        
        # Optimize input processing
        with torch.no_grad():  # Disable gradient calculation
            inputs = tokenizer(
                prompt,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512  # Limit input length
            ).to(self.device)
            
            outputs = model.generate(
                **inputs,
                max_length=512,  # Reduced from 2048 for faster generation
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                num_beams=1,  # Disable beam search for faster generation
                early_stopping=True
            )
        
        return tokenizer.decode(outputs[0], skip_special_tokens=True)

def create_ui():
    manager = ModelManager()
    
    with gr.Blocks(title="AI Models Interface") as interface:
        gr.Markdown("# Fast AI Models Interface (CPU Optimized)")
        
        with gr.Row():
            model_dropdown = gr.Dropdown(
                choices=list(manager.available_models.keys()),
                label="Select Model",
                value="distilgpt2"  # Set default model
            )
            load_btn = gr.Button("Load Model")
        
        with gr.Row():
            with gr.Column():
                input_text = gr.Textbox(
                    lines=5,
                    label="Input Prompt",
                    placeholder="Enter your prompt here..."
                )
                submit_btn = gr.Button("Generate")
            
            with gr.Column():
                output_text = gr.Textbox(
                    lines=5,
                    label="Generated Output"
                )
        
        load_btn.click(
            fn=manager.load_model,
            inputs=[model_dropdown],
            outputs=[gr.Textbox(label="Status")]
        )
        
        submit_btn.click(
            fn=manager.generate_response,
            inputs=[input_text],
            outputs=[output_text]
        )
    
    return interface

if __name__ == "__main__":
    interface = create_ui()
    interface.launch(server_name="0.0.0.0", server_port=7860)
