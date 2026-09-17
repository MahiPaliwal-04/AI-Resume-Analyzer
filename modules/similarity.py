
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(resume_text, job_description):
    """
    Calculate similarity between resume and job description
    using TF-IDF and Cosine Similarity.
    """

    # Check for empty input
    if not resume_text or not job_description:
        return 0.0

    # Convert inputs to strings
    resume_text = str(resume_text)
    job_description = str(job_description)

    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    try:

        # Convert text into TF-IDF vectors
        tfidf_matrix = vectorizer.fit_transform(
            [resume_text, job_description]
        )

        # Calculate cosine similarity
        similarity = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:2]
        )

        # Convert similarity into percentage
        score = similarity[0][0] * 100

        # Keep score between 0 and 100
        score = max(0.0, min(score, 100.0))

        return round(score, 2)

    except ValueError:

        # Handles cases where no usable vocabulary exists
        return 0.0

