"""
ComfyUI node-type → model folder mapping.

Used by download_hf_model to resolve where to store a downloaded model file
based on the ComfyUI node class that references it.

Usage
-----
    from agenty_core.utils.model_node_mapping import get_storage_path

    dest = get_storage_path("UNETLoader", "flux1-dev.safetensors", "/AI/ComfyUI")
    # → /AI/ComfyUI/models/unet/flux1-dev.safetensors
"""

import os

# ---------------------------------------------------------------------------
# Mapping: ComfyUI node class → relative folder under the ComfyUI root
# ---------------------------------------------------------------------------

NODE_TO_FOLDER: dict[str, str] = {
    # Checkpoints (SD1.5, SDXL, etc.)
    "CheckpointLoaderSimple": "models/checkpoints",
    "CheckpointLoader": "models/checkpoints",
    "unCLIPCheckpointLoader": "models/checkpoints",
    "CheckpointLoaderNF4": "models/checkpoints",
    "ImageOnlyCheckpointLoader": "models/checkpoints",  # SVD, Hunyuan3D 2.1

    # UNETs (Flux, Wan, modern diffusion models)
    "UNETLoader": "models/unet",
    "UnetLoaderGGUF": "models/unet",

    # LoRAs
    "LoraLoader": "models/loras",
    "LoraLoaderModelOnly": "models/loras",
    "LoRALoader": "models/loras",  # case variant

    # VAEs
    "VAELoader": "models/vae",

    # CLIP Text Encoders
    "CLIPLoader": "models/clip",
    "DualCLIPLoader": "models/clip",
    "TripleCLIPLoader": "models/clip",
    "CLIPVisionLoader": "models/clip_vision",

    # ControlNets
    "ControlNetLoader": "models/controlnet",
    "DiffControlNetLoader": "models/controlnet",
    "ControlNetLoaderAdvanced": "models/controlnet",

    # Upscale Models
    "UpscaleModelLoader": "models/upscale_models",
    "LatentUpscaleModelLoader": "models/latent_upscale_models",

    # GLIGEN (text-to-image guidance)
    "GLIGENLoader": "models/gligen",

    # Style Models
    "StyleModelLoader": "models/style_models",

    # Embeddings / Textual Inversion
    "Embedding": "models/embeddings",  # referenced in prompts, not a loader node

    # Hypernetworks (legacy)
    "HypernetworkLoader": "models/hypernetworks",

    # PhotoMaker (ID consistency)
    "PhotoMakerLoader": "models/photomaker",

    # IP-Adapter
    "IPAdapterModelLoader": "models/ipadapter",
    "IPAdapterUnifiedLoader": "models/ipadapter",

    # InstantID
    "InstantIDModelLoader": "models/instantid",

    # Segmentation / Detection
    "UltralyticsDetectorProvider": "models/ultralytics/bbox",
    "SAMModelLoader": "models/sams",  # Segment Anything

    # AnimateDiff
    "AnimateDiffLoader": "models/animatediff_models",
    "AnimateDiffMotionLoRA": "models/animatediff_motion_lora",

    # CogVideoX
    "CogVideoXModelLoader": "models/CogVideo/CogVideoX",

    # Mochi (video)
    "MochiModelLoader": "models/mochi",

    # LTX Video
    "LTXVModelLoader": "models/ltxv",
    "LTXAVTextEncoderLoader": "models/text_encoders",
    "LTXVAudioVAELoader": "models/checkpoints",

    # Model Patches
    "ModelPatchLoader": "models/model_patches",
}


# ---------------------------------------------------------------------------
# Fallback: model *filename* → folder, for when the loader node class is not
# known (e.g. the download+rerun path keys off a filename named in a blocker).
#
# Ordered list of (keyword-substrings, folder); first match wins, so more
# specific signals must precede generic ones (clip_vision before the text
# encoders; a "*_vae" before the diffusion-model families). Folder names match
# the canonical ComfyUI models/ subdirs (extra_model_paths.yaml.example) and the
# leaf dirs this server actually scans. See
# https://docs.comfy.org/development/core-concepts/models
# ---------------------------------------------------------------------------

FILENAME_FOLDER_RULES: list[tuple[tuple[str, ...], str]] = [
    # Vision-CLIP before text encoders (both contain "clip"). The big ViT
    # backbones (H/G/bigG-14) are vision encoders, not text encoders.
    (("clip_vision", "clipvision", "clip-vision", "clip_vit", "clip-vit",
      "vit-h-14", "vit-g-14", "vit-bigg", "vit_bigg"), "models/clip_vision"),
    # Text encoders (T5 / CLIP-L/G / UMT5 / ByT5 / LLaVA / Gemma / long-CLIP).
    (("t5xxl", "t5-xxl", "t5_xxl", "umt5", "byt5", "mt5-", "google_t5", "oldt5",
      "clip_l", "clip-l", "clip_g", "clip-g", "llava_", "llava-",
      "gemma_2", "gemma-2", "longclip", "long_clip", "text_encoder",
      "text-encoder", "qwen2.5-vl", "qwen_2.5_vl"), "models/text_encoders"),
    # Identity/adapter models. InstantID before IP-Adapter: its file is named
    # ip-adapter_instant_id_* but belongs in models/instantid.
    (("instantid", "instant_id", "instant-id"), "models/instantid"),
    (("ip-adapter", "ip_adapter", "ipadapter"), "models/ipadapter"),
    (("photomaker",), "models/photomaker"),
    (("pulid",), "models/pulid"),
    (("controlnet", "control_net", "control-lora", "control_lora", "controllora",
      "t2i-adapter", "t2iadapter", "control_v11", "control-v11", "control_sd",
      "union_controlnet", "union-controlnet", "promax"), "models/controlnet"),
    (("style_model", "stylemodel", "flux1-redux", "flux-redux", "flux_redux",
      "redux"), "models/style_models"),
    (("gligen",), "models/gligen"),
    # Motion / video-adapter modules.
    (("animatediff", "mm_sd", "mm-sd", "motion_module", "motionmodule",
      "v3_sd15_mm", "temporaldiff"), "models/animatediff_models"),
    # Segmentation / detection / matting / geometry.
    (("sam_vit", "sam2_", "sam2.", "sam2-", "sam_hq", "mobile_sam", "sam_b.",
      "sam_l.", "sam_h.", "sam_hiera", "segment-anything", "segment_anything"),
     "models/sams"),
    (("mediapipe",), "models/mediapipe"),
    (("yolov", "yolo_", "yolo-", "_bbox", "-bbox", "face_yolo", "hand_yolo",
      "person_yolo"), "models/ultralytics"),
    (("birefnet", "rmbg", "u2net", "isnet", "inspyrenet", "briaai", "ben2",
      "bria_"), "models/background_removal"),
    (("depth_anything", "depthanything", "depth-anything"), "models/depth_anything"),
    (("moge",), "models/geometry_estimation"),
    # Upscalers (ESRGAN family and friends).
    (("upscal", "esrgan", "realesr", "swinir", "ultrasharp", "remacri", "nmkd",
      "4x-", "4x_", "8x_", "2x_", "1x-", "x4-", "siax", "foolhardy", "nomos",
      "datx", "hat_"), "models/upscale_models"),
    (("taesd",), "models/vae_approx"),
    # LoRAs (LyCORIS / LoKR / LoHa included).
    ((".lora", "_lora", "-lora", "lora_", "lora-", "lycoris", "lokr", "loha"),
     "models/loras"),
    # VAEs / autoencoders (after LoRA/TE so "*_vae" wins over model families).
    # "ae.safetensors"/"ae.sft" is Flux's bare-named VAE.
    (("_vae", "-vae", "vae_", "vae-", ".vae", "autoencoder", "_ae.", "-ae.",
      "ae.safetensors", "ae.sft", "ae.pt"), "models/vae"),
    (("model_patch", "modelpatch"), "models/model_patches"),
    (("embedding", "textual_inversion", "easynegative", "badhand"),
     "models/embeddings"),
    # Modern DiT / video diffusion — loaded via UNETLoader / diffusion_models.
    (("flux1", "flux-1", "flux_1", "flux-dev", "flux-schnell", "flux2", "flux_2",
      "wan2", "wan_2", "wan21", "wan22", "wan-2", "ltx", "ltxv", "hunyuan_video",
      "hunyuanvideo", "hunyuan_dit", "sd3.5", "sd3_5", "sd35_", "qwen_image",
      "qwen-image", "cosmos", "mochi", "hidream", "chroma", "auraflow", "pixart",
      "sana_", "lumina", "omnigen", "kolors", "longcat", "ace_step", "acestep",
      "z_image", "zimage", "nunchaku"), "models/diffusion_models"),
]


def guess_folder_from_filename(filename: str) -> str | None:
    """Best-effort ``models/<folder>`` for a model *filename* when the loader node
    class is unknown. Returns None if no confident match (caller should then fall
    back to a safe default such as ``checkpoints``)."""
    n = filename.replace("\\", "/").rsplit("/", 1)[-1].lower()
    for subs, folder in FILENAME_FOLDER_RULES:
        if any(s in n for s in subs):
            return folder
    return None


# ---------------------------------------------------------------------------
# Mapping: ComfyUI node class → input parameter name(s) that hold the filename
# ---------------------------------------------------------------------------

NODE_TO_PARAM: dict[str, str | list[str]] = {
    "CheckpointLoaderSimple": "ckpt_name",
    "CheckpointLoader": "ckpt_name",
    "unCLIPCheckpointLoader": "ckpt_name",
    "CheckpointLoaderNF4": "ckpt_name",
    "UNETLoader": "unet_name",
    "UnetLoaderGGUF": "unet_name",
    "LoraLoader": "lora_name",
    "LoraLoaderModelOnly": "lora_name",
    "LoRALoader": "lora_name",
    "VAELoader": "vae_name",
    "CLIPLoader": "clip_name",
    "DualCLIPLoader": ["clip_name1", "clip_name2"],   # takes TWO files
    "TripleCLIPLoader": ["clip_name1", "clip_name2", "clip_name3"],
    "CLIPVisionLoader": "clip_name",
    "ControlNetLoader": "control_net_name",
    "DiffControlNetLoader": "control_net_name",
    "ControlNetLoaderAdvanced": "control_net_name",
    "UpscaleModelLoader": "model_name",
    "LatentUpscaleModelLoader": "model_name",
    "GLIGENLoader": "gligen_name",
    "StyleModelLoader": "style_model_name",
    "HypernetworkLoader": "hypernetwork_name",
    "PhotoMakerLoader": "photomaker_model_name",
    "IPAdapterModelLoader": "ipadapter_file",
    "IPAdapterUnifiedLoader": "model",
    "InstantIDModelLoader": "instantid_file",
    "UltralyticsDetectorProvider": "model_name",
    "SAMModelLoader": "model_name",
    "AnimateDiffLoader": "model_name",
    "AnimateDiffMotionLoRA": "lora_name",
    "CogVideoXModelLoader": "model",
    "MochiModelLoader": "model_name",
    "LTXVModelLoader": "model_name",
    "LTXAVTextEncoderLoader": "t5xxl_name",
    "LTXVAudioVAELoader": "vae_name",
    "ModelPatchLoader": "model_patch_name",
}


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def get_storage_path(node_class_type: str, filename: str, comfyui_base: str) -> str:
    """Return the absolute destination path for a model file.

    Args:
        node_class_type: ComfyUI node class name e.g. ``"UNETLoader"``.
        filename:        Model filename e.g. ``"flux1-dev.safetensors"``.
        comfyui_base:    Root directory of the ComfyUI installation,
                         e.g. ``"D:/AI/ComfyUI"``.  The ``models/`` subtree
                         lives directly underneath this directory.

    Returns:
        Absolute path string where the file should be stored.

    Raises:
        ValueError: If *node_class_type* is not in :data:`NODE_TO_FOLDER`.
    """
    folder = NODE_TO_FOLDER.get(node_class_type)
    if not folder:
        raise ValueError(
            f"Unknown node type: {node_class_type!r}. "
            f"Known types: {sorted(NODE_TO_FOLDER)}"
        )

    return os.path.join(comfyui_base, folder, filename)
