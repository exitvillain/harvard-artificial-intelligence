import os
import random
import re
import sys
from collections import Counter 

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
    # since the dictionary that we need to return will have the same keys as the corpus that
    # gets passed into this function, I will just overwrite the values of the corpus(albeit, using a coppy) 
    # with probability values and return it. 
 
    # Find the ammount of links that this page has
    ammount_of_links = len(corpus[page])

    if ammount_of_links == 0:    # this line catches that annoying page about recurssion with a link to itself ha ha ha
        prob_of_each_linked_page = 0 
    else:           
        # There is 85 percent probability to go around for these linked pages. So lets divide to find probability of each page.
        prob_of_each_linked_page = damping_factor/ammount_of_links
    
    # Now we have to ciphen off the 15 percent between each and every page equally. The current page is also included in this 
    prob_to_add_to_each_page = (1 - damping_factor)/len(corpus)

  
    corpus_coppy = corpus.copy()
    for key in corpus_coppy:
        if key in corpus[page]:
            corpus_coppy[key] = round(prob_to_add_to_each_page + prob_of_each_linked_page,4)
        else:
            corpus_coppy[key] = prob_to_add_to_each_page
    return corpus_coppy



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    data = []

    # We need to pick a first page to start with completely at random
    next_sample = random.choice(list(corpus))
    data.append(next_sample)

    for _ in range(n - 1):   # n - 1 because one sample was already taken! 
        prob_distribution = transition_model(corpus,next_sample,damping_factor)
        pages = list(prob_distribution.keys())
        weights = list(prob_distribution.values())

        # generate a sample from the distribution
        next_sample = random.choices(pages,weights=weights,k=1)[0]
        data.append(next_sample)
    
    my_counter = Counter(data)

    # Use a dict comprehension to transform the my_counter dict to having sample frequences to actual percentages that add up to one
    ranks = {key: (frequency / n) for key, frequency in my_counter.items()}
    
    return ranks 


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # find the number of pages in the corpus, call it N
    N = len(corpus)

    # assign initial equal probailities to each page so the iterative algorithm knows where to start
    probabilities = {key: round(1/N,4) for key in corpus}
   
    
    while True:
        counter = 0 
        for page in corpus:
            summation = 0 
            for page_that_links_to_page in corpus:
                if page in corpus[page_that_links_to_page]:
                    # get the number of links that page i has
                    num_links = len(corpus[page_that_links_to_page])
                    summation += round((probabilities[page_that_links_to_page]/num_links),4)
            old_probability = probabilities[page] 
            probabilities[page] = round((damping_factor * summation),4) + round(((1 - damping_factor)/N),4)
            
            if abs(probabilities[page] - old_probability) <= 0.001:
                counter += 1
        
        if counter == N:
            break
       
    # normalize probabilities to sum to 1
    norm = sum(probabilities.values())
    probabilities = {k: v/norm for k, v in probabilities.items()}

    return probabilities 

if __name__ == "__main__":
    main()
