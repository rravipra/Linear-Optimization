# Linear-Optimization

Overall application of the project involves minimizing the loss of materials from customizing pre-existing material inventory to the inventory needed to begin a construction project. 

A simplification of the project involved receiving a preset size of stock (in this case wood) and dimensions and quantity of the final output required and us outputting the quantity of stock wood we need and how the stock wood should be cut to result in a minimum loss. We want to find/make an algorithm to minimize the loss of wood when we go from the original wood pieces to the pieces in the dimensions we need. We will start with a one dimensional optimization, we will assume that only the length of the wood needs to be changed and that the width and thickness are constant between input and output.

For example, we are given inputs of 12 ft of stock wood, and we are told we need to output 5 pieces of 6 ft wood, 3 pieces of 5 ft wood, and 4 pieces of 3ft wood.
We need to now find out how many pieces of 12 ft wood we need to produce the desired wood, how to best cut the stock wood to produce the desired wood with minimum loss, theoretical minimum loss, and loss produced by our cutting strategy.

Files:
The woodc_deploy file contains app.py which is the streamlit version of the algoithm to deploy it on huggingface. It also consists of requirements.txt for the libraries that need to be imported to run the code.

Deployed webpage link:
https://huggingface.co/spaces/rthvik07/woodc_deploy
