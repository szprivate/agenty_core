# Workflow recipe database  (task -> model -> node clusters)

- Tasks: 29 | task+model recipes: 165
- Self-contained: every recipe has user_intent + description + node clusters. No human annotation step.

# API / Partner Nodes - Image Edit  (`api_partner_nodes_image_edit`)  -  94 workflow(s), 12 model(s)

## API / Partner Nodes - Image Edit / Generic  (`api_partner_nodes_image_edit__generic`)  -  63 workflow(s)  -  source: mixed
- execution: api (API nodes: BeebleSwitchXImageEdit, BriaImageEditNode, BriaRemoveImageBackground, ByteDanceSeedNode, ByteDanceSeedreamNode, ByteDanceSeedreamNodeV2, ClaudeNode, GeminiImage2Node, GeminiNanoBanana2, GeminiNanoBanana2V2, GeminiNode, GrokImageEditNode, GrokImageNode, LumaImageEditNode2, LumaImageModifyNode, LumaImageNode, LumaImageNode2, LumaReferenceNode, OpenAIChatConfig, OpenAIChatNode, OpenAIGPTImage1, OpenAIGPTImageNodeV2, OpenRouterLLMNode, QuiverImageToSVGNode, RecraftCreateStyleNode, RecraftStyleV3InfiniteStyleLibrary, RecraftTextToImageNode, ReveImageEditNode, ReveImageRemixNode, RunwayTextToImageNode, WavespeedImageUpscaleNode)
- when to use: Use to generate an image.
- example request: "build an image workflow"
- description: API / cloud image editing via OpenAI GPT2. 1 image input -> 1 image output. Processes and generates content using ComfyUI workflows. | Claude Fable 5, Anthropic's first public Mythos-class frontier model, powers end-to-end creative workflows in ComfyUI. It takes 1 text prompt and generates 1 structured output including storyboard breakdowns, precise prompts for SD models and ControlNet, and custom node scripts. Ideal for concept artists refining visual narratives, AI filmmakers maintaining style consistency across series, and digital creators automating their entire rendering pipeline. | Converts an image input into an SVG output. | Create static ads for your product in the style of a reference advertisement | Describe a scene or world using GPT-5.6 Terra, a balanced multimodal model that interprets one uploaded image to guide visual storytelling and style consistency. Ideal for worldbuilding, mood board creation, and maintaining cohesive aesthetics across a series of works. | Edit existing images with Uni-1's Image Edit mode, preserving composition and core elements. Supports targeted adjustments like lighting and color using prompts and reference images. | Engage with OpenAI's advanced language models for intelligent conversations. | Enhance image quality with advanced text rendering and creative control using Grok Imagine Image Quality. Input images or prompts for improved detail and fidelity. | FIBO enables precise, predictable image editing through structured JSON control over lighting, composition, and camera settings | GPT-5.6 Luna streamlines visual pre-production by analyzing a single reference image and generating structured creative text from a user prompt. It takes 1 input image and produces no explicit visual outputs, focusing instead on rapid, standardized copywriting. Ideal for batch scene description expansion, shot list organization, and high-volume creative ideation. | GPT-5.6 Sol is a multimodal model workflow for visual storytelling, taking 1 input image and a user prompt to generate detailed scene descriptions and narrative sequences. Ideal for world-building, multi-shot storyboarding, and maintaining consistent art style across long-form illustration or video projects. | Generate a 3x3 grid of image variations from a simple prompt and reference image using Nano Banana. 

Pick your favorite frame from the grid, then recreate it as a standalone high-quality image while maintaining character and outfit consistency.

Great for concept exploration, pose variations, camera angles, outfit ideas, and fast visual inspiration without generating each image individually. | Generate brand-new original images using the Luma UNI-1 node with up to 9 reference images for style, character, color, lighting, and composition. Create unique compositions with detailed prompts, adjustable aspect ratios, and seed control. | Generate detailed image descriptions and creative briefs using Kimi K3, a multimodal model with million-token context windows for unified text and image understanding. Input one image and a text prompt to produce nuanced visual analyses or batch descriptions. Ideal for streamlining multi-shot visual series, generating automated script prompts for node-based workflows, and iteratively refining creative concepts through image feedback. | Generate high-contrast, clickable YouTube thumbnails using Nano Banana Pro. Creates dramatic compositions with exaggerated subjects and bold color strategies for maximum engagement. | Generate high-quality images from text prompts using Runway's AI model. | Generate images by blending style references with precise control using Luma Photon. | Generate images from input images using OpenAI GPT Image 1 API. | Generate images from multiple inputs using OpenAI GPT Image 1 API. | Generate images from text prompts using OpenAI GPT Image 1 API. | Generate new images based on reference styles and compositions with Runway's AI. | Grok 4.5 is a flagship multimodal model designed for complex engineering and creative tasks, with native visual parsing and high-speed inference. It takes creative briefs and generated images as inputs, producing standardized scene descriptions and iterative visual analysis. Ideal for multi-shot storyboarding, batch image description generation, and feedback-driven creative refinement. | Guide image generation using a combination of images and prompt. | Input a black and white illustration and generate a colored output. | Input an image or video for analysis. Receive detailed text output describing visual content, reasoning, and structured information extraction. | Input your query or image for analysis. Generate a natural language response powered by Anthropic Claude, supporting both text conversation and image understanding. | Learn how to create a product photography with image inputs, enter a subgraph, unbypass a node and get to know partner nodes using Nano Banana Pro. | Leverage Claude Sonnet 5 for high-value autonomous task execution, bridging the gap to flagship performance at a lower cost. Input any text prompt or script to generate precise image descriptions, automated workflow scripts, shot sequence logs, or node logic corrections. Ideal for batch production tasks, debugging ComfyUI node logic, and maintaining consistent output quality across repetitive generation workflows. | Load an image and enter a prompt to interact with Claude Opus 5, a highly capable and cost-efficient AI model that excels at coding, knowledge work, and problem-solving. Ideal for software engineering tasks, scientific research requiring visual analysis, and everyday productivity with a thoughtful, proactive assistant. | Remix and edit images using Reve's advanced model. Combine multiple reference images into a single output | Transform clothing photos into professional mall billboard advertisements featuring realistic fashion models. | Transform real building photos into architectural blueprints and then into detailed physical scale models. A complete architectural visualization pipeline from photo to miniature. | Transform uploaded images into realistic poster designs. Change character poses, faces, and clothing while maintaining artistic style and color schemes. Outputs a visually impactful poster with artistic typography. | Upload 1-5 style references and create a style ID to generate consistent, on brand images. | Upload a character or selfie and prompt the outfit/scene. Generate a 2x2 grid of isometric figurines of your character. | Upload a dieline of your product and assemble into a 3D package. | Upload a graphic design and select your desired aspect ratio. Generates and recomposes the graphic to fit the new aspect ratio. | Upload a photo of a character holding a product and your brands product. Generate an image with the products swapped. | Upload a photo of your character and your product. Generate an image of that character holding the product. | Upload a poster/ad design and with a short input about your brand, generate 4 mockups in multiple scenes. | Upload a product image and a cinematic style reference. Generate a sequence of stylized product advertisements with consistent composition and lighting. | Upload a reference image and generate a 1x4 grid. Select desired image and upscale/refine with Nano Banana Pro. | Upload a reference image and write a prompt to create campaign-ready posters, product shots, and multilingual signage. The model renders clean text and photorealistic outputs suitable for commercial work. | Upload a reference image of an icon, enter your brand information in the prompt and generate 9 unique on brand stylized icon assets. | Upload a selfie and describe your outfit in the prompt. Generate 4 fashion editorial photographs with fun doodle illustrations. Select which image to upscale and add back face details. | Upload an AI-generated image to restore details and upscale. The workflow preserves colors and sharpness while minimizing artifacts. Output is a high-quality, enlarged version of your input. | Upload an image and generate 12 stylized variations in under 15 seconds. | Upload an image and provide text instructions to edit it. Generate a modified output image using Reve's advanced editing model for tasks like object removal, restoration, or recomposition. | Upload an image of your character and a flatlay image of your clothing items. Generate 4 fashion editorial photographs of your character in the outfit. Select which image to upscale and add back details. | Upload an image of your character and a flatlay of an outfit to be tried on. Generate 4 images in 1 Nano Banana prompt. | Upload an image to automatically remove its background using the Bria API. The workflow processes the request asynchronously and returns the edited image with a transparent background. | Upload an image to edit with the Grok model. Generate a modified version with expressive, cinematic visuals | Upload an input image and automatically generate X prompts for camera angle and shot type. | Upload any image and input your desired aspect ratio. Generate an outpainted version of your image to perfectly fit the new dimensions. | Upload multiple images to create a consistent style reference. Generate new images using this reference to maintain visual coherence across outputs. | Upload the fashion editorial and product image. Generate 8 distinct angle variations with product consistency from only 2 Nano Banana generations. | Upload your character image and a reference style/lighting image. Generate an edited output with the reference lighting and style applied to your original image. | Upload your character portrait and outfit reference. Generate a new portrait with the specific outfit applied for consistent wardrobe control. Affordable alternative to Nano Banana Pro and Nano Banana 2. | Upload your character, scene and product. Integrates all images into a fashion editorial style photograph. | Upload your product and a simple text prompt for the poster or ad design. Iterate on the look before swapping the product into the generate layout. | Upload your product and enter a brief prompt for each grid position in a 3x3 grid. Generates 9 distinct images. Select the images you like and upscale to 4k using your product as reference. | Upload your profile picture, enter a theme and generate 64 variations.
- member workflows:
    - api_anthropic_claude
    - api_anthropic_claude_fable5
    - api_anthropic_claude_opus_5
    - api_anthropic_claude_sonnet5
    - api_beeble_switchx_image_edit
    - api_bria_image_edit
    - api_bytedance_seed
    - api_from_photo_2_miniature
    - api_grok_image_edit
    - api_grok_imagine_image_quality_image_edit
    - api_i2i_imageEdit_OpenAi_GPT2
    - api_luma_photon_i2i
    - api_luma_photon_style_ref
    - api_luma_uni_1_image_create
    - api_luma_uni_1_image_edit
    - api_openai_chat
    - api_openai_fashion_billboard_generator
    - api_openai_gpt_image_2_image_edit
    - api_openai_image_1_i2i
    - api_openai_image_1_multi_inputs
    - api_openai_image_1_t2i
    - api_openrouter_gpt5_6_luna
    - api_openrouter_gpt5_6_sol
    - api_openrouter_gpt5_6_terra
    - api_openrouter_grok4_5
    - api_openrouter_kimi_k3
    - api_quiver_image_to_svg
    - api_recraft_style_reference
    - api_reve_image_edit
    - api_reve_image_remix
    - api_runway_reference_to_image
    - api_runway_text_to_image
    - api_wavespeed_seedvr2_ai_image_fix
    - gsc_starter_3
    - template-recraft_create_style
    - template_3x3_contact_sheet
    - template_contact_sheet-step_1.app
    - template_contact_sheet-step_2.app
    - template_eric_seedance_5_subject_and_outfit_combine
    - template_eric_thumbnail_generator
    - template_graphic_color_remixer
    - template_sferro21_product_ad.app
    - template_sirolim_any_aspect_ratio_nb2
    - templates-1_input-multiple_styles_prompt.app
    - templates-2x2_grid-iso_miniatures
    - templates-3x3_grid_brand_icons
    - templates-8x8_grid-pfp
    - templates-9grid_social_media-v2.0
    - templates-assemble_dieline
    - templates-color_illustration
    - templates-fashion_shoot_prompt_doodle
    - templates-fashion_shoot_vton
    - templates-multiple_consistent_shots-nb_pro
    - templates-poster_product_integration
    - templates-poster_to_2x2_mockups-v2.0
    - templates-product_ad-v2.0
    - templates-split_stack
    - templates-subject_holding_product.app
    - templates-subject_product_swap.app
    - templates_doc_workbox_poster_recreator
    - templates_graphic_design_recomposer
    - templates_rob_fashion_shoot_vton-4in1.app
    - utility_bria_remove_image_background
- node clusters (required structure):
    - (none resolved)
- optional roles: PreviewImage, ImageCrop, ImageStitch, SimpleMath+, GrokImageEditNode, SaveImage, ImageBatchMulti, ImageCrop+, LoadImage, BatchImagesNode, GeminiImage2Node, MarkdownNote
- unresolved nodes: FluxResolutionNode, Get Image Size, ImageCrop+, ImageRemoveAlpha+, ImageRemoveBackground+, LayerUtility: ColorImage V2, MarkdownNote, Note, Paste By Mask, PrimitiveNode, RemBGSession+, Reroute, SimpleMath+

## API / Partner Nodes - Image Edit / Nano-Banana  (`api_partner_nodes_image_edit__nano_banana`)  -  8 workflow(s)  -  source: mixed
- execution: api (API nodes: GeminiImage2Node, GeminiImageNode, GeminiInputFiles, GeminiNanoBanana2, GeminiNanoBanana2V2, GeminiNode)
- when to use: Use to edit an existing image using Nano-Banana, Gemini.
- example request: "build an image workflow using Nano-Banana"
- description: API / cloud image editing via Nano Banana 2. 1 image input -> 1 image output. Processes and generates content using ComfyUI workflows. | Design the text layout for your magazine cover photo, and explore packaging options for it. | Edit an image using Nano Banana 2 Lite, the fastest image generation model from Google's Gemini series, producing a side-by-side comparison of the original and edited result. I | Local style transfer FOR FULL BODY SHOTS via Nano-Banana Pro (Gemini). 1 video (layout reference) + 7 images (style + hero elements) -> 2 image outputs. Transfers the style reference onto the first video frame while integrating the look of hero element references. | Nano-banana (Gemini-2.5-Flash Image) - image editing with consistency. | Nano-banana Pro (Gemini 3.0 Pro Image) - Studio-quality 4K image generation and editing with enhanced text rendering and character consistency. | Upload an AI-generated image to upscale and enhance details. Generate a 4K output with improved sharpness and coherence using Nano Banana Pro. | Upload an image and a text prompt to edit it. Generate a new image that modifies the original based on your instructions, maintaining subject consistency and high visual fidelity.
- member workflows:
    - api_google_gemini_image
    - api_google_nano_banana2_image_edit
    - api_i2i_imageEdit_nanoBanana2
    - api_nano_banana_2_lite_image_edit
    - api_nano_banana_pro
    - styletransfer_NanoBananaPro
    - template-multistyle-magazine-cover-nanobananapro
    - utility_nanobanana_pro_ai_image_fix
- node clusters (required structure):
    - (none resolved)
- optional roles: VHS_LoadImagePath, GeminiImage2Node, SaveImage, BatchImagesNode, GeminiInputFiles, LoadImage, MarkdownNote, GeminiImageNode, GeminiNanoBanana2, GeminiNanoBanana2V2, GeminiNode, ImageCompare
- unresolved nodes: MarkdownNote

## API / Partner Nodes - Image Edit / Flux  (`api_partner_nodes_image_edit__flux`)  -  7 workflow(s)  -  source: official
- execution: api (API nodes: FluxEraseNode, FluxKontextMaxImageNode, FluxKontextProImageNode, FluxProExpandNode, FluxProUltraImageNode, FluxVTONode)
- when to use: Use to generate an image using Flux.
- example request: "build an image workflow using Flux"
- description: Edit images with Flux.1 Kontext max image. | Edit images with Flux.1 Kontext pro image. | Generate images with excellent prompt following and visual quality using FLUX.1 Pro. | Input multiple images and edit them with Flux.1 Kontext. | Upload a person photo and a garment image. Generate a virtual try-on result with the garment applied to the person while preserving face and pose. | Upload an image and paint a mask over the object to remove. The workflow erases the masked area and reconstructs the background. | Upload an image to expand its canvas using Flux.1. Generate an outpainted image with extended content.
- member workflows:
    - api_bfl_flux1_expand_image
    - api_bfl_flux_1_kontext_max_image
    - api_bfl_flux_1_kontext_multiple_images_input
    - api_bfl_flux_1_kontext_pro_image
    - api_bfl_flux_pro_t2i
    - api_flux_erase_image
    - api_flux_vto
- node clusters (required structure):
    - inputs: LoadImage
    - output: SaveImage
- optional roles: MarkdownNote, ImageStitch, FluxEraseNode, FluxKontextMaxImageNode, FluxKontextProImageNode, FluxProExpandNode, FluxProUltraImageNode, FluxVTONode, ImageCompare, PreviewImage
- unresolved nodes: MarkdownNote

## API / Partner Nodes - Image Edit / Seedream  (`api_partner_nodes_image_edit__seedream`)  -  4 workflow(s)  -  source: mixed
- execution: api (API nodes: ByteDanceSeedreamNode, ByteDanceSeedreamNodeV2)
- when to use: Use to edit an existing image using Seedream.
- example request: "build an image workflow using Seedream"
- description: API / cloud image editing via Seedream 5.0 lite. 2 image inputs -> 1 image output. Processes and generates content using ComfyUI workflows. | Edit images with precision using Seedream 5.0 Pro, targeting specific regions while preserving lighting, depth, and texture. The workflow takes 1 input image and produces 2 output images through an optional Painter node and preview. Ideal for product photography edits, portrait consistency adjustments, and creating structured layouts with multilingual text. | Multi-modal AI model for text-to-image and image editing. Generate 2K images in under 2 seconds with natural language control. | Upload an image of your product and background. Composite them and seamlessly relight and fuse together using Seedream 4.5.
- member workflows:
    - api_bytedance_seedream4
    - api_bytedance_seedream_5_0_lite_image_edit
    - api_bytedance_seedream_5_0_pro_image_edit
    - templates-product_scene_relight
- node clusters (required structure):
    - inputs: LoadImage
- optional roles: BatchImagesNode, ByteDanceSeedreamNode, ByteDanceSeedreamNodeV2, MarkdownNote, Painter, PreviewImage, RegexReplace, ResizeAndPadImage, SaveImage, SaveImageAdvanced
- unresolved nodes: MarkdownNote

## API / Partner Nodes - Image Edit / Flux 2  (`api_partner_nodes_image_edit__flux_2`)  -  2 workflow(s)  -  source: official
- execution: api (API nodes: Flux2MaxImageNode, Flux2ProImageNode)
- when to use: Use to generate an image using Flux 2.
- example request: "build an image workflow using Flux 2"
- description: Generate up to 4MP photorealistic images with multi-reference consistency and professional text rendering. | Replace objects in images with unmatched quality using FLUX.2 [max]. Perfect for product photography, furniture swaps, and maintaining scene consistency with highest editing precision.
- member workflows:
    - api_bfl_flux2_max_sofa_swap
    - api_flux2
- node clusters (required structure):
    - inputs: LoadImage (x3)
    - output: SaveImage
    - other operations: BatchImagesNode
- paired/multiple required: LoadImage x3
- optional roles: Flux2MaxImageNode, Flux2ProImageNode

## API / Partner Nodes - Image Edit / Flux 2 Klein  (`api_partner_nodes_image_edit__flux_2_klein`)  -  2 workflow(s)  -  source: official
- execution: api (API nodes: ByteDanceSeedreamNode, GeminiImage2Node, GeminiNanoBanana2, GrokImageEditNode, OpenAIGPTImage1)
- when to use: Use to edit an existing image using Flux 2 Klein, Qwen Image.
- example request: "build an image workflow using Flux 2 Klein"
- description: One click generations to test all the leading image editing models. | upload one input image and select multiple editing models. generate side-by-side outputs to directly compare model effects and quality.
- member workflows:
    - templates-all_in_one-image_edit_models
    - templates_all_in_one_image_edit_models.app
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: CLIPLoader (x3), UNETLoader (x3), VAELoader (x3)
    - conditioning: BasicGuider, CFGGuider, CLIPTextEncode (x3), FluxGuidance, TextEncodeQwenImageEditPlus (x2)
    - latent / canvas: VAEEncode (x3)
    - sampling: KSampler, KSamplerSelect (x2), SamplerCustomAdvanced (x2)
    - decoding: VAEDecode (x3)
    - output: SaveImage (x7)
    - other operations: ByteDanceSeedreamNode, CFGNorm, EmptyFlux2LatentImage (x2), Flux2Scheduler (x2), FluxKontextImageScale, FluxKontextMultiReferenceLatentMethod (x2), GeminiImage2Node, GetImageSize (x2), GrokImageEditNode, ImageScaleToTotalPixels (x2), MarkdownNote (x2), ModelSamplingAuraFlow, Note, OpenAIGPTImage1, PrimitiveStringMultiline, RandomNoise (x2), ReferenceLatent (x3)
- paired/multiple required: SaveImage x7, CLIPTextEncode x3, ReferenceLatent x3, CLIPLoader x3, UNETLoader x3, VAEDecode x3, VAEEncode x3, VAELoader x3, EmptyFlux2LatentImage x2, Flux2Scheduler x2, ImageScaleToTotalPixels x2, KSamplerSelect x2, RandomNoise x2, SamplerCustomAdvanced x2, FluxKontextMultiReferenceLatentMethod x2, MarkdownNote x2, TextEncodeQwenImageEditPlus x2
- optional roles: GeminiNanoBanana2
- unresolved nodes: MarkdownNote, Note, Reroute

## API / Partner Nodes - Image Edit / Gemini  (`api_partner_nodes_image_edit__gemini`)  -  2 workflow(s)  -  source: official
- execution: api (API nodes: GeminiNodeV2, OpenRouterLLMNode)
- when to use: Use to produce an image using Gemini.
- example request: "build an image workflow using Gemini"
- description: Experience Google's multimodal AI with Gemini's reasoning capabilities. | Select a model from OpenRouter's curated list (Claude, GPT, Gemini, etc.). Generate a text response with optional media uploads for vision-capable models.
- member workflows:
    - api_google_gemini
    - api_openrouter_llm
- node clusters (required structure):
    - inputs: LoadImage
- optional roles: GeminiNodeV2, MarkdownNote, OpenRouterLLMNode, SaveText
- unresolved nodes: MarkdownNote

## API / Partner Nodes - Image Edit / Magnific  (`api_partner_nodes_image_edit__magnific`)  -  2 workflow(s)  -  source: mixed
- execution: api (API nodes: MagnificImageRelightNode, MagnificImageStyleTransferNode)
- when to use: Use to transfer a style onto an image using Magnific.
- example request: "build an image workflow using Magnific"
- description: API image relighting via Magnific. 1 source image + 1 lighting reference image -> 1 relit image output. Applies the lighting conditions from the reference onto the source image. | Upload a target image and a style reference image. Generate a new image that merges the artistic style of the reference with the structure of your target.
- member workflows:
    - api_magnific_image_relight
    - api_magnific_image_style_transfer
- node clusters (required structure):
    - inputs: LoadImage (x2)
    - output: SaveImage
- paired/multiple required: LoadImage x2
- optional roles: MagnificImageRelightNode, MagnificImageStyleTransferNode

## API / Partner Nodes - Image Edit / Flux Krea  (`api_partner_nodes_image_edit__flux_krea`)  -  1 workflow(s)  -  source: official
- execution: api (API nodes: Krea2ImageNode, Krea2StyleReferenceNode)
- when to use: Use to generate an image using Flux Krea.
- example request: "build an image workflow using Flux Krea"
- description: Upload a style reference image and input a text prompt. Generate an image matching the prompt while applying the aesthetic style from your reference.
- member workflows:
    - api_krea2_style_reference
- node clusters (required structure):
    - inputs: LoadImage (x2)
    - output: SaveImage
    - other operations: Krea2ImageNode, Krea2StyleReferenceNode (x2), MarkdownNote
- paired/multiple required: Krea2StyleReferenceNode x2, LoadImage x2
- unresolved nodes: MarkdownNote

## API / Partner Nodes - Image Edit / Kling  (`api_partner_nodes_image_edit__kling`)  -  1 workflow(s)  -  source: custom
- execution: api (API nodes: KlingOmniProImageNode)
- when to use: Use to generate an image using Kling.
- example request: "build an image workflow using Kling"
- description: Generate an image using Kling. Structurally it applies a sequence of node operations. Boundary inputs: IMAGE; outputs: IMAGE.
- member workflows:
    - api_kling_o3_image
- node clusters (required structure):
    - inputs: LoadImage (x2)
    - output: SaveImage
    - other operations: ImageBatchMulti, KlingOmniProImageNode
- paired/multiple required: LoadImage x2

## API / Partner Nodes - Image Edit / WAN  (`api_partner_nodes_image_edit__wan`)  -  1 workflow(s)  -  source: official
- execution: api (API nodes: GrokImageNode)
- when to use: Use to generate an image using WAN, Z-Image.
- example request: "build an image workflow using WAN"
- description: Upload an image that you want a variation of. The workflow captions the input image, generates with Grok Image, and upscales with Z-image to add realistic textures.
- member workflows:
    - template_rob_realistic_2k_images_quick_variations
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: CLIPLoader, UNETLoader, UpscaleModelLoader, VAELoader
    - conditioning: CLIPTextEncode (x2)
    - latent / canvas: VAEEncode
    - sampling: KSampler
    - decoding: VAEDecode
    - output: SaveImage (x2)
    - other operations: AILab_QwenVL, GrokImageNode, ImageCompare, ImageRemoveAlpha+, ImageScaleBy, ImageScaleToTotalPixels, ImageUpscaleWithModel, ModelSamplingAuraFlow, Note, PreviewAny, StringConcatenate (x2)
- paired/multiple required: CLIPTextEncode x2, SaveImage x2
- unresolved nodes: AILab_QwenVL, ImageRemoveAlpha+, Note

## API / Partner Nodes - Image Edit / Z-Image  (`api_partner_nodes_image_edit__z_image`)  -  1 workflow(s)  -  source: official
- execution: api (API nodes: GrokImageNode)
- when to use: Use to generate an image using Z-Image.
- example request: "build an image workflow using Z-Image"
- description: Upload a reference image, uses Grok to caption and generate variations with a fast 2x upscale for added details.
- member workflows:
    - templates_rob_realistic_2k_images_quick_variations.app
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: CLIPLoader, UNETLoader, UpscaleModelLoader, VAELoader
    - conditioning: CLIPTextEncode (x2)
    - latent / canvas: VAEEncode
    - sampling: KSampler
    - decoding: VAEDecode
    - output: SaveImage (x2)
    - other operations: AILab_QwenVL, GrokImageNode, ImageCompare, ImageRemoveAlpha+, ImageScaleBy, ImageScaleToTotalPixels, ImageUpscaleWithModel, ModelSamplingAuraFlow, Note, PreviewAny, StringConcatenate (x2)
- paired/multiple required: CLIPTextEncode x2, SaveImage x2
- unresolved nodes: AILab_QwenVL, ImageRemoveAlpha+, Note


# Text to Image  (`text_to_image`)  -  73 workflow(s), 12 model(s)

## Text to Image / Generic  (`text_to_image__generic`)  -  23 workflow(s)  -  source: mixed
- execution: local
- when to use: Use to generate an image from a text prompt.
- example request: "build an image workflow"
- description: A lightweight 2B model that generates images from English and Russian prompts with high visual quality. | Chroma1-Radiance works directly with image pixels instead of compressed latents, delivering higher quality images with reduced artifacts and distortion. | Demonstrate how to convert between various built-in data types within a workflow. Input any data value and output its converted form. | Enhance SDXL images using refiner models. | Generate detailed anime-style images with NewBie Exp0.1's Next-DiT architecture. Supports XML structured prompts for better multi-character scenes and attribute control. | Generate high-quality images from text prompts using OmniGen2's unified 7B multimodal model with dual-path architecture. | Generate high-quality images from text prompts using the Boogu Turbo model, a distilled 10B-parameter text-to-image pipeline that produces photorealistic outputs in just 4 steps. The workflow accepts one text prompt and outputs a single 1024x1024 image. Ideal for rapid prototyping of photorealistic concepts, generating marketing visuals, and creating bilingual text-rendered images with strong prompt adherence. | Generate high-quality images from text prompts using the compact 4B-parameter Mage-Flow Turbo model, producing a single image output without any file inputs. This workflow supports native-resolution generation from 512 to 2048 pixels per side at any aspect ratio, including extreme 4:1 dimensions. Ideal for rapid concept visualization, creative asset generation, and low-latency image prototyping on modest hardware. | Generate high-quality images using SDXL. | Generate high-resolution images from text prompts using Mage-Flow, a compact 4B-parameter diffusion model that outputs a single image at native resolutions from 512 to 2048 pixels per side. Ideal for rapid concept visualization, creative asset generation, and research in controlled image synthesis under limited compute budgets. | Generate images from text prompts. | Generate images in a single step using SDXL Turbo. | Generate images quickly with HiDream I1 Fast - Lightweight version with 16 inference steps, ideal for rapid previews on lower-end hardware. | Generate images using SD 3.5. | Generate images with HiDream I1 Dev - Balanced version with 28 inference steps, suitable for medium-range hardware. | Generate images with HiDream I1 Full - Complete version with 50 inference steps for highest quality output. | Input a text prompt and optional negative prompt. Generate a 1024px image using PixelDiT's VAE-free pixel diffusion transformer. | Input a text prompt and select resolution and aspect ratio. Generate a high-quality image using the efficient Lens text-to-image model. | Input a text prompt and select resolution, aspect ratio, and inference steps. Generate a high-quality image using the Lens text-to-image model. | Input a text prompt to generate an image. This workflow uses the Capybara unified model for text-to-image synthesis. | Learn the basics of image generation in ComfyUI - load a model, write prompts, and generate your first image. | Ovis-Image is a 7B text-to-image model specifically optimized for high-quality text rendering in generated images. Designed to operate efficiently under computational constraints, it excels at accurately generating images containing text content. | [Local] OCIO color convert. 1 EXR (or PNG) in -> 1 PNG out. Loads via bepic_imageLoad (OIIO), applies bepic_colorTransform input ACES - ACEScg to output Output - sRGB with clamp on, saves 16-bit PNG via bEpic_imageSave (OIIO). For batches of non-contiguous frames, run one job per file and patch image_path + first_frame; keep auto_version false so saves go straight into the target folder.
- member workflows:
    - Image_capybara_v0_1_text_to_image
    - acescg_to_srgb
    - basic_datatype_conversion
    - default
    - gsl_starter_1_1
    - hidream_i1_dev
    - hidream_i1_fast
    - hidream_i1_full
    - image_boogu_image_0_1_turbo_t2i
    - image_chroma1_radiance_text_to_image
    - image_kandinsky5_t2i
    - image_lens_t2i
    - image_lens_turbo_t2i
    - image_mage_flow_t2i_int8
    - image_mage_flow_turbo_t2i_int8
    - image_newbieimage_exp0_1-t2i
    - image_omnigen2_t2i
    - image_ovis_text_to_image
    - image_pixeldit_t2i
    - sd3.5_simple_example
    - sdxl_refiner_prompt_example
    - sdxl_simple_example
    - sdxlturbo_example
- node clusters (required structure):
    - (none resolved)
- optional roles: Note, MarkdownNote, CLIPTextEncode, CheckpointLoaderSimple, KSamplerAdvanced, BasicScheduler, BetaSamplingScheduler, CFGGuider, CFGNorm, CLIPLoader, ChromaRadianceOptions, ConditioningZeroOut
- unresolved nodes: MarkdownNote, Note, PrimitiveNode

## Text to Image / Qwen Image  (`text_to_image__qwen_image`)  -  11 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate an image using Qwen Image, Anima, Z-Image.
- example request: "build an image workflow using Qwen Image"
- description: A t2v workflows for a style LoRA built on Qwen-Image. Produces images spanning cute anime character design, European bande dessinee, indie risograph prints, storybook watercolor, retro shoujo manga, and graphic novel illustration. | Apply a Qwen Image LoRA to transform any subject into a sour gummy candy-style character. Enter an animal name in the prompt to generate a stylized, edible-looking creature. | Generate 360-degree equirectangular projection images from text descriptions using a rank 128 LoRA on the 20B MMDiT model. | Generate images with exceptional multilingual text rendering and editing capabilities using Qwen-Image's 20B MMDiT model. | Generates images from text prompts using Qwen-Image, Alibaba's 20B MMDiT model with excellent multilingual text rendering. | Generates images from text prompts using Qwen-Image-2512, with enhanced human realism and finer natural detail over the base version. | Generates images from text prompts using Z-Image base weights with Qwen3 text encoder and bundled VAE. | Generates images from text prompts using Z-Image-Turbo defaults with Qwen3 text encoder and VAE. | Input a text prompt to generate detailed, reasoned responses using the Qwen3-4B-Thinking model.  | Qwen-Image 2512 Image generation with 2-steps Turbo LoRA. Input your text prompt to quickly produce a result, though some quality is sacrificed for speed. | Text-to-image model with enhanced human realism, finer natural details for landscapes and animal fur, and improved text rendering with accurate layout and multimodal composition.
- member workflows:
    - image_qwen_Image_2512
    - image_qwen_image
    - image_qwen_image_2512_with_2steps_lora
    - llm_qwen3_text_gen
    - template_qwen_Image_2512_360_lora
    - template_qwen_image_illustration_lora
    - template_sugar_coated_gummy_style_qwen
    - text_to_image
    - text_to_image_qwen_image
    - text_to_image_qwen_image_2512
    - text_to_image_z_image_base
- node clusters (required structure):
    - model loading: CLIPLoader
- optional roles: MarkdownNote, CLIPTextEncode, LoraLoaderModelOnly, ConditioningZeroOut, EmptySD3LatentImage, KSampler, ModelSamplingAuraFlow, Note, SaveImage, TextGenerate, UNETLoader, VAEDecode
- unresolved nodes: MarkdownNote, Note

## Text to Image / Z-Image  (`text_to_image__z_image`)  -  11 workflow(s)  -  source: mixed
- execution: local
- when to use: Use to generate an image using Z-Image.
- example request: "build an image workflow using Z-Image"
- description: Foundation for creative freedom. Diverse aesthetics with exceptional photorealistic quality; ideal for fine-tuning; responsive to negative prompts; high generation diversity. | Generate high-quality, diverse images from text prompts using the Z-Image Int8 model, which leverages an undistilled transformer for precise prompt adherence and broad stylistic coverage. The workflow takes no file inputs and produces 1 image output through a standard text-to-image pipeline. Ideal for professional creative projects, LoRA training and model development, and scenarios requiring robust negative control and high compositional diversity. | Generate images from text prompts using the Z-Image-Turbo model. | Generate photorealistic images using the Z-Image-Turbo int8 model, a distilled 6B-parameter variant optimized for sub-second inference through efficient 8-step sampling. The workflow takes a text prompt as input and outputs a single high-quality image. Ideal for rapid creative iteration, realistic concept art, and production-ready visual prototyping. | Generates images from text prompts using Z-Image-Turbo, Alibaba's distilled 6B DiT model. | Guide on how Switch Nodes work, simple Text Switch and LoRA Switch | Learn how to generate an image, connect nodes, run a workflow and download an image using Z-Image Turbo. | Learn the diffusion basics using Z-Image-Turbo. | Loads and executes a workflow sequentially using prompts from a text list. Iterates through each entry to generate multiple outputs from a single batch operation. | Send multiple prompts simultaneously to generate independent outputs in a single queue. Connect to Blueprint or Partner Nodes for batch processing of any modality. Use for prompt variation comparisons and batch generation. | [Local] text-to-image via Z-Image-Turbo. 1 text input -> 1 image output. High-speed image generation from text prompts.
- member workflows:
    - 01_get_started_text_to_image
    - basic_switch_node
    - gsc_creator_2_1
    - gsc_starter_1
    - image_z_image
    - image_z_image_int8
    - image_z_image_turbo
    - image_z_image_turbo_int8
    - templates_purz_batch_generation
    - text_to_image_z_image_turbo
    - utility_text_lists_select_prompt
- node clusters (required structure):
    - model loading: CLIPLoader, UNETLoader, VAELoader
    - conditioning: CLIPTextEncode
    - sampling: KSampler
    - decoding: VAEDecode
    - other operations: ModelSamplingAuraFlow
- optional roles: MarkdownNote, ConditioningZeroOut, EmptyLatentImage, EmptySD3LatentImage, FL_PromptMulti, FL_PromptSelectorBasic, LoraLoaderModelOnly, ResolutionSelector, SaveImage, SaveImageAdvanced
- unresolved nodes: FL_PromptMulti, FL_PromptSelectorBasic, MarkdownNote

## Text to Image / Flux  (`text_to_image__flux`)  -  6 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate an image from a text prompt using Flux.
- example request: "build an image workflow using Flux"
- description: Chroma - enhanced Flux model with improved image quality and better prompt understanding for stunning text-to-image generation. | Generate high-quality images with Flux Dev full version. Requires larger VRAM and multiple model files, but provides the best prompt following capability and image quality. | Generate images quickly with Flux.1 Schnell full version. Uses Apache2.0 license, requires only 4 steps to generate images while maintaining good image quality. | Generate images using Flux.1 Dev fp8 quantized version. Suitable for devices with limited VRAM, requires only one model file, but image quality is slightly lower than the full version. | Generates images from prompts using FLUX.1 [dev]: a 12B rectified-flow MMDiT with dual CLIP plus T5-XXL text encoders and guidance-distilled sampling for sharp prompt following versus classic DDPM diffusion. | Quickly generate images with Flux.1 Schnell fp8 quantized version. Ideal for low-end hardware, requires only 4 steps to generate images.
- member workflows:
    - flux_dev_checkpoint_example
    - flux_dev_full_text_to_image
    - flux_schnell
    - flux_schnell_full_text_to_image
    - image_chroma_text_to_image
    - text_to_image_flux_1_dev
- node clusters (required structure):
    - latent / canvas: EmptySD3LatentImage
    - decoding: VAEDecode
- optional roles: CLIPTextEncode, Note, BasicScheduler, CFGGuider, CLIPLoader, CLIPTextEncodeFlux, CheckpointLoaderSimple, ConditioningZeroOut, DualCLIPLoader, KSampler, KSamplerSelect, MarkdownNote
- unresolved nodes: MarkdownNote, Note

## Text to Image / Anima  (`text_to_image__anima`)  -  4 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate an image from a text prompt using Anima.
- example request: "build an image workflow using Anima"
- description: Input a text prompt describing an anime or artistic illustration. Generate a non-photorealistic image focused on anime concepts, characters, or styles. | Input a text prompt to generate an anime-style image using the Anima model. Configure settings like steps and CFG scale to control the output. The workflow produces a non-photorealistic illustration based on your description. | This subgraph converts text prompts into non-photorealistic illustrations using a 2-billion-parameter model optimized for anime and artistic styles. It is ideal for generating concept art, character designs, or stylized illustrations where photorealism is not required. The model excels with anime and artistic content but performs poorly on realistic subjects. | This subgraph generates non-photorealistic illustrations from text prompts using a 2-billion-parameter model optimized for anime concepts, characters, and styles. It is ideal for creating artistic images, concept art, or stylized illustrations where photorealism is not required. The model excels with anime and artistic content but performs poorly on realistic subjects.
- member workflows:
    - image_anima_base_v1
    - image_anima_preview
    - text_to_image_anima
    - text_to_image_anima_base_1_0
- node clusters (required structure):
    - model loading: CLIPLoader, UNETLoader, VAELoader
    - conditioning: CLIPTextEncode (x2)
    - latent / canvas: EmptyLatentImage
    - sampling: KSampler
    - decoding: VAEDecode
- paired/multiple required: CLIPTextEncode x2
- optional roles: LoraLoaderModelOnly, MarkdownNote, ResolutionSelector, SaveImage
- unresolved nodes: MarkdownNote

## Text to Image / ERNIE  (`text_to_image__ernie`)  -  4 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate an image from a text prompt using ERNIE.
- example request: "build an image workflow using ERNIE"
- description: Faster ERNIE Image Turbo variant (~8B DiT, distilled for fewer sampling steps): same strengths in Chinese/English on-image text and layout-heavy graphics as the base ERNIE Image lineup, with bundled encoders and VAE. | Generate images from text prompts using the ERNIE-Image model. Input a text description to produce detailed, structured visuals with a broad stylistic range. | Generate images from text prompts using the ERNIE-Image turbo model. Input a text description and receive a high-quality image with precise text rendering and structured layouts. | Generates images from text prompts using Baidu's open ERNIE Image (~8B DiT): bilingual in-image typography and layouts (posters, infographics, multi-panel compositions) alongside general scenes, with bundled encoders and VAE.
- member workflows:
    - image_ernie_image
    - image_ernie_image_turbo
    - text_to_image_ernie_image
    - text_to_image_ernie_image_turbo
- node clusters (required structure):
    - model loading: CLIPLoader (x2), UNETLoader, VAELoader
    - conditioning: CLIPTextEncode
    - sampling: KSampler
    - decoding: VAEDecode
    - other operations: ComfySwitchNode, EmptyFlux2LatentImage, PreviewAny (x3), PrimitiveBoolean, PrimitiveStringMultiline, StringReplace (x3), TextGenerate
- paired/multiple required: CLIPLoader x2
- optional roles: MarkdownNote, ConditioningZeroOut, SaveImage
- unresolved nodes: MarkdownNote

## Text to Image / Flux Krea  (`text_to_image__flux_krea`)  -  4 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate an image from a text prompt using Flux Krea.
- example request: "build an image workflow using Flux Krea"
- description: A fine-tuned FLUX model pushing photorealism to the max | FLUX.1 Krea [dev] (Black Forest Labs × Krea): open-weight 12B rectified-flow text-to-image drop-in alongside FLUX.1 [dev], tuned away from overcooked saturation toward more natural diversity in people, realism, and style while keeping ecosystem compatibility. | Generate images from text prompts using Krea 2, a foundation model built for aesthetic quality and creative control. It focuses on rendering expressive and artistic styles. Ideal for concept art exploration, visual brainstorming, and creating stylized imagery for design projects.
 | Generate images with the Krea-2 Turbo distilled text-to-image model using the high-performance Int8 Convrot format, which delivers better quality than FP8 while generally running faster across most GPUs. This workflow accepts no file inputs and produces a single image output, with optional style LoRA support for creative customization. Ideal for rapid concept art iteration, batch asset generation for games or marketing, and exploring the speed-quality sweet spot of the Convrot Int8 quantization.
- member workflows:
    - flux1_krea_dev
    - image_krea2_turbo_t2i
    - image_krea2_turbo_t2i_int8
    - text_to_image_flux_1_krea_dev
- node clusters (required structure):
    - model loading: UNETLoader, VAELoader
    - conditioning: CLIPTextEncode, ConditioningZeroOut
    - sampling: KSampler
    - decoding: VAEDecode
- optional roles: MarkdownNote, CLIPLoader, DualCLIPLoader, EmptyLatentImage, EmptySD3LatentImage, LoraLoaderModelOnly, ResolutionSelector, SaveImage, TextGenerate
- unresolved nodes: MarkdownNote

## Text to Image / Ideogram  (`text_to_image__ideogram`)  -  3 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate an image from a text prompt using Ideogram.
- example request: "build an image workflow using Ideogram"
- description: Generate images from text prompts using the Ideogram v4 model, a state-of-the-art open-weight text-to-image system with exceptional text rendering and layout control. No file inputs are required, producing 1 image output. Ideal for creating marketing visuals, generating design mockups with precise typography, and producing high-resolution artwork with controlled compositions. | Input a text prompt or structured JSON description. Generate an image with precise layout, color, and style control using Ideogram 4.0. | This subgraph generates images using Ideogram v4, accepting plain text or structured JSON prompts for precise layout and style control. It suits detailed illustrations, concept art, or marketing visuals needing predictable composition and color palettes. The model uses flow-matching with asymmetric guidance, so no negative prompt is needed, but JSON prompts yield the best results.
- member workflows:
    - image_ideogram4_t2i
    - image_ideogram4_t2i_int8
    - text_to_image_ideogram_v4
- node clusters (required structure):
    - model loading: CLIPLoader, UNETLoader (x2), VAELoader
    - conditioning: CLIPTextEncode, ConditioningZeroOut, DualModelGuider
    - sampling: KSamplerSelect, SamplerCustomAdvanced
    - decoding: VAEDecode
    - other operations: CFGOverride, ComfyMathExpression (x2), ComfyNumberConvert (x3), CustomCombo, EmptyFlux2LatentImage, Ideogram4Scheduler, JsonExtractString (x4), PrimitiveInt (x2), RandomNoise, StringReplace
- paired/multiple required: UNETLoader x2
- optional roles: MarkdownNote, ResolutionSelector, SaveImage
- unresolved nodes: MarkdownNote

## Text to Image / Flux 2  (`text_to_image__flux_2`)  -  2 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate an image from a text prompt using Flux 2.
- example request: "build an image workflow using Flux 2"
- description: Generates images from prompts using FLUX.2 [dev]: a newer 32B rectified-flow stack with distilled guidance plus a stronger long-context multimodal encoder for complex scenes, sharper typography/UI text, anatomy, lighting, and high-resolution latent decoding. | Text-to-image with enhanced lighting, materials, and realistic details.
- member workflows:
    - image_flux2_text_to_image
    - text_to_image_flux_2_dev
- node clusters (required structure):
    - model loading: CLIPLoader, LoraLoaderModelOnly, UNETLoader, VAELoader
    - conditioning: BasicGuider, CLIPTextEncode, FluxGuidance
    - sampling: KSamplerSelect, SamplerCustomAdvanced
    - decoding: VAEDecode
    - other operations: ComfySwitchNode (x2), EmptyFlux2LatentImage, Flux2Scheduler, PrimitiveBoolean, PrimitiveInt (x2), RandomNoise
- optional roles: MarkdownNote, SaveImage
- unresolved nodes: MarkdownNote

## Text to Image / Flux 2 Klein  (`text_to_image__flux_2_klein`)  -  2 workflow(s)  -  source: mixed
- execution: local
- when to use: Use to generate an image from a text prompt using Flux 2 Klein.
- example request: "build an image workflow using Flux 2 Klein"
- description: BFL distilled model. Outstanding quality at sub-second speed. Great for real-time generation while retaining quality. Marketing launch will focus on this model.
- member workflows:
    - image_flux2_klein_text_to_image
    - image_flux2_text_to_image_9b
- node clusters (required structure):
    - model loading: CLIPLoader, UNETLoader, VAELoader
    - conditioning: CFGGuider, CLIPTextEncode (x2)
    - sampling: KSamplerSelect, SamplerCustomAdvanced
    - decoding: VAEDecode
    - output: SaveImage
    - other operations: EmptyFlux2LatentImage, Flux2Scheduler, PrimitiveInt (x2), RandomNoise
- paired/multiple required: CLIPTextEncode x2
- optional roles: MarkdownNote
- unresolved nodes: MarkdownNote

## Text to Image / Lumina  (`text_to_image__lumina`)  -  2 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate an image from a text prompt using Lumina.
- example request: "build an image workflow using Lumina"
- description: Generates images from text prompts using NetaYume Lumina, fine-tuned from Neta Lumina for anime-style and illustration generation. | High-quality anime-style image generation with enhanced character understanding and detailed textures. Fine-tuned from Neta Lumina on Danbooru dataset.
- member workflows:
    - image_netayume_lumina_t2i
    - text_to_image_netayume_lumina
- node clusters (required structure):
    - model loading: CheckpointLoaderSimple
    - conditioning: CLIPTextEncode (x2)
    - latent / canvas: EmptySD3LatentImage
    - sampling: KSampler
    - decoding: VAEDecode
    - other operations: MarkdownNote, ModelSamplingAuraFlow, PrimitiveStringMultiline (x4), StringConcatenate (x2)
- paired/multiple required: CLIPTextEncode x2
- optional roles: SaveImage
- unresolved nodes: MarkdownNote

## Text to Image / LongCat  (`text_to_image__longcat`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate an image from a text prompt using LongCat.
- example request: "build an image workflow using LongCat"
- description: Generate an image from a text prompt. Input your desired scene description in English or Chinese. Output a photorealistic image with accurate text rendering.
- member workflows:
    - image_longcat_text_to_image
- node clusters (required structure):
    - model loading: CLIPLoader, UNETLoader, VAELoader
    - conditioning: CLIPTextEncode (x2), FluxGuidance (x2)
    - latent / canvas: EmptySD3LatentImage
    - sampling: KSampler
    - decoding: VAEDecode
    - output: SaveImage
    - other operations: CFGNorm, MarkdownNote, ResolutionSelector
- paired/multiple required: CLIPTextEncode x2, FluxGuidance x2
- unresolved nodes: MarkdownNote


# Image Edit  (`image_edit`)  -  63 workflow(s), 15 model(s)

## Image Edit / Qwen Image  (`image_edit__qwen_image`)  -  23 workflow(s)  -  source: mixed
- execution: local
- when to use: Use to edit an existing image using Qwen Image.
- example request: "build an image workflow using Qwen Image"
- description: Advanced image editing with multi-image support, improved consistency, and ControlNet integration. | Decompose an image into editable RGBA layers for high-fidelity recolor, replace, resize, and reposition workflows using Qwen-Image-Layered. | Decomposes an image into variable-resolution RGBA layers for independent editing using Qwen-Image-Layered. | Edit images with Qwen Image Edit 2511 Int8, using a quantized model for faster inference while maintaining high quality. Input one image and receive one edited output. Ideal for character-consistent portrait editing, multi-person group photo fusion, and industrial design modifications. | Edit images with precise bilingual text editing and dual semantic/appearance editing capabilities using Qwen-Image-Edit's 20B MMDiT model. | Edit your images with Qwen-Image-Edit, the latest OSS model | Edits images from text instructions using Qwen-Image-Edit-2509 with optional Lightning LoRA for few-step sampling. | Edits images via text instructions using Qwen-Image-Edit-2511 with improved character consistency and integrated LoRA. | Generate camera angle variations of your input with an easy to use 3D camera angle node. | Image Edit blueprint | Input an illustration and generate a hyper realistic version using Qwen Image Edit 2509. | Input an illustration and generate a realistic version using Qwen Image Edit 2509 with Anything2Real LoRA. | Learn how to relight a product, enter a subgraph, unbypass a node using Qwen Image Edit. | Local image editing via QWEN-Image-Edit-2511-Lightning. Up to 3 images (including optional depth/canny control inputs) -> 1 edited image output. Supports text-guided edits with optional structural control. | Prompt an environment and generate a equirectangular hdr image to use as skybox or lookdev in game development. | Relight images using Qwen-Image-Edit with LoRA support. | Replace materials in objects (e.g., furniture) by combining reference images with Qwen-Image-Edit-2511. | Upload a composited image of your product, draw a mask in the mask editor and relight your product into the scene. | Upload a portrait of your character and a reference lighting image. Generate an image with reference lighting applied and character consistency. | Upload an image and specify a subject. Generate an inflated version of that subject using the INFL8 LoRA for Qwen Image Edit. | Upload an image of your scene and generate multiple views of your input scene with 1 click. | Upload your target image and a reference lighting image. Relights your target image.

 | Upload your target image and use the trigger phrase "action the [thing]" (e.g., "action the scene"). Generate a toy or action figure version of your subject with articulated joints, plastic materials, and painted details.
- member workflows:
    - 02_qwen_Image_edit_subgraphed
    - gsl_starter_1_3
    - image-qwen_image_edit_2511_lora_inflation
    - image_edit
    - image_edit_qwen_2509
    - image_edit_qwen_2511
    - image_qwen_image_edit
    - image_qwen_image_edit_2509
    - image_qwen_image_edit_2509_relight
    - image_qwen_image_edit_2511
    - image_qwen_image_edit_2511_int8
    - image_qwen_image_layered
    - image_to_layers_qwen_image_layered
    - qwen2511_imageEdit
    - template_qwen_image_edit_2511_systms_action
    - templates-1_click_multiple_scene_angles-v1.0
    - templates-image_to_real
    - templates-portrait_light_migration
    - templates-qwen_image_edit-crop_and_stitch-fusion
    - templates-qwen_multiangle.app
    - templates_rob_image_to_real.app
    - templates_rob_portrait_light_migration.app
    - templates_text_prompt_to_360hdr.app
- node clusters (required structure):
    - model loading: CLIPLoader, UNETLoader, VAELoader
    - decoding: VAEDecode
- optional roles: TextEncodeQwenImageEditPlus, CFGNorm, ImageScaleToTotalPixels, KSampler, ModelSamplingAuraFlow, PreviewImage, SaveImage, VAEEncode, CLIPTextEncode, MarkdownNote, ReferenceLatent, EmptyQwenImageLayeredLatentImage
- unresolved nodes: Image Load, LayerUtility: If , MarkdownNote, Note, Reroute, SeedVR2LoadDiTModel, SeedVR2LoadVAEModel, SeedVR2VideoUpscaler, SimpleMath+

## Image Edit / Generic  (`image_edit__generic`)  -  12 workflow(s)  -  source: official
- execution: local
- when to use: Use to edit an existing image.
- example request: "build an image workflow"
- description: Edit images by following natural language instructions with JoyAI-Image-Edit, which leverages multimodal understanding for precise, spatially aware modifications. This workflow takes one reference image and produces one edited image output plus a side-by-side comparison view. Ideal for instruction-guided retouching, region-specific object replacement, and complex scene adjustments requiring relational grounding. | Edit images by following natural language instructions with Mage-Flow-Edit, an instruction-based model that handles background replacement, style changes, localized edits, and restoration using up to three reference images. The workflow takes one input image and produces one edited output plus a side-by-side comparison view. Ideal for creative photo retouching, product image styling, and restoring old or damaged photos. | Edit images using Boogu's instruction-driven model, taking one input image and generating an edited output alongside a side-by-side comparison view.  | Edit images using a reference photo and text instructions with the Mage-Flow-Edit Turbo model, a distilled 4B-parameter model that produces results in just 4 steps. It takes 1-3 reference images and a text prompt as input, then outputs an edited image matching your instructions. Ideal for quick style transfers, background replacements, and interactive photo editing sessions. | Edit images with HiDream E1 - Professional natural language image editing model. | Edit images with HiDream E1.1-superior image quality and editing accuracy compared to HiDream-E1-Full. | Edit images with natural language instructions using OmniGen2's advanced image editing capabilities and text rendering support. | Generate images by transferring concepts from reference images using SDXL Revision. | Image editing powered by video models' dynamic understanding, creating physically plausible results while preserving character and style consistency. | Input a text prompt and optional reference images. Generate a high-resolution image (up to 2048x2048) with support for text-to-image, image editing, and subject-driven personalization. | Input a text prompt and optionally upload reference images. Generate a high-resolution image up to 2048x2048 with text-to-image, editing, or subject-driven personalization. | Upload an image or video and input a text instruction. Generate an edited output using the Capybara model for tasks like style changes, object replacement, or time-of-day adjustments.
- member workflows:
    - Image_capybara_v0_1_image_edit
    - hidream_e1_1
    - hidream_e1_full
    - image_boogu_image_0_1_edit
    - image_chrono_edit_14B
    - image_hidream_o1
    - image_hidream_o1_dev
    - image_joyai_image_edit
    - image_mage_flow_edit_int8
    - image_mage_flow_edit_turbo_int8
    - image_omnigen2_image_edit
    - sdxl_revision_text_prompts
- node clusters (required structure):
    - inputs: LoadImage
    - decoding: VAEDecode
    - other operations: MarkdownNote
- optional roles: ReferenceLatent, CLIPTextEncode, CLIPVisionEncode, EmptyHiDreamO1LatentImage, ImageScaleToTotalPixels, RegexReplace, TextEncodeJoyImageEdit, VAEEncode, unCLIPConditioning, BasicScheduler, CFGGuider, CFGNorm
- unresolved nodes: MarkdownNote, Note, PrimitiveNode, Reroute

## Image Edit / Flux 2 Klein  (`image_edit__flux_2_klein`)  -  7 workflow(s)  -  source: mixed
- execution: local
- when to use: Use to edit an existing image using Flux 2 Klein.
- example request: "build an image workflow using Flux 2 Klein"
- description: A smaller foundation model with exceptional quality-to-size ratio. Ideal for local deployment, fine-tuning on limited hardware, and efficient generation and editing workflows. | BFL undistilled foundation model. Maximum flexibility and control. Great for fine-tuning. | Edits an input image via text instructions using FLUX.2 [klein] 4B. | The fastest variant in the Klein family. Built for interactive applications, real-time previews, and latency-critical production use cases. | Upload reference images and a text prompt. Generate multiple edited images using cached image data for faster processing. | Use the FLUX.2 Klein 9B model to intelligently extend and expand image content. Input an image to generate seamless outpainting and extended compositions. | [Local] image editing via Flux. 1 image input -> 1 image output. Performs image editing using the Flux 2 Klein distilled model.
- member workflows:
    - image_edit_flux_2_klein_4b
    - image_flux2_klein_9b_kv_image_edit
    - image_flux2_klein_image_edit_4b_base
    - image_flux2_klein_image_edit_4b_distilled
    - image_flux2_klein_image_edit_9b_base
    - image_flux2_klein_image_edit_9b_distilled
    - templates_doc_workbox_klein_9b_image_extend
- node clusters (required structure):
    - model loading: CLIPLoader, UNETLoader, VAELoader
    - conditioning: CFGGuider, CLIPTextEncode
    - latent / canvas: VAEEncode
    - sampling: KSamplerSelect, SamplerCustomAdvanced
    - decoding: VAEDecode
    - other operations: EmptyFlux2LatentImage, Flux2Scheduler, GetImageSize, ImageScaleToTotalPixels, RandomNoise, ReferenceLatent (x2)
- paired/multiple required: ReferenceLatent x2
- optional roles: ConditioningZeroOut, LoadImage, MarkdownNote, SaveImage, ColorMatch, DrawMaskOnImage, FluxKVCache, ImageCompare, ImagePadForOutpaint
- unresolved nodes: MarkdownNote

## Image Edit / Flux  (`image_edit__flux`)  -  5 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate an image using Flux.
- example request: "build an image workflow using Flux"
- description: Generate images by transferring style from reference images using Flux.1 Redux. | Generate images guided by depth information using Flux.1 LoRA. | Smart image editing that keeps characters consistent, edits specific parts without affecting others, and preserves original styles. | Supports various tasks such as image inpainting, outpainting, and object removal by bytedance-research team | Use reference images to control both style and subject - keep your character's face while changing artistic style, or apply artistic styles to new scenes
- member workflows:
    - flux1_dev_uso_reference_image_gen
    - flux_depth_lora_example
    - flux_kontext_dev_basic
    - flux_redux_model_example
    - image_flux.1_fill_dev_OneReward
- node clusters (required structure):
    - inputs: LoadImage
    - conditioning: CLIPTextEncode, FluxGuidance
    - decoding: VAEDecode
    - output: SaveImage
    - other operations: MarkdownNote (x2)
- paired/multiple required: MarkdownNote x2
- optional roles: CLIPVisionEncode, USOStyleReference, CLIPVisionLoader, CheckpointLoaderSimple, ConditioningZeroOut, DifferentialDiffusion, DualCLIPLoader, InpaintModelConditioning, KSampler, LoraLoaderModelOnly, ModelPatchLoader, Note
- unresolved nodes: MarkdownNote, Note, PrimitiveNode

## Image Edit / Flux 2  (`image_edit__flux_2`)  -  3 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate an image using Flux 2.
- example request: "build an image workflow using Flux 2"
- description: Create product mockups by applying design patterns to packaging, mugs, and other products using multi-reference consistency. | Edits an image from text instructions using Flux.2 [dev], with guidance, schedulers, and optional Turbo LoRAs. | Generate photorealistic images with multi-reference consistency and professional text rendering.
- member workflows:
    - image_edit_flux_2_dev
    - image_flux2
    - image_flux2_fp8
- node clusters (required structure):
    - model loading: CLIPLoader, LoraLoaderModelOnly, UNETLoader, VAELoader
    - conditioning: BasicGuider, CLIPTextEncode, FluxGuidance
    - latent / canvas: VAEEncode
    - sampling: KSamplerSelect, SamplerCustomAdvanced
    - decoding: VAEDecode
    - other operations: ComfySwitchNode (x2), EmptyFlux2LatentImage, Flux2Scheduler, GetImageSize, PrimitiveBoolean, PrimitiveInt (x2), RandomNoise, ReferenceLatent
- optional roles: ImageScaleToTotalPixels, LoadImage, MarkdownNote, SaveImage
- unresolved nodes: MarkdownNote

## Image Edit / FireRed  (`image_edit__firered`)  -  2 workflow(s)  -  source: official
- execution: local
- when to use: Use to edit an existing image using FireRed.
- example request: "build an image workflow using FireRed"
- description: Edits images via text instructions using FireRed Image Edit 1.1, a diffusion-based instruction-following editing model. | Upload an image and a text prompt to edit it. Generate a modified image with enhanced identity consistency, multi-element fusion, or professional photo restoration.
- member workflows:
    - image_edit_firered_image_edit_1_1
    - image_firered_image_edit1_1
- node clusters (required structure):
    - model loading: CLIPLoader, LoraLoaderModelOnly, UNETLoader, VAELoader
    - conditioning: TextEncodeQwenImageEditPlus (x2)
    - latent / canvas: VAEEncode
    - sampling: KSampler
    - decoding: VAEDecode
    - other operations: CFGNorm, ComfySwitchNode (x3), ModelSamplingAuraFlow, PrimitiveBoolean, PrimitiveFloat (x2), PrimitiveInt (x2), ResizeImageMaskNode
- paired/multiple required: TextEncodeQwenImageEditPlus x2
- optional roles: LoadImage, MarkdownNote, SaveImage
- unresolved nodes: MarkdownNote

## Image Edit / LongCat  (`image_edit__longcat`)  -  2 workflow(s)  -  source: official
- execution: local
- when to use: Use to edit an existing image using LongCat.
- example request: "build an image workflow using LongCat"
- description: Edit images using the LongCat-Image-Edit model. Supports bilingual instructions for global, local, text, and reference-guided editing while preserving visual consistency. | Edits images via text instructions using LongCat Image Edit, an instruction-following image editing diffusion model.
- member workflows:
    - image_edit_longcat_image_edit
    - image_longcat_image_edit
- node clusters (required structure):
    - model loading: CLIPLoader, UNETLoader, VAELoader
    - conditioning: FluxGuidance (x2), TextEncodeQwenImageEdit (x2)
    - latent / canvas: VAEEncode
    - sampling: KSampler
    - decoding: VAEDecode
    - other operations: FluxKontextMultiReferenceLatentMethod (x2), ImageScaleToTotalPixels
- paired/multiple required: FluxGuidance x2, FluxKontextMultiReferenceLatentMethod x2, TextEncodeQwenImageEdit x2
- optional roles: MarkdownNote, ImageCompare, LoadImage, SaveImage
- unresolved nodes: MarkdownNote

## Image Edit / Z-Image  (`image_edit__z_image`)  -  2 workflow(s)  -  source: mixed
- execution: local
- when to use: Use to generate an image using Z-Image.
- example request: "build an image workflow using Z-Image"
- description: Learn how to upscale an image and auto-generate a prompt using Z Image Turbo. | [Local] image-to-image via Z-Image-Turbo. 1 image input + text prompt -> 1 image output. Uses TextEncodeZImageOmni to feed the input image directly into conditioning for high-fidelity i2i edits. Denoise defaults to 0.75 - lower for more structure preservation, higher for more creative freedom.
- member workflows:
    - gsc_creator_2_3
    - image_z_image_turbo_i2i
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: CLIPLoader, UNETLoader, VAELoader
    - conditioning: CLIPTextEncode
    - latent / canvas: VAEEncode
    - sampling: KSampler
    - decoding: VAEDecode
    - output: SaveImage
    - other operations: ModelSamplingAuraFlow
- optional roles: MarkdownNote, ConditioningZeroOut, DownloadAndLoadFlorence2Model, EmptySD3LatentImage, Florence2Run, ImageCompare, ImageScaleBy, ImageScaleToMaxDimension, ImageUpscaleWithModel, TextEncodeZImageOmni, UpscaleModelLoader
- unresolved nodes: DownloadAndLoadFlorence2Model, Florence2Run, MarkdownNote

## Image Edit / Bernini  (`image_edit__bernini`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to edit an existing image using Bernini.
- example request: "build an image workflow using Bernini"
- description: Edits a single image using a text prompt, leveraging Bernini-R's latent semantic planning for changes like object addition, removal, or style transfer. Ideal for creative edits requiring precise semantic understanding, such as adding a snowman to a scene or altering an object's appearance.
- member workflows:
    - image_edit_bernini_r
- node clusters (required structure):
    - model loading: CLIPLoader, LoraLoaderModelOnly (x2), UNETLoader (x2), VAELoader
    - conditioning: BasicScheduler, BerniniConditioning, CLIPTextEncode (x2), SplitSigmas
    - sampling: KSamplerSelect, SamplerCustom (x2)
    - decoding: VAEDecode
    - other operations: ComfySwitchNode (x5), CustomCombo, MarkdownNote, PreviewAny, PrimitiveBoolean, PrimitiveFloat (x2), PrimitiveInt (x5), PrimitiveStringMultiline, RegexExtract, StringConcatenate, StringReplace
- paired/multiple required: CLIPTextEncode x2, LoraLoaderModelOnly x2, SamplerCustom x2, UNETLoader x2
- unresolved nodes: MarkdownNote

## Image Edit / Flux Krea  (`image_edit__flux_krea`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate an image using Flux Krea.
- example request: "build an image workflow using Flux Krea"
- description: Generate images with the Krea-2 Turbo model while referencing the style of 1-2 uploaded images, using the high-performance Int8 Convrot format for faster, higher-quality inference. This workflow accepts up to two reference image inputs and produces a single stylized output, with optional LoRA support for further creative control. Ideal for matching a specific artistic style in concept art, producing consistent brand visuals, and exploring rapid style transfer for iterative design.
- member workflows:
    - image_krea2_turbo_int8_image_style_reference
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: CLIPLoader, LoraLoaderModelOnly, UNETLoader, VAELoader
    - conditioning: BasicScheduler, CFGGuider, ConditioningZeroOut, TextEncodeQwenImageEditPlus
    - latent / canvas: EmptyLatentImage (x2)
    - sampling: KSamplerSelect, SamplerCustomAdvanced
    - decoding: VAEDecode
    - output: SaveImage
    - other operations: ComfySwitchNode, FluxKontextMultiReferenceLatentMethod, GetImageSize, MarkdownNote, ModelSamplingFlux, PreviewAny, PrimitiveBoolean, PrimitiveStringMultiline (x2), RandomNoise, ResolutionSelector, StringConcatenate, TextGenerate
- paired/multiple required: EmptyLatentImage x2
- unresolved nodes: MarkdownNote

## Image Edit / Lotus  (`image_edit__lotus`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate an image using Lotus.
- example request: "build an image workflow using Lotus"
- description: Run Lotus Depth in ComfyUI for zero-shot, efficient monocular depth estimation with high detail retention.
- member workflows:
    - image_lotus_depth_v1_1
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: UNETLoader, VAELoader
    - conditioning: BasicGuider, BasicScheduler, LotusConditioning
    - latent / canvas: VAEEncode
    - sampling: KSamplerSelect, SamplerCustomAdvanced
    - decoding: VAEDecode
    - output: SaveImage
    - other operations: DisableNoise, ImageInvert, MarkdownNote, SetFirstSigma
- unresolved nodes: MarkdownNote

## Image Edit / SAM3  (`image_edit__sam3`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to segment an image using SAM3.
- example request: "build an image workflow using SAM3"
- description: Use the SAM3 model to segment the main subject or content from a photo or image, isolating specific objects or regions. Input an image and receive a segmented mask output.
- member workflows:
    - utility_image_segment_sam3
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: CheckpointLoaderSimple
    - conditioning: CLIPTextEncode
    - output: PreviewImage
    - other operations: JoinImageWithAlpha, MarkdownNote (x2), MaskPreview, SAM3_Detect
- paired/multiple required: MarkdownNote x2
- unresolved nodes: MarkdownNote

## Image Edit / SDPose  (`image_edit__sdpose`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to estimate a pose map using SDPose.
- example request: "build an image workflow using SDPose"
- description: Upload an image to detect human poses. Supports detection for both single individuals and multiple people within the same scene.
- member workflows:
    - utility_sdpose_multi_person
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: CheckpointLoaderSimple, UNETLoader
    - output: PreviewImage, SaveImage
    - other operations: DrawBBoxes, ImageBlend, MarkdownNote (x2), PrimitiveInt, RTDETR_detect, ResizeImageMaskNode (x2), SDPoseDrawKeypoints, SDPoseKeypointExtractor
- paired/multiple required: MarkdownNote x2, ResizeImageMaskNode x2
- unresolved nodes: MarkdownNote

## Image Edit / WAN  (`image_edit__wan`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to edit an existing image using WAN.
- example request: "build an image workflow using WAN"
- description: Edit images with the Boogu Image Edit model, now optimized with convrot int8 quantization for faster inference and better quality than fp8. This workflow takes 1 input image and produces 1 edited image output. Ideal for quick image edits, batch processing with improved performance, and users wanting to leverage the convrot int8 format's speed and quality advantages.
- member workflows:
    - image_boogu_image_0_1_edit_int8
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: CLIPLoader, UNETLoader, VAELoader
    - conditioning: BasicScheduler, TextEncodeBooguEdit
    - latent / canvas: EmptyLatentImage
    - sampling: KSamplerSelect, SamplerCustom
    - decoding: VAEDecode
    - output: SaveImageAdvanced
    - other operations: GetImageSize, ImageCompare, MarkdownNote (x3), ModelSamplingAuraFlow, ResizeImageMaskNode
- paired/multiple required: MarkdownNote x3
- unresolved nodes: MarkdownNote

## Image Edit / WAN 2.2  (`image_edit__wan_2_2`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate a video using WAN 2.2.
- example request: "build a video workflow using WAN 2.2"
- description: Learn how to load images,  generate a video and how to find a node using Wan 2.2
- member workflows:
    - gsl_starter_1_2
- node clusters (required structure):
    - inputs: LoadImage (x4)
    - model loading: CLIPLoader (x4), LoraLoaderModelOnly (x8), UNETLoader (x8), VAELoader (x4)
    - conditioning: CLIPTextEncode (x8)
    - sampling: KSamplerAdvanced (x8)
    - decoding: VAEDecode (x4)
    - other operations: BatchImagesNode, MarkdownNote (x5), ModelSamplingSD3 (x8), Note (x8), WanFirstLastFrameToVideo (x4)
- paired/multiple required: CLIPTextEncode x8, KSamplerAdvanced x8, LoraLoaderModelOnly x8, ModelSamplingSD3 x8, Note x8, UNETLoader x8, MarkdownNote x5, CLIPLoader x4, LoadImage x4, VAEDecode x4, VAELoader x4, WanFirstLastFrameToVideo x4
- unresolved nodes: MarkdownNote, Note


# API / Partner Nodes - Text to Video  (`api_partner_nodes_text_to_video`)  -  52 workflow(s), 8 model(s)

## API / Partner Nodes - Text to Video / Generic  (`api_partner_nodes_text_to_video__generic`)  -  36 workflow(s)  -  source: mixed
- execution: api (API nodes: ByteDance2ReferenceNode, ByteDance2TextToVideoNode, ByteDanceCreateImageAsset, ByteDanceCreateVideoAsset, ByteDanceSeedreamNode, ByteDanceTextToVideoNode, GeminiImage2Node, GeminiNanoBanana2V2, GeminiNode, GrokVideoNode, GrokVideoReferenceNode, HappyHorseReferenceVideoApi, HappyHorseTextToVideoApi, HeyGenAvatarVideoNode, HeyGenCreateAvatarNode, KlingStartEndFrameNode, KlingVideoNode, LumaConceptsNode, LumaRay32ExtendVideoNode, LumaRay32TextToVideoNode, LumaVideoNode, MinimaxHailuo03ReferenceNode, MinimaxHailuo03TextToVideoNode, MinimaxHailuoVideoNode, MinimaxTextToVideoNode, OpenAIGPTImageNodeV2, PixverseTemplateNode, PixverseTextToVideoNode, SyncTalkingImageNode, Vidu2ReferenceVideoNode, Vidu2TextToVideoNode, Vidu3TextToVideoNode, ViduReferenceVideoNode, ViduStartEndToVideoNode, ViduTextToVideoNode)
- when to use: Use to generate a video.
- example request: "build a video workflow"
- description: API text-to-video via Seedance 2.0 (ByteDance). Text prompt only -> 1 video output. Generates high-quality video from a text description using the Seedance 2.0 model. | Create an AI avatar video from a text prompt or uploaded image using HeyGen's avatar generation technology, outputting a single talking-head video. You can save the avatar ID for reuse in future videos. Ideal for personalized digital presenters, social media content creation, and multilingual video production without recording talent. | Create complete audio-visual stories from text with synchronized voices, music, and sound effects. | Create smooth video transitions between defined start and end frames with natural motion interpolation and consistent visual quality. | Generate a reference-based video from a single input image using Seedance 2.0, producing native 4K output with 10-bit color depth and clean fine detail retention. The workflow takes 1 image and outputs 1 video. Ideal for high-resolution motion graphics, cinematic VFX shots requiring downstream grading, and professional video production where 4K finishing is essential. | Generate a talking-head video from a single face photo and an audio clip, with lips and lower-face motion precisely synchronized to the speech. This process outputs one video from one image and one audio input, keeping hands, products, and background completely unchanged. Ideal for product demos, e-commerce introductions, and marketing videos where a static product-holding photo is paired with a voiceover. | Generate a video with synchronized audio from a text prompt using HappyHorse 1.1, producing a single video output with dialogue, sound effects, and music baked in. Ideal for short episodic series, e-commerce commercials, and game cutscenes. | Generate an 8-panel storyboard from a simple text prompt, then use that storyboard as the foundation for Seedance 2.0. The storyboard provides a visual blueprint for the sequence, allowing you to guide the video with more control over the action, camera angles, composition, and overall storytelling. | Generate cinematic video from two reference images using Seedance 2.0 Mini, producing a single video output with AI-driven camera motion and consistent character generation. Ideal for storytelling, branded content, and short film creation where shot composition and visual continuity are essential. | Generate cinematic videos from reference images and text prompts. Preserve subject identity and composition while adding expressive motion with synchronized audio. Control camera movement and lighting through detailed prompts. | Generate cinematic videos from text prompts with Dreamina's Seedance 2.0 Mini, supporting AI camera controls and consistent character generation across scenes. This workflow takes only prompt input and produces 1 video output. Ideal for AI filmmaking, branded content creation, and multi-shot storytelling projects. | Generate cinematic videos from text prompts with synchronized audio, controlled camera motion, and stable visuals. Input text descriptions to output high-quality video sequences. | Generate cinematic-quality videos from text prompts using Luma Ray 3.2, with optional video extension by providing a generation ID from a previous run. Ideal for creating short film sequences, marketing content, and iterative video refinement. | Generate high-quality 1080p videos from text prompts with Vidu Q2 model | Generate high-quality 1080p videos from text prompts with adjustable movement amplitude and duration control using Vidu's advanced AI model. | Generate high-quality videos directly from text prompts using ByteDance's Seedance model. Supports multiple resolutions and aspect ratios with natural motion and cinematic quality. | Generate high-quality videos directly from text prompts. Explore MiniMax's advanced AI capabilities to create diverse visual narratives with professional CGI effects and stylistic elements to bring your descriptions to life. | Generate high-quality videos from text prompts with optional first-frame control using MiniMax Hailuo-02 model. Supports multiple resolutions (768P/1080P) and durations (6/10s) with intelligent prompt optimization. | Generate high-quality, realistic videos from text prompts with fluid motion and rich detail. Input text descriptions to produce dynamic videos with accurate semantic comprehension. | Generate video directly from text using the MiniMax H3 model, producing a 5-15 second clip with native stereo audio. Ideal for rapid concept visualization, short-form social media content, and pre-visualization for film or advertising projects. | Generate video from a reference image or set of multimodal inputs using MiniMax H3, which interprets text, images, video, and audio together to produce coherent 5-15 second clips with native stereo audio. Input up to 2 images for first/last frame control, or up to 9 images, 3 video clips, and 3 audio clips in Omni Reference mode, and output a single video in your chosen aspect ratio. Ideal for commercial content creation, character-driven storytelling, and rapid visual concept validation. | Generate video from reference images using HappyHorse 1.1, locking character and scene appearance while following a text prompt for motion. This workflow takes 2 input images (character reference and scene reference) and produces 1 video output. Ideal for short films, advertising, and game cutscenes requiring consistent character design and controllable narrative. | Generate videos that preserve subject characters from multiple reference images using text prompts. Input up to 9 reference images and a scene description to produce a 3-15 second video output. | Generate videos with accurate prompt interpretation and stunning video dynamics. | Generate videos with consistent subjects using multiple reference images (up to 7) for character and style continuity across the video sequence. | Generate videos with reference-based consistency for up to 3 subjects, maintaining character and style continuity across the video sequence with cinematic camera movements. | High-quality videos can be generated using simple prompts. | Input a text prompt or upload an image to generate a 1-16 second video with synchronized audio and automatic scene transitions. | Input text prompts or an initial image frame to generate up to 15-second videos with synchronized audio using the Grok model. | Swap products into a reference scene while preserving composition and lighting. Generates a final product image and an automatic video prompt for creating polished product videos. | Upload a blank billboard and overlay text. Generate a smooth zoom in shot revealing your message. | Upload a photo of your vehicle and generate a studio quality video of the vehicle from multiple angles. | Upload a reference image and generate a video using the Grok API, supporting up to 6 reference images for enhanced consistency. | Upload a reference video of a real person for identity verification. Use your own photo to validate and generate a personalized video output. | Upload an image and optional text prompt to generate a video with native audio, realistic motion, and high-quality output up to 720p resolution. | Upload two reference images and input a short text description. Generate a detailed Seedance 2.0-style prompt automatically with an LLM helper.
- member workflows:
    - api_bytedance_seedance1_5_text_to_video
    - api_bytedance_text_to_video
    - api_grok_imagine_video_1_5
    - api_grok_reference_to_video
    - api_grok_video
    - api_hailuo_minimax_t2v
    - api_hailuo_minimax_video
    - api_happyhorse1_0_r2v
    - api_happyhorse1_0_t2v
    - api_happyhorse1_1_r2v
    - api_happyhorse1_1_t2v
    - api_heygen_avatar_video
    - api_luma_ray3_3_t2v
    - api_luma_t2v
    - api_minimax_h3_r2v
    - api_minimax_h3_t2v
    - api_pixverse_t2v
    - api_seedance2_0_mini_r2v
    - api_seedance2_0_mini_t2v
    - api_seedance2_0_r2v
    - api_seedance2_0_r2v_4k
    - api_seedance2_0_r2v_real_human
    - api_seedance2_0_t2v
    - api_seedance2_t2v
    - api_sync_so_talking_image
    - api_vidu_q2_r2v
    - api_vidu_q2_t2v
    - api_vidu_q3_text_to_video
    - api_vidu_reference_to_video
    - api_vidu_start_end_to_video
    - api_vidu_text_to_video
    - template_product_placement
    - template_seedance2_storyboard_to_video
    - template_seedance_2_0_plus_llm_prompt_helper
    - templates-car_product
    - templates-led_billboard
- node clusters (required structure):
    - (none resolved)
- optional roles: RegexExtract, BatchImagesNode, ByteDanceSeedreamNode, LoadImage, SaveImage, SaveVideo, GeminiNode, GetVideoComponents, KlingStartEndFrameNode, MarkdownNote, SimpleMath+, GeminiImage2Node
- unresolved nodes: MarkdownNote, Note, Reroute, SimpleMath+

## API / Partner Nodes - Text to Video / Kling  (`api_partner_nodes_text_to_video__kling`)  -  6 workflow(s)  -  source: mixed
- execution: api (API nodes: KlingAvatarNode, KlingOmniProTextToVideoNode, KlingTextToVideoWithAudio, KlingVideoNode)
- when to use: Use to generate a video from a text prompt using Kling.
- example request: "build a video workflow using Kling"
- description: API multi-shot storyboard video via Kling 3.0 (kling-v3). 1 input image (start frame, LoadImage node) -> 1 video output (VHS_VideoCombine). Generates 1-6 sequential shots in a single generation: each shot has its own text prompt (max 512 chars) and duration set directly on the KlingVideoNode. Use for storyboards, scene sequences, and narrative clips with multiple camera cuts. Prompts go into multi_shot.storyboard_N_prompt inputs; multi_shot must match shot count exactly (e.g. '3 storyboards'). Aspect ratio defaults to 16:9, resolution to 720p - override only on explicit user request. | Bring your stories to life with videos featuring synchronized dialogue, music, sound effects, and ambient audio from text prompts. | Generate videos from text descriptions using Kling O1. Create dynamic video content with natural language prompts. | Input text or image prompts to generate 15-second video sequences with multi-shot compositions, complex camera movements, and consistent subjects. | Upload a portrait and an audio file to generate a talking avatar video with synchronized lip movements and natural facial expressions. | Upload text, audio, or images to generate a 15-second video with synchronized audio, character consistency, and storyboard control.
- member workflows:
    - Kling3_multiShot
    - api_king_o3_t2v
    - api_kling2_6_t2v
    - api_kling_avatar2
    - api_kling_omni_t2v
    - api_kling_v3_video
- node clusters (required structure):
    - (none resolved)
- optional roles: GetVideoComponents, KlingAvatarNode, KlingOmniProTextToVideoNode, KlingTextToVideoWithAudio, KlingVideoNode, LoadAudio, LoadImage, MarkdownNote, SaveVideo, VHS_VideoCombine
- unresolved nodes: MarkdownNote

## API / Partner Nodes - Text to Video / Anima  (`api_partner_nodes_text_to_video__anima`)  -  3 workflow(s)  -  source: official
- execution: api (API nodes: GeminiImage2Node, GeminiNanoBanana2, HeyGenTalkingPhotoNode)
- when to use: Use to generate an image using Anima.
- example request: "build a video workflow using Anima"
- description: Generate a talking-head video from a single photograph using HeyGen's Avatar IV engine, which produces a fully animated video with lip-synced speech, facial expressions, head movements, and automatic gestures. Ideal for creating digital avatars for presentations, virtual characters for interactive content, and personalized video messages from a single image. | Upload a single image to generate an animated sequence. The workflow creates a sprite sheet with multiple frames for use in games or animations. | Upload an image of your sprite and receive individual frames of idle, attack, walk and jump animations. 
- member workflows:
    - api_heygen_talking_photo
    - template_purz_nb2_single_image_sprite_sheet
    - templates-sprite_sheet
- node clusters (required structure):
    - inputs: LoadImage
- optional roles: PreviewImage, SimpleMath+, ImageCompositeMasked, ImageCrop, MaskPreview+, ImageResizeKJv2, SaveImage, ColorToMask, CropMask, ImageFromBatch, ImagePadForOutpaintMasked, InvertMask
- unresolved nodes: Image Crop Location, LayerUtility: ColorImage V2, MarkdownNote, MaskBoundingBox+, MaskPreview+, PrimitiveNode, Reroute, SimpleMath+

## API / Partner Nodes - Text to Video / WAN  (`api_partner_nodes_text_to_video__wan`)  -  3 workflow(s)  -  source: official
- execution: api (API nodes: Wan2ReferenceVideoApi, Wan2TextToVideoApi, WanTextToVideoApi)
- when to use: Use to generate a video from a text prompt using WAN.
- example request: "build a video workflow using WAN"
- description: Generate videos from text prompts using Wan 2.7. Supports audio reference to create lip-synced video | Generate videos with synchronized audio, enhanced motion, and superior quality. | Upload a reference video and character image to generate a video with consistent character features.
- member workflows:
    - api_wan2_7_r2v
    - api_wan2_7_t2v
    - api_wan_text_to_video
- node clusters (required structure):
    - output: SaveVideo
- optional roles: LoadImage, MarkdownNote, LoadAudio, RecordAudio, Wan2ReferenceVideoApi, Wan2TextToVideoApi, WanTextToVideoApi
- unresolved nodes: MarkdownNote

## API / Partner Nodes - Text to Video / Gemini  (`api_partner_nodes_text_to_video__gemini`)  -  1 workflow(s)  -  source: official
- execution: api (API nodes: GeminiVideoOmni)
- when to use: Use to generate a video from a text prompt using Gemini.
- example request: "build a video workflow using Gemini"
- description: Generate cinematic video from natural language prompts using Gemini Omni Flash, transforming text descriptions into a single video output with world-aware motion, lighting, and sound. Ideal for social media content creation, rapid video prototyping, and iterative visual storytelling with conversational editing.
- member workflows:
    - api_google_gemini_omni_flash_t2v
- node clusters (required structure):
    - output: SaveVideo
    - other operations: CustomCombo (x2), GeminiVideoOmni, MarkdownNote, PreviewAny, PrimitiveStringMultiline, StringConcatenate (x4)
- paired/multiple required: CustomCombo x2
- unresolved nodes: MarkdownNote

## API / Partner Nodes - Text to Video / LTX-2  (`api_partner_nodes_text_to_video__ltx_2`)  -  1 workflow(s)  -  source: custom
- execution: api (API nodes: LtxvApiTextToVideo)
- when to use: Use to generate a video from a text prompt using LTX-2.
- example request: "build a video workflow using LTX-2"
- description: Generate a video from a text prompt using LTX-2. Structurally it applies a sequence of node operations. Boundary inputs: VIDEO; outputs: AUDIO, IMAGE.
- member workflows:
    - api_ltxv_text_to_video
- node clusters (required structure):
    - output: VHS_VideoCombine
    - other operations: GetVideoComponents, LtxvApiTextToVideo

## API / Partner Nodes - Text to Video / Veo  (`api_partner_nodes_text_to_video__veo`)  -  1 workflow(s)  -  source: custom
- execution: api (API nodes: Veo3VideoGenerationNode)
- when to use: Use to produce a video using Veo.
- example request: "build a video workflow using Veo"
- description: Produce a video using Veo. Structurally it applies a sequence of node operations. Boundary inputs: IMAGE; outputs: VIDEO.
- member workflows:
    - api_veo3
- node clusters (required structure):
    - inputs: LoadImage
    - output: SaveVideo
    - other operations: Veo3VideoGenerationNode

## API / Partner Nodes - Text to Video / WAN 2.6  (`api_partner_nodes_text_to_video__wan_2_6`)  -  1 workflow(s)  -  source: custom
- execution: api (API nodes: WanTextToVideoApi)
- when to use: Use to generate a video from a text prompt using WAN 2.6.
- example request: "build a video workflow using WAN 2.6"
- description: API text-to-video via Wan 2.6. Text prompt only -> 1 video output. Generates 1080P video with enhanced quality, smoother motion, and improved prompt understanding.
- member workflows:
    - api_wan2_6_t2v
- node clusters (required structure):
    - output: VHS_VideoCombine
    - other operations: GetVideoComponents, WanTextToVideoApi


# Image to Video  (`image_to_video`)  -  42 workflow(s), 7 model(s)

## Image to Video / LTX-2  (`image_to_video__ltx_2`)  -  12 workflow(s)  -  source: mixed
- execution: local
- when to use: Use to generate a video from an input image using LTX-2, Anima.
- example request: "build a video workflow using LTX-2"
- description: Apply the ltx2.3-transition LoRA to create smooth style and scene transitions. This workflow uses a specialized model to blend visual elements. | Generate personalized videos with synchronized audio from a text prompt, reference image, and short audio clip. Use ID-LoRA to adapt a person's appearance and voice in a single generative model. | Generate short video clips that stay visually consistent with a reference sheet inventorying characters, props, and locations. Input a composite reference image and a split prompt describing the action, outputting a single video clip. Ideal for character-driven animation, consistent prop visualization, and location-specific scene generation. | Generate videos from still images. | Generates video from Canny edge maps using LTX-2, with optional synchronized audio. | Generates video from a single input image using LTX-2.3. | Generates video from pose reference frames using LTX-2, with optional synchronized audio. | Transform static images into dynamic videos with synchronized audio-video generation using LTX-2 distilled model. Optimized for faster generation while maintaining quality. Features expressive lip sync, natural motion, and improved speed. | Transform static images into dynamic videos with synchronized audio-video generation using LTX-2. Features expressive lip sync, natural motion, and efficient performance. | Upload an image and an audio file to generate a high-quality video with synchronized lip movements using LTX-2.3. | Upload any image to apply the Squish It LoRA effect. Generate a squished animation using the LTX-2 I2V model.
- member workflows:
    - canny_to_video_ltx_2_0
    - image_to_video_ltx_2_3
    - ltxv_image_to_video
    - pose_to_video_ltx_2_0
    - template_ltx2_3_ic_lora_ingredients
    - template_ltx2_3_style_transition
    - video_ltx2_3_i2v
    - video_ltx2_3_ia2v
    - video_ltx2_3_id_lora
    - video_ltx2_i2v
    - video_ltx2_i2v_distilled
    - video_ltx2_i2v_lora
- node clusters (required structure):
    - model loading: CheckpointLoaderSimple
    - conditioning: CLIPTextEncode, LTXVConditioning
    - other operations: CreateVideo
- optional roles: LoraLoaderModelOnly, MarkdownNote, CFGGuider, KSamplerSelect, LTXVAddGuide, LTXVConcatAVLatent, LTXVImgToVideoInplace, LTXVPreprocess, LTXVSeparateAVLatent, LoadImage, ManualSigmas, RandomNoise
- unresolved nodes: MarkdownNote, Note, Reroute

## Image to Video / WAN  (`image_to_video__wan`)  -  12 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate a video using WAN, Anima.
- example request: "build a video workflow using WAN"
- description: Draw the movement trajectory you want for the input image. | Generate dynamic videos with cinematic camera movements using Wan 2.1 Fun Camera 1.3B model. | Generate high-quality videos with advanced camera control using the full 14B model | Generate minute-scale coherent dance videos from music using a hierarchical Wan Dancer framework. Input a music file and reference image to produce high-resolution dance videos with global structure and temporal continuity. | Generate videos from a single image using Wan-Move, with fine-grained point-level motion control via trajectory guidance. | Generate videos from images using Wan 2.1. | Generate videos from start and end frames using Wan 2.1 inpainting. | Trajectory-controlled Video Generation. | Upload a character image and an audio file. Generate a lip-sync video where the character's mouth movements match the provided audio track. | Upload a source Image and target audio. Generate a full-body dubbed video with synchronized motion while preserving the original identity, background, and camera movement. | Upload an input image and use the Animate Path node to draw paths for a viral video effect. | Use WanMove to generate dynamic images from trajectories and create video dynamic effects with daydream illusion
- member workflows:
    - image_to_video_wan
    - template-Animation_Trajectory_Control_Wan_ATI
    - templates-wan2_1_infinitetalk_music
    - templates_rob_wan_ati_motion_control
    - video_wan2.1_fun_camera_v1.1_1.3B
    - video_wan2.1_fun_camera_v1.1_14B
    - video_wan2_1_infinitetalk
    - video_wan_ati
    - video_wan_dancer
    - video_wanmove_480p
    - video_wanmove_480p_hallucination
    - wan2.1_fun_inp
- node clusters (required structure):
    - inputs: LoadImage
    - output: SaveVideo
    - other operations: CreateVideo
- optional roles: AudioEncoderEncode, CLIPTextEncode, CustomCombo, GenerateTracks, MarkdownNote, AudioEncoderLoader, BasicScheduler, CFGGuider, CLIPLoader, CLIPVisionEncode, ConditioningZeroOut, KSamplerSelect
- unresolved nodes: AudioSeparation, FL_PathAnimator, MarkdownNote, Note, PrimitiveNode, Reroute

## Image to Video / WAN 2.2  (`image_to_video__wan_2_2`)  -  8 workflow(s)  -  source: mixed
- execution: local
- when to use: Use to generate a video from an input image using WAN 2.2, Qwen Image.
- example request: "build a video workflow using WAN 2.2"
- description: Fast text-to-video and image-to-video generation with 5B parameters. Optimized for rapid prototyping and creative exploration. | Generate videos from an input image using Wan2.2 14B | Image to Video blueprint | Image-to-video with Wan 2.2 using a start image plus text prompt to extend motion from the still frame. | Transform static images and audio into dynamic videos with perfect synchronization and minute-level generation. | Transform static images into dynamic videos with precise motion control and style preservation using Wan 2.2. | Upload 1 input image and generate 5 alternate angles to be used as start frames with Wan2.2. Each video is stacked horizontally in a final 9x16 video.
- member workflows:
    - 03_video_wan2_2_14B_i2v_subgraphed
    - image_to_video
    - image_to_video_wan_2_2
    - template_rob_split_stack_qwen_multi_wan22
    - video_wan2_2_14B_fun_camera
    - video_wan2_2_14B_i2v
    - video_wan2_2_14B_s2v
    - video_wan2_2_5B_ti2v
- node clusters (required structure):
    - model loading: CLIPLoader, UNETLoader, VAELoader
    - conditioning: CLIPTextEncode (x2)
    - decoding: VAEDecode
    - other operations: CreateVideo, ModelSamplingSD3
- paired/multiple required: CLIPTextEncode x2
- optional roles: LoraLoaderModelOnly, FluxKontextMultiReferenceLatentMethod, KSamplerAdvanced, TextEncodeQwenImageEditPlus, KSampler, LatentConcat, MarkdownNote, SaveVideo, WanSoundImageToVideoExtend, CFGNorm, FluxKontextImageScale, GetVideoComponents
- unresolved nodes: MarkdownNote, Note, RIFE VFI, Reroute

## Image to Video / Generic  (`image_to_video__generic`)  -  6 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate a video from an input image.
- example request: "build a video workflow"
- description: A lightweight 2B model that generates videos from English and Russian prompts with high visual quality. | Generate videos basic on audio, image, and text, keep the character's lip sync. | Generate videos by first creating images from text prompts. | Input a text prompt and select a model checkpoint. Generate a high-quality video using Causal Forcing or Causal Forcing++ with 1 to 4 inference steps. | Upload an image and provide a text instruction. Generate a new video where the input is edited according to your instruction, preserving structure and temporal coherence. | Upload an image or video and a text instruction to perform generation or editing tasks. Generate a new or edited image or video based on the provided instruction.
- member workflows:
    - txt_to_image_to_video
    - video_capybara_v0_1_image_to_video
    - video_capybara_v0_1_video_edit
    - video_causal_forcing_i2v
    - video_humo
    - video_kandinsky5_i2v
- node clusters (required structure):
    - conditioning: CLIPTextEncode (x2)
    - decoding: VAEDecode
    - output: SaveVideo
    - other operations: CreateVideo, MarkdownNote
- paired/multiple required: CLIPTextEncode x2
- optional roles: KSampler, ARVideoI2V, AudioEncoderEncode, AudioEncoderLoader, BasicScheduler, CFGGuider, CLIPLoader, CLIPVisionEncode, CLIPVisionLoader, CheckpointLoaderSimple, DualCLIPLoader, EmptyLatentImage
- unresolved nodes: MarkdownNote

## Image to Video / Anima  (`image_to_video__anima`)  -  2 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate an image using Anima.
- example request: "build a video workflow using Anima"
- description: Drag and drop then dream through a stack of images | upload one image to get a seamless loop animation
- member workflows:
    - template_animate_diff_loops
    - templates_purz_animatediff_simple_weighted_ipadapters_looping_animation
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: CheckpointLoaderSimple
    - conditioning: CLIPTextEncode (x2)
    - latent / canvas: EmptyLatentImage
    - sampling: KSampler
    - decoding: VAEDecode
    - output: VHS_VideoCombine (x2)
    - other operations: ADE_AnimateDiffSamplingSettings, ADE_LoadAnimateDiffModel, ADE_MultivalDynamic, ADE_UseEvolvedSampling
- paired/multiple required: CLIPTextEncode x2, VHS_VideoCombine x2
- optional roles: ImageScaleToTotalPixels, ImageStitch, RepeatImageBatch, ADE_AnimateDiffUniformContextOptions, ADE_ApplyAnimateDiffModel, FreeU_V2, IPAdapterBatch, MarkdownNote, ADE_AnimateDiffLoRALoader, ADE_ApplyAnimateDiffModelSimple, ADE_LoopedUniformContextOptions, AILab_QwenVL
- unresolved nodes: ADE_AnimateDiffLoRALoader, ADE_AnimateDiffSamplingSettings, ADE_AnimateDiffUniformContextOptions, ADE_ApplyAnimateDiffModel, ADE_ApplyAnimateDiffModelSimple, ADE_LoadAnimateDiffModel, ADE_LoopedUniformContextOptions, ADE_MultivalDynamic, ADE_UseEvolvedSampling, AILab_QwenVL, FL_KsamplerPlus, FL_UpscaleModel, IPAdapterBatch, IPAdapterMS, IPAdapterModelLoader, IPAdapterUnifiedLoader, IPAdapterWeights, MarkdownNote, PrepImageForClipVision, Upscale Model Loader

## Image to Video / Bernini  (`image_to_video__bernini`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to edit an existing image using Bernini.
- example request: "build an image workflow using Bernini"
- description: Generate an edited image with matched lighting and view a side-by-side before/after comparison. Ideal for portrait and product relighting, consistent lighting across photo sets, and e-commerce catalog photography.
- member workflows:
    - video_bernini_r_image_editing
- node clusters (required structure):
    - inputs: LoadImage (x2)
    - model loading: CLIPLoader, LoraLoaderModelOnly (x2), UNETLoader (x2), VAELoader
    - conditioning: BasicScheduler, BerniniConditioning, CLIPTextEncode (x2), SplitSigmas
    - sampling: KSamplerSelect, SamplerCustom (x2)
    - decoding: VAEDecode
    - output: SaveImage
    - other operations: BatchImagesNode, ComfySwitchNode (x5), CustomCombo, GetImageSize, ImageCompare, MarkdownNote (x4), PreviewAny, PrimitiveBoolean, PrimitiveFloat (x2), PrimitiveInt (x5), PrimitiveStringMultiline, RegexExtract, ResizeImageMaskNode, StringConcatenate, StringReplace
- paired/multiple required: MarkdownNote x4, CLIPTextEncode x2, LoadImage x2, LoraLoaderModelOnly x2, SamplerCustom x2, UNETLoader x2
- unresolved nodes: MarkdownNote

## Image to Video / Hunyuan3D  (`image_to_video__hunyuan3d`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate a video from an input image using Anima, Hunyuan3D.
- example request: "build a video workflow using Anima"
- description: Animate still images into dynamic videos with precise motion and camera control. Maintains visual consistency while bringing photos and illustrations to life with smooth, natural movements.
- member workflows:
    - video_hunyuan_video_1.5_720p_i2v
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: DualCLIPLoader, LatentUpscaleModelLoader, UNETLoader (x2), VAELoader
    - conditioning: BasicScheduler (x2), CFGGuider (x3), CLIPTextEncode (x2), SplitSigmas
    - sampling: KSamplerSelect (x2), SamplerCustomAdvanced (x3)
    - decoding: VAEDecode (x2), VAEDecodeTiled (x2)
    - output: SaveVideo (x2)
    - other operations: CLIPVisionEncode, CLIPVisionLoader, CreateVideo (x2), DisableNoise, EasyCache (x2), HunyuanVideo15ImageToVideo, HunyuanVideo15LatentUpscaleWithModel, HunyuanVideo15SuperResolution, MarkdownNote (x3), ModelSamplingSD3 (x2), Note (x3), RandomNoise (x2)
- paired/multiple required: CFGGuider x3, MarkdownNote x3, Note x3, SamplerCustomAdvanced x3, BasicScheduler x2, CLIPTextEncode x2, CreateVideo x2, EasyCache x2, KSamplerSelect x2, ModelSamplingSD3 x2, RandomNoise x2, SaveVideo x2, UNETLoader x2, VAEDecode x2, VAEDecodeTiled x2
- unresolved nodes: MarkdownNote, Note


# Video to Video  (`video_to_video`)  -  34 workflow(s), 10 model(s)

## Video to Video / LTX-2  (`video_to_video__ltx_2`)  -  11 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate a video using LTX-2.
- example request: "build a video workflow using LTX-2"
- description: Generate LTX 2.3 videos with IC-LoRA using aligned control inputs like depth, pose, or edges. | Generate high-quality videos from depth maps with synchronized audio-video generation using LTX-2. Features precise depth control, spatial awareness, and efficient performance. | Generate high-quality videos from edge detection (Canny) guidance with synchronized audio-video generation using LTX-2. Features precise edge control, structural consistency, and efficient performance. | Generate high-quality videos from pose guidance with synchronized audio-video generation using LTX-2. Features precise pose control, expressive motion, and efficient performance. | Generates depth-controlled video with LTX-2: motion and structure follow a depth-reference video alongside text prompting, optional first-frame image conditioning, with optional synchronized audio. | LTX 2.3 LoRA that makes anyone in the input video have Googly Eyes. This workflow utilizes the Googlyeyes LTX 2.3 LoRA by TheBurgstall | Upload an input video and prompt for the object to get removed from the video's foreground.  | Upload an input video or archival footage and restore it with 1 click. | Upload an input video with subtitles or text occlusions and remove the text elements with one click. | Upload an input video with watermarks and remove them with one click | Video Outpainting using the LTX 2.3 Video Outpainting IC LoRA. Expand your video in any direction!
- member workflows:
    - depth_to_video_ltx_2_0
    - template_ltx2_3_lora_googly_eyes
    - template_ltx2_3_lora_remove_subtitles_from_video
    - template_ltx2_3_lora_restore_archival_footage
    - template_ltx2_3_lora_video_outpainting
    - template_ltx2_3_obscura_remova_lora_remove_object_from_video
    - template_ltx2_3_remove_watermark_from_video
    - video_ltx2_3_ic_lora
    - video_ltx2_canny_to_video
    - video_ltx2_depth_to_video
    - video_ltx2_pose_to_video
- node clusters (required structure):
    - conditioning: CLIPTextEncode (x2), LTXVConditioning
    - latent / canvas: LTXVEmptyLatentAudio
    - decoding: LTXVAudioVAEDecode
    - other operations: EmptyLTXVLatentVideo, GetImageSize, LTXVConcatAVLatent, LTXVCropGuides, LTXVSeparateAVLatent, MarkdownNote
- paired/multiple required: CLIPTextEncode x2
- optional roles: KSamplerSelect, SamplerCustomAdvanced, CFGGuider, GetVideoComponents, LTXVImgToVideoInplace, RandomNoise, VHS_VideoCombine, LoraLoaderModelOnly, ManualSigmas, MoGeRender, ResizeImageMaskNode, VAEDecode
- unresolved nodes: CM_FloatToInt, Float32ColorCorrect, LTXAddVideoICLoRAGuide, LTXFloatToInt, LTXICLoRALoaderModelOnly, LTXVImgToVideoConditionOnly, LTXVSetAudioRefTokens, LTXVTiledVAEDecode, MarkdownNote, Note, Reroute

## Video to Video / WAN VACE  (`video_to_video__wan_vace`)  -  6 workflow(s)  -  source: mixed
- execution: local
- when to use: Use to generate a video using WAN VACE, SAM3, WAN 2.2.
- example request: "build a video workflow using WAN VACE"
- description: Use a base video + a stylized reference image to create the stylized video using WAN 2.1 VACE | Use simple prompt to mask out certain objects within a video, and replace the object using prompt, or optional reference image. Model used: SAM3 + WAN 2.1 VACE inpainting | [Local] image editing via Wan. 3 image inputs -> 1 image output. Performs advanced image-to-image editing and transformations.
- member workflows:
    - Wan22Vace_VID2VID
    - templates_shane_change_any_objects
    - templates_shane_video_restyle
    - video_wan_vace_14B_ref2v
    - video_wan_vace_14B_v2v
    - video_wan_vace_outpainting
- node clusters (required structure):
    - (none resolved)
- optional roles: INTConstant, CLIPTextEncode, DiffusionModelLoaderKJ, DiffusionModelSelector, GetVideoComponents, ImageCompositeMasked, ImageResizeKJv2, KSamplerAdvanced, LoadImage, LoraLoaderModelOnly, MaskBlur+, ModelSamplingSD3
- unresolved nodes: DepthAnything_V2, DownloadAndLoadDepthAnythingV2Model, ImageConstant, ImageResize+, Int, MarkdownNote, MaskBlur+, TextBox1, easy mathInt

## Video to Video / WAN  (`video_to_video__wan`)  -  5 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate a video guided by a control map (canny/depth/pose) using WAN, Anima, SCAIL.
- example request: "build a video workflow using WAN"
- description: Animate a reference character using a driving video or replace characters entirely with SCAIL-2 Int8, which delivers higher quality than fp8 while running faster. The workflow accepts one reference image and one driving video, outputting an animated character sequence with replaced identity. Ideal for cross-identity character swaps, animal-driven animation, and multi-character scenes without intermediate pose representations. | Generate videos guided by pose, depth, and edge controls using Wan 2.1 ControlNet. | Learn how to control a video with Pose Estimation and Wan Animate. | One-Touch SCAIL Pose Control based on the composition of the Reference Image | Upload 1 reference character image and 1 driving video. Generate an animated video of the character matching the driving video's motion. Ideal for character animation, in-video character replacement, and motion transfer projects.
- member workflows:
    - gsc_advanced_3_2
    - video-wan21_scail
    - video_wan21_scail2_character_replacement
    - video_wan21_scail2_character_replacement_int8
    - wan2.1_fun_control
- node clusters (required structure):
    - inputs: LoadImage, LoadVideo
    - output: SaveVideo
    - other operations: CLIPVisionLoader, CreateVideo, GetVideoComponents, MarkdownNote
- optional roles: CLIPTextEncode, ImageFromBatch, LoraLoaderModelOnly, PreviewImage, SAM3_VideoTrack, BasicScheduler, CLIPLoader, CLIPVisionEncode, CheckpointLoaderSimple, ImageResizeKJv2, KSamplerSelect, ModelSamplingSD3
- unresolved nodes: MarkdownNote, Note, OnnxDetectionModelLoader, PoseDetectionVitPoseToDWPose, RenderNLFPoses, SimpleMath+

## Video to Video / WAN 2.2  (`video_to_video__wan_2_2`)  -  4 workflow(s)  -  source: mixed
- execution: local
- when to use: Use to generate a video using WAN 2.2, Anima.
- example request: "build a video workflow using WAN 2.2"
- description: Multi-condition video control with pose, depth, and edge guidance. Compact 5B size for experimental development. | Unified character animation and replacement framework with precise motion and expression replication. | Upload a video and a character image. Automatically replace the character in the video using the Wan2.2 Animate model.
- member workflows:
    - template_purz_wan22_animate_auto_character_replace
    - video_wan2_2_14B_animate
    - video_wan2_2_14B_fun_control
    - video_wan2_2_5B_fun_control
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: CLIPLoader, UNETLoader, VAELoader
    - conditioning: CLIPTextEncode (x2)
    - decoding: VAEDecode
    - other operations: CreateVideo, ModelSamplingSD3
- paired/multiple required: CLIPTextEncode x2
- optional roles: MarkdownNote, SaveVideo, ImageFromBatch, KSampler, TrimVideoLatent, WanAnimateToVideo, DWPreprocessor, GetVideoComponents, ImageBatch, ImageScale, KSamplerAdvanced, LoraLoaderModelOnly
- unresolved nodes: DownloadAndLoadSAM2Model, DrawViTPose, MarkdownNote, Note, OnnxDetectionModelLoader, PoseAndFaceDetection, Reroute, Sam2Segmentation

## Video to Video / Generic  (`video_to_video__generic`)  -  2 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate a video.
- example request: "build a video workflow"
- description: Upload a starting image and a mask video to define the injection area. Generate a dynamic video by injecting noise patterns from a dedicated noise video, with AI auto-generated prompts. | Upload a video and select either RIFE or FILM frame interpolation model to generate smoother, higher frame rate video output.
- member workflows:
    - templates_mjm_Injected
    - utility_video_frame_interpolation
- node clusters (required structure):
    - output: SaveVideo
    - other operations: CreateVideo, PrimitiveInt
- optional roles: ImageScale, CLIPTextEncode, FILM VFI, INTConstant, VHS_LoadVideo, VHS_VideoCombine, ADE_AnimateDiffLoaderWithContext, ADE_AnimateDiffSamplingSettings, ADE_LoopedUniformContextOptions, ADE_MultivalDynamic, ADE_NoisedImageInjection, AILab_QwenVL
- unresolved nodes: ADE_AnimateDiffLoaderWithContext, ADE_AnimateDiffSamplingSettings, ADE_LoopedUniformContextOptions, ADE_MultivalDynamic, ADE_NoisedImageInjection, AILab_QwenVL, FILM VFI, MarkdownNote

## Video to Video / SDPose  (`video_to_video__sdpose`)  -  2 workflow(s)  -  source: official
- execution: local
- when to use: Use to estimate a pose map using SDPose.
- example request: "build a video workflow using SDPose"
- description: Upload a video to detect human poses. Supports detection for both single individuals and multiple people within the same scene | Upload a video to extract pose keypoints and generate a pose map. The workflow supports multiple person detection and uses an enhanced SDPose model for accurate whole-body feature extraction.
- member workflows:
    - utility_sdpose_multi_person_video
    - utility_sdpose_ood_video_to_pose_map
- node clusters (required structure):
    - inputs: LoadVideo
    - model loading: CheckpointLoaderSimple
    - output: SaveVideo
    - other operations: CreateVideo, GetVideoComponents, MarkdownNote, ResizeImageMaskNode, SDPoseDrawKeypoints, SDPoseKeypointExtractor
- optional roles: DrawBBoxes, ImageBlend, PreviewImage, RTDETR_detect, UNETLoader
- unresolved nodes: MarkdownNote

## Video to Video / Anima  (`video_to_video__anima`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate a video using Anima.
- example request: "build a video workflow using Anima"
- description: Upload a character image and input your prompt. Generate an animated video where the character expands with an inflation effect.
- member workflows:
    - templates_ingi_infl8
- node clusters (required structure):
    - inputs: VHS_LoadVideo
    - model loading: CLIPLoader, LoraLoaderModelOnly, OnnxDetectionModelLoader, UNETLoader, VAELoader, WanVideoLoraSelectMulti, WanVideoModelLoader, WanVideoVAELoader
    - conditioning: LoadWanVideoT5TextEncoder, TextEncodeQwenImageEditPlus (x2), WanVideoTextEncode
    - latent / canvas: VAEEncode
    - sampling: KSampler, WanVideoSamplerv2
    - decoding: VAEDecode
    - output: SaveImage, VHS_VideoCombine
    - other operations: BlockifyMask, CFGNorm, CLIPVisionLoader, ComfyMathExpression, DownloadAndLoadSAM2Model, DrawMaskOnImage, DrawViTPose, FluxKontextImageScale, FluxKontextMultiReferenceLatentMethod (x2), GetImageRangeFromBatch, GrowMaskWithBlur, ImageResizeKJv2 (x2), MarkdownNote, ModelSamplingAuraFlow, Note (x2), PoseAndFaceDetection, Sam2Segmentation, VHS_VideoInfo, WanVideoAnimateEmbeds, WanVideoClipVisionEncode, WanVideoDecode, WanVideoSchedulerv2
- paired/multiple required: FluxKontextMultiReferenceLatentMethod x2, ImageResizeKJv2 x2, Note x2, TextEncodeQwenImageEditPlus x2
- unresolved nodes: DownloadAndLoadSAM2Model, DrawViTPose, MarkdownNote, Note, OnnxDetectionModelLoader, PoseAndFaceDetection, Sam2Segmentation

## Video to Video / Bernini  (`video_to_video__bernini`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to edit an existing video using Bernini.
- example request: "build a video workflow using Bernini"
- description: Generate an edited video with consistent relighting using Bernini-R. Ideal for portrait and product relighting, e-commerce catalog photography, and creating consistent lighting across photo sets.
- member workflows:
    - video_bernini_r_video_editing
- node clusters (required structure):
    - inputs: LoadImage, LoadVideo
    - model loading: CLIPLoader, LoraLoaderModelOnly (x2), UNETLoader (x2), VAELoader
    - conditioning: BasicScheduler, BerniniConditioning, CLIPTextEncode (x2), SplitSigmas
    - sampling: KSamplerSelect, SamplerCustom (x2)
    - decoding: VAEDecode
    - output: SaveVideo
    - other operations: BatchImagesNode, ComfySwitchNode (x5), CreateVideo, CustomCombo, GetImageSize, GetVideoComponents (x2), MarkdownNote (x4), PreviewAny (x2), PrimitiveBoolean, PrimitiveFloat (x2), PrimitiveInt (x5), PrimitiveStringMultiline, RegexExtract, StringConcatenate, StringReplace, Video Slice
- paired/multiple required: MarkdownNote x4, CLIPTextEncode x2, GetVideoComponents x2, LoraLoaderModelOnly x2, SamplerCustom x2, UNETLoader x2
- unresolved nodes: MarkdownNote

## Video to Video / Depth Anything  (`video_to_video__depth_anything`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to edit an existing video using Bernini, Depth Anything.
- example request: "build a video workflow using Bernini"
- description: This subgraph uses Depth Anything 3 to predict spatially consistent geometry from any number of images or video frames, with or without known camera poses. It outputs depth maps, camera poses, and optionally 3D Gaussian parameters for novel view synthesis.
- member workflows:
    - video_edit_bernini_r
- node clusters (required structure):
    - model loading: CLIPLoader, LoraLoaderModelOnly (x2), UNETLoader (x2), VAELoader
    - conditioning: BasicScheduler, BerniniConditioning, CLIPTextEncode (x2), SplitSigmas
    - sampling: KSamplerSelect, SamplerCustom (x2)
    - decoding: VAEDecode
    - other operations: ComfySwitchNode (x5), CreateVideo, CustomCombo, GetVideoComponents, MarkdownNote, PreviewAny, PrimitiveBoolean, PrimitiveFloat (x2), PrimitiveInt (x5), PrimitiveStringMultiline, RegexExtract, StringConcatenate, StringReplace
- paired/multiple required: CLIPTextEncode x2, LoraLoaderModelOnly x2, SamplerCustom x2, UNETLoader x2
- unresolved nodes: MarkdownNote

## Video to Video / SAM3  (`video_to_video__sam3`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to segment an image using SAM3.
- example request: "build an image workflow using SAM3"
- description: Use the SAM3 model to segment the main subject or content from a video, isolating specific objects or regions. Input an video and receive a segmented masks output.

- member workflows:
    - utility_video_segment_sam3
- node clusters (required structure):
    - inputs: LoadVideo
    - model loading: CheckpointLoaderSimple
    - conditioning: CLIPTextEncode
    - other operations: GetVideoComponents, MarkdownNote (x2), MaskPreview, Note, SAM3_Detect
- paired/multiple required: MarkdownNote x2
- unresolved nodes: MarkdownNote, Note


# API / Partner Nodes - Video to Video  (`api_partner_nodes_video_to_video`)  -  33 workflow(s), 9 model(s)

## API / Partner Nodes - Video to Video / Generic  (`api_partner_nodes_video_to_video__generic`)  -  19 workflow(s)  -  source: mixed
- execution: api (API nodes: BeebleSwitchXVideoEdit, BriaRemoveVideoBackground, BriaTransparentVideoBackground, BriaVideoGreenScreen, BriaVideoReplaceBackground, ByteDance2ReferenceNode, ByteDanceSeedreamNode, GeminiImage2Node, GeminiNode, GrokVideoEditNode, GrokVideoExtendNode, HappyHorseVideoEditApi, HeyGenVideoTranslateNode, KlingOmniProEditVideoNode, KlingStartEndFrameNode, LumaRay32ExtendVideoNode, LumaRay32VideoEditNode, MinimaxHailuoVideoNode, RunwayAleph2KeyframeNode, RunwayAleph2PromptImageNode, RunwayAleph2VideoToVideoNode, ViduExtendVideoNode)
- when to use: Use to generate a video.
- example request: "build a video workflow"
- description: API reference-to-video via Seedance 2.0 (ByteDance). 1 reference image + 1 reference video -> 1 video output. Generates, edits, or extends video using multimodal references for subject consistency, video editing, and video extension. | Edit a video using text instructions and optional reference images for style transfer or local replacement. Takes a video and up to 5 reference images as input, outputs an edited video. | Edit videos using natural language commands with Luma Ray 3.2, processing one input video and generating an edited output based on your textual instructions.  | Extend any video to a custom aspect ratio. Convert vertical videos to horizontal format and vice versa. Includes an application mode for easy use. | Generate a single edited video that preserves original motion and timing while applying your chosen changes. Ideal for portrait and product relighting, consistent lighting across photo sets, and e-commerce apparel presentation. | Take a picture with your phone, upload it and generate a studio grade product video. | Translate video content into another language with full lip-sync using HeyGen Translate, which automatically transcribes speech, translates it, generates a cloned voice, and re-syncs mouth movements. Takes 1 input video and produces 1 output video. Ideal for localizing talking-head videos, dubbing multilingual presentations, and creating lip-synced content for global audiences. | Upload a short video and a text prompt describing the next scene. Generate a seamless video extension using Grok extend. | Upload a source video and a reference image, then provide a prompt describing the desired environment and lighting. Generate an edited video where masked regions follow your prompt and reference, while unmasked regions preserve the original pixels and motion, plus an alpha matte for compositing. | Upload a video and a background image. Detect the main subject and replace the original background with the provided image. Ideal for content creation, virtual production, and background cleanup in video projects. | Upload a video and generate its frames with a transparent background, outputting image and mask sequences along with a WebM video supporting an alpha channel. | Upload a video and use the Vidu Q2 model to extend it up to 7 seconds and enhance the resolution to 1080p. | Upload a video to edit. Input your desired modifications. Generate an edited video using the Grok API. | Upload a video to generate a green screen version with a transparent or solid background. | Upload a video to remove its background and replace it with your chosen color. Generate a video with the subject isolated and a new solid background. | Upload a video to remove the background. Generate a new video with a transparent or solid color background. | Upload your character and clothing items or accessories. Generate a fashion photograph base and use as a reference to 8x grid images, together with multi-KeyFrame Video Stitching 
- member workflows:
    - 0193-spec-0160-renderLightChar-v006
    - api_beeble_switchx_video_edit
    - api_bria_remove_video_background
    - api_bria_remove_video_background_transparent
    - api_bria_video_green_screen
    - api_bria_video_replace_background
    - api_grok_video_edit
    - api_grok_video_extend
    - api_happyhorse1_0_video_edit
    - api_heygen_video_translate
    - api_luma_ray3_2_video_edit
    - api_runway_aleph2_video_edit
    - api_seedance2_reference2v
    - api_vidu_video_extension
    - template_horizontal_vertical_extension
    - templates-photo_to_product_vid
    - templates-stitched_vid_contact_sheet
    - utility-bria_remove_video_background
    - v2v_api_switchx_videoStyleTransfer
- node clusters (required structure):
    - (none resolved)
- optional roles: BatchImagesNode, ImageFromBatch, SimpleMath+, GetVideoComponents, ResizeAndPadImage, PreviewImage, SaveImage, SaveVideo, GeminiNode, ImageCrop, KlingStartEndFrameNode, AudioMerge
- unresolved nodes: Get Image Size, ImageRemoveAlpha+, JWImageResizeByShorterSide, LayerUtility: ColorImage V2, MarkdownNote, Note, Paste By Mask, Reroute, SimpleMath+

## API / Partner Nodes - Video to Video / Kling  (`api_partner_nodes_video_to_video__kling`)  -  5 workflow(s)  -  source: mixed
- execution: api (API nodes: KlingMotionControl, KlingOmniProEditVideoNode, KlingOmniProVideoToVideoNode)
- when to use: Use to edit an existing video using Kling.
- example request: "build a video workflow using Kling"
- description: API video editing via Kling O3. 1 video + 1 reference image -> 1 edited video output. Enables precise subject editing and scene composition with native audio-visual synchronization. | Apply precise character actions and expressions from a reference video to your character image with synchronized motion control. | Edit videos with natural language commands, featuring video reference mode for quick generation of high-quality style transfers, element additions, and background modifications. | Transform videos with Kling O1. Edit video content, change styles, or replace characters using text prompts and reference images. | Upload a character image and a motion reference video. Generate a new video where your character performs the actions from the reference, with enhanced facial consistency using optional element binding.
- member workflows:
    - api_kling_motion_control
    - api_kling_motion_control3
    - api_kling_o3_video_edit
    - api_kling_omni_edit_video
    - api_kling_omni_v2v
- node clusters (required structure):
    - inputs: LoadImage, LoadVideo
- optional roles: BatchImagesNode, GetVideoComponents, KlingMotionControl, KlingOmniProEditVideoNode, KlingOmniProVideoToVideoNode, MarkdownNote, Note, SaveVideo, VHS_VideoCombine, Video Slice
- unresolved nodes: MarkdownNote, Note

## API / Partner Nodes - Video to Video / Gemini  (`api_partner_nodes_video_to_video__gemini`)  -  2 workflow(s)  -  source: official
- execution: api (API nodes: ByteDance2ReferenceNode, GeminiNode, GeminiVideoOmni, OpenAIGPTImageNodeV2)
- when to use: Use to generate a video using Gemini.
- example request: "build a video workflow using Gemini"
- description: A one click workflow to recreate an input video with your character. All you need to do is upload the video and your character. This workflow uses Google Gemini LLM to analyze the input video and reverse engineer a prompt. You can prompt for specific details to inject into this analysis. The workflow extracts the first frame of the video and swaps your character into it, sends this into Seedance 2.0 Reference-to-Video and generates | Edit videos with natural language using Gemini Omni Flash, transforming a single input video into one edited output based on your descriptive instructions. Specify the duration and aspect ratio in your prompt, and leverage Omni's world knowledge for intuitive edits like changing backgrounds or adding atmosphere. Ideal for quick social media remixes, cinematic scene adjustments, and iterative video refinements without technical prompts.
- member workflows:
    - api_google_gemini_omni_flash_video_edit
    - template_seedance2_0_viral_videos_character_swap
- node clusters (required structure):
    - inputs: LoadVideo
    - output: SaveVideo
    - other operations: PreviewAny, StringConcatenate
- optional roles: CustomCombo, ByteDance2ReferenceNode, GeminiNode, GeminiVideoOmni, GetVideoComponents, ImageFromBatch, LoadImage, MarkdownNote, OpenAIGPTImageNodeV2, SaveImage, Video Slice
- unresolved nodes: MarkdownNote

## API / Partner Nodes - Video to Video / Topaz  (`api_partner_nodes_video_to_video__topaz`)  -  2 workflow(s)  -  source: official
- execution: api (API nodes: TopazVideoEnhance, TopazVideoEnhanceV2)
- when to use: Use to upscale / enhance a video using Topaz.
- example request: "build a video workflow using Topaz"
- description: Upload a video to enhance its resolution using the Topaz Starlight Precise 2.5 model. This workflow produces sharper 4K output with reduced artifacts compared to previous versions. | Upscale GenAI video footage with Astra 2's creative diffusion, adding dynamic detail and texture. Adjust creativity, sharpness, and prompt-based guidance for precise stylization of AI-generated content.
- member workflows:
    - api_topaz_astra2
    - api_topaz_starlight_precise25
- node clusters (required structure):
    - inputs: LoadVideo
    - output: SaveVideo
- optional roles: TopazVideoEnhance, TopazVideoEnhanceV2

## API / Partner Nodes - Video to Video / Anima  (`api_partner_nodes_video_to_video__anima`)  -  1 workflow(s)  -  source: official
- execution: api (API nodes: SyncLipSyncNode)
- when to use: Use to generate a video using Anima.
- example request: "build a video workflow using Anima"
- description: Synchronize a video's lip movements with a new audio track using the Sync Labs sync-3 model, which automatically adjusts the speaker's mouth to match your uploaded audio. This workflow takes 1 video and 1 audio input to produce 1 synced video output. Ideal for dubbing foreign-language content, correcting mismatched dialogue in video production, or animating a static portrait to speak.
- member workflows:
    - api_sync_so_lip_sync_video
- node clusters (required structure):
    - inputs: LoadVideo
    - output: SaveVideo
    - other operations: LoadAudio, RecordAudio, SyncLipSyncNode

## API / Partner Nodes - Video to Video / WAN  (`api_partner_nodes_video_to_video__wan`)  -  1 workflow(s)  -  source: official
- execution: api (API nodes: Wan2VideoEditApi)
- when to use: Use to edit an existing video using WAN.
- example request: "build a video workflow using WAN"
- description: Upload a video and corresponding images to edit and replace characters or scenes using the Wan2.7 model.
- member workflows:
    - api_wan2_7_video_edit
- node clusters (required structure):
    - inputs: LoadImage (x2), LoadVideo
    - output: SaveVideo
    - other operations: Wan2VideoEditApi
- paired/multiple required: LoadImage x2

## API / Partner Nodes - Video to Video / WAN 2.2  (`api_partner_nodes_video_to_video__wan_2_2`)  -  1 workflow(s)  -  source: official
- execution: api (API nodes: GeminiNanoBanana2)
- when to use: Use to generate an image using Anima, WAN 2.2.
- example request: "build a video workflow using Anima"
- description: Wan Animate 2.2 - Character & Scene Replacement - Uses Nano Banana 2 to generate a reference image from the first frame, then swaps the full scene. Optimized for human subjects.
- member workflows:
    - templates_purz_wan22_animate_auto_full_scene
- node clusters (required structure):
    - inputs: VHS_LoadVideo
    - model loading: CLIPLoader, LoraLoaderModelOnly (x2), OnnxDetectionModelLoader, UNETLoader, VAELoader
    - conditioning: CLIPTextEncode (x2)
    - sampling: KSampler
    - decoding: VAEDecode
    - output: SaveImage, SaveVideo (x4)
    - other operations: BlockifyMask, CLIPVisionEncode, CLIPVisionLoader, CreateVideo (x4), DownloadAndLoadSAM2Model, DrawMaskOnImage, DrawViTPose, GeminiNanoBanana2, GetImageSizeAndCount, GrowMaskWithBlur, ImageFromBatch (x2), ImageScale (x2), MarkdownNote (x2), ModelSamplingSD3, Note, PoseAndFaceDetection, PrimitiveInt (x2), Sam2Segmentation, StringConcatenate, TrimVideoLatent, VHS_VideoInfo, WanAnimateToVideo
- paired/multiple required: CreateVideo x4, SaveVideo x4, CLIPTextEncode x2, ImageFromBatch x2, ImageScale x2, LoraLoaderModelOnly x2, MarkdownNote x2
- unresolved nodes: DownloadAndLoadSAM2Model, DrawViTPose, MarkdownNote, Note, OnnxDetectionModelLoader, PoseAndFaceDetection, Sam2Segmentation

## API / Partner Nodes - Video to Video / WAN 2.6  (`api_partner_nodes_video_to_video__wan_2_6`)  -  1 workflow(s)  -  source: official
- execution: api (API nodes: WanReferenceVideoApi)
- when to use: Use to generate a video using WAN 2.6.
- example request: "build a video workflow using WAN 2.6"
- description: Creating identity-preserved videos with natural movement and cinematic quality.
- member workflows:
    - api_wan_r2v
- node clusters (required structure):
    - inputs: LoadVideo (x2)
    - output: SaveVideo
    - other operations: WanReferenceVideoApi
- paired/multiple required: LoadVideo x2

## API / Partner Nodes - Video to Video / WAN VACE  (`api_partner_nodes_video_to_video__wan_vace`)  -  1 workflow(s)  -  source: official
- execution: api (API nodes: OpenAIChatNode)
- when to use: Use to generate a video using WAN VACE.
- example request: "build a video workflow using WAN VACE"
- description: Upload a video clip to generate a seamless, looping video output.
- member workflows:
    - template_sirolim_seamless_loop
- node clusters (required structure):
    - inputs: VHS_LoadVideo
    - model loading: CLIPLoader, LoraLoaderModelOnly, UNETLoader, VAELoader
    - conditioning: CLIPTextEncode (x2)
    - sampling: KSampler
    - decoding: VAEDecode
    - output: SaveVideo, VHS_VideoCombine (x2)
    - other operations: BatchImagesNode (x2), CreateVideo, ImageBatch, ImageFromBatch (x4), ImageResize+, ImageToMask, LayerUtility: ColorImage V2 (x3), MarkdownNote, OpenAIChatNode, PreviewAny, PrimitiveInt (x2), ReverseImageBatch (x3), SimpleMath+, UNetTemporalAttentionMultiply, VHS_DuplicateImages (x3), WanVaceToVideo
- paired/multiple required: ImageFromBatch x4, LayerUtility: ColorImage V2 x3, ReverseImageBatch x3, VHS_DuplicateImages x3, BatchImagesNode x2, CLIPTextEncode x2, VHS_VideoCombine x2
- unresolved nodes: ImageResize+, LayerUtility: ColorImage V2, MarkdownNote, SimpleMath+


# API / Partner Nodes - Image to Video  (`api_partner_nodes_image_to_video`)  -  29 workflow(s), 9 model(s)

## API / Partner Nodes - Image to Video / Generic  (`api_partner_nodes_image_to_video__generic`)  -  13 workflow(s)  -  source: official
- execution: api (API nodes: ByteDanceImageToVideoNode, GeminiImage2Node, GeminiNanoBanana2, HappyHorseImageToVideoApi, KlingOmniProImageToVideoNode, LumaRay32ExtendVideoNode, LumaRay32ImageToVideoNode, MinimaxImageToVideoNode, PixverseImageToVideoNode, PixverseTemplateNode, RunwayImageToVideoNodeGen4, Vidu2ImageToVideoNode, Vidu3ImageToVideoNode, ViduImageToVideoNode)
- when to use: Use to generate a video from an input image.
- example request: "build a video workflow"
- description: Generate cinematic-quality videos from text prompts using Luma Ray 3.2, with support for extending previous generations by providing a generation ID. The workflow accepts 1 input image and produces 1 video output, enabling seamless iterative refinement. Ideal for creating short film sequences, marketing content, and professional video production. | Generate dynamic videos from images using Runway Gen4 Turbo. | Generate dynamic videos from static images with motion and effects using PixVerse. | Generate high-quality, fluid videos from images using HappyHorse-1.0-I2V with realistic dynamic rendering and accurate text and image semantic comprehension. | Generate refined videos from images and text with CGI integration using MiniMax. | Learn how to create a UGC video with your character and product in app mode. | Transform images into living characters with speech, motion, and synchronized sound effects. | Transform static images into dynamic 1080p videos with cinematic camera control, multi-subject consistency | Transform static images into dynamic 1080p videos with precise motion control and customizable movement amplitude using Vidu. | Transform static images into dynamic videos using ByteDance's Seedance model. Analyzes image structure and generates natural motion with consistent visual style and coherent video sequences. | Upload an image and provide a text prompt to generate a 1-16 second video with synchronized audio and intelligent scene transitions. | Upload your logo, texture and elements. Generate a video of the textured logo for an on brand asset.
- member workflows:
    - api_bytedance_image_to_video
    - api_bytedance_seedance1_5_image_to_video
    - api_hailuo_minimax_i2v
    - api_happyhorse1_0_i2v
    - api_luma_ray3_3_i2v
    - api_pixverse_i2v
    - api_pixverse_template_i2v
    - api_runway_gen4_turo_image_to_video
    - api_vidu_image_to_video
    - api_vidu_q2_i2v
    - api_vidu_q3_image_to_video
    - gsc_advanced_3_1
    - templates-textured_logo_elements
- node clusters (required structure):
    - inputs: LoadImage
    - output: SaveVideo
- optional roles: MarkdownNote, BatchImagesNode, ResizeAndPadImage, ByteDanceImageToVideoNode, GeminiImage2Node, GeminiNanoBanana2, HappyHorseImageToVideoApi, KlingOmniProImageToVideoNode, LumaRay32ExtendVideoNode, LumaRay32ImageToVideoNode, MinimaxImageToVideoNode, PixverseImageToVideoNode
- unresolved nodes: MarkdownNote, PrimitiveNode

## API / Partner Nodes - Image to Video / Kling  (`api_partner_nodes_image_to_video__kling`)  -  7 workflow(s)  -  source: mixed
- execution: api (API nodes: ByteDanceSeedreamNodeV2, GeminiImage2Node, GeminiNanoBanana2, GeminiNode, KlingImageToVideoWithAudio, KlingOmniProImageToVideoNode, OpenAIChatConfig, OpenAIChatNode)
- when to use: Use to generate a video from an input image using Kling, Anima, Nano-Banana.
- example request: "build a video workflow using Kling"
- description: API image-to-video via Kling O3 (Kling 3.0). 1 reference image (+ optional audio/text prompt) -> 1 video output. Generates character-consistent video with native audio output and precise storyboard control. | Local image editing via Kling. 6 image inputs -> 1 video output. Processes and generates content using ComfyUI workflows. | This is the base workflow behind my viral Wes Anderson-style reel on Instagram.  It shows how to go from a simple prompt to a Wes Anderson-style image using a cinematic image model, then enhance it with Nanobanana to improve textures and details, and finally turn it into a video using the current best video model, Kling 3.0. | Transform static images into dynamic videos with Kling O1. Add motion, camera movements, and life to your images using text prompts. | Transform static images into dynamic videos with synchronized dialogue, singing, sound effects, and ambient audio. | Upload a start frame and references of your product. Select total duration and number of shots and automatically generate prompts for each shot. | Upload an image to automatically generate a descriptive script. This script is then used to create a video with the Kling 3.0 Omni model.
- member workflows:
    - akagane-video-batch1
    - api_kling2_6_i2v
    - api_kling_o3_i2v
    - api_kling_omni_i2v
    - template_sirolim_image_script_video
    - templates_ohneis_i2v
    - templates_rob_kling3_0_multishot_llm_product
- node clusters (required structure):
    - (none resolved)
- optional roles: RegexExtract, LoadImage, StringToInt, AgentYRefNote, OpenAIChatConfig, OpenAIChatNode, AgentYImageCollector, Note, RegexReplace, ResizeAndPadImage, SaveImage, SomethingToString
- unresolved nodes: AgentYRefNote, MarkdownNote, Note, PrimitiveNode, Reroute, StringToInt, Text Multiline

## API / Partner Nodes - Image to Video / Anima  (`api_partner_nodes_image_to_video__anima`)  -  2 workflow(s)  -  source: official
- execution: api (API nodes: HappyHorseImageToVideoApi, LumaConceptsNode, LumaImageToVideoNode)
- when to use: Use to generate a video from an input image using Anima.
- example request: "build a video workflow using Anima"
- description: Animate a static first frame into a short video with synchronized audio using HappyHorse 1.1, taking 1 input image and producing 1 video output. Ideal for e-commerce product demos, brand marketing content, and short episodic series. | Take static images and instantly create magical high quality animations.
- member workflows:
    - api_happyhorse1_1_i2v
    - api_luma_i2v
- node clusters (required structure):
    - inputs: LoadImage
    - output: SaveVideo
- optional roles: LumaConceptsNode, HappyHorseImageToVideoApi, LumaImageToVideoNode, MarkdownNote
- unresolved nodes: MarkdownNote

## API / Partner Nodes - Image to Video / WAN  (`api_partner_nodes_image_to_video__wan`)  -  2 workflow(s)  -  source: official
- execution: api (API nodes: Wan2ImageToVideoApi, WanImageToVideoApi)
- when to use: Use to generate a video from an input image using WAN.
- example request: "build a video workflow using WAN"
- description: Transform images into videos with synchronized audio, enhanced motion, and superior quality. | Upload an image and audio file to generate a video with synchronized sound, using the first and last frames for control.
- member workflows:
    - api_wan2_7_i2v
    - api_wan_image_to_video
- node clusters (required structure):
    - inputs: LoadImage
    - output: SaveVideo
- optional roles: MarkdownNote, LoadAudio, RecordAudio, Wan2ImageToVideoApi, WanImageToVideoApi
- unresolved nodes: MarkdownNote

## API / Partner Nodes - Image to Video / Gemini  (`api_partner_nodes_image_to_video__gemini`)  -  1 workflow(s)  -  source: official
- execution: api (API nodes: GeminiVideoOmni)
- when to use: Use to generate a video from an input image using Gemini.
- example request: "build a video workflow using Gemini"
- description: Generate a video from two images using Gemini Omni Flash, which interprets natural language prompts to control duration and aspect ratio. The workflow accepts 2 input images and produces 1 video output. Ideal for creating short brand clips, dynamic social media content, and iterative video edits through conversational prompting.
- member workflows:
    - api_google_gemini_omni_flash_i2v
- node clusters (required structure):
    - inputs: LoadImage (x2)
    - output: SaveVideo
    - other operations: CustomCombo (x2), GeminiVideoOmni, MarkdownNote, PreviewAny, PrimitiveStringMultiline, StringConcatenate (x4)
- paired/multiple required: CustomCombo x2, LoadImage x2
- unresolved nodes: MarkdownNote

## API / Partner Nodes - Image to Video / LTX-2  (`api_partner_nodes_image_to_video__ltx_2`)  -  1 workflow(s)  -  source: custom
- execution: api (API nodes: LtxvApiImageToVideo)
- when to use: Use to generate a video from an input image using LTX-2.
- example request: "build a video workflow using LTX-2"
- description: Generate a video from an input image using LTX-2. Structurally it applies a sequence of node operations. Boundary inputs: IMAGE; outputs: AUDIO, IMAGE.
- member workflows:
    - api_ltxv_image_to_video
- node clusters (required structure):
    - inputs: LoadImage
    - output: VHS_VideoCombine
    - other operations: GetVideoComponents, LtxvApiImageToVideo

## API / Partner Nodes - Image to Video / Veo  (`api_partner_nodes_image_to_video__veo`)  -  1 workflow(s)  -  source: official
- execution: api (API nodes: VeoVideoGenerationNode)
- when to use: Use to generate a video from an input image using Veo.
- example request: "build a video workflow using Veo"
- description: Generate videos from images using Google Veo2 API.
- member workflows:
    - api_veo2_i2v
- node clusters (required structure):
    - inputs: LoadImage
    - output: SaveVideo
    - other operations: MarkdownNote, VeoVideoGenerationNode
- unresolved nodes: MarkdownNote

## API / Partner Nodes - Image to Video / WAN 2.6  (`api_partner_nodes_image_to_video__wan_2_6`)  -  1 workflow(s)  -  source: custom
- execution: api (API nodes: WanImageToVideoApi)
- when to use: Use to generate a video from an input image using WAN 2.6.
- example request: "build a video workflow using WAN 2.6"
- description: API image-to-video via Wan 2.6. 1 image -> 1 video output. Generates 1080P video with enhanced image quality, smoother motion, and natural movement.
- member workflows:
    - api_wan2_6_i2v
- node clusters (required structure):
    - inputs: LoadImage
    - output: VHS_VideoCombine
    - other operations: GetVideoComponents, WanImageToVideoApi

## API / Partner Nodes - Image to Video / WAN VACE  (`api_partner_nodes_image_to_video__wan_vace`)  -  1 workflow(s)  -  source: official
- execution: api (API nodes: GeminiImage2Node, KlingImage2VideoNode)
- when to use: Use to generate a video using WAN VACE.
- example request: "build a video workflow using WAN VACE"
- description: Upload a product video and generate a dynamic product scene transformation using Nano Banana Pro & Wan VACE 2.1
- member workflows:
    - templates_product_scene_transformation
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: CLIPLoader (x4), LoraLoaderModelOnly (x4), UNETLoader (x4), VAELoader (x4)
    - conditioning: CLIPTextEncode (x8)
    - sampling: KSampler (x4)
    - decoding: VAEDecode (x4)
    - output: SaveImage, SaveVideo (x2)
    - other operations: BatchImagesNode, CM_IntToFloat, CreateVideo, DepthAnything_V2, DownloadAndLoadDepthAnythingV2Model, GeminiImage2Node, GetImageRangeFromBatch, GetImageSize, GetVideoComponents, ImageBatchMulti, ImageCrop (x4), ImageFromBatch (x8), ImageRemoveAlpha+ (x5), ImageRemoveBackground+, ImageResize+, ImageResizeKJv2, KlingImage2VideoNode, MarkdownNote, Note, PrimitiveFloat, PrimitiveInt (x3), PrimitiveStringMultiline, RemBGSession+, Reroute (x4), ResizeAndPadImage, SimpleMath+ (x10), TrimVideoLatent (x4), VHS_SelectEveryNthImage, WanVaceToVideo (x4)
- paired/multiple required: SimpleMath+ x10, CLIPTextEncode x8, ImageFromBatch x8, ImageRemoveAlpha+ x5, CLIPLoader x4, ImageCrop x4, KSampler x4, LoraLoaderModelOnly x4, TrimVideoLatent x4, UNETLoader x4, VAEDecode x4, VAELoader x4, WanVaceToVideo x4, SaveVideo x2
- unresolved nodes: CM_IntToFloat, DepthAnything_V2, DownloadAndLoadDepthAnythingV2Model, ImageRemoveAlpha+, ImageRemoveBackground+, ImageResize+, MarkdownNote, Note, RemBGSession+, Reroute, SimpleMath+


# API / Partner Nodes - 3D  (`api_partner_nodes_3d`)  -  28 workflow(s), 4 model(s)

## API / Partner Nodes - 3D / Generic  (`api_partner_nodes_3d__generic`)  -  17 workflow(s)  -  source: official
- execution: api (API nodes: GeminiImage2Node, RecraftRemoveBackgroundNode, Rodin3D_Detail, Rodin3D_Gen2, Rodin3D_Gen25_Image, Rodin3D_Gen25_Text, Rodin3D_Regular, Rodin3D_Sketch, Rodin3D_Smooth, TripoConversionNode, TripoImageToModelNode, TripoMultiviewToModelNode, TripoP1ImageToModelNode, TripoP1MultiviewToModelNode, TripoP1TextToModelNode, TripoRefineNode, TripoRetargetNode, TripoRigNode, TripoTextToModelNode, TripoTextureNode)
- when to use: Use to generate a 3D model.
- example request: "build a 3d workflow"
- description:  Use an outline reference, and a style reference as input to generate 2D sprite as model textures. Useful for background set dressing in 2D/2.5D game. | Build 3D models from multiple angles with Tripo's advanced scanner. | Craft 3D objects from descriptions with Tripo's text-driven modeling. | Generate detailed 3D models from single photos using Rodin AI. | Generate detailed 4X mesh quality 3D models from photos using Rodin Gen2 | Generate precise 3D models from text with Tripo 3.0's ultra-high resolution geometry and realistic PBR materials. | Generate production-ready 3D hero assets with high-density geometry and PBR materials. Takes text prompts or reference images as input and outputs detailed 3D meshes suitable for close-up renders and game assets. | Generate professional 3D assets from 2D images using Tripo engine. | Input a text description of a 3D model. Generate a game-ready 3D model with clean topology and optimized polygon counts | Input a text description or upload reference images. Generate a detailed 3D model with textures, exportable in multiple formats. | Sculpt comprehensive 3D models using Rodin's multi-angle reconstruction. | Transform images or sketches into 3D models with Tripo 3.0's sharp geometry and production-ready PBR textures. | Upload a reference image of your object. Generate a high-detail 3D model with dense geometry and PBR-ready materials. | Upload a reference image of your subject. Generate a game-ready 3D model with clean topology and optimized polygon budgets | Upload an image or multi-view references to generate a clean low-poly 3D model with controlled polygon count and organized topology, ready for export to game engines. | Upload multiview images of your object. Generate a high-detail 3D model with dense geometry and PBR-ready materials. | Upload single or multi-view images to create a 3D model with adjustable quality and enhanced texture
- member workflows:
    - api_rodin3d_gen2_5_image_to_3d
    - api_rodin3d_gen2_5_text_to_3d
    - api_rodin_gen2
    - api_rodin_image_to_model
    - api_rodin_multiview_to_model
    - api_tripo3_0_image_to_model
    - api_tripo3_0_text_to_model
    - api_tripo3_1_image_to_model
    - api_tripo3_1_multiview_to_model
    - api_tripo3_1_text_to_model
    - api_tripo_image_to_model
    - api_tripo_multiview_to_model
    - api_tripo_p1_image_to_model
    - api_tripo_p1_mv_to_model
    - api_tripo_p1_text_to_model
    - api_tripo_text_to_model
    - templates_3d_match_game_art_style.app
- node clusters (required structure):
    - (none resolved)
- optional roles: LoadImage, Preview3D, MarkdownNote, SaveImage, BatchImagesNode, GeminiImage2Node, ImageCompare, Note, RecraftRemoveBackgroundNode, Rodin3D_Detail, Rodin3D_Gen2, Rodin3D_Gen25_Image
- unresolved nodes: MarkdownNote, Note

## API / Partner Nodes - 3D / Hunyuan3D  (`api_partner_nodes_3d__hunyuan3d`)  -  6 workflow(s)  -  source: official
- execution: api (API nodes: Tencent3DPartNode, TencentImageToModelNode, TencentModelTo3DUVNode, TencentSmartTopologyNode, TencentTextToModelNode)
- when to use: Use to generate a 3D model using Hunyuan3D.
- example request: "build a 3d workflow using Hunyuan3D"
- description: Input a dense mesh (from AI generation or photogrammetry scans) and create a light weight model with good topology and unwrapped UV. Great for 3D game assets optimization. | Input a text prompt or upload a reference image to generate a detailed 3D model asset. | Upload a 3D model to automatically segment it into its constituent parts, generating a fully decomposed 3D asset for reuse and editing. | Upload a 3D model to perform UV unwrapping. Generate a processed model with optimized UV layout for texturing. | Upload a high-poly 3D model file. Generate a lower-polygon, topologically optimized 3D model with a specified reduction level. | Upload an image to generate a 3D model with geometry and PBR textures. 
- member workflows:
    - api_hunyuan3d_image_to_model
    - api_hunyuan3d_model2uv
    - api_hunyuan3d_part
    - api_hunyuan3d_retopo_uv
    - api_hunyuan3d_smart_topology
    - api_hunyuan3d_text_to_model
- node clusters (required structure):
    - other operations: SaveGLB
- optional roles: SaveImage, LoadImage, Load3D, MarkdownNote, Preview3D, Tencent3DPartNode, TencentImageToModelNode, TencentModelTo3DUVNode, TencentSmartTopologyNode, TencentTextToModelNode
- unresolved nodes: MarkdownNote

## API / Partner Nodes - 3D / Meshy  (`api_partner_nodes_3d__meshy`)  -  4 workflow(s)  -  source: mixed
- execution: api (API nodes: GeminiNanoBanana2, MeshyImageToModelNode, MeshyMultiImageToModelNode, MeshyTextToModelNode, TripoImageToModelNode)
- when to use: Use to generate a 3D model using Meshy.
- example request: "build a 3d workflow using Meshy"
- description: API image-to-3D via Meshy 6. 1 image -> 1 3D model output. Generates characters, objects, or mechanical parts with production-quality geometry and clean topology. | API multi-image-to-3D via Meshy 6. 3+ images -> 1 3D model output. More input views yield better detail capture, accurate proportions, and cleaner mesh structure. | API text-to-3D via Meshy 6. Text prompt only -> 1 3D model output. Creates characters, mechanical objects, or game-ready low-poly assets with refined geometry. | Input a single image to automatically generate three orthographic views. Use these multiviews with Meshy to create a textured 3D model.
- member workflows:
    - api_meshy_image_to_model
    - api_meshy_multi_image_to_model
    - api_meshy_text_to_model
    - templates_mjm_image_to_3d
- node clusters (required structure):
    - other operations: SaveGLB
- optional roles: GeminiNanoBanana2, LoadImage, SaveImage, BatchImagesNode, MarkdownNote, MeshyImageToModelNode, MeshyMultiImageToModelNode, MeshyTextToModelNode, Preview3D, TripoImageToModelNode
- unresolved nodes: MarkdownNote

## API / Partner Nodes - 3D / Qwen Image  (`api_partner_nodes_3d__qwen_image`)  -  1 workflow(s)  -  source: official
- execution: api (API nodes: TencentImageToModelNode)
- when to use: Use to generate a 3D model using Hunyuan3D, Qwen Image.
- example request: "build a 3d workflow using Hunyuan3D"
- description: Use one frontal image to generate a consistent and highly detailed 3D model. Model used: Multiangle QWEN Edit + Hunyuan 3D
- member workflows:
    - templates_shane_single_image_to_3d_model
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: CLIPLoader, LoraLoaderModelOnly (x2), UNETLoader, VAELoader
    - conditioning: TextEncodeQwenImageEditPlus (x2)
    - latent / canvas: VAEEncode
    - sampling: KSampler
    - decoding: VAEDecode
    - output: SaveImage
    - other operations: CFGNorm, FluxKontextImageScale, FluxKontextMultiReferenceLatentMethod (x2), MarkdownNote, ModelSamplingAuraFlow, Preview3D, QwenMultiangleCameraNode, TencentImageToModelNode
- paired/multiple required: FluxKontextMultiReferenceLatentMethod x2, LoraLoaderModelOnly x2, TextEncodeQwenImageEditPlus x2
- unresolved nodes: MarkdownNote


# API / Partner Nodes - Text to Image  (`api_partner_nodes_text_to_image`)  -  28 workflow(s), 8 model(s)

## API / Partner Nodes - Text to Image / Generic  (`api_partner_nodes_text_to_image__generic`)  -  14 workflow(s)  -  source: mixed
- execution: api (API nodes: ElevenLabsSpeechToText, GrokImageNode, OpenAIDalle2, OpenAIDalle3, OpenAIGPTImageNodeV2, QuiverTextToSVGNode, RecraftColorRGB, RecraftControls, RecraftTextToVectorNode, RecraftV4TextToImageNode, RecraftV4TextToVectorNode, ReveImageCreateNode)
- when to use: Use to generate an image from a text prompt.
- example request: "build an image workflow"
- description: Create campaign-ready posters, product shots, and multilingual signage using OpenAI's latest model. Upload an optional reference image, write a detailed prompt, and generate high-quality, photorealistic outputs. | Generate a clean, flat vector logo from a text prompt using Recraft V4.1, producing one scalable SVG output with no file input required. Ideal for branding and logo design, vector illustration projects, and creating consistent flat-color graphics for presentations or merchandise. | Generate enhanced images with improved details, text rendering, and creative control using the advanced quality mode in Grok Imagine. | Generate high-quality vector images from text prompts using Recraft's AI vector generator. | Generate images from text prompts using OpenAI Dall-E 2 API. | Generate images from text prompts using OpenAI Dall-E 3 API. | Generate photorealistic and illustrative images from text prompts using Recraft V4.1, producing one high-quality image per generation. This model excels at interpreting short prompts with creative flair, delivering natural photorealism, expressive vectors, and clean illustrations. Ideal for concept art, logo and typography design, and lifestyle product mockups. | Input a text prompt and optional reference images to generate one or more SVG vector graphics. | Input a text prompt to generate a high-resolution image. Use the Recraft V4 model for enhanced realism, text accuracy, and detailed vector graphics. Output a 1024x1024 or 2048x2048 image based on your selected version. | Input text prompts to generate clean, editable vector SVG graphics. Create logos, icons, or illustrations with structured paths suitable for design tools. | Input text prompts to generate high-quality images quickly using the Grok model. | Input text prompts to generate high-quality images with detailed aesthetics and accurate text rendering. | Local generation via ComfyUI Model. text input -> 1 image output. Processes and generates content using ComfyUI workflows. | Upload an audio or video file to transcribe its speech into accurate, editable text.
- member workflows:
    - api_elevenLabs_speech_to_text
    - api_grok_imagine_image_quality_image_generation
    - api_grok_text_to_image
    - api_openai_dall_e_2_t2i
    - api_openai_dall_e_3_t2i
    - api_openai_gpt_image_2_t2i
    - api_quiver_text_to_svg
    - api_recraft_v4_1_t2i
    - api_recraft_v4_1_text_to_vector
    - api_recraft_v4_t2i
    - api_recraft_v4_text_to_vector
    - api_recraft_vector_gen
    - api_reve_image_create
    - api_t2i_OpenAi_GPT2
- node clusters (required structure):
    - (none resolved)
- optional roles: RecraftColorRGB, MarkdownNote, ElevenLabsSpeechToText, GrokImageNode, LoadAudio, OpenAIDalle2, OpenAIDalle3, OpenAIGPTImageNodeV2, QuiverTextToSVGNode, RecordAudio, RecraftControls, RecraftTextToVectorNode
- unresolved nodes: MarkdownNote

## API / Partner Nodes - Text to Image / Nano-Banana  (`api_partner_nodes_text_to_image__nano_banana`)  -  4 workflow(s)  -  source: mixed
- execution: api (API nodes: GeminiImage2Node, GeminiNanoBanana2V2)
- when to use: Use to generate an image from a text prompt using Nano-Banana, Gemini.
- example request: "build an image workflow using Nano-Banana"
- description: API / cloud generation via Nano Banana 2. text input -> 1 image output. | API / cloud generation via Nano Banana 2. text input -> 1 image output. Processes and generates content using ComfyUI workflows. | Generate images from text descriptions using the ultra-fast Gemini 3.1 Flash-Lite Image model, designed for rapid creation and iteration with no file inputs required. This workflow produces one or more generated images based on your text prompt, with support for interleaved text and image inputs. Ideal for quick concept visualization, rapid prototyping, and iterative design exploration. | Generate images from text prompts using the Nano Banana 2 model, producing one image output with no file inputs required. Ideal for rapid prototyping, concept art generation, and creative exploration.
- member workflows:
    - NanoBanana2_text_to_image
    - api_google_nano_banana2_text_to_image
    - api_nano_banana_2_lite_t2i
    - api_t2i_nanoBananaPro
- node clusters (required structure):
    - (none resolved)
- optional roles: GeminiImage2Node, GeminiNanoBanana2V2, SaveImage, SaveImageAdvanced

## API / Partner Nodes - Text to Image / Ideogram  (`api_partner_nodes_text_to_image__ideogram`)  -  3 workflow(s)  -  source: mixed
- execution: api (API nodes: GeminiNode, IdeogramPImage, IdeogramV3, IdeogramV4)
- when to use: Use to generate an image from a text prompt using Ideogram.
- example request: "build an image workflow using Ideogram"
- description: Generate images from text descriptions using Ideogram's fast P-Image model, which delivers quality comparable to leading image models at significantly lower cost and latency. One text prompt is accepted and one image is output, with controls for quality level and resolution. Ideal for rapid iteration in design workflows, high-volume content production, and cost-sensitive A/B testing of visual concepts. | Input a text prompt in structured JSON format. Generate a high-quality image with precise layout control, text rendering, and color palette support.
- member workflows:
    - api_ideogram_p_image_t2i
    - api_ideogram_v3_t2i
    - api_ideogram_v4_t2i
- node clusters (required structure):
    - (none resolved)
- optional roles: BuildJsonPromptIdeogram, CreateBoundingBoxes, GeminiNode, IdeogramPImage, IdeogramV3, IdeogramV4, MarkdownNote, SaveImage, SaveImageAdvanced
- unresolved nodes: MarkdownNote

## API / Partner Nodes - Text to Image / Kling  (`api_partner_nodes_text_to_image__kling`)  -  2 workflow(s)  -  source: official
- execution: api (API nodes: KlingImageGenerationNode, KlingOmniProImageNode)
- when to use: Use to generate an image from a text prompt using Kling.
- example request: "build an image workflow using Kling"
- description: Generate an image from a text prompt using the Kling 3.0 model. Input your descriptive text to receive a high-quality, prompt-accurate visual output. | Generate high-quality images from text prompts using Kling O1, with support for up to 10 reference images to guide style and content. Features flexible aspect ratios and 1K/2K resolution options.
- member workflows:
    - api_kling_omni_image
    - api_kling_v3_t2i
- node clusters (required structure):
    - output: SaveImage
- optional roles: KlingImageGenerationNode, KlingOmniProImageNode

## API / Partner Nodes - Text to Image / Seedream  (`api_partner_nodes_text_to_image__seedream`)  -  2 workflow(s)  -  source: official
- execution: api (API nodes: ByteDanceSeedreamNode, ByteDanceSeedreamNodeV2)
- when to use: Use to generate an image from a text prompt using Seedream.
- example request: "build an image workflow using Seedream"
- description: Generate images from text prompts using Seedream 5.0 Pro, producing one high-quality output. Ideal for creative concept art, marketing visual mockups, and rapid ideation for design projects. | Input your text prompt to generate a detailed image. This workflow creates a visual representation of your description with precise control over style and layout.
- member workflows:
    - api_bytedance_seedream_5_0_lite_t2i
    - api_bytedance_seedream_5_0_pro_t2i
- node clusters (required structure):
    - (none resolved)
- optional roles: ByteDanceSeedreamNode, ByteDanceSeedreamNodeV2, SaveImage, SaveImageAdvanced

## API / Partner Nodes - Text to Image / Flux Krea  (`api_partner_nodes_text_to_image__flux_krea`)  -  1 workflow(s)  -  source: official
- execution: api (API nodes: Krea2ImageNode)
- when to use: Use to generate an image from a text prompt using Flux Krea.
- example request: "build an image workflow using Flux Krea"
- description: Input a text prompt describing your desired scene. Generate four aesthetic, high-quality images that interpret your prompt with creative variety.
- member workflows:
    - api_krea2_t2i
- node clusters (required structure):
    - output: SaveImage
    - other operations: Krea2ImageNode

## API / Partner Nodes - Text to Image / WAN  (`api_partner_nodes_text_to_image__wan`)  -  1 workflow(s)  -  source: official
- execution: api (API nodes: WanTextToImageApi)
- when to use: Use to generate an image from a text prompt using Flux, WAN.
- example request: "build an image workflow using Flux"
- description: Generate images with excellent prompt following and visual quality using FLUX.1 Pro.
- member workflows:
    - api_wan_text_to_image
- node clusters (required structure):
    - output: SaveImage
    - other operations: MarkdownNote, WanTextToImageApi
- unresolved nodes: MarkdownNote

## API / Partner Nodes - Text to Image / Z-Image  (`api_partner_nodes_text_to_image__z_image`)  -  1 workflow(s)  -  source: custom
- execution: api (API nodes: OpenRouterLLMNode)
- when to use: Use to generate a video using Z-Image.
- example request: "build a video workflow using Z-Image"
- description: Local generation via ComfyUI Model. text input -> 1 video output. Processes and generates content using ComfyUI workflows.
- member workflows:
    - story_refs_only
- node clusters (required structure):
    - model loading: CLIPLoader, UNETLoader, VAELoader
    - conditioning: CLIPTextEncode (x3)
    - latent / canvas: EmptySD3LatentImage
    - sampling: KSampler (x2)
    - decoding: VAEDecode (x2)
    - other operations: AgentYPython (x2), ModelSamplingAuraFlow, OpenRouterLLMNode (x2), PrimitiveStringMultiline
- paired/multiple required: CLIPTextEncode x3, AgentYPython x2, KSampler x2, OpenRouterLLMNode x2, VAEDecode x2


# Image Tools  (`image_tools`)  -  26 workflow(s), 4 model(s)

## Image Tools / Generic  (`image_tools__generic`)  -  22 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate an image.
- example request: "build an image workflow"
- description: Adds a glow/bloom effect around bright image areas via GPU fragment shader. | Adds lens-style chromatic aberration (color fringing) using a real-time GPU fragment shader. | Adds procedural film grain texture for a cinematic look via GPU fragment shader. | Adjusts black point, white point, and gamma for tonal range control via GPU shader. | Adjusts hue, saturation, and lightness of an image using a real-time GPU fragment shader. | Adjusts image brightness and contrast using a real-time GPU fragment shader. | Adjusts saturation, temperature, tint, and vibrance using a real-time GPU fragment shader. | Applies Gaussian, Box, or Radial blur to soften images and create stylized depth or motion effects. | Applies bilateral (edge-preserving) blur to soften images while retaining detail. | Apply a pixel sorting algorithm to create glitch art. Control the effect direction, threshold, and blending with the original image. Outputs a stylized, smeared version of the input. | Balances colors across shadows, midtones, and highlights using a real-time GPU fragment shader. | Combine four input images into a 2x2 grid. Automatically resizes mismatched images and outputs a single 2048x2048 image. | Enhances edge contrast via unsharp masking for a sharper image appearance. | Fine-tunes tone and color with per-channel curve adjustments using a real-time GPU fragment shader. | Input your text prompt and optionally an image, audio, or video. Generate text output with configurable reasoning, coding, and multilingual support. | Interactive walkthrough of core image and mask nodes - create and refine masks, combine overlapping masks with different operations, and composite images using feathered masks. No models required. | Manipulates individual RGBA channels for masking, compositing, and channel effects. | Sharpens image details using a GPU fragment shader for enhanced clarity. | Side-by-side demo of built-in blueprint color-grading subgraphs.  | Splits an image into a 2×2 grid of four equal tiles. | Splits an image into a 3×3 grid of nine equal tiles. | Splits an image into a configurable columns×rows grid of equal tiles for tiled generation or processing.
- member workflows:
    - basic_image_color_adjustment
    - basic_mask_operations_and_compositing
    - brightness_and_contrast
    - chromatic_aberration
    - color_adjustment
    - color_balance
    - color_curves
    - crop_images_2x2
    - crop_images_3x3
    - edge_preserving_blur
    - film_grain
    - glow
    - hue_and_saturation
    - image_blur
    - image_channels
    - image_levels
    - llm_gemma4_text_gen
    - sharpen
    - split_image_grid_to_tiles
    - templates_purz_pixel_sort_image
    - unsharp_mask
    - utility_image_stitch
- node clusters (required structure):
    - (none resolved)
- optional roles: MaskPreview, PreviewImage, GLSLShader, ImageCropV2, MarkdownNote, MaskComposite, CustomCombo, CurveEditor, LoadImage, ImageStitch, EmptyImage, FeatherMask
- unresolved nodes: FL_PixelSort, MarkdownNote

## Image Tools / Qwen Image  (`image_tools__qwen_image`)  -  2 workflow(s)  -  source: official
- execution: local
- when to use: Use to caption an image as text using Qwen Image.
- example request: "build a text workflow using Qwen Image"
- description: Generate text with visual understanding using Qwen3-VL models, processing one input image to produce contextual text responses. Ideal for image captioning, visual question answering, and multimodal content generation. | Use the Qwen3.5 model to analyze an input image and generate descriptive text prompts. This workflow performs image captioning and reverse prompt engineering.
- member workflows:
    - llm_qwen3_5_text_gen
    - llm_qwen3vl_text_gen
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: CLIPLoader
    - other operations: MarkdownNote, PreviewAny, TextGenerate
- unresolved nodes: MarkdownNote

## Image Tools / BiRefNet  (`image_tools__birefnet`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to remove the background from an image using BiRefNet.
- example request: "build an image workflow using BiRefNet"
- description: Removes or replaces image backgrounds using BiRefNet segmentation and alpha compositing.
- member workflows:
    - remove_background_birefnet
- node clusters (required structure):
    - other operations: InvertMask, JoinImageWithAlpha, LoadBackgroundRemovalModel, RemoveBackground

## Image Tools / Z-Image  (`image_tools__z_image`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate an image using Z-Image.
- example request: "build an image workflow using Z-Image"
- description: Adds customizable glitch and tearing effects to images. Control distortion intensity, chromatic aberration, and pattern randomness. Outputs a stylistically distorted image.
- member workflows:
    - templates_purz_image_glitch
- node clusters (required structure):
    - inputs: LoadImage
    - output: SaveImage
    - other operations: FL_Glitch, MarkdownNote
- unresolved nodes: FL_Glitch, MarkdownNote


# Audio  (`audio`)  -  23 workflow(s), 5 model(s)

## Audio / ACE-Step  (`audio__ace_step`)  -  11 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate audio from a text prompt using ACE-Step.
- example request: "build an audio workflow using ACE-Step"
- description: Edit existing songs to change style and lyrics using ACE-Step v1 M2M. | Generate high-quality audio from text prompts using the 4B parameter ACE-Step 1.5 XL model.  | Generate high-quality music from text prompts using a 4B parameter SFT model. Control output with CFG for precise prompt adherence.  | Generate high-quality music from text prompts using the distilled 4B ACE-Step model. Produces commercial-ready audio in just 8 inference steps without CFG. | Generate instrumental music from text prompts using ACE-Step v1. | Generate songs from text prompts using ACE-Step v1 | Generate songs with vocals from text prompts using ACE-Step v1, supporting multilingual and style customization. | Generates audio/music from text prompts using ACE-Step 1.5, a diffusion-based audio generation model. | Input a text prompt describing the music style and optional lyrics. Generate a full, high-quality audio song in under 10 seconds on consumer hardware. | Input a text prompt to generate music. This 4B model version offers stronger audio understanding and composition capabilities compared to smaller variants. | Input style tags and lyrics to generate a full song. The workflow uses the ACE-Step 1.5 model to produce commercial-grade music in under 10 seconds on consumer hardware.
- member workflows:
    - 05_audio_ace_step_1_t2a_song_subgraphed
    - audio_ace_step1_5_xl_base
    - audio_ace_step1_5_xl_sft
    - audio_ace_step1_5_xl_turbo
    - audio_ace_step_1_5_checkpoint
    - audio_ace_step_1_5_split
    - audio_ace_step_1_5_split_4b
    - audio_ace_step_1_m2m_editing
    - audio_ace_step_1_t2a_instrumentals
    - audio_ace_step_1_t2a_song
    - text_to_audio_ace_step_1_5
- node clusters (required structure):
    - conditioning: ConditioningZeroOut
    - sampling: KSampler
    - decoding: VAEDecodeAudio
- optional roles: MarkdownNote, CheckpointLoaderSimple, DualCLIPLoader, EmptyAceStep1.5LatentAudio, EmptyAceStepLatentAudio, LatentApplyOperationCFG, LatentOperationTonemapReinhard, LoadAudio, ModelSamplingAuraFlow, ModelSamplingSD3, Note, SaveAudioMP3
- unresolved nodes: MarkdownNote, Note, PrimitiveNode

## Audio / Generic  (`audio__generic`)  -  6 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate audio from a text prompt.
- example request: "build an audio workflow"
- description: Input Music -> Separate Vocals / Bass / Drums / Other | Load an audio file and separate it into vocal and instrumental stems using the MelBandRoFormer model. Outputs two MP3 files for isolated vocals and background music. | Upload a short voice clip and input text to generate new speech in the cloned voice. | Upload a short voice sample and input your text prompt. Select a target language to generate spoken audio in multiple languages using the cloned reference voice. | Upload an audio clip and a short voice reference to generate a converted audio output that clones the target voice while preserving the original timing and performance. | Upload voice samples and enter a multi-speaker dialog script. Generate a conversation audio file with cloned voices for each speaker.
- member workflows:
    - audio-chatterbox_tts
    - audio-chatterbox_tts_dialog
    - audio-chatterbox_tts_multilingual
    - audio-chatterbox_vc
    - audio_melbandroformer_audio_separation
    - utility-audioseparation
- node clusters (required structure):
    - output: SaveAudioMP3
    - other operations: LoadAudio, MarkdownNote
- optional roles: AudioCrop, AudioStemSeparate, FL_ChatterboxDialogTTS, FL_ChatterboxMultilingualTTS, FL_ChatterboxTTS, FL_ChatterboxVC, MelBandRoFormerModelLoader, MelBandRoFormerSampler
- unresolved nodes: AudioCrop, AudioStemSeparate, FL_ChatterboxDialogTTS, FL_ChatterboxMultilingualTTS, FL_ChatterboxTTS, FL_ChatterboxVC, MarkdownNote, MelBandRoFormerModelLoader, MelBandRoFormerSampler

## Audio / Qwen Image  (`audio__qwen_image`)  -  3 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate audio from a text prompt using Qwen Image, Stable Audio.
- example request: "build an audio workflow using Qwen Image"
- description: Generates music, instrument loops, sound effects, and one-shots from text using Stable Audio 3 Medium, with optional Qwen 3.5 category-based prompt expansion (Music, Instrument, SFX, One-shot). | Generates music, instrument loops, sound effects, and one-shots from text using the Stable Audio 3 Medium base checkpoint, with optional Qwen 3.5 category-based prompt expansion (Music, Instrument, SFX, One-shot). | Input a short text description of a sound, music, or effect. The workflow expands your prompt with Qwen and generates a stereo audio clip from Stable Audio 3.
- member workflows:
    - audio_generation_stable_audio_3_medium
    - audio_generation_stable_audio_3_medium_base
    - audio_stable_audio_3_medium_base
- node clusters (required structure):
    - model loading: CLIPLoader (x2), CheckpointLoaderSimple
    - conditioning: CLIPTextEncode (x2)
    - latent / canvas: EmptyLatentAudio
    - sampling: KSampler
    - decoding: VAEDecodeAudio
    - other operations: ComfyMathExpression, ComfySwitchNode, CustomCombo, JsonExtractString, PreviewAny (x2), PrimitiveBoolean, PrimitiveFloat, PrimitiveStringMultiline, StringReplace (x3), TextGenerate
- paired/multiple required: CLIPLoader x2, CLIPTextEncode x2
- optional roles: MarkdownNote, SaveAudioMP3
- unresolved nodes: MarkdownNote

## Audio / Stable Audio  (`audio__stable_audio`)  -  2 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate audio from a text prompt using Stable Audio.
- example request: "build an audio workflow using Stable Audio"
- description: Generate audio from text prompts using Stable Audio. | Input a short text idea, optional duration, seed, and category. Generate stereo audio (music, SFX, or instruments) using Stable Audio 3 with optional AI-driven text expansion.
- member workflows:
    - audio_stable_audio_3_medium
    - audio_stable_audio_example
- node clusters (required structure):
    - model loading: CLIPLoader, CheckpointLoaderSimple
    - conditioning: CLIPTextEncode (x2)
    - latent / canvas: EmptyLatentAudio
    - sampling: KSampler
    - decoding: VAEDecodeAudio
    - output: SaveAudioMP3
    - other operations: MarkdownNote
- paired/multiple required: CLIPTextEncode x2
- optional roles: CustomCombo, TextGenerate
- unresolved nodes: MarkdownNote

## Audio / LTX-2  (`audio__ltx_2`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate audio from a text prompt using LTX-2.
- example request: "build an audio workflow using LTX-2"
- description: Upload an audio file and a starting image frame. Generate a video synchronized to the audio using the LTX-2 model.
- member workflows:
    - video_ltx_2_audio_to_video
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: DualCLIPLoader, UNETLoader, VAELoaderKJ (x2)
    - conditioning: CFGGuider (x5), CLIPTextEncode (x2), ConditioningZeroOut, LTXVConditioning
    - latent / canvas: LTXVAudioVAEEncode (x5), VAEEncode (x4)
    - sampling: KSamplerSelect (x5), SamplerCustomAdvanced (x5)
    - decoding: VAEDecodeTiled (x5)
    - output: SaveVideo (x2), VHS_VideoCombine (x4)
    - other operations: AudioCrop, AudioSeparation, CreateVideo (x2), EmptyLTXVLatentVideo, FloatConstant, GetImageRangeFromBatch (x4), ImageBatchExtendWithOverlap (x4), ImageResizeKJv2, LTX2SamplingPreviewOverride, LTX2_NAG, LTXVAddGuideMulti (x4), LTXVAudioVideoMask (x4), LTXVChunkFeedForward, LTXVConcatAVLatent (x5), LTXVCropGuides (x4), LTXVImgToVideoInplaceKJ, LTXVPreprocess, LTXVScheduler (x5), LTXVSeparateAVLatent (x5), LoadAudio, MarkdownNote (x4), PrimitiveFloat, RandomNoise (x5), Reroute (x8), SetLatentNoiseMask, SolidMask, TrimAudioDuration (x5)
- paired/multiple required: CFGGuider x5, KSamplerSelect x5, LTXVAudioVAEEncode x5, LTXVConcatAVLatent x5, LTXVScheduler x5, LTXVSeparateAVLatent x5, RandomNoise x5, SamplerCustomAdvanced x5, TrimAudioDuration x5, VAEDecodeTiled x5, GetImageRangeFromBatch x4, ImageBatchExtendWithOverlap x4, LTXVAddGuideMulti x4, LTXVAudioVideoMask x4, LTXVCropGuides x4, MarkdownNote x4, VAEEncode x4, VHS_VideoCombine x4, CLIPTextEncode x2, CreateVideo x2, SaveVideo x2, VAELoaderKJ x2
- unresolved nodes: AudioCrop, AudioSeparation, MarkdownNote, Reroute


# Image Edit with ControlNet  (`image_edit_with_controlnet`)  -  18 workflow(s), 7 model(s)

## Image Edit with ControlNet / Z-Image  (`image_edit_with_controlnet__z_image`)  -  7 workflow(s)  -  source: mixed
- execution: local
- when to use: Use to generate an image guided by a control map (canny/depth/pose) using Z-Image.
- example request: "build an image workflow using Z-Image"
- description: Generates an image from a Canny edge map using Z-Image-Turbo, with text conditioning. | Generates an image from a depth map using Z-Image-Turbo with text conditioning. | Generates an image from pose keypoints using Z-Image-Turbo with text conditioning. | Generates images from a text prompt and ControlNet conditioning (e.g. depth, canny) using Z-Image-Turbo. | Learn how to guide diffusion for precise image editing with inpainting and controlnet using Z Image Turbo. | Load an image, draw a mask over the area to edit, and input a prompt. Generate a new image where only the masked region is redrawn according to your prompt. | [Local] image editing via Z-Image-Turbo. 1 image input -> 1 image output. Uses ControlNet for precise and controlled image editing.
- member workflows:
    - canny_to_image_z_image_turbo
    - controlnet_z_image_turbo
    - depth_to_image_z_image_turbo
    - gsc_creator_2_2
    - gsl_creator_2
    - image_z_image_turbo_fun_union_controlnet
    - pose_to_image_z_image_turbo
- node clusters (required structure):
    - model loading: CLIPLoader, ModelPatchLoader, UNETLoader, VAELoader
    - conditioning: CLIPTextEncode, ConditioningZeroOut
    - sampling: KSampler
    - decoding: VAEDecode
    - other operations: ModelSamplingAuraFlow
- optional roles: MarkdownNote, ImageResize+, MaskPreview, PreviewImage, AIO_Preprocessor, BasicGuider, BasicScheduler, Canny, DifferentialDiffusion, DisableNoise, EmptySD3LatentImage, ImageCompare
- unresolved nodes: ImageResize+, MarkdownNote

## Image Edit with ControlNet / Qwen Image  (`image_edit_with_controlnet__qwen_image`)  -  4 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate an image guided by a control map (canny/depth/pose) using Qwen Image.
- example request: "build an image workflow using Qwen Image"
- description: Control image generation using Qwen-Image ControlNet models. Supports canny, depth, and inpainting controls through model patching. | Generate images with Qwen-Image InstantX ControlNet, supporting canny, soft edge, depth, pose | Generate images with precise structural control using Qwen-Image's unified ControlNet LoRA. Supports multiple control types including canny, depth, lineart, softedge, normal, and openpose for diverse creative applications. | Upload an image and select a control type from Canny, HED, Depth, Pose, MLSD, Scribble, or Grayscale. Generate a new image guided by the chosen structural condition.
- member workflows:
    - image_qwen_Image_2512_controlnet
    - image_qwen_image_controlnet_patch
    - image_qwen_image_instantx_controlnet
    - image_qwen_image_union_control_lora
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: CLIPLoader, LoraLoaderModelOnly, UNETLoader, VAELoader
    - conditioning: CLIPTextEncode (x2)
    - sampling: KSampler
    - decoding: VAEDecode
    - output: PreviewImage, SaveImage
    - other operations: MarkdownNote (x2), ModelSamplingAuraFlow
- paired/multiple required: MarkdownNote x2, CLIPTextEncode x2
- optional roles: Note, ReferenceLatent, VAEEncode, BasicGuider, BasicScheduler, Canny, ControlNetApplyAdvanced, ControlNetLoader, DisableNoise, EmptySD3LatentImage, FluxKontextImageScale, ImageInvert
- unresolved nodes: MarkdownNote, Note, Reroute

## Image Edit with ControlNet / Anima  (`image_edit_with_controlnet__anima`)  -  2 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate an image guided by a control map (canny/depth/pose) using Anima.
- example request: "build an image workflow using Anima"
- description: Apply lightweight, LoRA-like conditional control to Anima-Base v1.0 anime-style images using ControlNet-LLLite, accepting one conditioning input and one optional mask for inpainting to produce a single generated output. Ideal for anime inpainting with dynamic masking, style transfer from lineart or grayscale sketches, and controlled character generation in multi-scene compositions. | Generate anime-style illustrations from a depth map using the Anima LLLite model, which applies a lightweight ControlNet correction for precise spatial control. Input 1 image to produce 2 image outputs plus a comparison view. Ideal for 3D scene reconstruction, VFX depth passes, and AR asset preparation.
- member workflows:
    - image_anima_lllite_any_control_to_image
    - image_anima_lllite_depth_control_to_image
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: CLIPLoader, LoraLoaderModelOnly, ModelPatchLoader, UNETLoader, VAELoader
    - conditioning: CLIPTextEncode (x2)
    - latent / canvas: EmptyLatentImage
    - sampling: KSampler
    - decoding: VAEDecode
    - output: PreviewImage, SaveImage
    - other operations: AnimaLLLiteApply, ComfySwitchNode (x3), GetImageSize, ImageCompare, MarkdownNote, PrimitiveBoolean, PrimitiveFloat (x2), PrimitiveInt (x2), ResizeImageMaskNode
- paired/multiple required: CLIPTextEncode x2
- optional roles: Canny, DA3Inference, DA3Render, ImageInvert, LoadDA3Model
- unresolved nodes: MarkdownNote

## Image Edit with ControlNet / Generic  (`image_edit_with_controlnet__generic`)  -  2 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate an image.
- example request: "build an image workflow"
- description: Generate images guided by blurred reference images using SD 3.5. | Generate images guided by edge detection using SD 3.5 Canny ControlNet.
- member workflows:
    - sd3.5_large_blur
    - sd3.5_large_canny_controlnet_example
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: CheckpointLoaderSimple
    - conditioning: CLIPTextEncode, ConditioningZeroOut, ControlNetApplyAdvanced, ControlNetLoader
    - latent / canvas: EmptySD3LatentImage
    - sampling: KSampler
    - decoding: VAEDecode
    - output: SaveImage
    - other operations: MarkdownNote
- optional roles: Canny, ImageScale, PreviewImage
- unresolved nodes: MarkdownNote

## Image Edit with ControlNet / Flux  (`image_edit_with_controlnet__flux`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate an image guided by a control map (canny/depth/pose) using Flux.
- example request: "build an image workflow using Flux"
- description: Generate images guided by edge detection using Flux.1 Canny.
- member workflows:
    - flux_canny_model_example
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: DualCLIPLoader, UNETLoader, VAELoader
    - conditioning: CLIPTextEncode, ConditioningZeroOut, FluxGuidance, InstructPixToPixConditioning
    - sampling: KSampler
    - decoding: VAEDecode
    - output: PreviewImage, SaveImage
    - other operations: Canny, MarkdownNote
- unresolved nodes: MarkdownNote

## Image Edit with ControlNet / Lotus  (`image_edit_with_controlnet__lotus`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate an image using Lotus.
- example request: "build an image workflow using Lotus"
- description: Generate images guided by depth information using SD 3.5.
- member workflows:
    - sd3.5_large_depth
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: CheckpointLoaderSimple, UNETLoader, VAELoader
    - conditioning: BasicGuider, BasicScheduler, CLIPTextEncode, ConditioningZeroOut, ControlNetApplyAdvanced, ControlNetLoader, LotusConditioning
    - latent / canvas: EmptySD3LatentImage, VAEEncode (x2)
    - sampling: KSampler, KSamplerSelect, SamplerCustomAdvanced
    - decoding: VAEDecode (x2)
    - output: PreviewImage, SaveImage
    - other operations: DisableNoise, ImageInvert, ImageScaleToTotalPixels, MarkdownNote (x3), SetFirstSigma
- paired/multiple required: MarkdownNote x3, VAEDecode x2, VAEEncode x2
- unresolved nodes: MarkdownNote

## Image Edit with ControlNet / WAN  (`image_edit_with_controlnet__wan`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate an image guided by a control map (canny/depth/pose) using Qwen Image, WAN.
- example request: "build an image workflow using Qwen Image"
- description: Describe the elements you want in the image and decompose it precisely from the image.
- member workflows:
    - image_qwen_image_layered_control
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: CLIPLoader, UNETLoader, VAELoader
    - conditioning: CLIPTextEncode (x2)
    - latent / canvas: VAEEncode
    - sampling: KSampler
    - decoding: VAEDecode
    - output: SaveImage
    - other operations: EmptyQwenImageLayeredLatentImage, GetImageSize, ImageScaleToMaxDimension, LatentCutToBatch, MarkdownNote (x2), ModelSamplingAuraFlow, ReferenceLatent (x2)
- paired/multiple required: CLIPTextEncode x2, MarkdownNote x2, ReferenceLatent x2
- unresolved nodes: MarkdownNote


# Preprocessors / Estimation  (`preprocessors_estimation`)  -  18 workflow(s), 7 model(s)

## Preprocessors / Estimation / SDPose  (`preprocessors_estimation__sdpose`)  -  4 workflow(s)  -  source: official
- execution: local
- when to use: Use to estimate a pose map using SDPose.
- example request: "build an image workflow using SDPose"
- description: Detects multiple people in an image and outputs per-person pose keypoints, skeleton renders, and bounding boxes using SDPose. | Extracts human pose keypoints and stick-figure visuals from an image using SDPose-OOD, with optional bounding-box input per subject. | Extracts multi-person pose keypoints and skeleton frame sequences from video using SDPose with built-in person detection. | Upload an image to extract pose keypoints and generate a corresponding pose map using the SDPose-OOD model.
- member workflows:
    - image_to_pose_map_sdpose_multi_person
    - image_to_pose_map_sdpose_ood
    - utility_sdpose_ood_image_to_pose
    - video_to_pose_map_sdpose_multi_person
- node clusters (required structure):
    - model loading: CheckpointLoaderSimple
    - other operations: ResizeImageMaskNode, SDPoseDrawKeypoints, SDPoseKeypointExtractor
- optional roles: GetVideoComponents, LoadImage, MarkdownNote, RTDETR_detect, SaveImage, UNETLoader
- unresolved nodes: MarkdownNote

## Preprocessors / Estimation / Depth Anything  (`preprocessors_estimation__depth_anything`)  -  3 workflow(s)  -  source: official
- execution: local
- when to use: Use to estimate a depth map using Depth Anything.
- example request: "build an image workflow using Depth Anything"
- description: This subgraph processes a video input through Depth Anything 3 to produce temporally consistent depth maps for each frame, outputting a depth video. It is ideal for video content requiring spatial geometry estimation, such as 3D reconstruction, SLAM, or novel view synthesis from moving cameras. The model uses a plain transformer backbone trained with a depth-ray representation, supporting any number of views without requiring known camera poses. | This subgraph takes an input image and produces a depth map using the Depth Anything 3 model, which recovers spatially consistent geometry from any number of views. It is ideal for single or multi-view images, videos, and 3D scenes where accurate depth estimation is needed for tasks like SLAM, novel view synthesis, or spatial perception. The model uses a plain transformer backbone and supports both monocular and multi-view inputs without. | Upload 1 image. Generate a depth map using Depth Anything 3 and view a side-by-side comparison of the original and depth output. Ideal for 3D scene reconstruction, AR/VR asset preparation, and visual effects depth passes.
- member workflows:
    - image_depth_estimation_depth_anything_3
    - utility_depth_anything3_image_depth_estimation
    - video_depth_estimation_depth_anything_3
- node clusters (required structure):
    - other operations: DA3Inference, DA3Render, LoadDA3Model
- optional roles: MarkdownNote, GetVideoComponents, ImageCompare, LoadImage, PreviewImage, Video Slice
- unresolved nodes: MarkdownNote

## Preprocessors / Estimation / MediaPipe  (`preprocessors_estimation__mediapipe`)  -  3 workflow(s)  -  source: official
- execution: local
- when to use: Use to detect facial landmarks using MediaPipe.
- example request: "build a 3d workflow using MediaPipe"
- description: Detects facial landmarks from a video using MediaPipe, outputting landmark data, face bounding boxes, and an optional face-region mask. | Detects facial landmarks from an image using MediaPipe, outputting landmark data, face bounding boxes, and an optional face-region mask. | Input an image and detect up to 6 facial landmarks per face, enabling ultrafast multi-face detection
- member workflows:
    - image_face_detection_mediapipe
    - utility_face_detection_mediapipe
    - video_face_detection_mediapipe
- node clusters (required structure):
    - other operations: LoadMediaPipeFaceLandmarker, MediaPipeFaceLandmarker, MediaPipeFaceMask
- optional roles: MarkdownNote, PreviewImage, DrawBBoxes, GetVideoComponents, LoadImage, MaskPreview, MediaPipeFaceMeshVisualize, Video Slice
- unresolved nodes: MarkdownNote

## Preprocessors / Estimation / MoGe  (`preprocessors_estimation__moge`)  -  3 workflow(s)  -  source: official
- execution: local
- when to use: Use to estimate a depth map using MoGe.
- example request: "build an image workflow using MoGe"
- description: Estimates monocular depth from an input image using MoGe, outputting both raw and colorized depth maps plus a mask. | Estimates monocular depth from an input video using MoGe, outputting both raw and colorized depth maps plus a mask. | Upload a single RGB image and adjust inference resolution and batch size. Generate a colored depth preview and raw depth map,
- member workflows:
    - image_depth_estimation_moge
    - utility_moge_depth_estimation
    - video_depth_estimation_moge
- node clusters (required structure):
    - other operations: ComfyMathExpression, ComfySwitchNode (x2), GetImageSize, ImageToMask, LoadMoGeModel, MoGeInference, MoGeRender (x3), ResizeImagesByLongerEdge
- paired/multiple required: MoGeRender x3
- optional roles: MarkdownNote, PreviewImage, GetVideoComponents, LoadImage, MaskPreview
- unresolved nodes: MarkdownNote

## Preprocessors / Estimation / Lotus  (`preprocessors_estimation__lotus`)  -  2 workflow(s)  -  source: official
- execution: local
- when to use: Use to estimate a depth map using Lotus.
- example request: "build an image workflow using Lotus"
- description: Estimates a monocular depth map from an input image using the Lotus depth estimation model. | Image to Depth Map (Lotus) blueprint
- member workflows:
    - image_depth_estimation_lotus_depth
    - image_to_depth_map_lotus
- node clusters (required structure):
    - model loading: UNETLoader, VAELoader
    - conditioning: BasicGuider, BasicScheduler, LotusConditioning
    - latent / canvas: VAEEncode
    - sampling: KSamplerSelect, SamplerCustomAdvanced
    - decoding: VAEDecode
    - other operations: DisableNoise, ImageInvert, SetFirstSigma

## Preprocessors / Estimation / SAM3  (`preprocessors_estimation__sam3`)  -  2 workflow(s)  -  source: official
- execution: local
- when to use: Use to segment an image using SAM3.
- example request: "build an image workflow using SAM3"
- description: Segments images into masks using Meta SAM3 from text prompts, points, or boxes. | Segments video into temporally consistent masks using Meta SAM3 from text or interactive prompts.
- member workflows:
    - image_segmentation_sam3
    - video_segmentation_sam3
- node clusters (required structure):
    - model loading: CheckpointLoaderSimple
    - conditioning: CLIPTextEncode
    - other operations: SAM3_Detect
- optional roles: GetVideoComponents, Note
- unresolved nodes: Note

## Preprocessors / Estimation / BiRefNet  (`preprocessors_estimation__birefnet`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to remove the background from an image using BiRefNet.
- example request: "build an image workflow using BiRefNet"
- description: Upload an image with any background. Generate a version with the background removed and a precision segmentation mask.
- member workflows:
    - utility_birefnet_remove_background
- node clusters (required structure):
    - inputs: LoadImage
    - output: PreviewImage
    - other operations: InvertMask, JoinImageWithAlpha, LoadBackgroundRemovalModel, MarkdownNote, MaskPreview, RemoveBackground
- unresolved nodes: MarkdownNote


# Upscale  (`upscale`)  -  16 workflow(s), 4 model(s)

## Upscale / Generic  (`upscale__generic`)  -  10 workflow(s)  -  source: mixed
- execution: local
- when to use: Use to upscale / enhance an image.
- example request: "build an image workflow"
- description: Local, simple image upscaling via specified ESRGAN model. 1 image -> 1 upscaled image output. Supports various models. | Restore and enhance images using SUPIR's generative prior and text guidance. Accepts image and optional text prompts for intelligent restoration with high-quality results. | Upload a video to upscale and enhance its resolution using the SeedVR2 model for high-definition output. | Upload a video to upscale it using a fast GAN model. The output resolution is determined by your chosen model (e.g., 2x or 4x). For best results, upscale first, then resize to your target resolution. | Upload an image and select an interpolation method. Upscale the image using traditional algorithms for faster processing with minimal detail changes. | Upload an image to upscale it with SeedVR2 and generate a high-definition output. | Upscale and restore video footage using SeedVR2 3B Int8, a one-step diffusion model that enhances resolution while maintaining temporal consistency across frames. This workflow takes one degraded video as input and outputs a single high-resolution, restored video. Ideal for restoring old or degraded footage, upscaling low-resolution videos, and enhancing archival media. | Upscale images using SeedVR2 3B Int8, a one-step diffusion-based video restoration model that produces high-quality results with improved temporal consistency. Ideal for restoring degraded footage, upscaling low-resolution videos, and enhancing archival media. | Upscale images using SeedVR2 7B Int8, a one-step diffusion model that enhances resolution through adversarial training and adaptive window attention. Input 1 image and receive 1 upscaled output with improved detail and clarity. Ideal for restoring low-resolution photos, preparing assets for print, or sharpening lightly degraded digital images. | Upscales video to 4× resolution using a GAN-based upscaling model.
- member workflows:
    - upscale_using_model
    - utility-gan_upscaler
    - utility_image_upscale_supir
    - utility_interpolation_image_upscale
    - utility_seedvr2_3b_int8_upscale_image
    - utility_seedvr2_3b_int8_upscale_video
    - utility_seedvr2_7b_int8_upscale_image
    - utility_seedvr2_image_upscale
    - utility_seedvr2_video_upscale
    - video_upscale_gan_x4
- node clusters (required structure):
    - (none resolved)
- optional roles: CLIPTextEncodeSDXL, MarkdownNote, BOOLConstant, BasicScheduler, CLIPLoader, CheckpointLoaderSimple, ColorTransfer, CreateVideo, EmptyLatentImage, GetVideoComponents, ImageCompare, ImageFromBatch
- unresolved nodes: LayerUtility: If , MarkdownNote, SeedVR2LoadDiTModel, SeedVR2LoadVAEModel, SeedVR2VideoUpscaler, SimpleMath+

## Upscale / Z-Image  (`upscale__z_image`)  -  3 workflow(s)  -  source: official
- execution: local
- when to use: Use to upscale / enhance an image using Z-Image.
- example request: "build an image workflow using Z-Image"
- description: One click workflow to generate a character portrait, refine/add skin details, and upscale to 4k. All done in less than 60 seconds. | Upload an image to upscale it to 2K resolution using the Z-Image-Turbo model. | Upscales images to higher resolution using Z-Image-Turbo.
- member workflows:
    - image_upscale_z_image_turbo
    - templates_hellorob_facegen_skindetail_upscale
    - utility_z_image_turbo_2k_upscaler.app
- node clusters (required structure):
    - model loading: CLIPLoader, UNETLoader, UpscaleModelLoader, VAELoader
    - conditioning: CLIPTextEncode (x2)
    - sampling: KSampler
    - decoding: VAEDecode
    - other operations: ModelSamplingAuraFlow
- paired/multiple required: CLIPTextEncode x2
- optional roles: ImageCompare, LoraLoaderModelOnly, MarkdownNote, PreviewImage, SaveImage, BBoxDetect(FaceParsing), BBoxDetectorLoader(FaceParsing), BBoxListItemSelect(FaceParsing), CheckpointLoaderSimple, ConditioningZeroOut, EmptySD3LatentImage, FaceParse(FaceParsing)
- unresolved nodes: BBoxDetect(FaceParsing), BBoxDetectorLoader(FaceParsing), BBoxListItemSelect(FaceParsing), FaceParse(FaceParsing), FaceParsingModelLoader(FaceParsing), FaceParsingProcessorLoader(FaceParsing), FaceParsingResultsParser(FaceParsing), ImageCropWithBBox(FaceParsing), ImageInsertWithBBox(FaceParsing), LayerUtility: If , MarkdownNote, Note, PrimitiveNode, Reroute, SeedVR2LoadDiTModel, SeedVR2LoadVAEModel, SeedVR2VideoUpscaler, SimpleMath+

## Upscale / Flux  (`upscale__flux`)  -  2 workflow(s)  -  source: mixed
- execution: local
- when to use: Use to upscale / enhance an image using Flux, Z-Image.
- example request: "build an image workflow using Flux"
- description: Input a latent image from a diffusion model and select a PiD checkpoint. Generate a high-resolution decoded image with 4x or 8x upscaling in a single pass. | Local image upscaling using UltimateSD upscale node (this uses a diffusion model for the upscale process, allowing a creative upscale that invents details). Setup with Flux-1 dev fp8. 1 image -> 1 upscaled image output.
- member workflows:
    - upscale_ultimateSD
    - utility_pid_latent_upscale_dit
- node clusters (required structure):
    - conditioning: CLIPTextEncode (x2)
    - output: SaveImage
- paired/multiple required: CLIPTextEncode x2
- optional roles: CLIPLoader, ConditioningZeroOut, MarkdownNote, UNETLoader, VAEDecode, VAELoader, BasicScheduler, CheckpointLoaderSimple, EmptyChromaRadianceLatentImage, EmptySD3LatentImage, ImageCompare, KSampler
- unresolved nodes: MarkdownNote

## Upscale / WAN 2.2  (`upscale__wan_2_2`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to upscale / enhance a video using WAN 2.2.
- example request: "build a video workflow using WAN 2.2"
- description: Upload a video and upscale it to a higher resolution with Wan 2.2
- member workflows:
    - utility_video_upscale
- node clusters (required structure):
    - inputs: LoadVideo
    - model loading: WanVideoLoraSelect, WanVideoModelLoader, WanVideoSetLoRAs, WanVideoVAELoader
    - conditioning: WanVideoTextEncodeCached
    - sampling: WanVideoSampler
    - output: SaveVideo (x2)
    - other operations: ComfyMathExpression (x2), CreateVideo (x2), GetImageSize (x2), GetVideoComponents (x3), ImageFromBatch, ImageResize+, ImageStitch, MarkdownNote (x4), PrimitiveInt (x2), ResizeImageMaskNode, ResolutionSelector, WanVideoDecode, WanVideoEmptyEmbeds, WanVideoEncode, WanVideoTorchCompileSettings
- paired/multiple required: MarkdownNote x4, GetVideoComponents x3, CreateVideo x2, SaveVideo x2
- unresolved nodes: ImageResize+, MarkdownNote


# API / Partner Nodes - First / Last Frame to Video  (`api_partner_nodes_first_last_frame_to_video`)  -  15 workflow(s), 4 model(s)

## API / Partner Nodes - First / Last Frame to Video / Generic  (`api_partner_nodes_first_last_frame_to_video__generic`)  -  7 workflow(s)  -  source: mixed
- execution: api (API nodes: ByteDance2FirstLastFrameNode, ByteDanceCreateImageAsset, ByteDanceFirstLastFrameNode, GeminiImage2Node, GeminiImageNode, Vidu2StartEndToVideoNode)
- when to use: Use to generate a video interpolating between a first and last frame.
- example request: "build a video workflow"
- description: API first-last-frame-to-video via Seedance 2.0 (ByteDance). 1 first frame image + 1 optional last frame image -> 1 video output. Generates video interpolated between keyframes with precise motion control. | Create smooth video transitions between start and end frames with cinematic camera movements, multi-subject consistency. | Generate cinematic video transitions between start and end frames with fluid motion, scene consistency, and professional polish using ByteDance's Seedance model. | Upload a reference image of a real person for identity verification and generate a personalized video with first and last frame control using Seedance2.0 FLF2V. | Upload a start frame and end frame, and Seedance 1.5 Pro automatically generates a smooth video transition with synchronized audio between them. | Upload the first and last frames of your video. Generate a high-quality video sequence using the Seedance2.0 model. | Upload your logotype and apply a texture + elements for on brand asset
- member workflows:
    - api_bytedance_flf2v
    - api_bytedance_seedance1_5_flf2v
    - api_seedance2_0_flf2v
    - api_seedance2_0_flf2v_real_human
    - api_seedance2_i2v_flf
    - api_vidu_q2_flf2v
    - templates-textured_logotype-v2.1
- node clusters (required structure):
    - inputs: LoadImage (x2)
- paired/multiple required: LoadImage x2
- optional roles: MarkdownNote, ByteDanceCreateImageAsset, SaveImage, ByteDance2FirstLastFrameNode, ByteDanceFirstLastFrameNode, GeminiImage2Node, GeminiImageNode, GetVideoComponents, ImageBatch, ResizeAndPadImage, SaveVideo, VHS_VideoCombine
- unresolved nodes: MarkdownNote

## API / Partner Nodes - First / Last Frame to Video / Kling  (`api_partner_nodes_first_last_frame_to_video__kling`)  -  4 workflow(s)  -  source: mixed
- execution: api (API nodes: GeminiNode, KlingFirstLastFrameNode, KlingOmniProFirstLastFrameNode)
- when to use: Use to generate a video interpolating between a first and last frame using Kling.
- example request: "build a video workflow using Kling"
- description: API first-last-frame-to-video via Kling O3 (Kling 3.0). Up to 4 reference/keyframe images -> 1 video output. Generates videos with precise semantic control, longer duration, and improved narrative coherence. | Input a first and last frame image to generate a continuous video sequence with multi-shot generation, precise element control, and support for multilingual prompts. | Upload 8 images (in order) to be used as keyframes for 7 Kling 3.0 FL2V videos. | Upload an image to generate a unique, looping AI video. The workflow uses an LLM to create prompts, employs Kling3.0 for video generation, and stitches the clips into a seamless final loop.
- member workflows:
    - api_kling_o3_flf2v
    - api_kling_v3_flf2v
    - template_contact_sheet-step_3.app
    - templates_mjm_airt_machine_api
- node clusters (required structure):
    - inputs: LoadImage
- optional roles: ImageFromBatch, KSampler, LoraLoaderModelOnly, VAEDecode, BatchImagesNode, GeminiNode, KlingFirstLastFrameNode, SaveVideo, CLIPTextEncode, ConditioningZeroOut, EmptySD3LatentImage, GetVideoComponents
- unresolved nodes: MarkdownNote, Note, PrimitiveNode, Reroute

## API / Partner Nodes - First / Last Frame to Video / Anima  (`api_partner_nodes_first_last_frame_to_video__anima`)  -  3 workflow(s)  -  source: official
- execution: api (API nodes: ByteDanceFirstLastFrameNode, GeminiImage2Node, GeminiNanoBanana2V2, GeminiNode, MinimaxHailuo03FirstLastFrameNode)
- when to use: Use to generate a video interpolating between a first and last frame using Anima.
- example request: "build a video workflow using Anima"
- description: Generate a video from a first and last frame using MiniMax H3, producing a smooth animation between the two images. You provide 2 images, and the workflow outputs a single video clip. Ideal for creating seamless transitions in animation, visualizing before-and-after transformations, and generating consistent motion for character or scene sequences. | Upload a vector image of your logo, and prompt your desired texture. Generate a textured 3D first and last frame with automated prompting for the final animation. | Upload an image of a device or object to generate start and end frames. The workflow animates the transition to an exploded view and back, outputting a seamless video loop.
- member workflows:
    - api_minimax_h3_flf2v
    - template_eric_exploded_view
    - templates-3D_logo_texture_animation
- node clusters (required structure):
    - inputs: LoadImage
    - output: SaveVideo
- optional roles: GeminiImage2Node, SaveImage, ByteDanceFirstLastFrameNode, GeminiNanoBanana2V2, GetVideoComponents, Note, BatchImagesNode, CreateVideo, GeminiNode, MinimaxHailuo03FirstLastFrameNode
- unresolved nodes: Note

## API / Partner Nodes - First / Last Frame to Video / WAN 2.2  (`api_partner_nodes_first_last_frame_to_video__wan_2_2`)  -  1 workflow(s)  -  source: official
- execution: api (API nodes: GeminiImageNode, GeminiNode)
- when to use: Use to generate a video using WAN 2.2.
- example request: "build a video workflow using WAN 2.2"
- description: Upload a starting image and its prompt to generate a looping video from the first to the last frame.
- member workflows:
    - templates_mjm_looped_restyler
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: CLIPLoader (x2), LoraLoaderModelOnly (x4), UNETLoader (x4), VAELoader (x2)
    - conditioning: CLIPTextEncode (x4)
    - sampling: KSamplerAdvanced (x4)
    - decoding: VAEDecode (x2)
    - output: PreviewImage (x3), SaveVideo
    - other operations: CreateVideo (x3), GeminiImageNode, GeminiNode (x2), GetImageSizeAndCount, GetVideoComponents (x2), ImageBatch, ImageScaleToTotalPixels (x2), ImageStitch, ModelSamplingSD3 (x4), SplitImageWithAlpha, WanFirstLastFrameToVideo (x2)
- paired/multiple required: CLIPTextEncode x4, KSamplerAdvanced x4, LoraLoaderModelOnly x4, ModelSamplingSD3 x4, UNETLoader x4, CreateVideo x3, PreviewImage x3, CLIPLoader x2, GeminiNode x2, GetVideoComponents x2, ImageScaleToTotalPixels x2, VAEDecode x2, VAELoader x2, WanFirstLastFrameToVideo x2


# API / Partner Nodes - Upscale  (`api_partner_nodes_upscale`)  -  15 workflow(s), 5 model(s)

## API / Partner Nodes - Upscale / Generic  (`api_partner_nodes_upscale__generic`)  -  6 workflow(s)  -  source: official
- execution: api (API nodes: HitPawGeneralImageEnhance, HitPawVideoEnhance, RecraftCreativeUpscaleNode, RecraftCrispUpscaleNode, WavespeedFlashVSRNode, WavespeedImageUpscaleNode)
- when to use: Use to upscale / enhance an image.
- example request: "build an image workflow"
- description: Upload a low-quality portrait image and adjust the upscaling factor. Generate a high-fidelity, detailed portrait with enhanced skin textures and facial features. | Upload a low-resolution or noisy image to restore and upscale. Generate a high-resolution output with enhanced details, reduced artifacts, and preserved natural look. | Upload a video to enhance and upscale. Generate a restored output with improved clarity, temporal stability, and optional portrait enhancement. | Upload a video to upscale it to 720p, 1080p, 2K, or 4K. The workflow enhances detail, reduces artifacts, and ensures consistent motion for a high-quality, natural-looking output. | Upload an image to enhance and upscale it. Recraft's AI reconstructs details and improves textures, outputting a higher-quality image with a natural appearance. | Upload an image to upscale its resolution. Generate an enhanced 2K, 4K, or 8K output that preserves details and reduces artifacts in JPEG, PNG, or WEBP format.
- member workflows:
    - api_wavespeed_flshvsr_video_upscale
    - api_wavespeed_image_upscale
    - utility_hitpaw_general_image_enhance
    - utility_hitpaw_video_enhance
    - utility_recraft_creative_image_upscale
    - utility_recraft_crisp_image_upscale
- node clusters (required structure):
    - (none resolved)
- optional roles: MarkdownNote, HitPawGeneralImageEnhance, HitPawVideoEnhance, ImageCompare, LoadImage, LoadVideo, RecraftCreativeUpscaleNode, RecraftCrispUpscaleNode, SaveImage, SaveVideo, WavespeedFlashVSRNode, WavespeedImageUpscaleNode
- unresolved nodes: MarkdownNote

## API / Partner Nodes - Upscale / Magnific  (`api_partner_nodes_upscale__magnific`)  -  3 workflow(s)  -  source: mixed
- execution: api (API nodes: MagnificImageSkinEnhancerNode, MagnificImageUpscalerCreativeNode, MagnificImageUpscalerPreciseV2Node)
- when to use: Use to upscale / enhance an image using Magnific.
- example request: "build an image workflow using Magnific"
- description: API creative image upscaling via Magnific. 1 image -> 1 upscaled image output. Supports up to 16x enlargement with creative detail enhancement. | API precise image upscaling via Magnific. 1 image -> 1 high-resolution image output. Upscales with strict detail preservation and enhanced sharpness. | Enhance skin and overall image quality by uploading your image and selecting a preset to adjust lighting, color grading, and realism.
- member workflows:
    - api_magnific_image_upscale_creative
    - api_magnific_image_upscale_precise
    - api_magnific_skin_enhancer
- node clusters (required structure):
    - inputs: LoadImage
    - output: SaveImage
- optional roles: ImageCompare, MagnificImageSkinEnhancerNode, MagnificImageUpscalerCreativeNode, MagnificImageUpscalerPreciseV2Node

## API / Partner Nodes - Upscale / Topaz  (`api_partner_nodes_upscale__topaz`)  -  3 workflow(s)  -  source: mixed
- execution: api (API nodes: TopazImageEnhance, TopazVideoEnhance)
- when to use: Use to upscale / enhance an image using Topaz.
- example request: "build an image workflow using Topaz"
- description: API video upscaling via Topaz AI. 1 video -> 1 enhanced video output. Supports resolution upscaling (Starlight/Astra Fast model) and frame interpolation (apo-8 model). | Upload a landscape image to upscale and enhance details. Generate a high-resolution output optimized for natural scenery using Topaz Reimagine. | Upload an illustration to upscale using Topaz. Generate a smooth, stylized image with accurate colors, though some artifacts may appear.
- member workflows:
    - api_topaz_video_enhance
    - utility-topaz_landscape_upscaler
    - utility_topaz_illustration_upscale
- node clusters (required structure):
    - (none resolved)
- optional roles: ImageCompare, ImageScaleBy, LoadImage, LoadVideo, MarkdownNote, SaveImage, SaveVideo, TopazImageEnhance, TopazVideoEnhance
- unresolved nodes: MarkdownNote, PrimitiveNode

## API / Partner Nodes - Upscale / Nano-Banana  (`api_partner_nodes_upscale__nano_banana`)  -  2 workflow(s)  -  source: official
- execution: api (API nodes: GeminiImage2Node)
- when to use: Use to upscale / enhance an image using Nano-Banana.
- example request: "build an image workflow using Nano-Banana"
- description: Upload a product image to enhance its detail and sharpness. Generate an upscaled, high-quality output with improved typography and realistic coherence using the Nano Banana Pro model. | Upload a stylized art or illustration. Generate a creatively upscaled 4K image with enhanced detail using the Nano Banana Pro model, ideal for marketing or gaming assets.
- member workflows:
    - utility_nanobanana_pro_illustration_upscale
    - utility_nanobanana_pro_product_upscale
- node clusters (required structure):
    - inputs: LoadImage
    - output: SaveImage
    - other operations: GeminiImage2Node

## API / Partner Nodes - Upscale / Z-Image  (`api_partner_nodes_upscale__z_image`)  -  1 workflow(s)  -  source: custom
- execution: api (API nodes: TopazImageEnhance)
- when to use: Use to upscale / enhance an image using Topaz, Z-Image.
- example request: "build an image workflow using Topaz"
- description: API image enhancement/upscaling via Topaz Reimagine. 1 image -> 1 enhanced image output. Applies face enhancement and detail restoration for professional results.
- member workflows:
    - api_topaz_image_enhance
- node clusters (required structure):
    - inputs: LoadImage
    - output: SaveImage
    - other operations: TopazImageEnhance


# API / Partner Nodes - Audio  (`api_partner_nodes_audio`)  -  13 workflow(s), 3 model(s)

## API / Partner Nodes - Audio / Generic  (`api_partner_nodes_audio__generic`)  -  11 workflow(s)  -  source: official
- execution: api (API nodes: ByteDanceSeedAudio, ElevenLabsAudioIsolation, ElevenLabsInstantVoiceClone, ElevenLabsSpeechToSpeech, ElevenLabsTextToDialogue, ElevenLabsTextToSoundEffects, ElevenLabsTextToSpeech, ElevenLabsVoiceSelector, HeyGenTextToSpeechNode, SoniloTextToMusic, SoniloVideoToMusic)
- when to use: Use to generate audio from a text prompt.
- example request: "build an audio workflow"
- description: Generate high-quality, production-ready music from text prompts. Input descriptive text to create original soundtracks with streaming playback and precise duration control. | Generate natural-sounding speech from text using HeyGen's advanced TTS engine, supporting a wide range of languages and accents with customizable voices. Input your text and select from numerous preset voices or clone a custom voice from a short audio sample. Ideal for creating voiceovers for videos, generating multilingual narration, and producing personalized audio content. | Generate synchronized soundtracks from video footage. Input a video to produce music that matches its pacing and emotional cues, outputting a perfectly timed audio file. | Input a text prompt to generate custom sound effects and ambient audio. | Input a text prompt to generate speech, dialogue, background music, and sound effects in one audio file. Describe voices, emotion, and scene details to create multi-speaker audio up to 2 minutes. | Input text and select a voice profile to generate a high-quality, emotionally expressive audio dialogue. | Input text to generate speech with ultra-realistic voices, or upload a voice sample to clone it for synthesis. | Upload a character image and write a text prompt to generate audio. The model derives the voice from your image, then produces speech, ambience, background music, and sound effects. | Upload a reference audio clip and write a text prompt to clone the voice into a new scene. Generate dialogue, background music, and sound effects with up to 3 reference voices. | Upload a source audio file to apply a new voice tone or clone a different voice, generating a modified audio output. | Upload an audio file containing background noise. Use the ElevenLabs API to isolate and output a clean voice track.
- member workflows:
    - api_bytedance_seed_audio1_0_t2a
    - api_bytedance_seed_audio1_0_ta2a
    - api_bytedance_seed_audio1_0_ti2a
    - api_elevenlabs_speech_to_speech
    - api_elevenlabs_text_to_dialogue
    - api_elevenlabs_text_to_sound_effects
    - api_elevenlabs_text_to_speech
    - api_elevenlabs_voice_isolation
    - api_heygen_text_to_speech
    - api_sonilo_t2m
    - api_sonilo_v2m
- node clusters (required structure):
    - (none resolved)
- optional roles: AudioAdjustVolume, ElevenLabsVoiceSelector, LoadAudio, AudioMerge, ByteDanceSeedAudio, CreateVideo, ElevenLabsAudioIsolation, ElevenLabsInstantVoiceClone, ElevenLabsSpeechToSpeech, ElevenLabsTextToDialogue, ElevenLabsTextToSoundEffects, ElevenLabsTextToSpeech
- unresolved nodes: MarkdownNote, Note

## API / Partner Nodes - Audio / ACE-Step  (`api_partner_nodes_audio__ace_step`)  -  1 workflow(s)  -  source: official
- execution: api (API nodes: GeminiNode)
- when to use: Use to generate audio from a text prompt using ACE-Step.
- example request: "build an audio workflow using ACE-Step"
- description: Input a music style and optional lyrics. Generate a full song with AI-created lyrics and audio.
- member workflows:
    - audio_ace_step_1_5_split_llm
- node clusters (required structure):
    - model loading: DualCLIPLoader, UNETLoader, VAELoader
    - conditioning: ConditioningZeroOut, TextEncodeAceStepAudio1.5
    - sampling: KSampler
    - decoding: VAEDecodeAudio
    - output: SaveAudioMP3
    - other operations: EmptyAceStep1.5LatentAudio, GeminiNode, MarkdownNote, ModelSamplingAuraFlow, PreviewAny, PrimitiveFloat, PrimitiveNode, RegexExtract (x2)
- paired/multiple required: RegexExtract x2
- unresolved nodes: MarkdownNote, PrimitiveNode

## API / Partner Nodes - Audio / LTX  (`api_partner_nodes_audio__ltx`)  -  1 workflow(s)  -  source: official
- execution: api (API nodes: ElevenLabsInstantVoiceClone, ElevenLabsTextToSpeech, ElevenLabsVoiceSelector, GeminiNode)
- when to use: Use to generate a video using LTX.
- example request: "build a video workflow using LTX"
- description: Upload an image to generate AI prompts and synthesize speech. Create a final video with accurate lip sync using Eleven Labs and LTX Video.
- member workflows:
    - template_image_speech_to_video
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: CheckpointLoaderSimple, LTXVAudioVAELoader, LatentUpscaleModelLoader, LoraLoader, LoraLoaderModelOnly (x2)
    - conditioning: CFGGuider (x2), CLIPTextEncode (x2), LTXAVTextEncoderLoader, LTXVConditioning, ManualSigmas (x2)
    - latent / canvas: LTXVAudioVAEEncode
    - sampling: KSamplerSelect (x2), LTXVLatentUpsampler, SamplerCustomAdvanced (x2)
    - decoding: LTXVAudioVAEDecode, VAEDecodeTiled
    - output: SaveAudioMP3, SaveVideo
    - other operations: ComfyMathExpression (x4), CreateVideo, ElevenLabsInstantVoiceClone, ElevenLabsTextToSpeech, ElevenLabsVoiceSelector, EmptyLTXVLatentVideo, GeminiNode, LTXVConcatAVLatent (x2), LTXVCropGuides, LTXVImgToVideoInplace (x2), LTXVPreprocess, LTXVSeparateAVLatent (x2), LoadAudio, MarkdownNote (x3), PreviewAny (x4), PrimitiveBoolean, PrimitiveFloat, PrimitiveInt (x3), PrimitiveStringMultiline, RandomNoise (x2), RegexExtract (x2), Reroute, ResizeImageMaskNode, ResizeImagesByLongerEdge, SetLatentNoiseMask, SolidMask, TextGenerateLTX2Prompt, TrimAudioDuration
- paired/multiple required: MarkdownNote x3, CFGGuider x2, CLIPTextEncode x2, KSamplerSelect x2, LTXVConcatAVLatent x2, LTXVImgToVideoInplace x2, LTXVSeparateAVLatent x2, LoraLoaderModelOnly x2, ManualSigmas x2, RandomNoise x2, RegexExtract x2, SamplerCustomAdvanced x2
- unresolved nodes: MarkdownNote, Reroute


# Text to Video  (`text_to_video`)  -  13 workflow(s), 6 model(s)

## Text to Video / LTX-2  (`text_to_video__ltx_2`)  -  5 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate a video from a text prompt using LTX-2.
- example request: "build a video workflow using LTX-2"
- description: Generate a video from a text prompt, optionally using an image for reference. Receive a high-quality video with improved motion, audio, and detail, optimized for portrait or landscape formats. | Generate high-quality videos from text prompts with synchronized audio-video generation using LTX-2 distilled model. Optimized for faster generation while maintaining quality. Features expressive lip sync, dynamic motion generation, and improved speed. | Generate high-quality videos from text prompts with synchronized audio-video generation using LTX-2. Features expressive lip sync, dynamic motion generation, and efficient performance. | Generate videos from text prompts. | Generates video from text prompts using LTX-2.3, Lightricks' video diffusion model.
- member workflows:
    - ltxv_text_to_video
    - text_to_video_ltx_2_3
    - video_ltx2_3_t2v
    - video_ltx2_t2v
    - video_ltx2_t2v_distilled
- node clusters (required structure):
    - model loading: CheckpointLoaderSimple
    - conditioning: CLIPTextEncode, LTXVConditioning
    - sampling: KSamplerSelect
    - other operations: CreateVideo, EmptyLTXVLatentVideo
- optional roles: MarkdownNote, LoraLoaderModelOnly, CFGGuider, LTXVConcatAVLatent, LTXVImgToVideoInplace, LTXVSeparateAVLatent, ManualSigmas, RandomNoise, SamplerCustomAdvanced, CLIPLoader, EmptyImage, ImageScaleBy
- unresolved nodes: MarkdownNote, Note, Reroute

## Text to Video / Hunyuan3D  (`text_to_video__hunyuan3d`)  -  2 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate a video from a text prompt using Hunyuan3D.
- example request: "build a video workflow using Hunyuan3D"
- description: Generate high-quality 720p videos from text prompts with cinematic camera control, emotional expressions, and physics simulation. Supports multiple styles including realistic, anime, and 3D with text rendering. | Generate videos from text prompts using Hunyuan model.
- member workflows:
    - hunyuan_video_text_to_video
    - video_hunyuan_video_1.5_720p_t2v
- node clusters (required structure):
    - model loading: DualCLIPLoader, UNETLoader, VAELoader
    - conditioning: BasicScheduler, CLIPTextEncode
    - sampling: KSamplerSelect, SamplerCustomAdvanced
    - decoding: VAEDecode, VAEDecodeTiled
    - output: SaveVideo
    - other operations: CreateVideo, MarkdownNote, ModelSamplingSD3, Note (x2), RandomNoise
- paired/multiple required: Note x2
- optional roles: CFGGuider, EasyCache, BasicGuider, DisableNoise, EmptyHunyuanLatentVideo, EmptyHunyuanVideo15Latent, FluxGuidance, HunyuanVideo15LatentUpscaleWithModel, HunyuanVideo15SuperResolution, LatentUpscaleModelLoader, SplitSigmas
- unresolved nodes: MarkdownNote, Note

## Text to Video / WAN  (`text_to_video__wan`)  -  2 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate a video from a text prompt using WAN.
- example request: "build a video workflow using WAN"
- description: Generate text-to-video with alpha channel support for transparent backgrounds and semi-transparent objects. | Generate videos from text prompts using Wan 2.1.
- member workflows:
    - text_to_video_wan
    - video_wan2.1_alpha_t2v_14B
- node clusters (required structure):
    - model loading: CLIPLoader, UNETLoader, VAELoader
    - conditioning: CLIPTextEncode (x2)
    - sampling: KSampler
    - decoding: VAEDecode
    - other operations: EmptyHunyuanLatentVideo, ModelSamplingSD3
- paired/multiple required: CLIPTextEncode x2
- optional roles: LoraLoaderModelOnly, MarkdownNote, CreateVideo, ImageToMask, InvertMask, JoinImageWithAlpha, SaveAnimatedWEBP, SaveVideo
- unresolved nodes: MarkdownNote

## Text to Video / WAN 2.2  (`text_to_video__wan_2_2`)  -  2 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate a video from a text prompt using WAN 2.2.
- example request: "build a video workflow using WAN 2.2"
- description: Generate high-quality videos from text prompts with cinematic aesthetic control and dynamic motion generation using Wan 2.2. | Generates video from text prompts using Wan2.2, Alibaba's diffusion video model.
- member workflows:
    - text_to_video_wan_2_2
    - video_wan2_2_14B_t2v
- node clusters (required structure):
    - model loading: CLIPLoader, LoraLoaderModelOnly (x2), UNETLoader (x2), VAELoader
    - conditioning: CLIPTextEncode (x2)
    - sampling: KSamplerAdvanced (x2)
    - decoding: VAEDecode
    - other operations: CreateVideo, EmptyHunyuanLatentVideo, MarkdownNote, ModelSamplingSD3 (x2)
- paired/multiple required: CLIPTextEncode x2, KSamplerAdvanced x2, LoraLoaderModelOnly x2, ModelSamplingSD3 x2, UNETLoader x2
- optional roles: Note, SaveVideo
- unresolved nodes: MarkdownNote, Note

## Text to Video / Generic  (`text_to_video__generic`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate a video from a text prompt.
- example request: "build a video workflow"
- description: A lightweight 2B model that generates videos from English and Russian prompts with high visual quality.
- member workflows:
    - video_kandinsky5_t2v
- node clusters (required structure):
    - model loading: DualCLIPLoader, UNETLoader, VAELoader
    - conditioning: CLIPTextEncode (x2)
    - sampling: KSampler
    - decoding: VAEDecode
    - output: SaveVideo
    - other operations: CreateVideo, Kandinsky5ImageToVideo, MarkdownNote (x2), ModelSamplingSD3
- paired/multiple required: CLIPTextEncode x2, MarkdownNote x2
- unresolved nodes: MarkdownNote

## Text to Video / WAN VACE  (`text_to_video__wan_vace`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate a video from a text prompt using WAN VACE.
- example request: "build a video workflow using WAN VACE"
- description: Transform text descriptions into high-quality videos. Supports both 480p and 720p with VACE-14B model.
- member workflows:
    - video_wan_vace_14B_t2v
- node clusters (required structure):
    - model loading: CLIPLoader (x2), LoraLoader (x2), UNETLoader (x2), VAELoader
    - conditioning: CLIPTextEncode (x2)
    - sampling: KSampler
    - decoding: VAEDecode
    - output: SaveVideo
    - other operations: CreateVideo, MarkdownNote (x5), ModelSamplingSD3, SaveAnimatedWEBP, TrimVideoLatent, WanVaceToVideo
- paired/multiple required: MarkdownNote x5, CLIPLoader x2, CLIPTextEncode x2, LoraLoader x2, UNETLoader x2
- unresolved nodes: MarkdownNote


# Video Tools  (`video_tools`)  -  13 workflow(s), 2 model(s)

## Video Tools / Generic  (`video_tools__generic`)  -  12 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate a video.
- example request: "build a video workflow"
- description: Concatenates two videos end-to-end with optional resize, letterbox padding, and audio merge or drop. | Convert a Video to Lineart/Canny for Control Processors | Convert a Video to a temporally stable Depth Map | Convert a Video to a temporally stable Normal Map | Convert a Video to a temporally stable Pose Control Map | Extracts one image frame from a video at a chosen index, with optional trim and FPS control. | Generate intermediate frames between existing video frames to create smoother motion. Input a video and receive a fluid, higher-frame-rate output without changing the total duration. | Increases video frame rate by synthesizing intermediate frames with a frame interpolation model. | Smooth out low frame-rate videos | Smoothly blend two video sequences using a crossfade effect. Input two image sequences and define the transition length and blend mode. Outputs a single, merged video sequence. | Stitches multiple video clips into a single sequential video file. | Upload a portrait image and a reference expression video. Generate a video of the portrait with the facial expressions from the reference.
- member workflows:
    - frame_interpolation
    - get_any_video_frame
    - merge_videos
    - templates_liveportrait.app
    - templates_purz_crossfade
    - utility-depthAnything-v2-relative-video
    - utility-frame_interpolation-film
    - utility-lineart-video
    - utility-normal_crafter-video
    - utility-openpose-video
    - utility_gimm_frame_interpolation
    - video_stitch
- node clusters (required structure):
    - (none resolved)
- optional roles: GetVideoComponents, ImageResizeKJv2, VHS_LoadVideo, AudioMerge, BatchImagesNode, CreateVideo, DWPreprocessor, DepthAnything_V2, DownloadAndLoadDepthAnythingV2Model, DownloadAndLoadGIMMVFIModel, DownloadAndLoadLivePortraitModels, EmptyAudio
- unresolved nodes: DepthAnything_V2, DownloadAndLoadDepthAnythingV2Model, DownloadAndLoadGIMMVFIModel, DownloadAndLoadLivePortraitModels, FILM VFI, FL_VideoCrossfade, GIMMVFI_interpolate, LivePortraitComposite, LivePortraitCropper, LivePortraitLoadMediaPipeCropper, LivePortraitProcess, MarkdownNote, NormalCrafterNode

## Video Tools / Depth Anything  (`video_tools__depth_anything`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to estimate a depth map using Anima, Depth Anything.
- example request: "build a video workflow using Anima"
- description: Upload 1 image to generate a depth map for video depth estimation. Output a single depth-processed image ready for use in downstream workflows. Ideal for video generation tasks requiring depth control, 3D scene preprocessing, and animation depth mapping.
- member workflows:
    - utility_depth_anything3_video_depth_estimation
- node clusters (required structure):
    - inputs: LoadVideo
    - output: PreviewImage, SaveVideo
    - other operations: CreateVideo, DA3Inference, DA3Render, GetVideoComponents, LoadDA3Model, MarkdownNote (x2), Video Slice
- paired/multiple required: MarkdownNote x2
- unresolved nodes: MarkdownNote


# 3D  (`3d`)  -  11 workflow(s), 3 model(s)

## 3D / Hunyuan3D  (`3d__hunyuan3d`)  -  6 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate a 3D model using Hunyuan3D.
- example request: "build a 3d workflow using Hunyuan3D"
- description: Generate 3D models from multiple views using Hunyuan3D 2.0 MV Turbo. | Generate 3D models from multiple views using Hunyuan3D 2.0 MV. | Generate 3D models from single images using Hunyuan3D 2.0. | Generate 3D models from single images using Hunyuan3D 2.1. | Generates 3D mesh models from a single input image using Hunyuan3D 2.0/2.1.
- member workflows:
    - 04_hunyuan_3d_2.1_subgraphed
    - 3d_hunyuan3d-v2.1
    - 3d_hunyuan3d_image_to_model
    - 3d_hunyuan3d_multiview_to_model
    - 3d_hunyuan3d_multiview_to_model_turbo
    - image_to_model_hunyuan3d_2_1
- node clusters (required structure):
    - model loading: ImageOnlyCheckpointLoader
    - latent / canvas: EmptyLatentHunyuan3Dv2
    - sampling: KSampler
    - decoding: VAEDecodeHunyuan3D
    - other operations: CLIPVisionEncode, ModelSamplingAuraFlow, VoxelToMesh
- optional roles: LoadImage, MarkdownNote, FluxGuidance, Hunyuan3Dv2Conditioning, Hunyuan3Dv2ConditioningMultiView, Note, SaveGLB
- unresolved nodes: MarkdownNote, Note

## 3D / MoGe  (`3d__moge`)  -  3 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate an image using MoGe.
- example request: "build a 3d workflow using MoGe"
- description: Estimates 3D scene geometry from an input image using MoGe, outputting a mesh plus OpenGL and DirectX normal maps. | Upload an equirectangular 360° panorama image and generate a textured GLB mesh with vertex colors. | Upload an image to estimate its perspective geometry. Generate a 3D depth map and surface normals from the input.
- member workflows:
    - 3d_moge_panorama_to_mesh
    - 3d_moge_perspective_to_mesh
    - geometry_estimation_moge
- node clusters (required structure):
    - other operations: ComfyMathExpression, ComfySwitchNode (x2), GetImageSize, LoadMoGeModel, MoGePointMapToMesh, ResizeImagesByLongerEdge
- optional roles: MarkdownNote, MoGeRender, PreviewImage, LoadImage, MoGeInference, MoGePanoramaInference, SaveGLB
- unresolved nodes: MarkdownNote

## 3D / TripoSplat  (`3d__triposplat`)  -  2 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate a 3D model using TripoSplat.
- example request: "build a 3d workflow using TripoSplat"
- description: This subgraph takes a single 2D image as input and generates a variable number of 3D Gaussians (up to 262,144) as output, enabling high-quality 3D reconstruction. It is ideal for asset creation, AR/VR, game development, and simulation environments, handling diverse image styles from photos to illustrations. | Upload a single 2D image. Generate a high-quality 3D Gaussian splat representation with controllable density and budget for rendering.
- member workflows:
    - 3d_triposplat_image_to_gaussian_splat
    - image_to_gaussian_splat_triposplat
- node clusters (required structure):
    - model loading: UNETLoader, VAELoader (x2)
    - conditioning: TripoSplatConditioning
    - sampling: KSampler
    - decoding: VAEDecodeTripoSplat
    - output: PreviewImage
    - other operations: CLIPVisionLoader, ComfySwitchNode (x2), InvertMask (x2), JoinImageWithAlpha, LoadBackgroundRemovalModel, RemoveBackground, TripoSplatPreprocessImage, TripoSplatSamplingPreview
- paired/multiple required: InvertMask x2, VAELoader x2
- optional roles: MarkdownNote, SaveGLB, CreateCameraInfo, CreateVideo, LoadImage, RenderSplat, SaveVideo, SplatToFile3D, SplatToMesh
- unresolved nodes: MarkdownNote


# First / Last Frame to Video  (`first_last_frame_to_video`)  -  9 workflow(s), 4 model(s)

## First / Last Frame to Video / WAN 2.2  (`first_last_frame_to_video__wan_2_2`)  -  4 workflow(s)  -  source: mixed
- execution: local
- when to use: Use to generate a video using WAN 2.2, Z-Image.
- example request: "build a video workflow using WAN 2.2"
- description: Creates a smooth video using 6 key frames.It auto fills in the motion between frames and stitches the segments together seamlessly. | Learn how to load images,  generate a video and how to find a node using Wan 2.2. | Upload any image to generate a unique, looping AI video. The workflow uses an LLM to create five prompts, produces images and video clips, and stitches them into a final seamless loop.
- member workflows:
    - gsc_starter_2
    - templates-6-key-frames
    - templates_mjm_airt_machIne
    - video_wan2_2_14B_flf2v
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: CLIPLoader, UNETLoader (x2), VAELoader
    - conditioning: CLIPTextEncode (x2)
    - sampling: KSamplerAdvanced (x2)
    - decoding: VAEDecode
    - other operations: CreateVideo, ModelSamplingSD3 (x2), WanFirstLastFrameToVideo
- paired/multiple required: CLIPTextEncode x2, KSamplerAdvanced x2, ModelSamplingSD3 x2, UNETLoader x2
- optional roles: LoraLoaderModelOnly, KSampler, Note, AILab_QwenVL, ConditioningZeroOut, EmptySD3LatentImage, ImageBatchMulti, ImageResizeKJv2, ImageUpscaleWithModelBatched, ImpactStringSelector, ModelSamplingAuraFlow, PreviewImage
- unresolved nodes: AILab_QwenVL, MarkdownNote, Note, SimpleMath+

## First / Last Frame to Video / LTX-2  (`first_last_frame_to_video__ltx_2`)  -  3 workflow(s)  -  source: mixed
- execution: local
- when to use: Use to generate a video interpolating between a first and last frame using LTX-2.
- example request: "build a video workflow using LTX-2"
- description: Generates a video interpolating between first and last keyframes using LTX-2.3. | Generates a video that interpolates between the first and last keyframes using LTX-2.3, including optional audio.
- member workflows:
    - first_last_frame_to_video
    - first_last_frame_to_video_ltx_2_3
    - video_ltx2_3_flf2v
- node clusters (required structure):
    - model loading: CheckpointLoaderSimple, LTXVAudioVAELoader
    - conditioning: CFGGuider, CLIPTextEncode (x2), LTXAVTextEncoderLoader, LTXVConditioning, ManualSigmas
    - latent / canvas: LTXVEmptyLatentAudio
    - sampling: SamplerCustomAdvanced, SamplerEulerAncestral
    - decoding: LTXVAudioVAEDecode, VAEDecodeTiled
    - other operations: ComfyMathExpression, CreateVideo, EmptyLTXVLatentVideo, GetImageSize, LTXVAddGuide (x2), LTXVConcatAVLatent, LTXVCropGuides, LTXVPreprocess (x2), LTXVSeparateAVLatent, PrimitiveInt (x4), RandomNoise, ResizeImageMaskNode (x2)
- paired/multiple required: CLIPTextEncode x2, LTXVAddGuide x2, LTXVPreprocess x2, ResizeImageMaskNode x2
- optional roles: LoadImage, GetVideoComponents, VHS_VideoCombine

## First / Last Frame to Video / WAN  (`first_last_frame_to_video__wan`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate a video interpolating between a first and last frame using WAN.
- example request: "build a video workflow using WAN"
- description: Generate videos by controlling first and last frames using Wan 2.1 FLF2V.
- member workflows:
    - wan2.1_flf2v_720_f16
- node clusters (required structure):
    - inputs: LoadImage (x2)
    - model loading: CLIPLoader, UNETLoader, VAELoader
    - conditioning: CLIPTextEncode (x2)
    - sampling: KSampler
    - decoding: VAEDecode
    - output: SaveVideo
    - other operations: CLIPVisionEncode (x2), CLIPVisionLoader, CreateVideo, MarkdownNote, ModelSamplingSD3, WanFirstLastFrameToVideo
- paired/multiple required: CLIPTextEncode x2, CLIPVisionEncode x2, LoadImage x2
- unresolved nodes: MarkdownNote

## First / Last Frame to Video / WAN VACE  (`first_last_frame_to_video__wan_vace`)  -  1 workflow(s)  -  source: custom
- execution: local
- when to use: Use to generate a video interpolating between a first and last frame using WAN VACE.
- example request: "build a video workflow using WAN VACE"
- description: Generate a video interpolating between a first and last frame using WAN VACE. Structurally it loads a diffusion model; uses a VAE; encodes a text prompt; runs a diffusion sampler; decodes the latent to pixels. Boundary inputs: IMAGE, INT; outputs: IMAGE, MASK.
- member workflows:
    - video_wan_vace_flf2v
- node clusters (required structure):
    - inputs: LoadImage (x2)
    - model loading: CLIPLoader, LoraLoader, UNETLoader, VAELoader
    - conditioning: CLIPTextEncode (x2)
    - sampling: KSampler
    - decoding: VAEDecode
    - output: PreviewImage (x2), VHS_VideoCombine
    - other operations: CreateVideo, GetVideoComponents, ImageBatch (x4), ImageToMask, MaskToImage (x2), ModelSamplingSD3, PrimitiveInt (x4), RepeatImageBatch, SolidMask (x2), TrimVideoLatent, WanVaceToVideo
- paired/multiple required: ImageBatch x4, CLIPTextEncode x2, LoadImage x2, MaskToImage x2, PreviewImage x2, SolidMask x2


# Inpaint / Outpaint  (`inpaint_outpaint`)  -  7 workflow(s), 3 model(s)

## Inpaint / Outpaint / Flux  (`inpaint_outpaint__flux`)  -  3 workflow(s)  -  source: official
- execution: local
- when to use: Use to inpaint masked regions of an image using Flux.
- example request: "build an image workflow using Flux"
- description: Extend images beyond boundaries using Flux.1 outpainting. | Fill missing parts of images using Flux.1 Fill Inpainting. | Inpaints masked image regions using Flux.1 fill [dev], Black Forest Labs' inpainting/outpainting model.
- member workflows:
    - flux_fill_inpaint_example
    - flux_fill_outpaint_example
    - image_inpainting_flux_1_fill_dev
- node clusters (required structure):
    - model loading: DualCLIPLoader, UNETLoader, VAELoader
    - conditioning: CLIPTextEncode, ConditioningZeroOut, FluxGuidance, InpaintModelConditioning
    - sampling: KSampler
    - decoding: VAEDecode
    - other operations: DifferentialDiffusion
- optional roles: ImagePadForOutpaint, LoadImage, MarkdownNote, SaveImage
- unresolved nodes: MarkdownNote

## Inpaint / Outpaint / Qwen Image  (`inpaint_outpaint__qwen_image`)  -  3 workflow(s)  -  source: official
- execution: local
- when to use: Use to inpaint masked regions of an image using Qwen Image.
- example request: "build an image workflow using Qwen Image"
- description: Inpaints masked regions using Qwen-Image, extending its multilingual text rendering to inpainting tasks. | Outpaints beyond image boundaries using Qwen-Image's outpainting capabilities. | Professional inpainting and image editing with Qwen-Image InstantX ControlNet. Supports object replacement, text modification, background changes, and outpainting.
- member workflows:
    - image_inpainting_qwen_image
    - image_outpainting_qwen_image
    - image_qwen_image_instantx_inpainting_controlnet
- node clusters (required structure):
    - model loading: CLIPLoader, LoraLoaderModelOnly, UNETLoader, VAELoader
    - conditioning: CLIPTextEncode (x2), ControlNetInpaintingAliMamaApply, ControlNetLoader
    - latent / canvas: VAEEncode
    - sampling: KSampler
    - decoding: VAEDecode
    - other operations: GrowMask, ImageBlur, ImageToMask, MaskPreview, MaskToImage, ModelSamplingAuraFlow
- paired/multiple required: CLIPTextEncode x2
- optional roles: MarkdownNote, SaveImage, ImageScaleToMaxDimension, ImageCompositeMasked, LoadImage, Note, FluxKontextImageScale, ImagePadForOutpaint, PreviewImage, SetLatentNoiseMask
- unresolved nodes: MarkdownNote, Note

## Inpaint / Outpaint / WAN  (`inpaint_outpaint__wan`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to inpaint masked regions of an image using Anima, WAN.
- example request: "build an image workflow using Anima"
- description: Inpaint anime images with Anima LLLite, a lightweight ControlNet variant that applies low-rank corrections for precise mask-based editing. Input 1 image and receive 1 inpainted output plus a comparison view. Ideal for fixing character details, removing unwanted objects from anime scenes, and seamless background restoration.
- member workflows:
    - image_anima_lllite_image_inpainting
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: CLIPLoader, LoraLoaderModelOnly, ModelPatchLoader, UNETLoader, VAELoader
    - conditioning: CLIPTextEncode (x2)
    - latent / canvas: EmptyLatentImage
    - sampling: KSampler
    - decoding: VAEDecode
    - output: SaveImage
    - other operations: AnimaLLLiteApply, ComfySwitchNode (x3), ImageCompare, MarkdownNote (x3), MaskPreview, Painter, PrimitiveBoolean, PrimitiveFloat (x2), PrimitiveInt (x2), ResizeImageMaskNode
- paired/multiple required: MarkdownNote x3, CLIPTextEncode x2
- unresolved nodes: MarkdownNote


# Video Inpaint  (`video_inpaint`)  -  7 workflow(s), 4 model(s)

## Video Inpaint / WAN VACE  (`video_inpaint__wan_vace`)  -  3 workflow(s)  -  source: official
- execution: local
- when to use: Use to inpaint regions of a video using WAN VACE, SAM3.
- example request: "build a video workflow using WAN VACE"
- description: Edit specific regions in videos while preserving surrounding content. Great for object removal or replacement. | Removes objects from video by inpainting masked regions using Wan 2.1 VACE, with SAM3 text-guided segmentation and optional Lightning LoRA turbo mode. | Video Inpaint(Wan2.1 VACE) blueprint
- member workflows:
    - video_inpaint_wan2_1_vace
    - video_inpainting_wan2_1_vace
    - video_wan_vace_inpainting
- node clusters (required structure):
    - model loading: CLIPLoader, LoraLoaderModelOnly, UNETLoader, VAELoader
    - conditioning: CLIPTextEncode (x2)
    - sampling: KSampler
    - decoding: VAEDecode
    - output: PreviewImage
    - other operations: CreateVideo, GetImageSize, GetVideoComponents, ImageCompositeMasked, ImageFromBatch, InvertMask, MaskToImage, ModelSamplingSD3, TrimVideoLatent, WanVaceToVideo
- paired/multiple required: CLIPTextEncode x2
- optional roles: MarkdownNote, CheckpointLoaderSimple, GrowMask, ImageToMask, LoadImage, LoadVideo, MaskPreview, RebatchImages, RepeatImageBatch, ResizeImageMaskNode, SAM3_Detect, SaveVideo
- unresolved nodes: MarkdownNote

## Video Inpaint / WAN 2.2  (`video_inpaint__wan_2_2`)  -  2 workflow(s)  -  source: official
- execution: local
- when to use: Use to inpaint masked regions of a video using WAN 2.2.
- example request: "build a video workflow using WAN 2.2"
- description: Efficient video inpainting from start and end frames. 5B model delivers quick iterations for testing workflows. | Generate videos from start and end frames using Wan 2.2 Fun Inp.
- member workflows:
    - video_wan2_2_14B_fun_inpaint
    - video_wan2_2_5B_fun_inpaint
- node clusters (required structure):
    - inputs: LoadImage (x2)
    - model loading: CLIPLoader, UNETLoader, VAELoader
    - conditioning: CLIPTextEncode (x2)
    - decoding: VAEDecode
    - output: SaveVideo
    - other operations: CreateVideo, MarkdownNote, ModelSamplingSD3, WanFunInpaintToVideo
- paired/multiple required: CLIPTextEncode x2, LoadImage x2
- optional roles: KSamplerAdvanced, LoraLoaderModelOnly, Note, KSampler
- unresolved nodes: MarkdownNote, Note

## Video Inpaint / SAM3  (`video_inpaint__sam3`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to inpaint regions of a video using SAM3.
- example request: "build a video workflow using SAM3"
- description: Removes objects from video by inpainting masked regions using VOID (CogVideoX), with SAM3 text-guided segmentation and optional two-pass optical-flow refinement.
- member workflows:
    - video_inpaint_void
- node clusters (required structure):
    - model loading: CLIPLoader, CheckpointLoaderSimple, UNETLoader (x2), VAELoader
    - conditioning: BasicScheduler (x2), CFGGuider (x2), CLIPTextEncode (x3), VOIDInpaintConditioning
    - sampling: SamplerCustomAdvanced (x2), VOIDSampler (x2)
    - decoding: VAEDecode (x2)
    - other operations: ComfyMathExpression (x2), ComfySwitchNode, CreateVideo (x2), GetImageSize, GetVideoComponents, ImageFromBatch, MaskPreview, OpticalFlowLoader, PrimitiveBoolean, PrimitiveInt (x4), RandomNoise, SAM3_Detect, TrimAudioDuration, VOIDWarpedNoise, VOIDWarpedNoiseSource
- paired/multiple required: CLIPTextEncode x3, BasicScheduler x2, CFGGuider x2, CreateVideo x2, SamplerCustomAdvanced x2, UNETLoader x2, VAEDecode x2, VOIDSampler x2

## Video Inpaint / WAN  (`video_inpaint__wan`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to inpaint regions of a video using WAN.
- example request: "build a video workflow using WAN"
- description: Upload a video and mask the object you want to remove. Generate a clean video with the object and its physical interactions deleted.
- member workflows:
    - utility_void_video_inpainting
- node clusters (required structure):
    - inputs: LoadVideo
    - model loading: CLIPLoader, CheckpointLoaderSimple, UNETLoader (x2), VAELoader
    - conditioning: BasicScheduler (x2), CFGGuider (x2), CLIPTextEncode (x3), VOIDInpaintConditioning
    - sampling: SamplerCustomAdvanced (x2), VOIDSampler (x2)
    - decoding: VAEDecode (x2)
    - output: SaveVideo (x2)
    - other operations: ComfyMathExpression (x2), ComfySwitchNode, CreateVideo (x2), GetImageSize, GetVideoComponents, ImageFromBatch, MarkdownNote (x2), MaskPreview, OpticalFlowLoader, PrimitiveBoolean, PrimitiveInt (x4), RandomNoise, SAM3_Detect, TrimAudioDuration, VOIDWarpedNoise, VOIDWarpedNoiseSource
- paired/multiple required: CLIPTextEncode x3, BasicScheduler x2, CFGGuider x2, CreateVideo x2, MarkdownNote x2, SamplerCustomAdvanced x2, SaveVideo x2, UNETLoader x2, VAEDecode x2, VOIDSampler x2
- unresolved nodes: MarkdownNote


# API / Partner Nodes - Character  (`api_partner_nodes_character`)  -  5 workflow(s), 2 model(s)

## API / Partner Nodes - Character / Generic  (`api_partner_nodes_character__generic`)  -  3 workflow(s)  -  source: official
- execution: api (API nodes: GeminiImage2Node)
- when to use: Use to edit an existing image.
- example request: "build an image workflow"
- description: Upload a portrait of your character and create multiple cinematic lighting conditions while maintaining character consistency. | Upload your character and generate 360 turnaround views for full body and close ups. | Upload your character, background scene and product. Generate a 2x2 grid, select your desired image and upscale
- member workflows:
    - template_character_portrait_relighting
    - templates-2x2_grid-character_bg_product
    - templates-character_sheet
- node clusters (required structure):
    - inputs: LoadImage
    - output: SaveImage (x3)
    - other operations: GeminiImage2Node (x2)
- paired/multiple required: SaveImage x3, GeminiImage2Node x2
- optional roles: SimpleMath+, PreviewImage, ImageCrop, ResizeAndPadImage, BatchImagesNode, ImageBatchMulti, ImageFromBatch, ImageResizeKJv2, ImageStitch
- unresolved nodes: Reroute, SimpleMath+

## API / Partner Nodes - Character / Nano-Banana  (`api_partner_nodes_character__nano_banana`)  -  2 workflow(s)  -  source: custom
- execution: api (API nodes: GeminiImage2Node, GeminiNode)
- when to use: Use to generate a multi-pose character sheet using Nano-Banana.
- example request: "build an image workflow using Nano-Banana"
- description: API character sheet generation FOR FACE CLOSEUPS via Nano-Banana Pro. 1 character image -> 1 image output (3x3 sheet). Uses an LLM call to generate a prompt from the reference, then renders 9 character views with varying facial expressions in a single sheet. | API character sheet generation via Nano-Banana Pro. 1 character image -> 1 image output (3x3 sheet). Uses an LLM call to generate a prompt from the reference, then renders 9 character views with varying body pose in a single sheet.
- member workflows:
    - NanoBananaPro_3x3CharacterSheet
    - NanoBananaPro_3x3CharacterSheet_closeups
- node clusters (required structure):
    - inputs: LoadImage
    - output: SaveImage
    - other operations: GeminiImage2Node, GeminiNode, PrimitiveStringMultiline


# API / Partner Nodes - Inpaint / Outpaint  (`api_partner_nodes_inpaint_outpaint`)  -  5 workflow(s), 2 model(s)

## API / Partner Nodes - Inpaint / Outpaint / Generic  (`api_partner_nodes_inpaint_outpaint__generic`)  -  3 workflow(s)  -  source: official
- execution: api (API nodes: BriaImageEditNode, OpenAIDalle2, OpenAIGPTImage1)
- when to use: Use to inpaint masked regions of an image.
- example request: "build an image workflow"
- description: A professional Bria-powered outpainting template designed for seamless image extension and edge-aware scene expansion | Edit images using inpainting with OpenAI Dall-E 2 API. | Edit images using inpainting with OpenAI GPT Image 1 API.
- member workflows:
    - api_bria_image_outpainting
    - api_openai_dall_e_2_inpaint
    - api_openai_image_1_inpaint
- node clusters (required structure):
    - inputs: LoadImage
- optional roles: MarkdownNote, BriaImageEditNode, ImagePadForOutpaint, OpenAIDalle2, OpenAIGPTImage1, PreviewImage, SaveImage
- unresolved nodes: MarkdownNote

## API / Partner Nodes - Inpaint / Outpaint / Nano-Banana  (`api_partner_nodes_inpaint_outpaint__nano_banana`)  -  2 workflow(s)  -  source: mixed
- execution: api (API nodes: GeminiImage2Node, GeminiNanoBanana2)
- when to use: Use to outpaint / extend an image beyond its borders using Nano-Banana.
- example request: "build an image workflow using Nano-Banana"
- description: API upscale and outpaint via Nano-Banana 2. 1 image -> 1 image output. Upscales the input image while also generating new content around the edges to expand the overall dimensions, guided by the original image's style and content. | Upload your image, input your desired aspect ratio and the images position (as a percentage) in the new aspect ratio composite. Uses Nano Banana Pro to generate an outpainted version of your image to fit the new dimensions.
- member workflows:
    - NanoBanana2_outpaintUpscale
    - template_outpaint_to_any_aspect_ratio_nano_banana_pro
- node clusters (required structure):
    - inputs: LoadImage
    - output: SaveImage
- optional roles: MarkdownNote, EmptyImage, FluxResolutionNode, GeminiImage2Node, GeminiNanoBanana2, ImageCompare, ImageCompositeMasked, ImagePadForOutpaint, ImageResize+, ImageResizeKJv2, PreviewImage
- unresolved nodes: FluxResolutionNode, ImageResize+, MarkdownNote


# Text Tools  (`text_tools`)  -  5 workflow(s), 2 model(s)

## Text Tools / Gemini  (`text_tools__gemini`)  -  3 workflow(s)  -  source: mixed
- execution: hybrid (API nodes: GeminiNode)
- when to use: Use to caption an image as text using Gemini.
- example request: "build a text workflow using Gemini"
- description: Generates descriptive captions for images using Google's Gemini multimodal LLM. | Generates descriptive captions for video input using Google's Gemini multimodal LLM. | [API] motion prompt generation via Gemini, analyses a video and output a desscription of the motion in it. 1 video input -> 1 output. Generates descriptive motion prompts for video generation.
- member workflows:
    - image_captioning_gemini
    - video_captioning_gemini
    - video_gemini_motionPromptGeneration
- node clusters (required structure):
    - other operations: GeminiNode
- optional roles: CreateVideo, GetVideoComponents, ImageResizeKJv2, LoadVideo, easy saveText
- unresolved nodes: easy saveText

## Text Tools / Generic  (`text_tools__generic`)  -  2 workflow(s)  -  source: official
- execution: hybrid (API nodes: GeminiNode)
- when to use: Use to expand a short prompt into a detailed one.
- example request: "build an image workflow"
- description: Expands short text prompts into detailed descriptions using a text generation model for better generation quality. | Selects one line from multiline text by zero-based index for batch or list-driven prompt workflows.
- member workflows:
    - prompt_enhance
    - select_per_line_text_by_index
- node clusters (required structure):
    - (none resolved)
- optional roles: GeminiNode, RegexExtract


# API / Partner Nodes - Image Edit with ControlNet  (`api_partner_nodes_image_edit_with_controlnet`)  -  3 workflow(s), 2 model(s)

## API / Partner Nodes - Image Edit with ControlNet / Generic  (`api_partner_nodes_image_edit_with_controlnet__generic`)  -  2 workflow(s)  -  source: official
- execution: api (API nodes: RecraftColorRGB, RecraftControls, RecraftStyleV3DigitalIllustration, RecraftStyleV3LogoRaster, RecraftStyleV3RealisticImage, RecraftTextToImageNode, RecraftVectorizeImageNode)
- when to use: Use to generate an image guided by a control map (canny/depth/pose).
- example request: "build an image workflow"
- description: Control style with visual examples, align positioning, and fine-tune objects. Store and share styles for perfect brand consistency. | Generate images with custom color palettes and brand-specific visuals using Recraft.
- member workflows:
    - api_recraft_image_gen_with_color_control
    - api_recraft_image_gen_with_style_control
- node clusters (required structure):
    - output: SaveImage
    - other operations: MarkdownNote (x2), RecraftColorRGB (x3), RecraftControls, RecraftStyleV3DigitalIllustration, RecraftStyleV3LogoRaster, RecraftStyleV3RealisticImage, RecraftTextToImageNode, RecraftVectorizeImageNode, SaveSVGNode
- paired/multiple required: RecraftColorRGB x3, MarkdownNote x2
- unresolved nodes: MarkdownNote

## API / Partner Nodes - Image Edit with ControlNet / WAN 2.2  (`api_partner_nodes_image_edit_with_controlnet__wan_2_2`)  -  1 workflow(s)  -  source: official
- execution: api (API nodes: GeminiNode)
- when to use: Use to upscale / enhance an image using WAN 2.2.
- example request: "build an image workflow using WAN 2.2"
- description: Upload an image and set a resize factor. Generate an AI prompt from your image and upscale it in two controlled stages to enhance detail and fidelity.
- member workflows:
    - utility_sirolim_image_controlled_upscale
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: WanVideoLoraSelect (x4), WanVideoModelLoader (x2), WanVideoSetLoRAs (x2), WanVideoVAELoader (x2)
    - conditioning: WanVideoTextEncodeCached (x2)
    - sampling: WanVideoSampler (x2)
    - output: SaveImage (x2)
    - other operations: GeminiNode, GetImageSize (x4), ImageCompare, ImageResize+ (x2), MarkdownNote (x3), PreviewAny, PrimitiveInt (x6), SimpleMath+ (x4), VHS_SelectImages (x2), WanVideoDecode (x2), WanVideoEmptyEmbeds (x2), WanVideoEncode (x2), WanVideoTorchCompileSettings (x2)
- paired/multiple required: SimpleMath+ x4, WanVideoLoraSelect x4, MarkdownNote x3, ImageResize+ x2, SaveImage x2, VHS_SelectImages x2, WanVideoDecode x2, WanVideoEmptyEmbeds x2, WanVideoEncode x2, WanVideoModelLoader x2, WanVideoSampler x2, WanVideoSetLoRAs x2, WanVideoTextEncodeCached x2, WanVideoTorchCompileSettings x2, WanVideoVAELoader x2
- unresolved nodes: ImageResize+, MarkdownNote, SimpleMath+


# Character  (`character`)  -  3 workflow(s), 2 model(s)

## Character / SCAIL  (`character__scail`)  -  2 workflow(s)  -  source: official
- execution: local
- when to use: Use to replace a character in a video using Anima, SCAIL.
- example request: "build a video workflow using Anima"
- description: Replaces a character in a video with a reference image using the SCAIL-2 model for end-to-end controlled animation without intermediate pose maps. Key inputs include a source video, a reference character image, and optional text prompts for style or context. Suitable for animated or live-action footage, multi-character scenes, and creative video editing where direct pose-free animation is needed; works best with moderate-length videos.
- member workflows:
    - character_replacement_scail_2_base
    - character_replacement_scail_2_extend
- node clusters (required structure):
    - model loading: CLIPLoader, CheckpointLoaderSimple, LoraLoaderModelOnly (x2), UNETLoader, VAELoader
    - conditioning: BasicScheduler, CLIPTextEncode (x4)
    - sampling: KSamplerSelect, SamplerCustom
    - decoding: VAEDecode
    - output: PreviewImage (x2)
    - other operations: CLIPVisionEncode, CLIPVisionLoader, ComfyMathExpression (x3), ComfySwitchNode (x3), GetImageSize, GetVideoComponents, ImageFromBatch, ModelSamplingSD3, PrimitiveBoolean (x2), PrimitiveFloat (x2), PrimitiveInt (x5), ResizeImageMaskNode, SAM3_VideoTrack (x2), SCAIL2ColoredMask, WanSCAILToVideo
- paired/multiple required: CLIPTextEncode x4, LoraLoaderModelOnly x2, PreviewImage x2, SAM3_VideoTrack x2
- optional roles: ColorTransfer

## Character / Qwen Image  (`character__qwen_image`)  -  1 workflow(s)  -  source: official
- execution: local
- when to use: Use to generate an image using Qwen Image.
- example request: "build an image workflow using Qwen Image"
- description: Upload an image of your character and get multiple views of that image from different angles
- member workflows:
    - templates-1_click_multiple_character_angles-v1.0
- node clusters (required structure):
    - inputs: LoadImage
    - model loading: CLIPLoader (x8), LoraLoaderModelOnly (x16), UNETLoader (x8), VAELoader (x8)
    - conditioning: TextEncodeQwenImageEditPlus (x16)
    - latent / canvas: VAEEncode (x8)
    - sampling: KSampler (x8)
    - decoding: VAEDecode (x8)
    - output: SaveImage (x8)
    - other operations: CFGNorm (x8), ComfySwitchNode (x24), FluxKontextImageScale (x8), FluxKontextMultiReferenceLatentMethod (x16), MarkdownNote, ModelSamplingAuraFlow (x8), Note (x8), PrimitiveBoolean (x8), PrimitiveFloat (x16), PrimitiveInt (x16)
- paired/multiple required: FluxKontextMultiReferenceLatentMethod x16, LoraLoaderModelOnly x16, TextEncodeQwenImageEditPlus x16, CFGNorm x8, CLIPLoader x8, FluxKontextImageScale x8, KSampler x8, ModelSamplingAuraFlow x8, Note x8, SaveImage x8, UNETLoader x8, VAEDecode x8, VAEEncode x8, VAELoader x8
- unresolved nodes: MarkdownNote, Note

