# 🤖 Ollama Local Model Testing Suite

A comprehensive Python toolkit for testing and evaluating local Ollama models with real-time streaming, performance metrics, and detailed logging.

## ✨ Features

- 🚀 **Real-time Streaming** - Watch model responses generate live
- 📊 **Performance Evaluation** - Detailed metrics including tokens/second, response time, and quality ratings
- 💾 **JSON Logging** - Automatically save all test results with timestamps and metrics
- 🔍 **Results Analysis** - Built-in viewer for analyzing test history and comparing models
- 🎯 **Easy Configuration** - Simple variables at the top for quick testing
- 🏆 **Performance Rating** - Automatic scoring from ⭐ to ⭐⭐⭐⭐⭐
- 📈 **Model Comparison** - Compare performance across different models
- 📋 **CSV Export** - Export results for external analysis

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Ollama installed and running
- Required Python packages (see installation)

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd Ollama-LLM-Local-Testing
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or manually:
   ```bash
   pip install ollama colorama
   ```

3. **Start Ollama** (if not already running)
   ```bash
   ollama serve
   ```

4. **Pull a model** (if you don't have one)
   ```bash
   ollama pull llama3.2
   # or
   ollama pull smollm2:135m
   ```

5. **Run the tester**
   ```bash
   python ollama_tester.py
   ```

## 📋 Configuration

Edit the variables at the top of `ollama_tester.py` to customize your tests:

```python
# =====================================
# CONFIGURATION VARIABLES (CHANGE THESE)
# =====================================

# Model name to use (make sure it's installed in Ollama)
MODEL_NAME = "llama3.2"

# Query to send to the model
QUERY = "Explain quantum computing in simple terms."

# Ollama server configuration
OLLAMA_HOST = "http://localhost:11434"

# Display configuration
SHOW_DETAILED_METRICS = True
SHOW_TOKEN_STATS = True

# JSON logging configuration
SAVE_TO_JSON = True
JSON_LOG_FILE = "ollama_test_results.json"
```

## 🔧 Usage Examples

### Basic Testing
```bash
# Test with default settings
python ollama_tester.py
```

### Custom Model Testing
1. Edit `MODEL_NAME` in the script to your desired model
2. Update `QUERY` with your test prompt
3. Run the script

### View Previous Results
```bash
python view_results.py
```

## 📊 Sample Output

```
============================================================
🤖 OLLAMA LOCAL MODEL TESTING
============================================================
📋 Configuration:
   Model: llama3.2
   Host: http://localhost:11434
   Time: 2025-07-08 14:30:25
❓ Query: Explain quantum computing in simple terms.
============================================================

📊 Previous Test Results (3 tests):
   1. 2025-07-08 14:25:10 | llama3.2 | Very Good | 18.4 tok/s
   2. 2025-07-08 14:20:05 | smollm2:135m | Good | 12.8 tok/s

✅ Model 'llama3.2' is available.

🚀 Starting query execution...
============================================================
📤 Response Stream:

Quantum computing is a revolutionary technology that...
[Live streaming response appears here]

============================================================
📊 PERFORMANCE EVALUATION
============================================================
⏱️  Total Time: 8.45 seconds
🚀 Time to First Token: 1.23 seconds
🔢 Total Tokens: 156
⚡ Tokens/Second: 18.46
📝 Response Length: 892 characters
📏 Average Word Length: 5.7 chars/word
🏆 Performance Rating: Very Good ⭐⭐⭐⭐
============================================================

💾 Results saved to ollama_test_results.json

✨ Testing completed!
📁 Results logged to: ollama_test_results.json
💡 To test with different parameters, modify the variables at the top of this script.
```

## 📈 Results Analysis

The `view_results.py` script provides comprehensive analysis:

### 1. Summary Statistics
- Total tests run
- Models tested
- Average performance metrics
- Rating distribution

### 2. Detailed Results
- View individual test results
- Full conversation history
- Performance breakdowns

### 3. Model Comparison
- Compare different models side-by-side
- Performance rankings
- Average metrics per model

### 4. Data Export
- Export to CSV for external analysis
- Includes all metrics and metadata

## 📁 File Structure

```
Ollama-LLM-Local-Testing/
├── ollama_tester.py          # Main testing script
├── view_results.py           # Results viewer and analyzer
├── requirements.txt          # Python dependencies
├── setup.sh                 # Automated setup script
├── README.md                # This file
├── ollama_test_results.json  # Generated results log
└── .gitignore               # Git ignore file
```

## 🔍 Metrics Explained

### Performance Metrics
- **Total Time**: Complete response generation time
- **Time to First Token**: Latency before first response chunk
- **Total Tokens**: Number of tokens in the response
- **Tokens/Second**: Generation speed (higher is better)
- **Response Length**: Character count of the response

### Performance Ratings
- ⭐⭐⭐⭐⭐ **Excellent**: >20 tok/s, <2s first token
- ⭐⭐⭐⭐ **Very Good**: >15 tok/s, <3s first token  
- ⭐⭐⭐ **Good**: >10 tok/s, <5s first token
- ⭐⭐ **Fair**: >5 tok/s, <10s first token
- ⭐ **Needs Improvement**: Below fair thresholds

## 🛠️ Advanced Usage

### Testing Multiple Models
1. Change `MODEL_NAME` between runs
2. Use the same `QUERY` for consistent comparison
3. View results with `python view_results.py`

### Batch Testing
Create a simple loop in your own script:
```python
from ollama_tester import OllamaEvaluator

models = ["llama3.2", "smollm2:135m", "qwen2:1.5b"]
queries = ["Explain AI", "Write a poem", "Solve 2+2"]

for model in models:
    for query in queries:
        # Update globals and run test
        # (Implementation details in the script)
```

### Custom Metrics
The JSON output includes all raw data, so you can:
- Calculate custom performance scores
- Create your own visualizations
- Build automated reports

## 🔧 Troubleshooting

### Common Issues

1. **"Model not available" error**
   ```bash
   ollama pull <model-name>
   ```

2. **"Error connecting to Ollama"**
   ```bash
   ollama serve
   ```

3. **Import errors**
   ```bash
   pip install -r requirements.txt
   ```

4. **Permission errors on scripts**
   ```bash
   chmod +x setup.sh view_results.py
   ```

### Performance Tips

- **Faster testing**: Use smaller models like `smollm2:135m`
- **Better quality**: Use larger models like `llama3.2`
- **Consistent results**: Use the same query across different models
- **Historical analysis**: Keep `SAVE_TO_JSON = True` enabled

## 📊 JSON Schema

The results are saved in this format:
```json
{
  "test_results": [
    {
      "timestamp": "2025-07-08T14:30:25.123456",
      "model_name": "llama3.2",
      "host": "http://localhost:11434",
      "query": "Your test query",
      "response": "Model's full response",
      "metrics": {
        "total_time": 8.45,
        "time_to_first_token": 1.23,
        "total_tokens": 156,
        "tokens_per_second": 18.46,
        "response_length_chars": 892,
        "average_word_length": 5.7
      },
      "performance": {
        "rating": "Very Good",
        "rating_stars": "⭐⭐⭐⭐",
        "performance_score": 15.23
      },
      "configuration": {
        "show_detailed_metrics": true,
        "show_token_stats": true
      }
    }
  ]
}
```

## 🤝 Contributing

Feel free to:
- Add new metrics
- Improve the rating system
- Add support for more model types
- Create visualization tools
- Submit bug reports and feature requests

## 📝 License

[Include your license information here]

## 🔗 Related Links

- [Ollama Official Website](https://ollama.ai)
- [Ollama GitHub Repository](https://github.com/ollama/ollama)
- [Available Models](https://ollama.ai/library)

---

**Happy Testing! 🚀**
