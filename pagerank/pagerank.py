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
    pages = corpus.keys()
    rem_df_probability = (1 - damping_factor) / len(pages)
    probability_distribution = {page: rem_df_probability for page in pages}
    links = corpus.get(page, pages)
    number_of_links = len(links)
    df_probability = damping_factor / number_of_links
    for link in links:
        probability_distribution[link] += df_probability
    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())
    sample = transition_model(corpus, random.choice(pages), damping_factor)
    for _ in range(n):
        choice = random.choices(list(sample.keys()), weights=list(sample.values()))[0]
        sample = transition_model(corpus, choice, damping_factor)
    return sample


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages_rank = dict()
    pages = corpus.keys()
    rank = 1 / len(pages)
    c1 = (1 - damping_factor) / len(pages)
    for page in pages:
        pages_rank[page] = rank
    while True:
        new_pages_rank = dict()
        for page in pages:
            links_weights = list()
            for link in corpus.get(page):
                if len(corpus[link]) > 0:
                    links_weights.append(pages_rank[link] / len(corpus[link]))
                else:
                    links_weights.append(pages_rank[link] / len(pages))
            links_ranks = damping_factor * sum(links_weights)
            new_pages_rank[page] = links_ranks + c1
        changes = list()
        for page in pages:
            changes.append(abs(pages_rank[page] - new_pages_rank[page]))
        if max(changes) < 0.001:
            break
        pages_rank = new_pages_rank.copy()
    return pages_rank


if __name__ == "__main__":
    main()