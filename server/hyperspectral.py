import numpy as np
from scipy import linalg
import utils
import scipy.io as sio
import matplotlib.pyplot as plt
from sklearn import metrics, decomposition


def LRSR(DictLRR, DictSRC, data, beta, lmda):
    """

    :param DictLRR: the background dictionary
    :param DictSRC: the anomaly dictionary
    :param data: the normalized data
    :param beta: parameters
    :param lmda: parameters
    :return: Z: the low rank coefficeinets
             S: the sparse coefficients
             E: the noise
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
    err = 0.000001
    itera = 1
    inv_Z = np.linalg.inv(np.dot(DictLRR.transpose(), DictLRR) + ILRR)
    inv_S = np.linalg.inv(np.dot(DictSRC.transpose(), DictSRC) + ISRC)

    while itera < 500:
        print("iteration:{0}".format(itera))
        # update J
        operator1 = 1 / mu
        tmpJ = Z + Y2 / mu
        Ju, Jsigma, Jvt = linalg.svd(tmpJ, full_matrices=False)
        # threshold1 =1/mu
        evp = Jsigma[Jsigma > operator1].shape[0]
        if evp >= 1:
            Jsigma[0:evp] -= operator1
            JsigmaM = np.diag(Jsigma[0:evp])
            print("current evp is: {0}".format(evp))
        else:
            evp = 1
            JsigmaM = 0

        J = np.dot(np.dot(Ju[:, 0:evp], JsigmaM), Jvt[0:evp, :])
        # update E
        operator3 = lmda / mu
        tmpE = data - np.dot(DictLRR, Z) - np.dot(DictSRC, S) + Y1 / mu
        terows, tecols = tmpE.shape
        for i in range(tecols):
            tmpValue1 = linalg.norm(tmpE[:, i])
            if tmpValue1 > operator3:
                E[:, i] = ((tmpValue1 - operator3) / tmpValue1) * tmpE[:, i]
            else:
                E[:, i] = 0
        # update L
        tmpL = S + Y3 / mu
        operator2 = beta / mu
        tmpL[tmpL > operator2] -= operator2
        tmpL[tmpL < -operator2] += operator2
        tmpL[(tmpL >= -operator2) & (tmpL <= operator2)] = 0
        L = tmpL.copy()
        # update Z
        tmpZ = (
            np.dot(DictLRR.transpose(), data - np.dot(DictSRC, S) - E)
            + J
            + (np.dot(DictLRR.transpose(), Y1) - Y2) / mu
        )
        Z = np.dot(inv_Z, tmpZ)
        # update S
        tmpS = (
            np.dot(DictSRC.transpose(), data - np.dot(DictLRR, Z) - E)
            + L
            + (np.dot(DictSRC.transpose(), Y1) - Y3) / mu
        )
        S = np.dot(inv_S, tmpS)
        # update Y1,Y2,Y3
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
        print("max err is:{0}".format(rlerr))
        print("current mu is:{0}".format(mu))
        if rlerr < err:
            break
    return Z, E, S


def dic_constr(
    data3d, groundtruth, win_size, cluster_num, K, selected_dic_percent, target_dic_num
):
    """
    :param data3d: the original 3D hyperpsectral image
    :param groundtruth:  a 2D matrix reflect the label of corresponding pixels
    :param win_size: the size of window, such as 3X3, 5X5, 7X7
    :param cluster_num: the number of classters such as 5, 10, 15, 20
    :param K: the level of sparsity
    :param selected_dic_percent: the selected percent of the atoms to build the background dictionary
    :param target_dic_num: the selected number to build the anomaly dictionary
    :return: data2d:  the normalized data
             bg_dic:  the background dictionary
             tg_dic:  the anomaly dictionary
             bg_dic_ac_label:  the index of background dictionary atoms
             tg_dic_label: the index of anomaly dictionary atoms
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
        print("current calculate cluster  {0}  ...".format(i))
        tmp = np.where(cluster_assment == i)
        if tmp[0].size == 0:
            continue
        else:
            class_data = win_matrix[:, :, tmp[0]]
            cd_rows, cd_cols, cd_n = class_data.shape
            dictionary = class_data[:, int((win_size * win_size + 1) / 2), :]
            dic_rows, dic_cols = dictionary.shape
            class_alpha = np.zeros((K, cd_cols, cd_n))
            class_index = np.zeros((K, cd_n))
            for j in range(cd_n):
                X = class_data[:, :, j]
                dictionary[:, (j * cd_cols) : (j * cd_cols + cd_cols - 1)] = 0
                alpha, index, chosen_atom, resdiual = utils.somp(dictionary, X, K)
                class_alpha[:, :, j] = alpha
                class_index[:, j] = index.transpose()
                resdiual_stack[:, :, save_num + j] = resdiual

            save_num = save_num + cd_n
            class_index = class_index.astype("int")
            class_global_alpha = np.zeros((dic_cols, cd_cols, cd_n))
            class_global_frequency = np.zeros((dic_cols, cd_cols, cd_n))
            for n_index in range(cd_n):
                class_global_alpha[class_index[:, n_index], :, n_index] = class_alpha[
                    :, :, n_index
                ]
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
            anomaly_weight = norm_frequency
            anomaly_weight[frequency > 0] = (
                sparsity_score[frequency > 0] / frequency[frequency > 0]
            )
            # sparsity_score = sparsity_score * norm_frequency
            sparsity_sort_index = np.argsort(-sparsity_score)
            sparsity_sort_index = sparsity_sort_index.astype("int")
            frequency_sort_index = np.argsort(-norm_frequency)
            frequency_sort_index = frequency_sort_index.astype("int")
            tmp_class_dic_label = np.array(tmp[0])
            class_order_data_index_tuple.append(tmp_class_dic_label)
            selected_dic_num = np.round(selected_dic_percent * cd_n)
            selected_dic_num = selected_dic_num.astype("int")
            bg_dic_ac_tuple.append(
                tmp_class_dic_label[sparsity_sort_index[0:selected_dic_num]]
            )
            bg_dic_fc_tuple.append(
                tmp_class_dic_label[frequency_sort_index[0:selected_dic_num]]
            )
            anomaly_weight_tuple.append(anomaly_weight)
            bg_dic_tuple.append(dictionary[:, sparsity_sort_index[0:selected_dic_num]])

            # sio.savemat(result_path + "dic_{0}_frequency.mat".format(i), {'dic_frequency': frequency})
            # sio.savemat(result_path + "dic_{0}_reflect.mat".format(i), {'dic_reflect': sum_alpha_2})

    bg_dic = np.column_stack(bg_dic_tuple)
    bg_dic_ac_label = np.hstack(bg_dic_ac_tuple)
    bg_dic_fc_label = np.hstack(bg_dic_fc_tuple)
    anomaly_weight = np.hstack(anomaly_weight_tuple)
    class_order_data_index = np.hstack(class_order_data_index_tuple)
    norm_res = np.zeros((wm_n, win_size * win_size))
    for i in range(wm_n):
        norm_res[i, :] = np.linalg.norm(resdiual_stack[:, :, i], axis=0)
    mean_norm_res = np.mean(norm_res, axis=1) * anomaly_weight.transpose()
    anomaly_level = mean_norm_res / np.linalg.norm(mean_norm_res)
    tg_sort_index = np.argsort(-anomaly_level)
    tg_dic = data2d[:, class_order_data_index[tg_sort_index[0:target_dic_num]]]
    print("successs!!")

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
    label = cluster_assment
    label = label.transpose()
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
    capture_plot(lambda: plt.imshow(bg_dic_show), "Background dictionary")
    capture_plot(lambda: plt.imshow(tg_dic_show), "Anomaly dictionary")
    capture_plot(lambda: plt.imshow(segm_show), "Segmentation")

    return background2d, target2d, images

def ROC_AUC(target2d, groundtruth):
    """

    :param target2d: the 2D anomaly component
    :param groundtruth: the groundtruth
    :return: auc: the AUC value
    """
    rows, cols = groundtruth.shape
    label = groundtruth.transpose().reshape(1, rows * cols)
    result = np.zeros((1, rows * cols))
    for i in range(rows * cols):
        result[0, i] = np.linalg.norm(target2d[:, i])

    # result = hyper.hypernorm(result, "minmax")
    fpr, tpr, thresholds = metrics.roc_curve(label.transpose(), result.transpose())
    auc = metrics.auc(fpr, tpr)
    plt.figure(2)
    plt.plot(fpr, tpr)
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.show()
    return auc
