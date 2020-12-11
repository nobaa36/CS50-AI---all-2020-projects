import sys

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
        
        for variable in self.domains.keys():
            domainsCopy = self.domains[variable].copy()
            for word in domainsCopy:
                if len(word) != variable.length:   
                    self.domains[variable].remove(word)
                    
    def areNeighbors(self, x, y):
        neighbors = self.crossword.neighbors(x)
        if y in neighbors:
            return True
        else:
            return False
        
    def getOverlapPoint(self, x , y):
        for overlap in self.crossword.overlaps:
            if overlap[0] == x and overlap[1] == y:
                return self.crossword.overlaps[overlap]
        
    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revisionMade = False
        areXYNeighbors = self.areNeighbors(x, y)        

        for wordX in self.domains[x].copy():
            if len(self.domains[y]) == 1 and wordX in self.domains[y]:
                revisionMade = True                  
                self.domains[x].remove(wordX)
                continue
            if areXYNeighbors: 
                consistencyFound = -1
                overlapPoint = self.getOverlapPoint(x, y)
                overlapLetter = wordX[overlapPoint[0]]
                allWordsInY = self.domains[y].copy()
                for wordY in self.domains[y]:
                    start = overlapPoint[1]
                    end = overlapPoint[1] + 1
                    foundPosition = wordY.find(overlapLetter, start, end)
                    if foundPosition == -1:
                        allWordsInY.remove(wordY)
                
                if len(allWordsInY) == 0:
                    revisionMade = True
                    self.domains[x].remove(wordX)
 

        return revisionMade
        

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        noDomainsEmpty = True
        initialArcs = []
        allVariables = self.domains.keys()
        
        for x in allVariables:
            for y in allVariables:
                if x is not y: 
                    initialArcs.append((x, y))
        
        for arc in initialArcs:
            self.revise(arc[0],arc[1]) 
            
            
        values = self.domains.values()
        for value in values: 
            if len(value) == 0:
                noDomainsEmpty = False         
        
        return noDomainsEmpty

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        complete = True
        for variable in assignment:
            if len(assignment[variable]) == 0:
                complete = False
                
        return complete

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        isConsistent = True

        for variableX in assignment:
            for variableY in assignment:
                if variableX is not variableY:
                    if assignment[variableX] == assignment[variableY] and len(assignment[variableX]) > 0 and len(assignment[variableY]) > 0:
                        isConsistent = False
                        break
                    
                    if self.areNeighbors(variableX, variableY):
                        overlapPoint = self.getOverlapPoint(variableX, variableY)
                        wordX = assignment[variableX]
                        wordY = assignment[variableY] 
                        if len(wordX) > 0 and len(wordY) > 0:
                            if wordX[overlapPoint[0]] != wordY[overlapPoint[1]]:
                                isConsistent = False
                                break

        return isConsistent   

    def getRuledOutWords(self, word, var, neighbors):
        counter = 0
        for neighbor in neighbors:
            values = self.domains[neighbor]
            if len(values) == 1:
                (value,) = values
                if value == word: 
                    counter += 1
            
            overlapPoint = self.getOverlapPoint(var, neighbor)
            for value in values: 
                if word[overlapPoint[0]] != value[overlapPoint[1]]:
                    counter += 1
            
        
        return counter             
    
    def order_domain_values(self, var, assignment):  
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        unorderedlist = self.domains[var]
        neighbors = self.crossword.neighbors(var) 
        for variable in assignment:
            if len(assignment[variable]) == 1 and variable in neighbors:
                neighbors.remove(variable)
        
        
        ruledOutCounter = []
        for word in unorderedlist:
            ruledOutWordsAmount = self.getRuledOutWords(word, var, neighbors)
            ruledOutCounter.append({'word' : word, 'counter' : ruledOutWordsAmount}) 
            
        ruledOutCounterSorted = sorted(ruledOutCounter, key=lambda k: k['counter'])
        orderedList = [i['word'] for i in ruledOutCounterSorted]

        return orderedList
      
        
        
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        remainingValuesCounter = []
        for variable in assignment:
            if len(assignment[variable]) == 0: 
                remainingValuesCounter.append({"variable" : variable, "valuesAmount" : len(self.domains[variable])})
        
        sortedRemainingValuesCounter = sorted(remainingValuesCounter, key=lambda k: k['valuesAmount'])
        if len(sortedRemainingValuesCounter) == 1:
            return sortedRemainingValuesCounter[0]['variable']
        if sortedRemainingValuesCounter[0]['valuesAmount'] != sortedRemainingValuesCounter[1]['valuesAmount']:
            return sortedRemainingValuesCounter[0]['variable']
        else:
            var1neighborsAmount = len(self.crossword.neighbors(sortedRemainingValuesCounter[0]['variable']))
            var2neighborsAmount = len(self.crossword.neighbors(sortedRemainingValuesCounter[1]['variable']))
            if var1neighborsAmount >= var2neighborsAmount:
                return sortedRemainingValuesCounter[0]['variable']
            else: 
                return sortedRemainingValuesCounter[1]['variable']

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        
        if len(assignment) == 0:
            assignment = dict()
            for variable in self.domains:
                if len(self.domains[variable]) == 1: 
                    (finalWord,) = self.domains[variable]
                    assignment[variable] = finalWord
                else:
                    assignment[variable] = {}        
           

        if self.consistent(assignment):
            if self.assignment_complete(assignment):
                return assignment
            else:
                unassigned_variable = self.select_unassigned_variable(assignment) 
                orderedList = self.order_domain_values(unassigned_variable, assignment)
                for word in orderedList:
                    customAssignment = assignment.copy()
                    customAssignment[unassigned_variable] = word
                    result = self.backtrack(customAssignment)
                    if result != None:
                        return result
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
