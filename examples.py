#!/usr/bin/env python3
"""
Content Creation Pipeline Examples
=================================

This script demonstrates various use cases for the content creation pipeline
using Replicate APIs. It includes examples for different content types and
advanced workflows.
"""

import os
import asyncio
import time
from content_creation_pipeline import (
    ReplicateContentPipeline, 
    ContentRequest, 
    ContentResult
)

async def example_basic_content_generation():
    """Example: Generate basic content of each type"""
    print("🎨 Example 1: Basic Content Generation")
    print("=" * 50)
    
    # Initialize pipeline
    api_token = os.getenv("REPLICATE_API_TOKEN")
    if not api_token:
        print("❌ Please set REPLICATE_API_TOKEN environment variable")
        return
    
    pipeline = ReplicateContentPipeline(api_token=api_token)
    
    # Generate text story
    print("📝 Generating story...")
    text_request = ContentRequest(
        content_type="text",
        prompt="Write a short science fiction story about a time traveler who meets their past self",
        style="creative",
        additional_params={"max_tokens": 800, "temperature": 0.8}
    )
    
    text_result = await pipeline.generate_text(text_request)
    if text_result.status == "completed":
        print(f"✅ Story generated: {text_result.urls[0]}")
        print(f"📊 Generation time: {text_result.generation_time:.2f}s")
    else:
        print(f"❌ Story generation failed: {text_result.metadata.get('error', 'Unknown error')}")
    
    # Generate illustration
    print("\n🖼️ Generating illustration...")
    image_request = ContentRequest(
        content_type="image",
        prompt="A time traveler in a retro-futuristic setting, meeting their past self",
        style="sci-fi, dramatic lighting, digital art",
        dimensions="1024x1024",
        additional_params={"guidance_scale": 8.0, "steps": 50}
    )
    
    image_result = await pipeline.generate_image(image_request)
    if image_result.status == "completed":
        print(f"✅ Illustration generated: {image_result.urls[0]}")
        print(f"📊 Generation time: {image_result.generation_time:.2f}s")
    else:
        print(f"❌ Illustration generation failed: {image_result.metadata.get('error', 'Unknown error')}")

async def example_marketing_campaign():
    """Example: Create a complete marketing campaign"""
    print("\n🚀 Example 2: Marketing Campaign Creation")
    print("=" * 50)
    
    api_token = os.getenv("REPLICATE_API_TOKEN")
    if not api_token:
        print("❌ Please set REPLICATE_API_TOKEN environment variable")
        return
    
    pipeline = ReplicateContentPipeline(api_token=api_token)
    
    # Product: Eco-friendly water bottle
    product_concept = "eco-friendly smart water bottle that tracks hydration"
    
    # Create marketing materials in parallel
    marketing_requests = [
        ContentRequest(
            content_type="text",
            prompt=f"Write compelling marketing copy for a {product_concept}. Include a catchy headline, key benefits, and call-to-action.",
            style="professional",
            additional_params={"max_tokens": 400}
        ),
        ContentRequest(
            content_type="image",
            prompt=f"Professional product photo of {product_concept}, clean white background, studio lighting",
            style="product photography, high quality, commercial",
            dimensions="1024x1024"
        ),
        ContentRequest(
            content_type="video",
            prompt=f"Product demonstration video showing {product_concept} in use",
            style="commercial, clean, modern",
            dimensions="1024x576",
            additional_params={"num_frames": 20, "fps": 8}
        ),
        ContentRequest(
            content_type="audio",
            prompt="Upbeat, modern background music for a product commercial",
            model_version="musicgen",
            duration=15
        )
    ]
    
    print("🔄 Generating marketing materials...")
    start_time = time.time()
    
    results = await pipeline.generate_content_batch(marketing_requests)
    
    total_time = time.time() - start_time
    print(f"\n📊 Campaign generated in {total_time:.2f} seconds")
    
    # Display results
    content_types = ["Marketing Copy", "Product Image", "Demo Video", "Background Music"]
    for i, (name, result) in enumerate(zip(content_types, results)):
        if result.status == "completed":
            print(f"✅ {name}: {result.urls[0]}")
        else:
            print(f"❌ {name} failed: {result.metadata.get('error', 'Unknown error')}")

async def example_social_media_content():
    """Example: Generate content for social media platforms"""
    print("\n📱 Example 3: Social Media Content Creation")
    print("=" * 50)
    
    api_token = os.getenv("REPLICATE_API_TOKEN")
    if not api_token:
        print("❌ Please set REPLICATE_API_TOKEN environment variable")
        return
    
    pipeline = ReplicateContentPipeline(api_token=api_token)
    
    # Theme: "Productivity tips for remote workers"
    theme = "productivity tips for remote workers"
    
    # Create content for different platforms
    social_requests = [
        # Instagram post
        ContentRequest(
            content_type="text",
            prompt=f"Write an engaging Instagram caption about {theme}. Include relevant hashtags and emoji.",
            style="casual",
            additional_params={"max_tokens": 200}
        ),
        ContentRequest(
            content_type="image",
            prompt=f"Instagram-style image about {theme}, clean workspace, motivational",
            style="bright, clean, modern lifestyle photography",
            dimensions="1024x1024"
        ),
        
        # TikTok content
        ContentRequest(
            content_type="text",
            prompt=f"Write a script for a short TikTok video about {theme}. Make it engaging and trendy.",
            style="casual",
            additional_params={"max_tokens": 150}
        ),
        ContentRequest(
            content_type="video",
            prompt=f"Short video about {theme}, dynamic and engaging for social media",
            style="TikTok style, quick cuts, modern",
            dimensions="576x1024",  # Vertical format
            additional_params={"num_frames": 15, "fps": 10}
        ),
        
        # Twitter thread
        ContentRequest(
            content_type="text",
            prompt=f"Write a Twitter thread (5 tweets) about {theme}. Make each tweet valuable and shareable.",
            style="professional",
            additional_params={"max_tokens": 300}
        )
    ]
    
    print("🔄 Generating social media content...")
    results = await pipeline.generate_content_batch(social_requests)
    
    content_names = [
        "Instagram Caption", "Instagram Image", 
        "TikTok Script", "TikTok Video", 
        "Twitter Thread"
    ]
    
    for name, result in zip(content_names, results):
        if result.status == "completed":
            print(f"✅ {name}: {result.urls[0]}")
        else:
            print(f"❌ {name} failed: {result.metadata.get('error', 'Unknown error')}")

async def example_educational_content():
    """Example: Create educational content series"""
    print("\n🎓 Example 4: Educational Content Series")
    print("=" * 50)
    
    api_token = os.getenv("REPLICATE_API_TOKEN")
    if not api_token:
        print("❌ Please set REPLICATE_API_TOKEN environment variable")
        return
    
    pipeline = ReplicateContentPipeline(api_token=api_token)
    
    # Topic: Machine Learning Basics
    topic = "Introduction to Machine Learning"
    
    # Create educational series
    print("🔄 Creating educational content series...")
    
    # Lesson 1: What is Machine Learning?
    lesson1_requests = [
        ContentRequest(
            content_type="text",
            prompt=f"Write a beginner-friendly explanation of '{topic}'. Include key concepts, examples, and why it matters.",
            style="educational",
            additional_params={"max_tokens": 1000}
        ),
        ContentRequest(
            content_type="image",
            prompt="Educational infographic about machine learning concepts, clean design, diagrams",
            style="educational, clean, professional infographic style",
            dimensions="1024x1024"
        ),
        ContentRequest(
            content_type="audio",
            prompt="Calm, focused background music for educational content",
            model_version="musicgen",
            duration=20
        )
    ]
    
    lesson1_results = await pipeline.generate_content_batch(lesson1_requests)
    
    print("\n📚 Lesson 1 - Introduction to Machine Learning:")
    content_types = ["Lesson Text", "Infographic", "Background Music"]
    for name, result in zip(content_types, lesson1_results):
        if result.status == "completed":
            print(f"✅ {name}: {result.urls[0]}")
        else:
            print(f"❌ {name} failed: {result.metadata.get('error', 'Unknown error')}")

async def example_creative_storytelling():
    """Example: Multi-modal creative storytelling"""
    print("\n📖 Example 5: Creative Multimedia Storytelling")
    print("=" * 50)
    
    api_token = os.getenv("REPLICATE_API_TOKEN")
    if not api_token:
        print("❌ Please set REPLICATE_API_TOKEN environment variable")
        return
    
    pipeline = ReplicateContentPipeline(api_token=api_token)
    
    # Use the built-in multimedia story creator
    story_concept = "A lonely robot discovers an abandoned garden and learns about life"
    
    print(f"🔄 Creating multimedia story: '{story_concept}'")
    
    story_results = await pipeline.create_multimedia_story(
        story_prompt=story_concept,
        include_audio=True
    )
    
    print("\n✨ Complete multimedia story created:")
    for content_type, result in story_results.items():
        if result.status == "completed":
            print(f"✅ {content_type.title()}: {result.urls[0]}")
            print(f"   📊 Generated in {result.generation_time:.2f}s")
        else:
            print(f"❌ {content_type.title()} failed: {result.metadata.get('error', 'Unknown error')}")

async def example_batch_content_variations():
    """Example: Generate multiple variations of the same content"""
    print("\n🔄 Example 6: Content Variations")
    print("=" * 50)
    
    api_token = os.getenv("REPLICATE_API_TOKEN")
    if not api_token:
        print("❌ Please set REPLICATE_API_TOKEN environment variable")
        return
    
    pipeline = ReplicateContentPipeline(api_token=api_token)
    
    base_prompt = "A futuristic cityscape at sunset"
    
    # Create variations with different styles
    variation_requests = [
        ContentRequest(
            content_type="image",
            prompt=base_prompt,
            style="cyberpunk, neon colors, dark atmosphere",
            dimensions="1024x1024"
        ),
        ContentRequest(
            content_type="image",
            prompt=base_prompt,
            style="watercolor painting, soft colors, artistic",
            dimensions="1024x1024"
        ),
        ContentRequest(
            content_type="image",
            prompt=base_prompt,
            style="photorealistic, golden hour lighting, cinematic",
            dimensions="1024x1024"
        ),
        ContentRequest(
            content_type="image",
            prompt=base_prompt,
            style="minimalist, clean lines, simple shapes",
            dimensions="1024x1024"
        )
    ]
    
    print("🔄 Generating style variations...")
    results = await pipeline.generate_content_batch(variation_requests)
    
    styles = ["Cyberpunk", "Watercolor", "Photorealistic", "Minimalist"]
    print(f"\n🎨 Generated {len(results)} variations of '{base_prompt}':")
    
    for style, result in zip(styles, results):
        if result.status == "completed":
            print(f"✅ {style} style: {result.urls[0]}")
        else:
            print(f"❌ {style} style failed: {result.metadata.get('error', 'Unknown error')}")

async def main():
    """Run all examples"""
    print("🤖 Content Creation Pipeline Examples")
    print("=====================================\n")
    
    examples = [
        example_basic_content_generation,
        example_marketing_campaign,
        example_social_media_content,
        example_educational_content,
        example_creative_storytelling,
        example_batch_content_variations
    ]
    
    for i, example in enumerate(examples, 1):
        try:
            await example()
            if i < len(examples):
                print("\n" + "="*60 + "\n")
                await asyncio.sleep(1)  # Brief pause between examples
        except Exception as e:
            print(f"❌ Example {i} failed: {str(e)}")
    
    print("\n✅ All examples completed!")
    print("\n💡 Tips:")
    print("- Check the 'generated_content' folder for all created files")
    print("- Adjust prompts and styles in the examples to experiment")
    print("- Use the configuration file to modify model settings")
    print("- Monitor your Replicate usage and costs")

if __name__ == "__main__":
    # Check for API token
    if not os.getenv("REPLICATE_API_TOKEN"):
        print("❌ Error: REPLICATE_API_TOKEN environment variable not set")
        print("\n📋 Setup instructions:")
        print("1. Get your API token from https://replicate.com/account/api-tokens")
        print("2. Set it as an environment variable:")
        print("   export REPLICATE_API_TOKEN='your-token-here'")
        print("3. Run this script again")
        exit(1)
    
    asyncio.run(main())