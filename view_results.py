"""
JSON Results Viewer for Ollama Test Results
===========================================
This script helps you view and analyze the saved test results from ollama_tester.py
"""

import json
import sys
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

JSON_LOG_FILE = "ollama_test_results.json"

def load_results():
    """Load results from JSON file"""
    try:
        with open(JSON_LOG_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("test_results", [])
    except FileNotFoundError:
        print(f"{Fore.RED}❌ No results file found: {JSON_LOG_FILE}")
        return []
    except json.JSONDecodeError:
        print(f"{Fore.RED}❌ Invalid JSON in file: {JSON_LOG_FILE}")
        return []

def display_summary(results):
    """Display summary statistics"""
    if not results:
        return
    
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}📊 TEST RESULTS SUMMARY")
    print(f"{Fore.CYAN}{'='*60}")
    
    total_tests = len(results)
    models_tested = set(r["model_name"] for r in results)
    
    print(f"{Fore.YELLOW}📈 Overall Statistics:")
    print(f"{Fore.WHITE}   Total Tests: {Fore.GREEN}{total_tests}")
    print(f"{Fore.WHITE}   Models Tested: {Fore.GREEN}{len(models_tested)}")
    print(f"{Fore.WHITE}   Models: {Fore.GREEN}{', '.join(models_tested)}")
    
    # Performance averages
    avg_tps = sum(r["metrics"]["tokens_per_second"] for r in results) / total_tests
    avg_time = sum(r["metrics"]["total_time"] for r in results) / total_tests
    avg_first_token = sum(r["metrics"]["time_to_first_token"] for r in results) / total_tests
    
    print(f"{Fore.YELLOW}⚡ Performance Averages:")
    print(f"{Fore.WHITE}   Tokens/Second: {Fore.GREEN}{avg_tps:.2f}")
    print(f"{Fore.WHITE}   Total Time: {Fore.GREEN}{avg_time:.2f}s")
    print(f"{Fore.WHITE}   Time to First Token: {Fore.GREEN}{avg_first_token:.2f}s")
    
    # Rating distribution
    ratings = [r["performance"]["rating"] for r in results]
    rating_counts = {}
    for rating in ratings:
        rating_counts[rating] = rating_counts.get(rating, 0) + 1
    
    print(f"{Fore.YELLOW}🏆 Performance Ratings:")
    for rating, count in rating_counts.items():
        percentage = (count / total_tests) * 100
        print(f"{Fore.WHITE}   {rating}: {Fore.GREEN}{count} ({percentage:.1f}%)")
    
    print()

def display_detailed_results(results, limit=None):
    """Display detailed results"""
    if not results:
        print(f"{Fore.YELLOW}📝 No test results found.")
        return
    
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}📋 DETAILED TEST RESULTS")
    print(f"{Fore.CYAN}{'='*60}")
    
    # Sort by timestamp (newest first)
    sorted_results = sorted(results, key=lambda x: x["timestamp"], reverse=True)
    
    if limit:
        sorted_results = sorted_results[:limit]
        print(f"{Fore.YELLOW}Showing latest {limit} results:")
    
    for i, result in enumerate(sorted_results, 1):
        timestamp = result["timestamp"][:19].replace('T', ' ')
        model = result["model_name"]
        query = result["query"]
        response = result["response"]
        metrics = result["metrics"]
        performance = result["performance"]
        
        print(f"\n{Fore.YELLOW}📋 Test #{len(results) - i + 1 if not limit else i}")
        print(f"{Fore.WHITE}🕒 Time: {Fore.GREEN}{timestamp}")
        print(f"{Fore.WHITE}🤖 Model: {Fore.GREEN}{model}")
        print(f"{Fore.WHITE}❓ Query: {Fore.CYAN}{query}")
        
        print(f"{Fore.WHITE}📊 Metrics:")
        print(f"{Fore.WHITE}   ⏱️  Total Time: {Fore.GREEN}{metrics['total_time']}s")
        print(f"{Fore.WHITE}   🚀 First Token: {Fore.GREEN}{metrics['time_to_first_token']}s")
        print(f"{Fore.WHITE}   🔢 Tokens: {Fore.GREEN}{metrics['total_tokens']}")
        print(f"{Fore.WHITE}   ⚡ Tokens/Sec: {Fore.GREEN}{metrics['tokens_per_second']}")
        
        rating_color = Fore.GREEN if performance['rating'] in ['Excellent', 'Very Good'] else Fore.YELLOW if performance['rating'] == 'Good' else Fore.RED
        print(f"{Fore.WHITE}🏆 Rating: {rating_color}{performance['rating']} {performance['rating_stars']}")
        
        # Show response preview
        response_preview = response[:100] + "..." if len(response) > 100 else response
        print(f"{Fore.WHITE}💬 Response: {Fore.CYAN}{response_preview}")
        
        print(f"{Fore.CYAN}{'-'*40}")

def compare_models(results):
    """Compare performance across different models"""
    if not results:
        return
    
    # Group by model
    model_results = {}
    for result in results:
        model = result["model_name"]
        if model not in model_results:
            model_results[model] = []
        model_results[model].append(result)
    
    if len(model_results) < 2:
        print(f"{Fore.YELLOW}📊 Need at least 2 different models to compare.")
        return
    
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}🆚 MODEL COMPARISON")
    print(f"{Fore.CYAN}{'='*60}")
    
    for model, model_tests in model_results.items():
        avg_tps = sum(r["metrics"]["tokens_per_second"] for r in model_tests) / len(model_tests)
        avg_time = sum(r["metrics"]["total_time"] for r in model_tests) / len(model_tests)
        test_count = len(model_tests)
        
        # Get most common rating
        ratings = [r["performance"]["rating"] for r in model_tests]
        most_common_rating = max(set(ratings), key=ratings.count)
        
        print(f"\n{Fore.YELLOW}🤖 {model}")
        print(f"{Fore.WHITE}   Tests: {Fore.GREEN}{test_count}")
        print(f"{Fore.WHITE}   Avg Tokens/Sec: {Fore.GREEN}{avg_tps:.2f}")
        print(f"{Fore.WHITE}   Avg Time: {Fore.GREEN}{avg_time:.2f}s")
        print(f"{Fore.WHITE}   Common Rating: {Fore.GREEN}{most_common_rating}")

def main():
    """Main function"""
    print(f"{Fore.CYAN}🔍 Ollama Test Results Viewer")
    print(f"{Fore.CYAN}{'='*30}")
    
    results = load_results()
    
    if not results:
        print(f"{Fore.YELLOW}💡 Run ollama_tester.py first to generate test results.")
        return
    
    while True:
        print(f"\n{Fore.YELLOW}📋 Options:")
        print(f"{Fore.WHITE}1. {Fore.GREEN}Summary Statistics")
        print(f"{Fore.WHITE}2. {Fore.GREEN}Latest 5 Results")
        print(f"{Fore.WHITE}3. {Fore.GREEN}All Results")
        print(f"{Fore.WHITE}4. {Fore.GREEN}Model Comparison")
        print(f"{Fore.WHITE}5. {Fore.GREEN}Export to CSV")
        print(f"{Fore.WHITE}0. {Fore.RED}Exit")
        
        try:
            choice = input(f"\n{Fore.CYAN}Choose option (0-5): {Fore.WHITE}").strip()
            
            if choice == "0":
                print(f"{Fore.YELLOW}👋 Goodbye!")
                break
            elif choice == "1":
                display_summary(results)
            elif choice == "2":
                display_detailed_results(results, limit=5)
            elif choice == "3":
                display_detailed_results(results)
            elif choice == "4":
                compare_models(results)
            elif choice == "5":
                export_to_csv(results)
            else:
                print(f"{Fore.RED}❌ Invalid option. Please choose 0-5.")
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}👋 Goodbye!")
            break

def export_to_csv(results):
    """Export results to CSV file"""
    if not results:
        return
    
    try:
        import csv
        csv_file = "ollama_test_results.csv"
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow([
                'Timestamp', 'Model', 'Query', 'Response', 'Total_Time', 
                'Time_to_First_Token', 'Total_Tokens', 'Tokens_per_Second',
                'Response_Length', 'Performance_Rating', 'Performance_Score'
            ])
            
            # Write data
            for result in results:
                writer.writerow([
                    result['timestamp'],
                    result['model_name'],
                    result['query'],
                    result['response'],
                    result['metrics']['total_time'],
                    result['metrics']['time_to_first_token'],
                    result['metrics']['total_tokens'],
                    result['metrics']['tokens_per_second'],
                    result['metrics']['response_length_chars'],
                    result['performance']['rating'],
                    result['performance']['performance_score']
                ])
        
        print(f"{Fore.GREEN}✅ Results exported to {csv_file}")
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error exporting to CSV: {e}")

if __name__ == "__main__":
    main()
