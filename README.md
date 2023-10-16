# Vision Search: A Scalable Web Search Engine

Vision Search is a powerful web search engine project that aims to provide efficient and relevant search results. It comprises three key components: Crawler, Indexer, and Ranker. Leveraging multithreading and concurrency, Vision Search can crawl hundreds of websites simultaneously, maintaining a queue of data for efficient indexing. This project ensures that websites are crawled ethically by considering the Robots.txt file for each site.

## Key Components

### 1. Crawler

The web crawling functionality is encapsulated in the `crawler.py` file. This component efficiently gathers data from various websites and directly feeds it into the database. The crawler operates in the background, allowing it to run indefinitely without any interference with other processes.

### 2. Indexer

Initially, our indexing process in the `indexer.py` used word count and priority based on HTML tags to determine the quality of search results. However, this method did not consider the context of the words, leading to room for improvement.

### 3. Ranker

The Ranker component, although not described in detail here, plays a crucial role in ranking search results for optimal user experience. It is responsible for delivering the most relevant websites based on user queries.

## Improving Indexing with TF-IDF Scores

In our pursuit of providing more context-aware search results, we are currently working on an improved indexing algorithm in the `indexer_new.py` file. Our goal is to implement Term Frequency-Inverse Document Frequency (TF-IDF) scores to enhance the indexing process.

### What is TF-IDF?

TF-IDF is a statistical measure that evaluates the importance of a term within a document relative to a collection of documents. By analyzing the TF-IDF scores of keywords on websites, we aim to provide a more context-rich search experience. This improved approach will consider the importance of specific terms in the context of the entire collection of documents, allowing for better understanding of their relevance.

### Benefits of TF-IDF Integration

1. **Contextual Relevance**: TF-IDF scores will consider the context in which words are used, improving the quality of search results.

2. **Faster Search**: By scoring websites for all keywords, we can retrieve results more efficiently, enhancing the search experience for users.

3. **Enhanced User Experience**: The improved indexing algorithm will lead to more accurate and context-aware search results, increasing the satisfaction of Vision Search users.

As we continue to develop and refine Vision Search, our team is committed to delivering a web search engine that provides efficient and context-aware search results. Stay tuned for updates as we implement the TF-IDF scoring system and strive to enhance the overall search experience.

Feel free to contribute to this project and help us make Vision Search an even better web search engine. Your feedback, suggestions, and contributions are highly appreciated.
