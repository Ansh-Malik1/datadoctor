'''
This is the file where code for checking leakage will be written.
Data leakage occurs when information from outside the training dataset is used to 
create the model — leading to unrealistically good performance during training but poor generalization
on real data.

The most common form is when features are too correlated with 
the target — i.e., they directly or indirectly contain the target value.

User will give :
1. Target
2. Threshold
'''
def detect_leakage():
    return