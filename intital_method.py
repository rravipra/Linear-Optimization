# length of each cut in descending order and in inches
cutlistlength = [125, 120, 108, 99, 60, 49, 43, 34, 30, 12]
##############  [10,   40,  26,  6, 17, 11, 24, 12,  9, 26]
# desired number of each cut length parallel to cutlistlength
cutlistdesnum = [10, 40, 26, 5, 10, 10, 24, 12, 5, 26]

# 1250 4800 2808 594 1020 593 1032 408 270 312
# 13087" current cuts ideal sum, 119" waste, 14,400" board used

# current number of each cut length, assumes no current inventory
cutlistcurrnum = [0] * 10

# hardcoded length, solution is built around this number being an input and changing
hclength = 250
i = 0
j = 0
currwaste = 0
totalwaste = 0
boardcount = 0


def cut(length, i, j):
    i = j
    while (i < 9 or cutlistcurrnum[j] <= cutlistdesnum[j] or j < 9):
        global boardcount
        global currwaste
        global totalwaste
        print(cutlistcurrnum, totalwaste, boardcount)
        # print(i)
        if (cutlistcurrnum[0] >= cutlistdesnum[0]
                and cutlistcurrnum[1] >= cutlistdesnum[1]
                and cutlistcurrnum[2] >= cutlistdesnum[2]
                and cutlistcurrnum[3] >= cutlistdesnum[3]
                and cutlistcurrnum[4] >= cutlistdesnum[4]
                and cutlistcurrnum[5] >= cutlistdesnum[5]
                and cutlistcurrnum[6] >= cutlistdesnum[6]
                and cutlistcurrnum[7] >= cutlistdesnum[7]
                and cutlistcurrnum[8] >= cutlistdesnum[8]
                and cutlistcurrnum[9] >= cutlistdesnum[9]):
            return cutlistcurrnum, totalwaste, boardcount
        try:
            if (length - cutlistlength[i] > 0):
                length = length - cutlistlength[i]
                cutlistcurrnum[i] += 1
            elif (length - cutlistlength[i] < 0):
                i += 1
            elif (length - cutlistlength[i] == 0):
                if (cutlistcurrnum[j] >= cutlistdesnum[j]):
                    j += 1
                    cut(hclength, i, j)
                    boardcount += 1
                else:
                    cut(hclength, i, j)
                    boardcount += 1

        except IndexError:
            currwaste = length
            if (currwaste >= cutlistlength[-1]):
                for x in range(len(cutlistlength)):
                    if (currwaste - cutlistlength[x] >= 0):
                        currwaste = currwaste - cutlistlength[x]
                        cutlistcurrnum[x] += 1

            totalwaste += currwaste
            break

    if (j > 9):
        return cutlistcurrnum, totalwaste, boardcount
    elif (cutlistcurrnum[j] == cutlistdesnum[j]):
        j += 1
        cut(length, i, j)
    elif (i > 9):
        if (cutlistcurrnum[j] >= cutlistdesnum[j]):
            j += 1

        currwaste = length
        if (currwaste >= cutlistlength[-1]):
            for x in range(len(cutlistlength)):
                if (currwaste - cutlistlength[x] >= 0):
                    currwaste = currwaste - cutlistlength[x]
                    cutlistcurrnum[x] += 1

        totalwaste += currwaste
        boardcount += 1
        cut(hclength, i, j)
    return cutlistcurrnum, totalwaste, boardcount


print(cut(hclength, i, j))

