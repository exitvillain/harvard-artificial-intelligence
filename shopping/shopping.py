import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer                0
        - Administrative_Duration, a floating point number     1
        - Informational, an integer
        - Informational_Duration, a floating point number      3
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number     5
        - BounceRates, a floating point number                 
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number                 9
        - Month, an index from 0 (January) to 11 (December)   10
        - OperatingSystems, an integer           11
        - Browser, an integer         12
        - Region, an integer    13
        - TrafficType, an integer   14
        - VisitorType, an integer 0 (not returning) or 1 (returning)  15
        - Weekend, an integer 0 (if false) or 1 (if true)       16

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    month_dict = {'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 
              'June': 5, 'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9,
              'Nov': 10, 'Dec': 11}
    evidence = []
    labels = [] 
    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            evidence_row = []
            for column in range(len(row)):
                if column == 1 or column == 3 or column == 5 or column == 6 or column == 7 or column == 8 or column == 9:
                    data_nugget = float(row[column])
                elif column == 0 or column == 2 or column == 4 \
                        or column == 11 or column == 12 or column == 13 or column == 14:
                    data_nugget = int(row[column])
                elif column == 10:
                    data_nugget = month_dict[row[column]]
                elif column == 15:
                    if row[column] == "Returning_Visitor":
                        data_nugget = 1
                    else:
                        data_nugget = 0 
                elif column  == 16:
                    data_nugget = 1 if row[column] == 'TRUE' else 0
                elif column == 17:
                    labels.append(1 if row[column] == 'TRUE' else 0)
                evidence_row.append(data_nugget)
            evidence.append(evidence_row)
    return(evidence,labels)



def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    result = KNeighborsClassifier(n_neighbors=1)
    return result.fit(evidence,labels)



def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    true_total = 0 
    false_total = 0 
    true_correct = 0 
    true_incorrect = 0
    false_correct = 0
    false_incorrect = 0 
    for actual, predicted in zip(labels, predictions):
        if actual == 1:
            true_total += 1
            if actual == predicted:
                true_correct += 1
            else:
                true_incorrect += 1
        else:
            false_total += 1 
            if actual == predicted:
                false_correct += 1
            else:
                false_incorrect +=1

    sensitivity = true_correct / true_total 
    specificity = false_correct/ false_total      
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
