# Importing necessary libraries
import os
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
nltk.download("stopwords")


def measure(files, text_dir):
    ''' For Calculating the Average Sentence Length, Percentage of Complex Words, Fod Index, Syllable Per Word, Complex Word Count'''
    stopwords_ = (stopwords.words("english"))
    with open(os.path.join(text_dir, files), "r") as f:
        text = f.read()
        sentence = text.split(". ")
        num_sentences = len(sentence)

        words = [ word for word in text.split() if word.lower() not in stopwords_ ]
        num_words = len(words)

        complex_words = []
        for word in words:
            vowels = ["a", "e", "i", "o", "u"]
            syllable_word_count = sum( 1 for letter in word if letter.lower() in vowels)
            if syllable_word_count > 2:
                complex_words.append(word)

        syllable_count = 0
        syllable_words = []
        for word in words:
            if word.endswith("es") or word.endswith("ed"):
                pass
            else:
                vowels = ["a", "e", "i", "o", "u"]
                syllable_count_words = sum(1 for letter in word if letter.lower() in vowels)
                if syllable_count_words >= 1:
                    syllable_words.append(word)
                    syllable_count += syllable_count_words
                
        avg_sentence_len = num_words / num_sentences
        avg_syllable_word_count = syllable_count / len(syllable_words)
        Percent_Complex_words  =  len(complex_words) / num_words
        Fog_Index = 0.4 * (avg_sentence_len + Percent_Complex_words)

    return avg_sentence_len, Percent_Complex_words, Fog_Index, len(complex_words),avg_syllable_word_count


def cleaned_words(files, text_dir):
    ''' For Calculating Word Count, Average Word Length '''
    stopwords_ = stopwords.words("english")
    with open(os.path.join(text_dir, files), "r") as f:
        text = f.read()

        words = [word for word in text.split() if word.lower() not in stopwords_]
        length = sum(len(word) for word in words)
        average_word_length = length / len(words)
    
    return len(words),average_word_length


def count_personal_pronouns(file, text_dir):
    ''' For Calculating Personal Pronouns '''
    with open(os.path.join(text_dir, file), 'r') as f:
        text = f.read()
        personal_pronouns = ["I", "we", "my", "ours", "us"]
        count = 0
        for pronoun in personal_pronouns: 
            count += len(re.findall(r"\b" + pronoun + r"\b", text.lower())) 
            # \b is used to match word boundaries
    
    return count


if __name__ == "__main__":
    
    # Reading the input file to a dataframe
    data = pd.read_excel("/home/vo1d/Desktop/VS_Code/Blackcoffer/Input.xlsx")
    
    
    # Extracting the article text and saving it inside the txt files named "URL_ID.txt"
    for (url, filename) in zip(data["URL"], data["URL_ID"]):
        try:
            file_name = filename + ".txt"
            file_path = "/home/vo1d/Desktop/VS_Code/Blackcoffer/files/" + file_name
            content = requests.get(url)
            soup = BeautifulSoup(content.text, "html.parser")  

            article_title = soup.find("h1", attrs = {"class": "entry-title"}).get_text()
            article_text = soup.find(class_ = "td-post-content tagdiv-type").get_text()
        
            total_text = article_title + "\n\n" + article_text
            
            with open(file_path, "w") as f:
                f.write(total_text)
                
        # bs4 throws an attribution error when it doesn't find the required html elements
        except AttributeError as e:
            print(f"Error in {file_name}")
            
            
    # Directories
    stopwords_dir = "/home/vo1d/Desktop/VS_Code/Blackcoffer/stopwords/"
    sentiment_dir = "/home/vo1d/Desktop/VS_Code/Blackcoffer/sentiment_docs/"
    text_dir = "/home/vo1d/Desktop/VS_Code/Blackcoffer/files/"
    
    
    # Storing stopwords in a list
    stop_words = []
    for files in os.listdir(stopwords_dir):
        with open(os.path.join(stopwords_dir, files), "r", encoding = "ISO-8859-1") as f:
            stop_words.extend(list(f.read().splitlines()))
            
            
    # Storing the positive and negative words in a list
    pos = []
    neg = []
    for files in os.listdir(sentiment_dir):
        if files == "positive-words.txt":
            with open(os.path.join(sentiment_dir, files), "r", encoding = "ISO-8859-1") as f:
                pos.extend(f.read().splitlines())
        elif files == "negative-words.txt":
            with open(os.path.join(sentiment_dir, files), "r", encoding = "ISO-8859-1") as f:
                neg.extend(f.read().splitlines())
                
                
    # Storing the article text in a list 
    data = list()
    for files in os.listdir(text_dir):
        with open(os.path.join(text_dir, files), "r", encoding = "ISO-8859-1") as f:
            text = (f.read().split())

            # Filtering the article text by removing the stop_words
            filtered_text = [words for words in text if words.lower() not in stop_words]
            data.append(filtered_text)
            
    
    # Calculating the Positive Score, Negative Score, Polarity Score, Subjectivity Score
    positive_words = []
    negative_words = []
    positive_score = []
    negative_score = []
    polarity_score = []
    subjectivity_score = []

    for i in range(0, len(data)):
        positive_words.append([word for word in data[i] if word.lower() in pos])
        negative_words.append([word for word in data[i] if word.lower() in neg])
        positive_score.append(len(positive_words[i]))
        negative_score.append(len(negative_words[i]))
        polarity_score.append((positive_score[i] - negative_score[i]) / (positive_score[i] + negative_score[i]) + 0.000001)
        subjectivity_score.append((positive_score[i] + negative_score[i]) / (len(data[i]) + 0.000001))
        
    
    
    # Calculating the Average Sentence Length, Percentage of Complex Words, Fod Index
    # Syllable Per Word, Complex Word Count
    print("Now average sentence length")
    avg_sentence_length = []
    Percentage_of_Complex_words  =  []
    Fog_Index = []
    complex_word_count =  []
    avg_syllable_word_count = []
    
    for files in os.listdir(text_dir):
        x,y,z,a,b = measure(files, text_dir)
        avg_sentence_length.append(x)
        Percentage_of_Complex_words.append(y)
        Fog_Index.append(z)
        complex_word_count.append(a)
        avg_syllable_word_count.append(b) 
        
    
    # Calculating Word Count, Average Word Length
    print("Now word count and average word length")
    word_count = []
    average_word_length = []
    for file in os.listdir(text_dir):
        x, y = cleaned_words(files, text_dir)
        word_count.append(x)
        average_word_length.append(y)
        
    
    # Calculating Personal Pronouns
    print("Now personal pronouns")
    pp_count = []
    for file in os.listdir(text_dir):
        x = count_personal_pronouns(file, text_dir)
        pp_count.append(x)
        
    
    # Reading the Output file into a dataframe
    output_df = pd.read_excel("/home/vo1d/Desktop/VS_Code/Blackcoffer/OutputDataStructure.xlsx")
    
    
    # URL_ID doesn't exist i.e. page doesn't exist
    # So dropping these rows from the dataframe
    output_df.drop([13, 19, 28, 35, 42, 48, 82, 83, 91, 98, 99], axis = 0, inplace = True)

    # Writing the values of variables to the dataframe
    variables = [positive_score, negative_score, polarity_score, subjectivity_score,
                avg_sentence_length, Percentage_of_Complex_words, Fog_Index, avg_sentence_length,
                complex_word_count, word_count, avg_syllable_word_count, pp_count, average_word_length]

    for i, var in enumerate(variables):
        output_df.iloc[:, i+2] = var

    # Now save the dataframe to the disk
    output_df.to_csv('/home/vo1d/Desktop/VS_Code/Blackcoffer/Output_Data.csv')