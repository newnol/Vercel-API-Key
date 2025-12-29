import base64
import os
from datetime import datetime
 
from dotenv import load_dotenv
from openai import OpenAI
 
load_dotenv()
 
def main():
    # Initialize the OpenAI client with AI Gateway
    client = OpenAI(
        api_key="sk-lb-LuVvR3CE-iKzPGHafeAP7xszMzDRaPCM",
        base_url="http://localhost:8000/v1",
    )
 
    # Generate an image
    result = client.images.generate(
        model="bfl/flux-2-pro",
        prompt="A majestic blue whale breaching the ocean surface at sunset",
        n=1,
        response_format="b64_json",
    )
 
    if not result.data:
        raise Exception("No image data received")
 
    print(f"Generated {len(result.data)} image(s)")
 
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
 
    # Save images to disk
    for i, image in enumerate(result.data):
        if image.b64_json:
            image_bytes = base64.b64decode(image.b64_json)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"output/image_{timestamp}_{i+1}.png"
 
            with open(output_file, "wb") as f:
                f.write(image_bytes)
            print(f"Saved image to {output_file}")
 
if __name__ == "__main__":
    main()