# Welcome to the Qiskit Hackathon at World of QUANTUM

## 📄  [Click here to download the In-Person Attendee Guide](https://github.com/qiskit-community/Qiskit-Hackathon-at-World-of-QUANTUM/raw/main/Attendee%20Guide%20In-Person.pdf)

### About

The Qiskit Hackathon@World of QUANTUM is the first Qiskit event happening in person in Germany hosted by the Federal Ministry of Education and Research (BMBF), IBM Quantum's Community Team and Messe München GmbH.

The hackathon will kickoff with an opening presentation and guideline review.

Participants will then form teams of 4-5 people and work on a challenge for the next 24 hours.

Mentors will be available to support and help the teams during the hackathon.

After the 24 hours, a committee of experts will evaluate the outcome and select the winners.


### Timeline

#### Tuesday 26 April
11:55 – 12:15 - Welcome note at the Forum World of QUANTUM

12:15 - 14:30 - Guidelines, lunch, and team formation in the Hackathon Space

14:30 - Start of the Hacking Phase in the Hackathon Space

*Between 20:00 (26 April) and 08:00 (27 April) you may ask questions in the dedicated Qiskit Event
Slack Channel [#hackathon-woq-support](https://qiskit.slack.com/archives/C03BJNQ0S15) for remote assistance. [[Click here to join
Qiskit Slack](https://ibm.co/joinqiskitslack), if needed.]

#### Tuesday 26 April
14:00 - End of the Hacking Phase and start of the Judging Phase

14:30 - 16:00 - Optional Project Presentation & Community Choice Award

16:00 - 16:30 - Closing Ceremony at the Forum World of QUANTUM

### Projects

Please find full details on the Hackathon Project format, team formation, and project submission in the [In-Person Attendee Guide](https://github.com/qiskit-community/Qiskit-Hackathon-at-World-of-QUANTUM/blob/main/Attendee%20Guide%20In-Person.pdf). 

Here is an [example of an Education Hackathon Project Submission](https://github.com/TigrisCallidus/Education-Hackathon-Template) for your review.

### Questions

If you have any questions, please ask the team of Qiskit Mentors at the event or post them in the dedicated Qiskit Event
Slack Channel [#hackathon-woq-support](https://qiskit.slack.com/archives/C03BJNQ0S15).

# Content Creation Pipeline with Replicate APIs

A comprehensive, production-ready pipeline for creating multimedia content using Replicate's AI models. This pipeline enables automated generation of text, images, videos, and audio content through a unified interface.

## 🚀 Features

### Content Types Supported
- **Text Generation**: Stories, articles, marketing copy, social media content
- **Image Creation**: Illustrations, product photos, concept art, social media visuals
- **Video Synthesis**: Short clips, animations, product demos, social content
- **Audio Generation**: Music, sound effects, ambient audio, speech synthesis

### Key Capabilities
- **Multi-modal Content Creation**: Generate complete multimedia stories and campaigns
- **Batch Processing**: Create multiple pieces of content in parallel
- **Style Customization**: Apply different artistic styles and themes
- **Format Flexibility**: Support for various dimensions, durations, and formats
- **Error Handling**: Robust error handling with retry mechanisms
- **Async Support**: Efficient async/await implementation for performance

## 📋 Requirements

- Python 3.8+
- Replicate API account and token
- Required packages (see `requirements.txt`)

## 🛠️ Installation

1. **Clone or download the pipeline files**:
   ```bash
   # Files needed:
   # - content_creation_pipeline.py
   # - requirements.txt
   # - config.yaml
   # - examples.py
   # - README.md
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Get your Replicate API token**:
   - Visit [Replicate API Tokens](https://replicate.com/account/api-tokens)
   - Create a new token
   - Copy the token value

4. **Set up environment variable**:
   ```bash
   # Linux/macOS
   export REPLICATE_API_TOKEN='your-token-here'
   
   # Windows
   set REPLICATE_API_TOKEN=your-token-here
   
   # Or create a .env file
   echo "REPLICATE_API_TOKEN=your-token-here" > .env
   ```

## 🎯 Quick Start

### Basic Usage

```python
import asyncio
from content_creation_pipeline import ReplicateContentPipeline, ContentRequest

async def main():
    # Initialize pipeline
    pipeline = ReplicateContentPipeline(api_token="your-replicate-token")
    
    # Generate an image
    image_request = ContentRequest(
        content_type="image",
        prompt="A beautiful sunset over mountains",
        style="photorealistic, cinematic",
        dimensions="1024x1024"
    )
    
    result = await pipeline.generate_image(image_request)
    print(f"Generated image: {result.urls[0]}")

asyncio.run(main())
```

### Multimedia Story Creation

```python
async def create_story():
    pipeline = ReplicateContentPipeline(api_token="your-replicate-token")
    
    # Generate a complete multimedia story
    story_results = await pipeline.create_multimedia_story(
        story_prompt="A robot discovering emotions through art",
        include_audio=True
    )
    
    for content_type, result in story_results.items():
        print(f"{content_type}: {result.urls[0]}")

asyncio.run(create_story())
```

## 📖 Detailed Usage

### Content Request Structure

The `ContentRequest` class is the main interface for content generation:

```python
ContentRequest(
    content_type="image",           # Required: "text", "image", "video", "audio"
    prompt="Your description",      # Required: What you want to generate
    style="artistic, colorful",     # Optional: Style modifiers
    dimensions="1024x1024",         # Optional: For images/videos
    duration=10,                    # Optional: For videos/audio (seconds)
    model_version="sdxl",          # Optional: Specific model to use
    additional_params={             # Optional: Model-specific parameters
        "guidance_scale": 8.0,
        "steps": 50
    }
)
```

### Text Generation

```python
text_request = ContentRequest(
    content_type="text",
    prompt="Write a marketing email for a new AI product",
    style="professional",
    additional_params={
        "max_tokens": 500,
        "temperature": 0.7
    }
)

result = await pipeline.generate_text(text_request)
```

**Available Text Models:**
- `llama-2-70b` (default): High-quality general purpose
- `llama-3-8b`: Faster, good for shorter content
- `mixtral-8x7b`: Excellent for complex reasoning

### Image Generation

```python
image_request = ContentRequest(
    content_type="image",
    prompt="A futuristic city with flying cars",
    style="cyberpunk, neon lights, detailed",
    dimensions="1024x1024",
    additional_params={
        "guidance_scale": 8.0,
        "steps": 50,
        "num_outputs": 1
    }
)

result = await pipeline.generate_image(image_request)
```

**Available Image Models:**
- `sdxl` (default): Stability AI's SDXL 1.0
- `dall-e-3`: OpenAI's DALL-E 3
- `flux-pro`: Black Forest Labs' Flux Pro

**Common Dimensions:**
- Square: `"1024x1024"`
- Landscape: `"1344x768"`, `"1536x640"`
- Portrait: `"768x1344"`, `"640x1536"`

### Video Generation

```python
video_request = ContentRequest(
    content_type="video",
    prompt="A cat playing with a ball of yarn",
    style="cute, playful, high quality",
    dimensions="1024x576",
    additional_params={
        "num_frames": 25,
        "fps": 8,
        "motion_bucket_id": 127
    }
)

result = await pipeline.generate_video(video_request)
```

**Available Video Models:**
- `stable-video` (default): Stability AI's Stable Video Diffusion
- `animate-diff`: Motion generation from images
- `gen-2`: Runway's Gen-2 model

### Audio Generation

```python
# Music generation
music_request = ContentRequest(
    content_type="audio",
    prompt="Upbeat electronic music for a workout video",
    model_version="musicgen",
    duration=20
)

# Speech synthesis
speech_request = ContentRequest(
    content_type="audio",
    prompt="Hello, welcome to our AI-powered content creation system!",
    model_version="bark",
    additional_params={
        "language": "en",
        "speaker": "default"
    }
)
```

**Available Audio Models:**
- `musicgen` (default): Meta's MusicGen for music
- `riffusion`: Riffusion music generation
- `bark`: Suno AI's Bark for speech

### Batch Content Generation

Generate multiple pieces of content in parallel:

```python
requests = [
    ContentRequest(content_type="text", prompt="Write a product description"),
    ContentRequest(content_type="image", prompt="Product hero image", dimensions="1024x1024"),
    ContentRequest(content_type="video", prompt="Product demo video", dimensions="1024x576"),
    ContentRequest(content_type="audio", prompt="Background music", duration=15)
]

results = await pipeline.generate_content_batch(requests)

for i, result in enumerate(results):
    print(f"Content {i+1}: {result.urls[0] if result.status == 'completed' else 'Failed'}")
```

## 🎨 Style Presets

The pipeline includes predefined style presets for different content types:

### Image Styles
- `photorealistic`: Professional photography look
- `artistic`: Creative and expressive
- `cyberpunk`: Futuristic neon aesthetic
- `vintage`: Retro and nostalgic
- `minimalist`: Clean and simple

### Video Styles
- `cinematic`: Film-quality production
- `animation`: Cartoon-style animation
- `documentary`: Natural, realistic style
- `music_video`: Dynamic and artistic

### Text Styles
- `creative`: Imaginative storytelling
- `professional`: Business communication
- `casual`: Conversational tone
- `academic`: Scholarly analysis

## 📁 Output Management

Generated content is automatically saved to the `generated_content/` directory:

```
generated_content/
├── text_1704067200.txt
├── image_1704067201.png
├── video_1704067202.mp4
├── audio_1704067203.wav
└── story_1704067204_metadata.json
```

Each file includes:
- **Timestamp**: For unique identification
- **Content type**: In the filename
- **Metadata**: JSON files for complex generations

## 🔧 Configuration

Modify `config.yaml` to customize:

- **Model Settings**: Change default models and parameters
- **Style Presets**: Add custom style definitions
- **Pipeline Settings**: Adjust timeouts, concurrency, output paths
- **Safety Settings**: Configure content filters and rate limits

Example configuration customization:

```yaml
# In config.yaml
pipeline:
  output_directory: "./my_content"
  max_concurrent_requests: 3
  timeout_seconds: 600

models:
  image:
    default: "flux-pro"  # Change default image model
```

## 🚀 Advanced Examples

### Marketing Campaign Creation

```python
async def create_marketing_campaign():
    pipeline = ReplicateContentPipeline(api_token="your-token")
    
    product = "eco-friendly water bottle"
    
    campaign_requests = [
        ContentRequest("text", f"Marketing copy for {product}", "professional"),
        ContentRequest("image", f"Hero image of {product}", "product photography"),
        ContentRequest("video", f"Demo video of {product}", "commercial"),
        ContentRequest("audio", "Upbeat commercial music", duration=15)
    ]
    
    results = await pipeline.generate_content_batch(campaign_requests)
    return results
```

### Social Media Content Suite

```python
async def create_social_content():
    theme = "productivity tips"
    
    social_requests = [
        # Instagram
        ContentRequest("text", f"Instagram caption about {theme}", "casual"),
        ContentRequest("image", f"Instagram post about {theme}", dimensions="1024x1024"),
        
        # TikTok
        ContentRequest("text", f"TikTok script about {theme}", "trendy"),
        ContentRequest("video", f"TikTok video about {theme}", dimensions="576x1024"),
        
        # Twitter
        ContentRequest("text", f"Twitter thread about {theme}", "professional")
    ]
    
    return await pipeline.generate_content_batch(social_requests)
```

### Educational Content Series

```python
async def create_lesson():
    topic = "Introduction to AI"
    
    lesson_requests = [
        ContentRequest("text", f"Lesson content about {topic}", "educational"),
        ContentRequest("image", f"Infographic about {topic}", "educational"),
        ContentRequest("audio", "Background music for learning", duration=30)
    ]
    
    return await pipeline.generate_content_batch(lesson_requests)
```

## 📊 Performance & Costs

### Typical Generation Times
- **Text**: 10-30 seconds
- **Images**: 15-45 seconds  
- **Videos**: 60-180 seconds
- **Audio**: 30-90 seconds

### Cost Optimization Tips
1. **Use appropriate models**: Choose the right model for your quality needs
2. **Batch requests**: Generate multiple items in parallel
3. **Optimize parameters**: Reduce steps/frames for faster generation
4. **Monitor usage**: Check Replicate dashboard regularly

### Rate Limits
- Default: 10 requests/minute, 100 requests/hour
- Configurable in `config.yaml`
- Automatic retry with exponential backoff

## 🛡️ Safety & Best Practices

### Content Safety
- Built-in content filtering for harmful content
- Automatic watermarking for AI-generated content
- Rate limiting to prevent abuse

### Error Handling
```python
try:
    result = await pipeline.generate_image(request)
    if result.status == "completed":
        print(f"Success: {result.urls[0]}")
    else:
        print(f"Failed: {result.metadata.get('error')}")
except Exception as e:
    print(f"Error: {str(e)}")
```

### Best Practices
1. **Always check result status** before using generated content
2. **Handle errors gracefully** with try/catch blocks
3. **Monitor API usage** to avoid unexpected costs
4. **Use appropriate timeouts** for long-running generations
5. **Cache results** when possible to avoid regeneration

## 🔍 Troubleshooting

### Common Issues

**API Token Not Set**
```bash
# Error: REPLICATE_API_TOKEN environment variable not set
export REPLICATE_API_TOKEN='your-token-here'
```

**Generation Timeout**
```python
# Increase timeout in config.yaml or request
additional_params={"timeout": 600}  # 10 minutes
```

**Out of Credits**
- Check your Replicate account balance
- Add payment method or credits
- Monitor usage in Replicate dashboard

**Model Not Found**
- Verify model IDs in `config.yaml`
- Check Replicate model availability
- Use alternative models as fallback

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# This will show detailed API calls and responses
```

## 📚 API Reference

### ReplicateContentPipeline

```python
class ReplicateContentPipeline:
    def __init__(self, api_token: str)
    
    async def generate_text(self, request: ContentRequest) -> ContentResult
    async def generate_image(self, request: ContentRequest) -> ContentResult
    async def generate_video(self, request: ContentRequest) -> ContentResult
    async def generate_audio(self, request: ContentRequest) -> ContentResult
    async def generate_content_batch(self, requests: List[ContentRequest]) -> List[ContentResult]
    async def create_multimedia_story(self, story_prompt: str, include_audio: bool = True) -> Dict[str, ContentResult]
    
    def get_model_info(self) -> Dict[str, Any]
```

### ContentRequest

```python
@dataclass
class ContentRequest:
    content_type: str  # "text", "image", "video", "audio"
    prompt: str
    style: Optional[str] = None
    duration: Optional[int] = None
    dimensions: Optional[str] = None
    model_version: Optional[str] = None
    additional_params: Optional[Dict[str, Any]] = None
```

### ContentResult

```python
@dataclass
class ContentResult:
    content_type: str
    prompt: str
    urls: List[str]
    metadata: Dict[str, Any]
    generation_time: float
    status: str  # "completed", "failed"
```

## 🌟 Examples

Run the comprehensive examples:

```bash
python examples.py
```

This will demonstrate:
1. Basic content generation
2. Marketing campaign creation
3. Social media content suite
4. Educational content series
5. Creative storytelling
6. Content variations

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Additional model integrations
- New content types (e.g., 3D models)
- Enhanced error handling
- Performance optimizations
- UI/web interface
- More style presets

## 📄 License

This project is open source. Check individual model licenses on Replicate.

## 🔗 Resources

- [Replicate Platform](https://replicate.com/)
- [Replicate API Documentation](https://replicate.com/docs)
- [Available Models](https://replicate.com/collections)
- [Pricing Information](https://replicate.com/pricing)

## 💬 Support

For issues and questions:
1. Check this README and configuration files
2. Review Replicate documentation
3. Check model-specific documentation
4. Monitor Replicate status page for service issues

---

**Happy Creating! 🎨✨**

*This pipeline enables anyone to harness the power of AI for content creation. Whether you're a marketer, educator, content creator, or developer, you can now generate professional-quality multimedia content with just a few lines of code.*




