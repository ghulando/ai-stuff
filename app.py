import gradio as gr
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
import os

class ModelManager:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = "cpu"
        self.model_path = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

    def load_model(self):
        if self.model is None:
            print("Loading TinyLlama model...")
            
            try:
                # Optimize tokenizer loading
                self.tokenizer = AutoTokenizer.from_pretrained(
                    self.model_path,
                    trust_remote_code=True
                )
                
                try:
                    # Try 8-bit quantization first
                    quantization_config = BitsAndBytesConfig(
                        load_in_8bit=True,
                        llm_int8_threshold=6.0
                    )
                    
                    # Load model with 8-bit quantization
                    self.model = AutoModelForCausalLM.from_pretrained(
                        self.model_path,
                        torch_dtype=torch.float32,
                        device_map=self.device,
                        low_cpu_mem_usage=True,
                        trust_remote_code=True,
                        quantization_config=quantization_config
                    )
                except ImportError:
                    print("8-bit quantization not available, falling back to 32-bit")
                    # Load model without quantization
                    self.model = AutoModelForCausalLM.from_pretrained(
                        self.model_path,
                        torch_dtype=torch.float32,
                        device_map=self.device,
                        low_cpu_mem_usage=True,
                        trust_remote_code=True
                    )
                
                # Enable model optimization
                self.model.eval()  # Set to evaluation mode
                torch.set_num_threads(os.cpu_count())  # Use all CPU cores
                
                return "Model loaded successfully!"
            except Exception as e:
                return f"Error loading model: {str(e)}"
        
        return "Model already loaded!"

    def generate_response(self, prompt):
        if self.model is None:
            return "Please load the model first!"
        
        # Optimize input processing
        with torch.no_grad():  # Disable gradient calculation
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512  # Limit input length
            ).to(self.device)
            
            outputs = self.model.generate(
                **inputs,
                max_length=512,  # Reduced for faster generation
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                num_beams=1,  # Disable beam search for faster generation
                early_stopping=True
            )
        
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

def create_ui():
    manager = ModelManager()
    
    with gr.Blocks(title="TinyLlama Interface") as interface:
        gr.Markdown("# TinyLlama Chat Interface (CPU Optimized)")
        
        with gr.Row():
            load_btn = gr.Button("Load TinyLlama Model")
            status = gr.Textbox(label="Status")
        
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
            outputs=[status]
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
