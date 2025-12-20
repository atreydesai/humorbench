"""Script to download and cache all models used in humorbench evaluation."""

import os
import sys
import gc
import time

# Set HuggingFace cache directory (same as vllm_inference.py)
HF_HOME = "/fs/nexus-scratch/adesai10"
os.environ["HF_HOME"] = HF_HOME
os.environ["HUGGINGFACE_HUB_CACHE"] = os.path.join(HF_HOME, "hub")

# List of models to download
MODELS = [
    "Qwen/Qwen3-8B",
    "Qwen/Qwen3-32B",
    "allenai/Olmo-3-7B-Instruct",
    "allenai/Olmo-3.1-32B-Instruct",
    "tiiuae/Falcon3-10B-Instruct",
    "swiss-ai/Apertus-8B-Instruct-2509",
    "mistralai/Ministral-8B-Instruct-2410",
]


def check_model_cache(model_name: str) -> bool:
    """Check if model is already cached."""
    cache_name = model_name.replace("/", "--")
    cache_dir = os.path.join(HF_HOME, "hub", f"models--{cache_name}")
    return os.path.exists(cache_dir)


def download_model_with_vllm(model_name: str) -> None:
    """Download model by loading it with VLLM (triggers download if not cached)."""
    llm = None
    try:
        from vllm import LLM
        
        print(f"\n{'='*80}")
        print(f"Downloading/loading model: {model_name}")
        print(f"{'='*80}")
        
        # Load model with VLLM - this will download if not cached
        llm = LLM(
            model=model_name,
            trust_remote_code=True,
            max_model_len=20000,
        )
        
        print(f"✓ Successfully loaded {model_name}")
        
    except Exception as e:
        print(f"✗ Error loading {model_name}: {e}")
        raise
    finally:
        # Clean up to free memory - critical to prevent OOM errors
        if llm is not None:
            del llm
        
        # Force garbage collection
        gc.collect()
        
        # Clear CUDA cache if available
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                torch.cuda.synchronize()
        except ImportError:
            pass


def download_model_with_transformers(model_name: str) -> None:
    """Alternative: Download model using transformers library.
    
    Note: Transformers-downloaded weights ARE compatible with VLLM.
    Both use the same HuggingFace cache format, so VLLM can use
    weights downloaded by transformers.
    """
    tokenizer = None
    model = None
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        
        print(f"\n{'='*80}")
        print(f"Downloading model: {model_name}")
        print(f"{'='*80}")
        
        # Download tokenizer
        print(f"Downloading tokenizer for {model_name}...")
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True,
        )
        print(f"✓ Tokenizer downloaded")
        
        # Download full model weights (this will cache them for VLLM to use)
        print(f"Downloading model weights for {model_name}...")
        print(f"  (This may take a while for large models...)")
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            torch_dtype="auto",
            low_cpu_mem_usage=True,  # More memory efficient
        )
        print(f"✓ Model weights downloaded and cached")
        
    except Exception as e:
        print(f"✗ Error downloading {model_name}: {e}")
        raise
    finally:
        # Clean up to free memory
        if tokenizer is not None:
            del tokenizer
        if model is not None:
            del model
        
        # Force garbage collection
        gc.collect()
        
        # Clear CUDA cache if available
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                torch.cuda.synchronize()
        except ImportError:
            pass


def main() -> None:
    """Download all models."""
    print(f"HuggingFace cache directory: {HF_HOME}/hub")
    print(f"Total models to download: {len(MODELS)}\n")
    
    # Check which models are already cached
    cached_models = []
    uncached_models = []
    
    for model in MODELS:
        if check_model_cache(model):
            print(f"✓ {model} is already cached")
            cached_models.append(model)
        else:
            print(f"✗ {model} needs to be downloaded")
            uncached_models.append(model)
    
    if not uncached_models:
        print("\n" + "="*80)
        print("All models are already cached! Nothing to download.")
        print("="*80)
        return
    
    print(f"\n{'='*80}")
    print(f"Downloading {len(uncached_models)} model(s)...")
    print(f"{'='*80}\n")
    
    # Try downloading with VLLM first (more reliable for VLLM-compatible models)
    # If that fails, fall back to transformers
    for i, model in enumerate(uncached_models, 1):
        print(f"\n[{i}/{len(uncached_models)}] Processing: {model}")
        
        try:
            # Try VLLM first
            download_model_with_vllm(model)
        except Exception as vllm_error:
            print(f"VLLM download failed, trying transformers method...")
            try:
                download_model_with_transformers(model)
            except Exception as transformers_error:
                print(f"\n✗ Failed to download {model}")
                print(f"  VLLM error: {vllm_error}")
                print(f"  Transformers error: {transformers_error}")
                print(f"  You may need to download this model manually")
                continue
        
        # Small delay between downloads to allow cleanup to complete
        if i < len(uncached_models):
            print("Cleaning up before next download...")
            time.sleep(2)
    
    print(f"\n{'='*80}")
    print("Download process completed!")
    print(f"{'='*80}")
    
    # Final status check
    print("\nFinal cache status:")
    for model in MODELS:
        if check_model_cache(model):
            print(f"✓ {model}")
        else:
            print(f"✗ {model} (not cached)")


if __name__ == "__main__":
    main()

