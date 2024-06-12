import sys
import copy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for v in self.domains:
            words_in_x_domain = copy.deepcopy(self.domains[v])
            for x in words_in_x_domain:
                if v.length != len(x):
                   self.domains[v].remove(x) 

        
       
        
    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # if there is no overlaps between varialbes, no need to revise. So Return False
        if self.crossword.overlaps[x,y] is None:
            return False

        (i,j) = self.crossword.overlaps[x,y]
        revision = False
        words_in_x_domain = copy.deepcopy(self.domains[x])
        for x_word in words_in_x_domain:
            trouble_words_counter = 0 
            for y_word in self.domains[y]:
                if x_word[i] == y_word[j]:
                    break
                else:
                    trouble_words_counter += 1
            if trouble_words_counter == len(self.domains[y]):
                self.domains[x].remove(x_word)
                revision = True
        
        return revision
       
       
        

            

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        
        if arcs is not None:
            q = arcs 
        else:
            q = []
            for key in self.crossword.overlaps:
                if self.crossword.overlaps[key] is not None:
                    q.append(key)
        while q:
            x, y = q.pop(0) 
            if self.revise(x,y):
                if len(self.domains[x]) == 0:
                    return False
                # we need to reinfoce arc consistency on some nodes
                for neighbor in self.crossword.neighbors(x) - {y}:
                        q.append((x,neighbor))
                """
                the following is an alternative aproach for the requeue. i used it at first when I didn't realize i could do 
                crossword.neighbors 
                
                for key in crossword.overlaps:
                    if key[0] == x and key[1] != y and crossword.overlaps[key] is not None and key not in q:
                        q.append(key)
                """

        return True
        
       

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # my original aproach, before i decided to get fancy 
        return len(assignment) == len(self.domains)

       
       


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        
        words = set()
        for key, value in assignment.items():

            # check for length of assignment word matching the space it takes up in the crossword
            if key.length != len(value):
                return False

            # check that each assignment word is unique
            if value in words:
                return False
            words.add(value)

            #check that there are no conflicts between neighbors
            for neighbor in self.crossword.neighbors(key): 
                (i,j) = self.crossword.overlaps[key,neighbor]
                if neighbor in assignment:
                    if value[i] != assignment[neighbor][j]:
                        return False
            
         # If we reach this point, then all checks have passed
        return True
       

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        #crossword.neighbors(var) returns a list of overlapping variables. so it returns a list of variable objects
        # self.domains is a dictioanry mapping values to a set of words
      
        conflicts = {}
        list_of_unasigned_neighbors = self.crossword.neighbors(var) - set(assignment.keys())
        for word in self.domains[var]:
            conflict_counter = 0 
            for neighbor_variable in list_of_unasigned_neighbors:
                (i,j) = self.crossword.overlaps[var,neighbor_variable]
                for y_word in self.domains[neighbor_variable]:
                    if word[i] != y_word[j]:
                        conflict_counter += 1 
            conflicts[word] = conflict_counter

        sorted_keys = sorted(conflicts, key = lambda k : conflicts[k])
        return sorted_keys
        
       
        
        """
        # for now just return a list of the words in the varialbes domain in any order
        return list(self.domains[var])
        """
       
        
      
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        
        """
        # this just returns any variable not in assignment without heuristics 
        for variable in self.domains:
            if variable not in assignment:
                return variable
        """
        
        
        def sorting_function(key):
            return (len(self.domains[key]), -len(self.crossword.neighbors(key)))

        unassigned_keys = [key for key in self.domains.keys() if key not in assignment]
        sorted_keys = sorted(unassigned_keys, key=sorting_function)
        return sorted_keys[0]
        

      

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # base case. If the assignment is complete, return it
        if self.assignment_complete(assignment):
            return assignment 
        else:
            var_to_assign = self.select_unassigned_variable(assignment)
            for word in self.order_domain_values(var_to_assign, assignment):
                new_assignment = assignment.copy()
                new_assignment[var_to_assign] = word
                if self.consistent(new_assignment):
                    result = self.backtrack(new_assignment)
                    if result is not None:
                        return result 
                new_assignment.pop(var_to_assign) 
            return None  



def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")
    
    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
