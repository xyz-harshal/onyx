
import numpy as np
from scipy import linalg
import utils
import scipy.io as sio
import matplotlib.pyplot as plt
from sklearn import metrics, decomposition

from io import BytesIO
import base64

def LRSR(DictLRR, DictSRC, data, beta, lmda):
    """
    :param DictLRR: the background dictionary
    :param DictSRC: the anomaly dictionary
    :param data: the normalized data
    :param beta: parameter for sparse regularization on S
    :param lmda: parameter for sparse regularization on E
    :return: Z: the low rank coefficients
             E: the noise (error)
             S: the sparse coefficients
    """
    dataRows, dataCols = data.shape
    DLRows, DLCols = DictLRR.shape
    DSRows, DSCols = DictSRC.shape
    ILRR = np.eye(DLCols)
    ISRC = np.eye(DSCols)
    Z = np.zeros((DLCols, dataCols))
    J = np.zeros((DLCols, dataCols))
    E = np.zeros((dataRows, dataCols))
    S = np.zeros((DSCols, dataCols))
    L = np.zeros((DSCols, dataCols))
    Y1 = np.zeros((dataRows, dataCols))
    Y2 = np.zeros((DLCols, dataCols))
    Y3 = np.zeros((DSCols, dataCols))
    mu = 0.0001
    mu_max = 10**10
    p = 1.1
    err = 1e-6
    itera = 1
    inv_Z = np.linalg.inv(np.dot(DictLRR.transpose(), DictLRR) + ILRR)
    inv_S = np.linalg.inv(np.dot(DictSRC.transpose(), DictSRC) + ISRC)

    while itera < 500:
        print("Iteration: {0}".format(itera))
        # update J using SVD thresholding
        operator1 = 1 / mu
        tmpJ = Z + Y2 / mu
        Ju, Jsigma, Jvt = linalg.svd(tmpJ, full_matrices=False)
        evp = Jsigma[Jsigma > operator1].shape[0]
        if evp >= 1:
            Jsigma[0:evp] -= operator1
            JsigmaM = np.diag(Jsigma[0:evp])
            print("Current evp is: {0}".format(evp))
            J = np.dot(np.dot(Ju[:, 0:evp], JsigmaM), Jvt[0:evp, :])
        else:
            # if no singular values exceed the threshold, set J to a zero matrix
            J = np.zeros_like(tmpJ)
        
        # update E (element-wise shrinkage)
        operator3 = lmda / mu
        tmpE = data - np.dot(DictLRR, Z) - np.dot(DictSRC, S) + Y1 / mu
        te_rows, te_cols = tmpE.shape
        for i in range(te_cols):
            tmpValue1 = linalg.norm(tmpE[:, i])
            if tmpValue1 > operator3:
                E[:, i] = ((tmpValue1 - operator3) / tmpValue1) * tmpE[:, i]
            else:
                E[:, i] = 0

        # update L (soft thresholding)
        tmpL = S + Y3 / mu
        operator2 = beta / mu
        tmpL[tmpL > operator2] -= operator2
        tmpL[tmpL < -operator2] += operator2
        tmpL[(tmpL >= -operator2) & (tmpL <= operator2)] = 0
        L = tmpL.copy()

        # update Z
        tmpZ = (np.dot(DictLRR.transpose(), data - np.dot(DictSRC, S) - E)
                + J + (np.dot(DictLRR.transpose(), Y1) - Y2) / mu)
        Z = np.dot(inv_Z, tmpZ)

        # update S
        tmpS = (np.dot(DictSRC.transpose(), data - np.dot(DictLRR, Z) - E)
                + L + (np.dot(DictSRC.transpose(), Y1) - Y3) / mu)
        S = np.dot(inv_S, tmpS)

        # update Lagrange multipliers Y1, Y2, Y3
        T1 = data - np.dot(DictLRR, Z) - E - np.dot(DictSRC, S)
        T2 = Z - J
        T3 = S - L
        Y1 += mu * T1
        Y2 += mu * T2
        Y3 += mu * T3

        # update mu
        err1 = linalg.norm(T1, np.inf)
        err2 = linalg.norm(T2, np.inf)
        err3 = linalg.norm(T3, np.inf)
        rlerr = max(err1, err2, err3)
        mu = min(p * mu, mu_max)

        itera += 1
        print("Max error: {0}".format(rlerr))
        print("Current mu: {0}".format(mu))
        if rlerr < err:
            break
    return Z, E, S

def dic_constr(data3d, groundtruth, win_size, cluster_num, K, selected_dic_percent, target_dic_num):
    """
    :param data3d: the original 3D hyperspectral image
    :param groundtruth: a 2D matrix reflecting the label of corresponding pixels
    :param win_size: the size of the window, e.g., 3x3, 5x5, 7x7
    :param cluster_num: the number of clusters (e.g., 5, 10, 15, 20)
    :param K: the level of sparsity
    :param selected_dic_percent: the percent of atoms selected to build the background dictionary
    :param target_dic_num: the number of atoms to build the anomaly dictionary
    :return: data2d: the normalized data
             bg_dic: the background dictionary
             tg_dic: the anomaly dictionary
             bg_dic_ac_label: indices of background dictionary atoms (via sparsity)
             tg_dic_label: indices of anomaly dictionary atoms
    """
    data2d = utils.hyperconvert2d(data3d)
    rows, cols, bands = data3d.shape
    data2d = utils.hypernorm(data2d, "L2_norm")
    sio.savemat("data2d.mat", {"data2d": data2d})
    data3d = utils.hyperconvert3d(data2d, rows, cols, bands)
    pca = decomposition.PCA(n_components=20, copy=True, whiten=False)
    dim_data = pca.fit_transform(data2d.transpose())
    data3d_dim = utils.hyperconvert3d(dim_data.transpose(), rows, cols, 10)
    win_dim = utils.hyperwincreat(data3d_dim, win_size)
    cluster_assment = utils.Kmeans_win(win_dim, cluster_num)
    sio.savemat("cluster_assment.mat", {"cluster_assment": cluster_assment})
    win_matrix = utils.hyperwincreat(data3d, win_size)
    sio.savemat("win_matrix.mat", {"win_matrix": win_matrix})
    wm_rows, wm_cols, wm_n = win_matrix.shape
    resdiual_stack = np.zeros((bands, win_size * win_size, wm_n))
    save_num = 0
    bg_dic_tuple = []
    bg_dic_ac_tuple = []
    bg_dic_fc_tuple = []
    class_order_data_index_tuple = []
    anomaly_weight_tuple = []
    
    for i in range(cluster_num):
        print("Calculating cluster {0} ...".format(i))
        tmp = np.where(cluster_assment == i)
        if tmp[0].size == 0:
            continue
        else:
            class_data = win_matrix[:, :, tmp[0]]
            cd_rows, cd_cols, cd_n = class_data.shape
            # Extract the central column from each window as the dictionary atoms
            dictionary = class_data[:, int((win_size * win_size + 1) / 2), :]
            dic_rows, dic_cols = dictionary.shape  # dic_cols equals cd_n
            class_alpha = np.zeros((K, cd_cols, cd_n))
            class_index = np.zeros((K, cd_n))
            for j in range(cd_n):
                X = class_data[:, :, j]
                # Zero out the j-th atom to avoid trivial self-representation
                dictionary[:, j] = 0
                alpha, index, chosen_atom, resdiual = utils.somp(dictionary, X, K)
                class_alpha[:, :, j] = alpha
                class_index[:, j] = index.transpose()
                resdiual_stack[:, :, save_num + j] = resdiual

            save_num += cd_n
            class_index = class_index.astype("int")
            class_global_alpha = np.zeros((dic_cols, cd_cols, cd_n))
            class_global_frequency = np.zeros((dic_cols, cd_cols, cd_n))
            for n_index in range(cd_n):
                class_global_alpha[class_index[:, n_index], :, n_index] = class_alpha[:, :, n_index]
                class_global_frequency[class_index[:, n_index], :, n_index] = 1

            posti_class_global_alpha = np.fabs(class_global_alpha)
            data_frequency = class_global_frequency[:, 0, :]
            frequency = np.sum(data_frequency, axis=1)
            sum_frequency = np.sum(frequency)
            norm_frequency = frequency / sum_frequency
            data_mean_alpha = np.mean(posti_class_global_alpha, axis=1)
            sum_alpha_2 = np.sum(data_mean_alpha, axis=1)
            norm_tmp = np.linalg.norm(sum_alpha_2)
            sparsity_score = sum_alpha_2 / norm_tmp
            anomaly_weight = norm_frequency.copy()
            anomaly_weight[frequency > 0] = sparsity_score[frequency > 0] / frequency[frequency > 0]
            sparsity_sort_index = np.argsort(-sparsity_score).astype("int")
            frequency_sort_index = np.argsort(-norm_frequency).astype("int")
            tmp_class_dic_label = np.array(tmp[0])
            class_order_data_index_tuple.append(tmp_class_dic_label)
            # Ensure selected_dic_num is an integer scalar
            selected_dic_num = int(np.round(selected_dic_percent * cd_n))
            bg_dic_ac_tuple.append(tmp_class_dic_label[sparsity_sort_index[0:selected_dic_num]])
            bg_dic_fc_tuple.append(tmp_class_dic_label[frequency_sort_index[0:selected_dic_num]])
            anomaly_weight_tuple.append(anomaly_weight)
            bg_dic_tuple.append(dictionary[:, sparsity_sort_index[0:selected_dic_num]])

    bg_dic = np.column_stack(bg_dic_tuple)
    bg_dic_ac_label = np.hstack(bg_dic_ac_tuple)
    bg_dic_fc_label = np.hstack(bg_dic_fc_tuple)
    anomaly_weight = np.hstack(anomaly_weight_tuple)
    class_order_data_index = np.hstack(class_order_data_index_tuple)
    norm_res = np.zeros((wm_n, win_size * win_size))
    for i in range(wm_n):
        norm_res[i, :] = np.linalg.norm(resdiual_stack[:, :, i], axis=0)
    mean_norm_res = np.mean(norm_res, axis=1) * anomaly_weight  # Ensure dimensions match if intended
    anomaly_level = mean_norm_res / np.linalg.norm(mean_norm_res)
    tg_sort_index = np.argsort(-anomaly_level)
    tg_dic = data2d[:, class_order_data_index[tg_sort_index[0:target_dic_num]]]
    print("Success!!")

    sio.savemat("bg_dic.mat", {"bg_dic": bg_dic})
    sio.savemat("bg_dic_ac_label.mat", {"bg_dic_ac_label": bg_dic_ac_label})
    sio.savemat("bg_dic_fc_label.mat", {"bg_dic_fc_label": bg_dic_fc_label})
    sio.savemat("tg_dic.mat", {"tg_dic": tg_dic})
    tg_dic_label = class_order_data_index[tg_sort_index[0:target_dic_num]]
    sio.savemat("tg_dic_label.mat", {"tg_dic_label": tg_dic_label})
    return data2d, bg_dic, tg_dic, bg_dic_ac_label, tg_dic_label

def result_show(bg_dic, tg_dic, Z, S, E, rows, cols, bands, bg_dic_label, tg_dic_label):
    background2d = np.dot(bg_dic, Z)
    background3d = utils.hyperconvert3d(background2d, rows, cols, bands)
    target2d = np.dot(tg_dic, S)
    target3d = utils.hyperconvert3d(target2d, rows, cols, bands)
    noise3d = utils.hyperconvert3d(E, rows, cols, bands)
    bg_dic_show = np.zeros((1, rows * cols))
    tg_dic_show = np.zeros((1, rows * cols))
    bg_dic_show[0, bg_dic_label] = 1
    tg_dic_show[0, tg_dic_label] = 1
    bg_dic_show = bg_dic_show.reshape(rows, cols)
    tg_dic_show = tg_dic_show.reshape(rows, cols)
    cluster_assment_file = sio.loadmat("cluster_assment.mat")
    cluster_assment = np.array(cluster_assment_file["cluster_assment"])
    label = cluster_assment.transpose()
    segm_show = label.reshape(rows, cols)

    images = []

    def capture_plot(plot_func, title):
        plt.figure()
        plot_func()
        plt.title(title)
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        img_str = base64.b64encode(buffer.getvalue()).decode()
        images.append(img_str)
        plt.close()

    capture_plot(lambda: plt.imshow(background3d.mean(2)), "Background")
    capture_plot(lambda: plt.imshow(target3d.mean(2)), "Anomaly")
    capture_plot(lambda: plt.imshow(noise3d.mean(2)), "Noise")
    capture_plot(lambda: plt.imshow(bg_dic_show), "Background Dictionary")
    capture_plot(lambda: plt.imshow(tg_dic_show), "Anomaly Dictionary")
    capture_plot(lambda: plt.imshow(segm_show), "Segmentation")

    return background2d, target2d, images

def ROC_AUC(target2d, groundtruth):
    """
    :param target2d: the 2D anomaly component
    :param groundtruth: the groundtruth matrix
    :return: auc: the computed AUC value
    """
    rows, cols = groundtruth.shape
    label = groundtruth.transpose().reshape(1, rows * cols)
    result = np.zeros((1, rows * cols))
    for i in range(rows * cols):
        result[0, i] = np.linalg.norm(target2d[:, i])

    fpr, tpr, thresholds = metrics.roc_curve(label.transpose(), result.transpose())
    auc = metrics.auc(fpr, tpr)
    plt.figure(2)
    plt.plot(fpr, tpr)
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.show()
    return auc
