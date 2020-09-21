import re

def load_corpus(path):
    with open(path) as f:
        corpus = f.readlines()
    return corpus

def clean_line(line):
    line = re.sub('[^A-Za-z0-9 ]+', '', line[:-1]) # remove non-alphanumeric characters - remove traditional endline
    return '<'+line.lower()+'>' # add the start and endline characters, remove capitals

def ngram(line, loc, n):
    return (line[loc + i] for i in range(n))

def unigram_table(corpus):
    counts = {}
    # count occuraces of each letter
    for line in corpus:
        line = clean_line(line)
        for char in line:
            if char not in counts:
                counts[char] = 1
            else:
                counts[char] += 1
    return counts

def unigram_probs(counts):
    #divide counts by total, to get probabilities
    total = 0
    for count in counts:
        total += counts[count]
    for count in counts:
        counts[count] /= total
    return counts

def transition_table(corpus, n_prior):
    transitions = {}
    # count occurances of each transition
    for line in corpus:
        line = clean_line(line)
        ngrams = [line[i:i+n_prior] for i in range(len(line)-n_prior)]
        for i in range(len(ngrams)-1):
            ngram = ngrams[i]
            if ngram not in transitions:
                transitions[ngram] = {ngrams[i+1]:1}
            else:
                if ngrams[i+1] not in transitions[ngram]:
                    transitions[ngram][ngrams[i+1]] = 1
                else:
                    transitions[ngram][ngrams[i+1]] += 1
    return transitions

#TODO: normalize by the unigram distribution - is it significantly different than normalizing each column (done here)
def ngram_probs(transitions):
    for w_prior in transitions:
        col_total = 0
        for w in transitions[w_prior]:
            col_total += transitions[w_prior][w]
        for w in transitions[w_prior]:
            transitions[w_prior][w] /= col_total
    return transitions

def ngram_k_smooth(transitions, k, calc_prob=True):
    all_ngrams = list(transitions.keys())
    for w_prior in transitions:
        col_total = 0
        for w in all_ngrams:
            if w in transitions[w_prior]:
                transitions[w_prior][w] += k
            else:
                transitions[w_prior][w] = k
            col_total += transitions[w_prior][w]
        # calculate the probabilities from the k-smoothed counts
        if calc_prob:
            for w in transitions[w_prior]:
                transitions[w_prior][w] /= col_total
    return transitions

# transition_tables should be in the form [ngrams, unigram]
def ngram_linear_interp(ngram_probs, unigram_probs, lambdas, calc_prob=True):
    p_hat = {}
    for idx, n_gram in enumerate(n_gram_probs):
        # TODO - finish the linear interp - basically, make the new p_hat table, and iterate through the different n, add to table
    return p_hat

# write them to json! that would be fun to try and figure out how json works
def write_model_path(path):
    with open(path, 'wb') as f:
        print(path)

if __name__ == "__main__":
    en_corpus = load_corpus('./assignment1-data/training.en')
    #en_unigram = unigram_table(en_corpus)
    en_bigram = transition_table(en_corpus,1)
    #en_trigram = transition_table(en_corpus,2)

    #en_bigram_probs = ngram_probs(en_bigram)
    en_bigram_k_smooth = ngram_probs_k_smooth(en_bigram, 1)

    print('Done')