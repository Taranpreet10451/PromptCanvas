# Install required packages first:
# !pip install torch diffusers customtkinter pillow

import tkinter
import customtkinter as ctk
from PIL import Image, ImageTk
import torch
from diffusers import StableDiffusionPipeline

# GUI Configuration
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class ImageGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("AI Image Generator")
        self.geometry("1200x800")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Authorization token (replace with your own)
        self.auth_token = "Key"
        
        # ========== Create UI Components ==========
        # Header Frame
        self.header_frame = ctk.CTkFrame(self, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)
        
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="PromptCanvas: AI-Powered Text-to-Image Studio",
            font=ctk.CTkFont(family="Helvetica", size=28, weight="bold"),
            text_color="#4B9CD3"
        )
        self.title_label.pack(pady=15)
        
        # Input Frame
        self.input_frame = ctk.CTkFrame(self, corner_radius=10)
        self.input_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        self.prompt_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Describe the image you want to generate...",
            width=1000,
            height=50,
            font=ctk.CTkFont(size=16),
            corner_radius=8
        )
        self.prompt_entry.pack(pady=15, padx=15)
        
        self.generate_btn = ctk.CTkButton(
            self.input_frame,
            text="Generate Image",
            width=200,
            height=40,
            fg_color="#1E90FF",
            hover_color="#0066CC",
            font=ctk.CTkFont(weight="bold"),
            command=self.generate_image
        )
        self.generate_btn.pack(pady=(0, 15))
        
        # Image Display Frame
        self.image_frame = ctk.CTkFrame(self, corner_radius=10)
        self.image_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)
        
        self.image_label = ctk.CTkLabel(
            self.image_frame,
            text="Your generated image will appear here",
            width=800,
            height=500,
            corner_radius=10,
            fg_color=("gray20", "gray10"),
            text_color="gray50"
        )
        self.image_label.pack(pady=20, expand=True)
        
        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(
            self.input_frame,
            orientation="horizontal",
            mode="indeterminate",
            height=3,
            progress_color="#1E90FF"
        )
        
        # Error Label
        self.error_label = ctk.CTkLabel(
            self.input_frame,
            text="",
            text_color="red",
            wraplength=1000
        )

    def generate_image(self):
        prompt = self.prompt_entry.get().strip()
        if not prompt:
            self.show_error("Please enter a description to generate an image!")
            return
            
        self.clear_error()
        self.generate_btn.configure(state="disabled")
        self.progress_bar.pack(pady=(0, 10))
        self.progress_bar.start()
        
        try:
            # Initialize pipeline
            device = "cuda" if torch.cuda.is_available() else "cpu"
            dtype = torch.float16 if device == "cuda" else torch.float32
            
            pipeline = StableDiffusionPipeline.from_pretrained(
                "CompVis/stable-diffusion-v1-4",
                torch_dtype=dtype,
                use_auth_token=self.auth_token
            ).to(device)
            
            # Generate image
            with torch.autocast(device):
                generated_image = pipeline(
                    prompt,
                    guidance_scale=8.5,
                    num_inference_steps=50
                ).images[0]
            
            # Display image
            generated_image.save("generated_image.png")
            display_image = ctk.CTkImage(
                light_image=Image.open("generated_image.png"),
                size=(768, 512)
            )
            self.image_label.configure(image=display_image, text="")
            
        except Exception as e:
            self.show_error(f"Generation failed: {str(e)}")
            
        finally:
            self.progress_bar.stop()
            self.progress_bar.pack_forget()
            self.generate_btn.configure(state="normal")

    def show_error(self, message):
        self.error_label.configure(text=message)
        self.error_label.pack(pady=(0, 10))

    def clear_error(self):
        self.error_label.configure(text="")
        self.error_label.pack_forget()

if __name__ == "__main__":
    app = ImageGeneratorApp()
    app.mainloop()
