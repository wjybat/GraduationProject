import os
import math
import matplotlib.pyplot as plt


def k_means(path):
    all_avg=[]
    # for k in range(2.10):
    for k in range(3,4):
        ReadFile = open(path+r'\result\tfidf_score.txt', mode='r', encoding='ANSI')
        total_sentences_count = len(ReadFile.readlines())
        ReadFile.seek(0, 0)
        gap = total_sentences_count // (k - 1)
        cores = []
        scores = ReadFile.readlines()
        for index in range(len(scores)):
            scores[index] = scores[index].strip().strip('[').strip(']').split(', ')
            scores[index] = list(map(float, scores[index]))
        cores.append(scores[0])
        for i in range(1, k - 1):
            cores.append(scores[i * gap])
        cores.append(scores[-1])
        catalog = [-1 for _ in scores]
        ReadFile.seek(0, 0)

        def eula_dist(a, b):
            if len(a) != len(b):
                print('wrong dimension!')
                exit(0)
            distance = 0.0
            for serial in range(len(a)):
                distance += (a[serial] - b[serial]) ** 2
            return distance

        changed = True
        times = 100
        cluster_mean=0
        while times > 0 and changed:
            all_means=[]
            changed = False
            index_score = 0
            for score in scores:
                nearest_dist = math.inf
                nearest_core = -1
                index_core = 0
                for core in cores:
                    dist = eula_dist(score, core)
                    if dist < nearest_dist:
                        nearest_dist = dist
                        nearest_core = index_core
                    index_core += 1
                catalog[index_score] = nearest_core
                index_score += 1
            for num in range(len(cores)):
                mean = [0.0 for _ in range(len(cores[0]))]
                count = 0
                cat_index = 0
                for item in catalog:
                    if item == num:
                        mean = [mean[i] + scores[cat_index][i] for i in range(len(mean))]
                        count += 1
                    cat_index += 1
                if count > 0:
                    mean = [mean[i] / count for i in range(len(mean))]
                if cores[num] != mean:
                    cores[num] = mean
                    changed = True
            times -= 1
            #     else:
            #         cat_index=0
            #         count=0
            #         cluster_mean=0.0
            #         for item in catalog:
            #             sum=0
            #             if item == num:
            #                 count+=1
            #                 for i in range(len(mean)):
            #                     sum += abs(mean[i] - scores[cat_index][i])**2
            #                 sum=sum**0.5
            #             cluster_mean+=sum
            #             cat_index+=1
            #         cluster_mean=cluster_mean/count
            #         all_means.append(cluster_mean)
            # avg=0
            # if len(all_means)==k:
            #     for x in all_means:
            #         avg+=x
            #     avg=avg/k
            #     all_avg.append(avg)
            # if changed is False:
            #     print(all_avg)
        ReadFile1 = open(path+r'\result\sentences.txt', mode='r', encoding='ANSI')
        sentences = ReadFile1.readlines()
        WriteFile = open(path+r'\result\cluster.txt', mode='w', encoding='ANSI')
        for num in range(len(cores)):
            WriteFile.write('类别'+str(num+1)+'：'+'\n')
            cat_index = 0
            for core_num in catalog:
                if core_num == num:
                    WriteFile.write('语句序号'+str(cat_index)+'：'+sentences[cat_index])
                cat_index += 1
            WriteFile.write('\n')
        ReadFile.close()
        ReadFile1.close()
        WriteFile.close()
        print(times)
    # x=range(2,10)
    # print(x)
    # plt.title('average distance under different k')
    # plt.xlabel('K')
    # plt.ylabel('average distance in clusters')
    # plt.plot(x,all_avg)
    # plt.show()


if __name__ == '__main__':
    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    k_means(path)
    # x=[1,3,4]
    # y=[5,10,9]
    # plt.plot(x,y)
    # plt.show()