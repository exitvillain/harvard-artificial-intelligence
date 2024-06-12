import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])
    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)


    
    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.
    
    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """



    jp = 1 
   
    for person in one_gene:
        
        if people[person]["father"] is None:      # if person has no parents listed, calculation is much simpler
            prob_person_has_one_coppy = PROBS["gene"][1]
        else:
            mother = people[person]["mother"]
            if mother in one_gene:
                prob_got_from_mom = .50
            elif mother in two_genes:
                prob_got_from_mom = 1 - PROBS["mutation"]
            else:
                prob_got_from_mom = PROBS["mutation"]
                    
            father = people[person]["father"]
            if father in one_gene:
                prob_got_from_dad = .50
            elif father in two_genes:
                prob_got_from_dad = 1 - PROBS["mutation"]
            else:
                prob_got_from_dad = PROBS["mutation"]

            prob_not_got_from_mom = 1 - prob_got_from_mom
            prob_not_got_from_dad = 1 - prob_got_from_dad

            prob_person_has_one_coppy = prob_got_from_mom * prob_not_got_from_dad + prob_got_from_dad * prob_not_got_from_mom 

        if person in have_trait:
            prob_person_trait_given_they_have_one_coppy = PROBS["trait"][1][True] * prob_person_has_one_coppy
        else:
            prob_person_trait_given_they_have_one_coppy = PROBS["trait"][1][False] * prob_person_has_one_coppy
                

        jp *= prob_person_trait_given_they_have_one_coppy 
        
    for person in two_genes:
        if people[person]["father"] is None:   
            prob_person_has_two_coppies = PROBS["gene"][2]
        else:
            mother = people[person]["mother"]
            if mother in one_gene:
                prob_got_from_mom = .50
            elif mother in two_genes:
                prob_got_from_mom = 1 - PROBS["mutation"]
            else:
                prob_got_from_mom = PROBS["mutation"]
                    
            father = people[person]["father"]
            if father in one_gene:
                prob_got_from_dad = .50
            elif father in two_genes:
                prob_got_from_dad = 1 - PROBS["mutation"]
            else:
                prob_got_from_dad = PROBS["mutation"]

            prob_not_got_from_mom = 1 - prob_got_from_mom
            prob_not_got_from_dad = 1 - prob_got_from_dad

            prob_person_has_two_coppies = prob_got_from_dad * prob_got_from_mom 

        if person in have_trait:
            prob_person_trait_given_they_have_two_coppies = PROBS["trait"][2][True] * prob_person_has_two_coppies
        else:
            prob_person_trait_given_they_have_two_coppies = PROBS["trait"][2][False] * prob_person_has_two_coppies
        
        jp *= prob_person_trait_given_they_have_two_coppies

    no_gene = []        # this little loop is to gather all the no gene people into a new list so we can iterate over them
    for person in people:
        if (person not in one_gene) and (person not in two_genes):
            no_gene.append(person)
    
    for person in no_gene:
        if people[person]["father"] is None:   
            prob_person_has_no_coppies = PROBS["gene"][0]
        else:
            mother = people[person]["mother"]
            if mother in one_gene:
                prob_got_from_mom = .50
            elif mother in two_genes:
                prob_got_from_mom = 1 - PROBS["mutation"]
            else:
                prob_got_from_mom = PROBS["mutation"]
                    
            father = people[person]["father"]
            if father in one_gene:
                prob_got_from_dad = .50
            elif father in two_genes:
                prob_got_from_dad = 1 - PROBS["mutation"]
            else:
                prob_got_from_dad = PROBS["mutation"]

            prob_not_got_from_mom = 1 - prob_got_from_mom
            prob_not_got_from_dad = 1 - prob_got_from_dad

            prob_person_has_no_coppies = prob_not_got_from_dad * prob_not_got_from_mom
        if person in have_trait:
            prob_person_trait_given_they_have_no_coppies = PROBS["trait"][0][True] * prob_person_has_no_coppies
        else:
            prob_person_trait_given_they_have_no_coppies = PROBS["trait"][0][False] * prob_person_has_no_coppies
        
        jp *= prob_person_trait_given_they_have_no_coppies
    
    return jp 
        

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in two_genes:
            probabilities[person]["gene"][2] += p
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        if person in have_trait:
            probabilities[person]["trait"][True] += p 
        if (person not in two_genes) and (person not in one_gene):
            probabilities[person]["gene"][0] += p 
        if person not in have_trait:
            probabilities[person]["trait"][False] += p 



def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
   
    for person in probabilities:
        norm = sum(probabilities[person]["gene"].values())
        probabilities[person]["gene"] = {k: v/norm for k, v in probabilities[person]["gene"].items()}

        norm = sum(probabilities[person]["trait"].values())
        probabilities[person]["trait"] = {k: v/norm for k, v in probabilities[person]["trait"].items()}
    


if __name__ == "__main__":
    main()
