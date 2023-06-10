# About

This repository was created in the context of the 2023 edition of the Scientific Day organized by the ISEP IEEE Student Branch and GroopTown. 

It aims to provide candidates tools to assess and evaluate their solutions. 

## Working with the repository 

### 1. Loading you Slideshows

Start by copying all the outfiles you want to evaluate in the `./outputs` folder of this repository. 

In the original state there is one example outfile named `./outputs/example.txt` don't hesitate to look at it !

### 2. Running the Evaluation

To launch an evaluation of all the outfiles in the `./outputs` run following command at the root of this repository: 

`python3 evaluate.py`

### 3. Reading the Feedback

The evaluation script will check the validity and score each outfile. Note, if at least one invalidity condition is met, a warning will be raised with indications regarding the issue. The score for each valid outfile will be displayed in the console alongside the total of all the file. 

Note, the total include doesn't check if two solutions are related to the same dataset. In your final score only the best score for each dataset will be taken into account so be aware of it.


