# Usage: modal run --detach convert_rkllm.py
import modal

FORCE_BUILD = False  # Set to True to force a new image build
PYTHON_VERSION = "3.10"

app = modal.App("convert-rkllm")

image = (
    modal.Image.debian_slim(
        python_version=PYTHON_VERSION,
        force_build=FORCE_BUILD)
    .apt_install("git")
    .run_commands(
        "git clone https://github.com/limcheekin/ez-er-rkllm-toolkit.git"
    )    
    .run_commands(
        "python -m pip install inquirer ez-er-rkllm-toolkit/docker-noninteractive/rkllm_toolkit-1.1.4-cp310-cp310-linux_x86_64.whl xformers"
    )
)

@app.function(
    image=image, timeout=3600 * 24 # max 24 hours
)
def convert():
    import os

    MODEL_NAME = "username/model" 

    os.environ["HF_TOKEN"] = "your_huggingface_token"
    os.environ["HF_USERNAME"] = "your_huggingface_username"
    os.system("git clone https://github.com/limcheekin/ez-er-rkllm-toolkit.git")
    os.system(f'python ez-er-rkllm-toolkit/docker-noninteractive/noninteractive_pipeline.py {MODEL_NAME}')

if __name__ == '__main__':
    with app.run():
        print(convert.call())