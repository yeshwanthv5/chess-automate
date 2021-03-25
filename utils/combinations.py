combinations = []
count = 0
for pawns in range(6, 11):
    for knights in range(0, 10):
        for bishops in range(0, 10):
            for rooks in range(0, 6):
                for queens in range(0, 5):
                    if pawns + 3*knights + 3*bishops + 4*rooks + 7*queens == 35:
                        combinations.append([pawns, knights, bishops, rooks, queens])
                        count += 1
print(combinations)
print(count)