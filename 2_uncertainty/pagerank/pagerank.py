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


def test():
    corpus = crawl('corpus2')
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    sum = 0
    print(f'PageRank Results from Sampling (n = {SAMPLES})')
    for page in sorted(ranks):
        print(f' {page}: {ranks[page]:.4f}')
        sum += ranks[page]
    print(f'Sum of all probabilities: {sum}')


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
    pages_pdist = {}  # Probability distribution
    total_count = len(corpus)  # Number of all pages in the corpus
    linked_count = len(corpus[page])  # Number of pages linked to by the page

    for p in corpus:
        pages_pdist[p] = (1 - damping_factor) / total_count
        if p in corpus[page]:
            pages_pdist[p] += damping_factor / linked_count

    return pages_pdist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pageranks = {page: 0 for page in corpus.keys()}
    # First sample is chosen at random
    sample = random.choice(list(corpus.keys()))
    idx = n

    while idx > 0:
        pageranks[sample] += 1  # Update sample's pagerank

        # Chose next sample according to transition model
        trmodel = transition_model(corpus, sample, DAMPING)
        population = list(trmodel.keys())
        weights = [trmodel[page] for page in population]
        sample = random.choices(population, weights)[0]

        idx -= 1

    return {page: pageranks[page] / n for page in corpus}


def pageranks_max_delta(iter_a, iter_b):
    """Retrun the maximum difference between the ranks of two iterations."""
    deltas = []

    for page in iter_a:
        rank_a = iter_a[page]
        rank_b = iter_b[page]
        deltas.append(abs(rank_a - rank_b))

    return max(deltas)


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initilize pageranks dictionary with the starting values of 1 / N
    pageranks = {page: 1 / len(corpus) for page in corpus}
    # Calculate the constant part of the formula for iterated pageranks
    prconstant = (1 - damping_factor) / len(corpus)

    while True:
        new_pageranks = {}

        for page in pageranks:
            backlinks = [p for p in corpus if page in corpus[p]]
            psum = 0

            for backlink in backlinks:
                psum += pageranks[backlink] / len(corpus[backlink])

            new_pageranks[page] = prconstant + damping_factor * psum

        if pageranks_max_delta(pageranks, new_pageranks) <= 0.001:
            return new_pageranks
        else:
            pageranks = new_pageranks


if __name__ == "__main__":
    main()
    # test()
