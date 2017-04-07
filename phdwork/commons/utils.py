'''
Essential functions commonly used in scripts.

'''

import numpy as np


def combine_classes(y, nb_parents):

    nb_classes = y.max() - y.min() + 1
    ratio = nb_classes/nb_parents

    y_parent = np.zeros_like(y)

    for parent in range(nb_parents):
        y_parent[y/ratio == parent] = parent

    return y_parent


def calculate_cl_acc(ground_truth, est, nb_all_clusters, cluster_offset=0, label_correction=False):

    majority = np.zeros(nb_all_clusters)
    population = np.zeros(nb_all_clusters)

    if label_correction:
        est = correct_labels(ground_truth, est)

    for cluster in range(cluster_offset, nb_all_clusters + cluster_offset):
        if np.bincount(ground_truth[est==cluster]).size != 0:
            majority[cluster-cluster_offset] = np.bincount(ground_truth[est==cluster]).max()
            population[cluster-cluster_offset] = np.bincount(ground_truth[est==cluster]).sum()

    cl_acc = majority[majority>0].sum()/population[population>0].sum()

    return cl_acc, population.sum()


def correct_labels(ground_truth, est):

    corrested_est = np.zeros_like(est, dtype='int')

    for cluster in range(est.max()+1):
        if np.bincount(ground_truth[est==cluster]).size != 0:
            true_label = np.bincount(ground_truth[est==cluster]).argmax()
            corrested_est[est==cluster] = true_label

    return corrested_est


def cumulate_metrics(X, metric_func, batch_size=128):

    count = 0

    metrics = np.zeros(get_metrics.function.n_returned_outputs)

    for batch_ind in range(0, len(X), batch_size):
        X_batch = X[batch_ind:batch_ind+batch_size,]
        metrics += metric_func([X_batch,0])
        count += 1

    metrics /= count

    return metrics
