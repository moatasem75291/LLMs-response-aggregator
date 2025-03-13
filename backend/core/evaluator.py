import logging
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
from datetime import datetime


logger = logging.getLogger(__name__)


class ResponseEvaluator:
    def __init__(self):
        """Initialize the ResponseEvaluator class."""
        try:
            nltk.download("punkt", quiet=True)
            nltk.download("stopwords", quiet=True)
        except Exception as e:
            logger.error(f"Failed to download NLTK resources: {str(e)}")

        self.stop_words = set(stopwords.words("english"))
        self.vectorizer = TfidfVectorizer()

    def evaluate_and_rank_responses(
        self, query: str, responses: List[Tuple[str, str, datetime]]
    ) -> List[Tuple[str, str, float, datetime]]:
        """
        Evaluate and rank responses based on quality metrics.
        Args:
            query: Original user query.
            responses: List of tuples (llm_name, response_text, timestamp).

        Returns:
            List of tuples (llm_name, response_text, score, timestamp) sorted by score.
        """

        if not responses:
            return []

        # prepare for cross-checking
        response_texts = [response[1] for response in responses]

        # calculate similarity scores
        try:
            tfidf_matrix = self.vectorizer.fit_transform(response_texts)
            similarities = cosine_similarity(tfidf_matrix)

        except Exception as e:
            logger.warning(f"Error calculating similarities: {str(e)}")
            similarities = [
                [1.0 for _ in range(len(responses))] for _ in range(len(responses))
            ]

        # Calculate relevance to query
        try:
            query_tokens = set(word_tokenize(query.lower())) - self.stop_words
        except Exception as e:
            logger.warning(f"Error tokenizing query: {str(e)}")
            query_tokens = set(query.lower().split())

        scored_responses = []
        for i, (source, content, timestamp) in enumerate(responses):
            try:
                content_tokens = set(word_tokenize(content.lower())) - self.stop_words
            except Exception as e:
                logger.warning(f"Error tokenizing response: {str(e)}")
                content_tokens = set(content.lower().split())

            # calculate relevance score
            relevance_score = (
                len(query_tokens.intersection(content_tokens)) / len(query_tokens)
                if query_tokens
                else 0
            )

            # Calculate cross-check score (average similarity with other responses)
            cross_check_score = sum(similarities[i]) / len(responses)

            # Calculate length score (penalize very short responses, reward medium-length ones)
            word_count = len(content.split())
            if word_count < 50:
                length_score = word_count / 50
            elif word_count < 500:
                length_score = 1.0
            else:
                length_score = 500 / word_count

            # Calculate final score
            final_score = (
                (relevance_score * 0.5)
                + (cross_check_score * 0.3)
                + (length_score * 0.2)
            )

            logger.info(
                f"Scored {source}: relevance={relevance_score:.2f}, cross-check={cross_check_score:.2f}, length={length_score:.2f}, final={final_score:.2f}"
            )
            scored_responses.append((source, content, final_score, timestamp))

        # Rank responses by score (highest first)
        return sorted(scored_responses, key=lambda x: x[2], reverse=True)
