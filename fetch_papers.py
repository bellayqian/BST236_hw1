import arxiv
import json
import os
from datetime import datetime

# Configure your search query here
SEARCH_QUERY = 'cat:cs.AI AND (ti:machine learning OR ti:deep learning OR ti:artificial intelligence)'
MAX_RESULTS = 50

def fetch_papers():
    # Create arxiv client
    client = arxiv.Client()
    
    # Create search object
    search = arxiv.Search(
        query=SEARCH_QUERY,
        max_results=MAX_RESULTS,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    
    # Fetch results
    papers = []
    for result in client.results(search):
        paper = {
            'title': result.title,
            'authors': [author.name for author in result.authors],
            'abstract': result.summary,
            'pdf_url': result.pdf_url,
            'published': result.published.isoformat(),
            'arxiv_url': result.entry_id,
            'categories': result.categories
        }
        papers.append(paper)
    
    return papers

def save_papers(papers):
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Save papers to JSON file
    with open('data/papers.json', 'w', encoding='utf-8') as f:
        json.dump({
            'last_updated': datetime.utcnow().isoformat(),
            'papers': papers
        }, f, ensure_ascii=False, indent=2)

def main():
    papers = fetch_papers()
    save_papers(papers)

if __name__ == '__main__':
    main()