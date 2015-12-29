"""
The learning algorithm takes the extracted features and makes sense of them in an observed way.
"""
import os
import bob.bio.gmm.algorithm
import bob.learn.em
import bob.io.base
import bob.bio.gmm.tools.gmm


def _get_file(file_name):
    return os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            os.pardir,
            "IntermediateFiles",
            file_name
    )


def _load_algorithm():
    """
    @return: bob.bio.base.algorithm.Algorithm
    """
    return bob.bio.gmm.algorithm.GMMRegular(
            number_of_gaussians=256,
            training_threshold=0.0,  # standard: 5e-4
            kmeans_training_iterations=25,  # Maximum number of iterations for K-Means
            gmm_training_iterations=25,  # Maximum number of iterations for ML GMM Training
            variance_threshold=5e-4,  # Minimum value that a variance can reach
            update_weights=True,
            update_means=True,
            update_variances=True,

            # parameters of the GMM enrollment
            relevance_factor=4,  # Relevance factor as described in Reynolds paper
            gmm_enroll_iterations=1,  # Number of iterations for the enrollment phase
            responsibility_threshold=0,
            # If set, the weight of a particular Gaussian will at least be greater than this threshold.
            # In the case the real weight is lower, the prior mean value will be used to estimate the current
            # mean and variance.
            INIT_SEED=5489,
            scoring_function=bob.learn.em.linear_scoring
    )


