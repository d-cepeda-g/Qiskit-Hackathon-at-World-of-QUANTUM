#!/usr/bin/env python3
"""
Content Creation Pipeline with Replicate APIs
============================================

A comprehensive pipeline for creating multimedia content using Replicate's AI models.
Supports text generation, image creation, video synthesis, and audio generation.
"""

import os
import time
import json
import asyncio
import logging
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import replicate
import requests
from PIL import Image
import io
import base64

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ContentRequest:
    """Data class for content generation requests"""
    content_type: str  # text, image, video, audio
    prompt: str
    style: Optional[str] = None
    duration: Optional[int] = None  # for video/audio in seconds
    dimensions: Optional[str] = None  # for images/video
    model_version: Optional[str] = None
    additional_params: Optional[Dict[str, Any]] = None

@dataclass
class ContentResult:
    """Data class for content generation results"""
    content_type: str
    prompt: str
    urls: List[str]
    metadata: Dict[str, Any]
    generation_time: float
    status: str

class ReplicateContentPipeline:
    """
    Main pipeline class for content creation using Replicate APIs
    """
    
    def __init__(self, api_token: str):
        """
        Initialize the pipeline with Replicate API token
        
        Args:
            api_token: Your Replicate API token
        """
        self.client = replicate.Client(api_token=api_token)
        
        # Model configurations for different content types
        self.models = {
            "text": {
                "gpt": "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
                "claude": "anthropic/claude-3-sonnet:cd2fd0478b0a4bb8b1e11d4b95c1e1a6e6b5d0b4c1a0a97cf49e36e82d6e3d8c"
            },
            "image": {
                "sdxl": "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                "dall-e": "openai/dall-e-3:7495cf2d4bc0ee0a6e9ad5c6ef3b49b9f4b6e0d4c85e6f9a9c8b0a5d3e7f2c1d",
                "midjourney": "tstramer/midjourney-diffusion:436b051ebd8f68d23e83d22de5e198e0995357afef113768c20f0b6fcef23c8b"
            },
            "video": {
                "stable-video": "stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb1a4a8b1b68faca5c8a21df5e5e3b2e2c4b5a6d7e",
                "runway": "runwayml/stable-video-diffusion:76b3bf5c3b3e4c5d8e9f0a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v",
                "animate-diff": "lucataco/animate-diff:1531004ee4c98894ab11a8456eb3e7c09b6e6b5a4f5c3d4e5f6g7h8i9j0k1l2m3n"
            },
            "audio": {
                "music": "riffusion/riffusion:8cf61ea6c56afd61d8f5b9ffd14d7c216c0a93844ce2d82ac1c9ecc9c7f24e05",
                "speech": "cjwbw/seamless-text-to-speech:9e178d5a32fcee7b9cb0e2e35b3ba23eb1b7e01b2c7de6bfe5e1b2c3d4e5f6g7h",
                "sound-effects": "afiaka87/riffusion-model:1a032e2dcc74ac4b65f0e96b1f7e4c8b5d9a4c3e5f8b2c7d9e1a3b5c8d2e6f9a"
            }
        }
        
        # Output directory for generated content
        self.output_dir = Path("generated_content")
        self.output_dir.mkdir(exist_ok=True)
        
    async def generate_text(self, request: ContentRequest) -> ContentResult:
        """
        Generate text content using language models
        
        Args:
            request: ContentRequest with text generation parameters
            
        Returns:
            ContentResult with generated text
        """
        start_time = time.time()
        
        try:
            model_name = request.model_version or "gpt"
            model = self.models["text"][model_name]
            
            # Prepare input parameters
            input_params = {
                "prompt": request.prompt,
                "max_new_tokens": request.additional_params.get("max_tokens", 1000) if request.additional_params else 1000,
                "temperature": request.additional_params.get("temperature", 0.7) if request.additional_params else 0.7,
                "top_p": request.additional_params.get("top_p", 0.95) if request.additional_params else 0.95,
            }
            
            # Add style/system prompt if provided
            if request.style:
                input_params["system_prompt"] = f"You are a {request.style} writer. Write in that style."
            
            # Generate text
            logger.info(f"Generating text with model: {model_name}")
            output = await self._run_prediction(model, input_params)
            
            # Process output
            generated_text = "".join(output) if isinstance(output, list) else str(output)
            
            # Save to file
            filename = f"text_{int(time.time())}.txt"
            file_path = self.output_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(generated_text)
            
            generation_time = time.time() - start_time
            
            return ContentResult(
                content_type="text",
                prompt=request.prompt,
                urls=[str(file_path)],
                metadata={
                    "model": model_name,
                    "length": len(generated_text),
                    "style": request.style
                },
                generation_time=generation_time,
                status="completed"
            )
            
        except Exception as e:
            logger.error(f"Text generation failed: {str(e)}")
            return ContentResult(
                content_type="text",
                prompt=request.prompt,
                urls=[],
                metadata={"error": str(e)},
                generation_time=time.time() - start_time,
                status="failed"
            )
    
    async def generate_image(self, request: ContentRequest) -> ContentResult:
        """
        Generate image content using diffusion models
        
        Args:
            request: ContentRequest with image generation parameters
            
        Returns:
            ContentResult with generated image URLs
        """
        start_time = time.time()
        
        try:
            model_name = request.model_version or "sdxl"
            model = self.models["image"][model_name]
            
            # Prepare input parameters
            input_params = {
                "prompt": request.prompt,
                "negative_prompt": request.additional_params.get("negative_prompt", "") if request.additional_params else "",
                "width": int(request.dimensions.split("x")[0]) if request.dimensions else 1024,
                "height": int(request.dimensions.split("x")[1]) if request.dimensions else 1024,
                "num_inference_steps": request.additional_params.get("steps", 50) if request.additional_params else 50,
                "guidance_scale": request.additional_params.get("guidance_scale", 7.5) if request.additional_params else 7.5,
                "num_outputs": request.additional_params.get("num_outputs", 1) if request.additional_params else 1,
            }
            
            # Add style to prompt if provided
            if request.style:
                input_params["prompt"] = f"{request.prompt}, {request.style} style"
            
            # Generate image
            logger.info(f"Generating image with model: {model_name}")
            output = await self._run_prediction(model, input_params)
            
            # Download and save images
            saved_paths = []
            if isinstance(output, list):
                for i, image_url in enumerate(output):
                    filename = f"image_{int(time.time())}_{i}.png"
                    file_path = await self._download_file(image_url, filename)
                    saved_paths.append(str(file_path))
            else:
                filename = f"image_{int(time.time())}.png"
                file_path = await self._download_file(output, filename)
                saved_paths.append(str(file_path))
            
            generation_time = time.time() - start_time
            
            return ContentResult(
                content_type="image",
                prompt=request.prompt,
                urls=saved_paths,
                metadata={
                    "model": model_name,
                    "dimensions": request.dimensions or "1024x1024",
                    "style": request.style,
                    "num_images": len(saved_paths)
                },
                generation_time=generation_time,
                status="completed"
            )
            
        except Exception as e:
            logger.error(f"Image generation failed: {str(e)}")
            return ContentResult(
                content_type="image",
                prompt=request.prompt,
                urls=[],
                metadata={"error": str(e)},
                generation_time=time.time() - start_time,
                status="failed"
            )
    
    async def generate_video(self, request: ContentRequest) -> ContentResult:
        """
        Generate video content using video diffusion models
        
        Args:
            request: ContentRequest with video generation parameters
            
        Returns:
            ContentResult with generated video URLs
        """
        start_time = time.time()
        
        try:
            model_name = request.model_version or "stable-video"
            model = self.models["video"][model_name]
            
            # Prepare input parameters
            input_params = {
                "prompt": request.prompt,
                "num_frames": request.additional_params.get("num_frames", 14) if request.additional_params else 14,
                "width": int(request.dimensions.split("x")[0]) if request.dimensions else 1024,
                "height": int(request.dimensions.split("x")[1]) if request.dimensions else 576,
                "fps": request.additional_params.get("fps", 6) if request.additional_params else 6,
                "motion_bucket_id": request.additional_params.get("motion_bucket_id", 127) if request.additional_params else 127,
                "noise_aug_strength": request.additional_params.get("noise_aug_strength", 0.1) if request.additional_params else 0.1,
            }
            
            # Add style to prompt if provided
            if request.style:
                input_params["prompt"] = f"{request.prompt}, {request.style} style"
            
            # Generate video
            logger.info(f"Generating video with model: {model_name}")
            output = await self._run_prediction(model, input_params)
            
            # Download and save video
            filename = f"video_{int(time.time())}.mp4"
            file_path = await self._download_file(output, filename)
            
            generation_time = time.time() - start_time
            
            return ContentResult(
                content_type="video",
                prompt=request.prompt,
                urls=[str(file_path)],
                metadata={
                    "model": model_name,
                    "dimensions": request.dimensions or "1024x576",
                    "style": request.style,
                    "duration": request.duration,
                    "fps": input_params["fps"]
                },
                generation_time=generation_time,
                status="completed"
            )
            
        except Exception as e:
            logger.error(f"Video generation failed: {str(e)}")
            return ContentResult(
                content_type="video",
                prompt=request.prompt,
                urls=[],
                metadata={"error": str(e)},
                generation_time=time.time() - start_time,
                status="failed"
            )
    
    async def generate_audio(self, request: ContentRequest) -> ContentResult:
        """
        Generate audio content using audio generation models
        
        Args:
            request: ContentRequest with audio generation parameters
            
        Returns:
            ContentResult with generated audio URLs
        """
        start_time = time.time()
        
        try:
            model_name = request.model_version or "music"
            model = self.models["audio"][model_name]
            
            # Prepare input parameters based on audio type
            if model_name == "music":
                input_params = {
                    "prompt_a": request.prompt,
                    "prompt_b": request.additional_params.get("prompt_b", request.prompt) if request.additional_params else request.prompt,
                    "denoising": request.additional_params.get("denoising", 0.75) if request.additional_params else 0.75,
                    "num_inference_steps": request.additional_params.get("steps", 50) if request.additional_params else 50,
                }
            elif model_name == "speech":
                input_params = {
                    "text": request.prompt,
                    "language": request.additional_params.get("language", "eng") if request.additional_params else "eng",
                    "speaker": request.additional_params.get("speaker", "default") if request.additional_params else "default",
                }
            else:  # sound-effects
                input_params = {
                    "prompt": request.prompt,
                    "duration": request.duration or 5,
                }
            
            # Generate audio
            logger.info(f"Generating audio with model: {model_name}")
            output = await self._run_prediction(model, input_params)
            
            # Download and save audio
            filename = f"audio_{int(time.time())}.wav"
            file_path = await self._download_file(output, filename)
            
            generation_time = time.time() - start_time
            
            return ContentResult(
                content_type="audio",
                prompt=request.prompt,
                urls=[str(file_path)],
                metadata={
                    "model": model_name,
                    "duration": request.duration,
                    "style": request.style
                },
                generation_time=generation_time,
                status="completed"
            )
            
        except Exception as e:
            logger.error(f"Audio generation failed: {str(e)}")
            return ContentResult(
                content_type="audio",
                prompt=request.prompt,
                urls=[],
                metadata={"error": str(e)},
                generation_time=time.time() - start_time,
                status="failed"
            )
    
    async def generate_content_batch(self, requests: List[ContentRequest]) -> List[ContentResult]:
        """
        Generate multiple pieces of content in parallel
        
        Args:
            requests: List of ContentRequest objects
            
        Returns:
            List of ContentResult objects
        """
        tasks = []
        
        for request in requests:
            if request.content_type == "text":
                tasks.append(self.generate_text(request))
            elif request.content_type == "image":
                tasks.append(self.generate_image(request))
            elif request.content_type == "video":
                tasks.append(self.generate_video(request))
            elif request.content_type == "audio":
                tasks.append(self.generate_audio(request))
            else:
                logger.warning(f"Unknown content type: {request.content_type}")
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Batch generation failed for request {i}: {str(result)}")
                processed_results.append(ContentResult(
                    content_type=requests[i].content_type,
                    prompt=requests[i].prompt,
                    urls=[],
                    metadata={"error": str(result)},
                    generation_time=0,
                    status="failed"
                ))
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def create_multimedia_story(self, story_prompt: str, include_audio: bool = True) -> Dict[str, ContentResult]:
        """
        Create a complete multimedia story with text, images, video, and audio
        
        Args:
            story_prompt: The main story prompt
            include_audio: Whether to generate audio content
            
        Returns:
            Dictionary with different content types and their results
        """
        logger.info(f"Creating multimedia story: {story_prompt}")
        
        # Create requests for different content types
        requests = [
            ContentRequest(
                content_type="text",
                prompt=f"Write a creative short story based on this concept: {story_prompt}",
                style="narrative"
            ),
            ContentRequest(
                content_type="image",
                prompt=f"A beautiful illustration of: {story_prompt}",
                style="cinematic, high quality",
                dimensions="1024x1024"
            ),
            ContentRequest(
                content_type="video",
                prompt=f"A short video scene showing: {story_prompt}",
                style="cinematic",
                dimensions="1024x576",
                additional_params={"num_frames": 25, "fps": 8}
            )
        ]
        
        if include_audio:
            requests.append(ContentRequest(
                content_type="audio",
                prompt=f"Ambient background music for: {story_prompt}",
                model_version="music",
                duration=10
            ))
        
        # Generate all content
        results = await self.generate_content_batch(requests)
        
        # Organize results by content type
        story_results = {}
        for request, result in zip(requests, results):
            story_results[request.content_type] = result
        
        # Save story metadata
        story_metadata = {
            "prompt": story_prompt,
            "created_at": time.time(),
            "content_types": list(story_results.keys()),
            "total_generation_time": sum(r.generation_time for r in results),
            "results": {k: asdict(v) for k, v in story_results.items()}
        }
        
        metadata_file = self.output_dir / f"story_{int(time.time())}_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(story_metadata, f, indent=2)
        
        logger.info(f"Multimedia story completed in {story_metadata['total_generation_time']:.2f} seconds")
        
        return story_results
    
    async def _run_prediction(self, model: str, inputs: Dict[str, Any]) -> Any:
        """
        Run a prediction with the Replicate API
        
        Args:
            model: Model identifier
            inputs: Input parameters for the model
            
        Returns:
            Model output
        """
        try:
            prediction = self.client.predictions.create(
                model=model,
                input=inputs
            )
            
            # Wait for completion
            prediction = self.client.predictions.wait(prediction)
            
            if prediction.status == "succeeded":
                return prediction.output
            else:
                raise Exception(f"Prediction failed with status: {prediction.status}")
                
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise
    
    async def _download_file(self, url: str, filename: str) -> Path:
        """
        Download a file from URL and save to output directory
        
        Args:
            url: URL to download from
            filename: Filename to save as
            
        Returns:
            Path to saved file
        """
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            file_path = self.output_dir / filename
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"Downloaded file: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"File download failed: {str(e)}")
            raise
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about available models
        
        Returns:
            Dictionary with model information
        """
        return {
            "available_models": self.models,
            "supported_content_types": list(self.models.keys()),
            "output_directory": str(self.output_dir)
        }


# Example usage and demo functions
async def demo_single_content():
    """Demo generating single pieces of content"""
    api_token = os.getenv("REPLICATE_API_TOKEN")
    if not api_token:
        raise ValueError("REPLICATE_API_TOKEN environment variable is required")
    
    pipeline = ReplicateContentPipeline(api_token=api_token)
    
    # Generate text
    text_request = ContentRequest(
        content_type="text",
        prompt="Write a creative story about AI helping humans create art",
        style="inspirational",
        additional_params={"max_tokens": 500}
    )
    
    text_result = await pipeline.generate_text(text_request)
    print(f"Generated text: {text_result.urls[0]}")
    
    # Generate image
    image_request = ContentRequest(
        content_type="image",
        prompt="A futuristic AI artist creating beautiful digital art",
        style="cyberpunk, neon colors",
        dimensions="1024x1024"
    )
    
    image_result = await pipeline.generate_image(image_request)
    print(f"Generated image: {image_result.urls[0]}")

async def demo_multimedia_story():
    """Demo creating a complete multimedia story"""
    api_token = os.getenv("REPLICATE_API_TOKEN")
    if not api_token:
        raise ValueError("REPLICATE_API_TOKEN environment variable is required")
    
    pipeline = ReplicateContentPipeline(api_token=api_token)
    
    story_results = await pipeline.create_multimedia_story(
        story_prompt="A robot discovering emotions through art",
        include_audio=True
    )
    
    print("Multimedia story created:")
    for content_type, result in story_results.items():
        print(f"  {content_type}: {result.urls[0] if result.urls else 'Failed'}")

if __name__ == "__main__":
    # Ensure API token is set
    if not os.getenv("REPLICATE_API_TOKEN"):
        print("Please set REPLICATE_API_TOKEN environment variable")
        exit(1)
    
    # Run demos
    print("Running content creation pipeline demos...")
    asyncio.run(demo_single_content())
    asyncio.run(demo_multimedia_story())