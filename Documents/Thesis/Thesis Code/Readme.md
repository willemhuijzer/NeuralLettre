
Flow of gathering results 
1. Generate variable combination of demographics that need to be evaluated. 
    - The file data_demographics/generate_demographics.ipynb generates a csv file with for each for the demographics that need to be inserted into the input text and eventually. 

1. Loop over question_id's
 2. Loop over the demographics combinations and create from the unfilled texts the filled texts
  3. Loop over the prompts framework and insert the filled texts
   4. Generate a response and save to results