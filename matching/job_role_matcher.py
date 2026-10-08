from models.embedding_model import model
from preprocessing.data_loader import get_job_roles

from sklearn.metrics.pairwise import cosine_similarity


def find_best_job_roles(job_role, top_n=5):
    """
    Find the most semantically similar job roles.
    """

    roles = get_job_roles()

    input_embedding = model.encode(
        [job_role]
    )

    role_embeddings = model.encode(
        roles
    )

    similarities = cosine_similarity(
        input_embedding,
        role_embeddings
    )[0]

    ranked = sorted(
        zip(roles, similarities),
        key=lambda x: x[1],
        reverse=True
    )

    results = []

    for role, score in ranked[:top_n]:

        results.append({
            "job_role": role,
            "similarity": round(
                float(score) * 100,
                2
            )
        })

    return results


def get_best_job_role(job_role):
    """
    Return the best matching job role.
    """

    results = find_best_job_roles(
        job_role,
        top_n=1
    )

    return results[0]