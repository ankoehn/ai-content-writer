# AI Content Writer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Streamlit application that generates content for blog posts, LinkedIn, and X (Twitter) based on a given subject and target audience. The application uses AI to create tailored content for different platforms in parallel.

## 🔍 Prerequisites

### Docker Desktop

This application requires Docker Desktop to run. If you don't have Docker Desktop installed, follow these steps:

#### Windows
1. Download Docker Desktop from [Docker's official website](https://www.docker.com/products/docker-desktop)
2. Run the installer and follow the installation wizard
3. Start Docker Desktop from the Start menu
4. Wait for Docker to start (you'll see the Docker icon in the system tray turn solid)

#### macOS
1. Download Docker Desktop from [Docker's official website](https://www.docker.com/products/docker-desktop)
2. Open the downloaded .dmg file and drag Docker to your Applications folder
3. Start Docker from your Applications folder
4. Wait for Docker to start (you'll see the Docker icon in the menu bar)

#### Linux
1. Follow the instructions for your specific distribution on [Docker's documentation](https://docs.docker.com/engine/install/)
2. Start Docker with `sudo systemctl start docker`
3. Verify installation with `docker --version`

## 🚀 Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-content-writer.git
   cd ai-content-writer
   ```

2. Create your environment file:
   ```bash
   cp .env_template .env
   ```

3. Edit the `.env` file and add your API keys:
   - Required: `TAVILY_API_KEY` for search functionality
   - Required: `OPENAI_API_KEY` for OpenAI models (default provider)
   - Optional: `DEEPSEEK_API_KEY` if using DeepSeek models

4. Configure your LLM provider in the `.env` file:
   - For OpenAI (default):
     ```
     LLM_PROVIDER=openai
     LLM_MODEL=gpt-4o
     ```
   - For DeepSeek:
     ```
     LLM_PROVIDER=deepseek
     LLM_MODEL=deepseek-chat
     DEEPSEEK_API_KEY=your_deepseek_api_key
     ```

## 🏃‍♂️ Running the Application

Start the application using Docker Compose:

```bash
# Run in foreground
docker compose up

# Or run in background
docker compose up -d
```

Access the application in your web browser at:
```
http://localhost:8085
```

## 📝 Usage

1. Open your browser and navigate to `http://localhost:8085`

2. Fill in the form with:
   - Campaign name
   - Content subject (what you want to write about)
   - Target audience (who the content is for)

3. Click "Create" to generate content

4. View the generated content for Blog, LinkedIn, and X

5. Access previously generated content from the history sidebar

6. Export your content history to Excel using the export button

## ⚙️ How It Works

1. The application uses the Tavily search engine to find relevant information about the content subject
2. It then processes this information using three different AI agents specialized for each platform:
   - Blog Agent: Creates a concise two-paragraph blog post
   - LinkedIn Agent: Creates an engaging LinkedIn post with emojis and hashtags
   - X Agent: Creates a short, impactful tweet with emojis and hashtags
3. Generated content is saved to a local JSON file for persistence

## 📁 Project Structure

- `app.py`: Main Streamlit application
- `docker-compose.yml`: Docker Compose configuration
- `Dockerfile`: Docker container configuration
- `requirements.txt`: Python dependencies
- `writer/`: Core content generation functionality
  - `ai/`: AI agents and LLM processing
  - `searchengine/`: Search engine integration
  - `model.py`: Data models
  - `config.py`: Configuration settings
  - `utils/`: Utility functions

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
