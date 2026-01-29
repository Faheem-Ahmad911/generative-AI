import asyncio
import time
import random
import pandas as pd  # Added for Excel handling
from typing import List, Union
from dataclasses import dataclass, asdict # added asdict to convert data easily
from functools import wraps

# --- TASK 1: DATA STRUCTURES ---
@dataclass
class ResearchResult:
    source: str
    content: str
    latency: float
    timestamp: float = time.time()

# --- TASK 2: THE RESILIENT DECORATOR ---
def retry(retries: int = 3, delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"⚠️  [Attempt {attempt + 1}/{retries}] {func.__name__} failed: {e}")
                    if attempt < retries - 1:
                        await asyncio.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

# --- TASK 3: THE ASYNC FETCHER ---
@retry(retries=3, delay=1.0)
async def fetch_research(source: str) -> ResearchResult:
    wait_time = random.uniform(1.0, 2.5)
    await asyncio.sleep(wait_time)
    
    if random.random() < 0.20: # 20% failure rate
        raise ConnectionError(f"Database {source} is unreachable.")
        
    return ResearchResult(
        source=source,
        content=f"AI insights from {source}...",
        latency=wait_time
    )

# --- TASK 4: THE ORCHESTRATOR & EXPORTER ---
async def main():
    sources = ["Arxiv", "PubMed", "JSTOR", "IEEE", "Google Scholar"]
    start_time = time.perf_counter()
    
    print(f"🚀 Starting parallel fetch...")

    tasks = [fetch_research(source) for source in sources]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Filter out errors and convert Dataclasses to Dictionaries for Pandas
    successful_data = [asdict(res) for res in results if isinstance(res, ResearchResult)]
    
    if successful_data:
        # Create DataFrame
        df = pd.DataFrame(successful_data)
        
        # Save to Excel
        filename = "research_results.xlsx"
        df.to_excel(filename, index=False)
        print(f"\n📁 Data saved successfully to {filename}")
        
        # Quick Stat Check
        print(f"📈 Average Latency: {df['latency'].mean():.2f}s")
    else:
        print("\n❌ No data was retrieved successfully to save.")

    end_time = time.perf_counter()
    print(f"🕒 Total Execution Time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())