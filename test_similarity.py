
from modules.similarity import calculate_similarity


# -----------------------------------
# Test 1: Strong Match
# -----------------------------------

resume_1 = """
Python developer with experience in Machine Learning,
SQL, Pandas, NumPy and Git.
"""

job_1 = """
We are looking for a Python developer with experience
in Machine Learning, SQL and Git.
"""


score_1 = calculate_similarity(
    resume_1,
    job_1
)


# -----------------------------------
# Test 2: Weak Match
# -----------------------------------

resume_2 = """
Python developer with experience in Machine Learning,
SQL, Pandas, NumPy and Git.
"""

job_2 = """
We are looking for a Java developer with experience
in Spring Boot, Java, Docker and Kubernetes.
"""


score_2 = calculate_similarity(
    resume_2,
    job_2
)


# -----------------------------------
# Display Results
# -----------------------------------

print("===================================")
print("       TF-IDF SIMILARITY TEST")
print("===================================")

print(f"\nTest 1 - Strong Match: {score_1}%")

print(f"Test 2 - Weak Match:   {score_2}%")

print("\n===================================")

