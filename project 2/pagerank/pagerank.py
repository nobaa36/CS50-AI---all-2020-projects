import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    model = dict()
    pagesCount = len(corpus)
    
    links = corpus[page]
    linksLength = len(links)
    if linksLength == 0:
        links = corpus.keys()
        linksLength = len(links)
    
    for x in corpus: 
        prWithoutDampingFactor = (1 - damping_factor) / pagesCount
        if x in links:
            model[x] = (damping_factor / linksLength) + prWithoutDampingFactor
        else:
            model[x] = prWithoutDampingFactor

    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pageRank = dict()
    counter = dict()
    allPages = []
    for page in corpus: 
        allPages.append(page)
        counter[page] = 0
        
    startPage = random.choice(tuple(allPages))
    counter[startPage] += 1 
    
    currentPage = startPage
    for x in range(SAMPLES - 1):
        weights = []
        transitionProbabilities = transition_model(corpus, currentPage, damping_factor)
        
        weights = transitionProbabilities.values()
        nextPage = random.choices(allPages, weights, k=1)
        counter[nextPage[0]] += 1 
        currentPage = nextPage[0]  
        
    for page in counter: 
        pageRank[page] = counter[page] / SAMPLES
    
    return pageRank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pageRank = dict()
    pagesCount = len(corpus)

    for page in corpus:
        pageRank[page] = 1 / pagesCount

    newPageRank = computeNewPageRank(damping_factor, pagesCount, pageRank, corpus) 
    
    return newPageRank
               
def computeNewPageRank(damping_factor, pagesCount, pageRank, corpus):
    threshold = 0.001
    prWithoutDampingFactor = (1 - damping_factor) / pagesCount

    newPageRank = dict()
  
    for currentPage in pageRank:
        linksToCurrentPage = findLinksToCurrentPage(currentPage, corpus)
        PR_Sum = 0
        for link in linksToCurrentPage:
            PR_Sum = PR_Sum + (pageRank[link] / len(corpus[link]))
        
        newPageRank[currentPage] = prWithoutDampingFactor + (damping_factor * PR_Sum)
            
    for page in pageRank:
        difference = abs(pageRank[page] - newPageRank[page])
        if difference > threshold:
            return computeNewPageRank(damping_factor, pagesCount, newPageRank, corpus)
            
    return newPageRank

def findLinksToCurrentPage(currentPage, corpus):
    linksToCurrentPage = []
    for page in corpus:
        if len(corpus[page]) == 0:
            corpus[page] = corpus.keys()
        
        if currentPage in corpus[page]:
            linksToCurrentPage.append(page)
    return linksToCurrentPage
    
if __name__ == "__main__":
    main()
