"""
The learning algorithm takes the extracted features and makes sense of them in an observed way.
"""
import os
import bob.bio.gmm.algorithm
import bob.learn.em


def _get_projector_database(file_name):
    return os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            os.pardir,
            "ProjectorFiles",
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


def run_training(features, label):
    """
    @param features: (numpy.array, numpy.array, ...)
    @param label: name
    """
    algorithm = _load_algorithm()
    algorithm.train_projector(features, _get_projector_database(label))


def check_sample(sample, labels):
    """
    @param sample: numpy.array A feature array
    @param labels: String[] The labels to compare the sample with
    @return:
    """
    scores = []
    for label in labels:
        algorithm = _load_algorithm()
        algorithm.load_enroller(_get_projector_database(label))
        scores += (label, algorithm.score(algorithm.ubm, sample))
    max_score = 0
    max_label = None
    for score in scores:
        if score[1] > max:
            max_label = score[0]
            max_score = score[1]
    return max_score, max_label

