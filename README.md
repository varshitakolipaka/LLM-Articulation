# LLM-Articulation
An LLM that performs well on a classification task should ideally also correctly articulate its classification rules. Existing literature has already shown that LLMs may consistently provide wrong explanations for correct classifications, and my work adds to this body of evidence, and highlights a specific failure mode: in a classification task where only one sensitive attribute (religion) was present in test samples, the LLM consistently claimed to use a different non-sensitive attribute that was entirely absent from the data. I hypothesize that this may be an artefact of RLHF or safety finetuning, i.e. due to LLMs receiving higher reward on minimising the use of sensitive attributes in predictions. 


Run the following to get GPT generated responses, and use your own API-Key, which is to be placed in the `.env` folder.

```
python get_responses.py
```
Run the following to generate all plots.
```
python analysis.py
```

