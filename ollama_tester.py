"""
Ollama Local Model Testing Script
=================================
This script runs local Ollama models with live streaming output and performance evaluation.
Configure the variables below to test different models and queries.
"""

import time
import json
import sys
from datetime import datetime
from colorama import init, Fore, Style
import ollama

# =====================================
# CONFIGURATION VARIABLES (CHANGE THESE)
# =====================================

# Model name to use (make sure it's installed in Ollama)
MODEL_NAME = "smollm2:135m"

# Query to send to the model
QUERY = "Explain quantum computing in simple terms."

# Ollama server configuration
OLLAMA_HOST = "http://localhost:11434"

# Display configuration
SHOW_DETAILED_METRICS = True
SHOW_TOKEN_STATS = True

# =====================================
# SCRIPT CODE (DON'T CHANGE BELOW)
# =====================================

# Initialize colorama for colored output
init(autoreset=True)

class OllamaEvaluator:
    def __init__(self, model_name, host=OLLAMA_HOST):
        self.model_name = model_name
        self.host = host
        self.client = ollama.Client(host=host)
        
    def print_header(self):
        """Print script header with configuration"""
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}🤖 OLLAMA LOCAL MODEL TESTING")
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}📋 Configuration:")
        print(f"{Fore.WHITE}   Model: {Fore.GREEN}{self.model_name}")
        print(f"{Fore.WHITE}   Host: {Fore.GREEN}{self.host}")
        print(f"{Fore.WHITE}   Time: {Fore.GREEN}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{Fore.YELLOW}❓ Query: {Fore.WHITE}{QUERY}")
        print(f"{Fore.CYAN}{'='*60}")
        print()
    
    def check_model_availability(self):
        """Check if the model is available"""
        try:
            response = self.client.list()
            models = response.models
            available_models = [model['name'] for model in models['models']]
            
            if self.model_name not in available_models:
                print(f"{Fore.RED}❌ Error: Model '{self.model_name}' is not available.")
                print(f"{Fore.YELLOW}📋 Available models:")
                for model in available_models:
                    print(f"   • {model}")
                print(f"{Fore.CYAN}💡 To install a model, run: ollama pull {self.model_name}")
                return False
            else:
                print(f"{Fore.GREEN}✅ Model '{self.model_name}' is available.")
                return True
        except Exception as e:
            print(f"{Fore.RED}❌ Error connecting to Ollama: {e}")
            print(f"{Fore.YELLOW}💡 Make sure Ollama is running: ollama serve")
            return False
    
    def run_query_with_streaming(self):
        """Run query with live streaming and collect metrics"""
        print(f"{Fore.YELLOW}🚀 Starting query execution...")
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}📤 Response Stream:")
        print()
        
        # Performance tracking variables
        start_time = time.time()
        first_token_time = None
        total_tokens = 0
        response_text = ""
        
        try:
            # Stream the response
            stream = self.client.chat(
                model=self.model_name,
                messages=[{'role': 'user', 'content': QUERY}],
                stream=True
            )
            
            print(f"{Fore.WHITE}", end="", flush=True)
            
            for chunk in stream:
                current_time = time.time()
                
                # Mark first token time
                if first_token_time is None:
                    first_token_time = current_time
                
                # Extract content from chunk
                if 'message' in chunk and 'content' in chunk['message']:
                    content = chunk['message']['content']
                    response_text += content
                    total_tokens += len(content.split())
                    
                    # Print content in real-time
                    print(content, end="", flush=True)
            
            end_time = time.time()
            
            print(f"\n{Style.RESET_ALL}")  # Reset color and add newline
            
            # Calculate metrics
            total_time = end_time - start_time
            time_to_first_token = first_token_time - start_time if first_token_time else 0
            tokens_per_second = total_tokens / total_time if total_time > 0 else 0
            
            # Display evaluation metrics
            self.display_metrics(total_time, time_to_first_token, total_tokens, tokens_per_second, response_text)
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}⚠️  Query interrupted by user.")
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error during query execution: {e}")
    
    def display_metrics(self, total_time, time_to_first_token, total_tokens, tokens_per_second, response_text):
        """Display performance evaluation metrics"""
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}📊 PERFORMANCE EVALUATION")
        print(f"{Fore.CYAN}{'='*60}")
        
        # Basic metrics
        print(f"{Fore.WHITE}⏱️  Total Time: {Fore.GREEN}{total_time:.2f} seconds")
        print(f"{Fore.WHITE}🚀 Time to First Token: {Fore.GREEN}{time_to_first_token:.2f} seconds")
        
        if SHOW_TOKEN_STATS:
            print(f"{Fore.WHITE}🔢 Total Tokens: {Fore.GREEN}{total_tokens}")
            print(f"{Fore.WHITE}⚡ Tokens/Second: {Fore.GREEN}{tokens_per_second:.2f}")
        
        if SHOW_DETAILED_METRICS:
            print(f"{Fore.WHITE}📝 Response Length: {Fore.GREEN}{len(response_text)} characters")
            print(f"{Fore.WHITE}📏 Average Word Length: {Fore.GREEN}{len(response_text) / max(total_tokens, 1):.1f} chars/word")
        
        # Performance rating
        self.display_performance_rating(tokens_per_second, time_to_first_token)
        
        print(f"{Fore.CYAN}{'='*60}")
    
    def display_performance_rating(self, tokens_per_second, time_to_first_token):
        """Display performance rating based on metrics"""
        print(f"{Fore.WHITE}🏆 Performance Rating:", end=" ")
        
        # Rating based on tokens per second and response time
        if tokens_per_second > 20 and time_to_first_token < 2:
            print(f"{Fore.GREEN}Excellent ⭐⭐⭐⭐⭐")
        elif tokens_per_second > 15 and time_to_first_token < 3:
            print(f"{Fore.GREEN}Very Good ⭐⭐⭐⭐")
        elif tokens_per_second > 10 and time_to_first_token < 5:
            print(f"{Fore.YELLOW}Good ⭐⭐⭐")
        elif tokens_per_second > 5 and time_to_first_token < 10:
            print(f"{Fore.YELLOW}Fair ⭐⭐")
        else:
            print(f"{Fore.RED}Needs Improvement ⭐")
    
    def run(self):
        """Main execution method"""
        self.print_header()
        
        if not self.check_model_availability():
            return
        
        print()
        self.run_query_with_streaming()
        
        print(f"\n{Fore.CYAN}✨ Testing completed!")
        print(f"{Fore.YELLOW}💡 To test with different parameters, modify the variables at the top of this script.")

def main():
    """Main function"""
    try:
        evaluator = OllamaEvaluator(MODEL_NAME, OLLAMA_HOST)
        evaluator.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Script terminated by user.")
    except Exception as e:
        print(f"{Fore.RED}❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
