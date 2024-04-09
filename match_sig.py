import json

from pyxdameraulevenshtein import damerau_levenshtein_distance, normalized_damerau_levenshtein_distance


def listSame(l1, l2):
    if len(l1) != len(l2):
        return False
    for idx in range(0, len(l1)):
        if l1[idx] != l2[idx]:
            return False
    return True


sig1 = json.loads(open(r"D:\desktop\tmp\sig\sig1.json", "r", encoding="utf8").read())
sig2 = json.loads(open(r"D:\desktop\tmp\sig\sig2.json", "r", encoding="utf8").read())

badCount = 0
match = []
notMatch = []

for sig1Item in sig1:
    matchItem = {
        "source": sig1Item,
        "match": []
    }
    for sig2Item in sig2:
        if sig1Item["Feature"] == sig2Item["Feature"]:
            matchItem["match"].append(sig2Item)
    if len(matchItem["match"]) != 0:
        match.append(matchItem)
    else:
        notMatch.append(sig1Item)

perfectMatch = []
multipleMatch = []
likelyMathc = []

for item in match:
    if len(item["match"]) > 1:
        multipleMatch.append(item)
        badCount += len(item["match"])
    else:
        perfectMatch.append(item)

for item in notMatch:
    dists = []
    for sig2Item in sig2:
        dist = damerau_levenshtein_distance(item["Feature"], sig2Item["Feature"])
        dists.append({
            "dist": dist,
            "match": sig2Item
        })
    dists = sorted(dists, key=lambda v: v["dist"])
    dists = dists[:5]
    likelyMathc.append({
        "source": item,
        "likely": dists
    })
    # print("likelyMathc:" + json.dumps(dists))


def print_match(m):
    for item in m:
        for matchItem in item["match"]:
            print(item["source"]["RawName"] + " - " + item["source"]["NowName"] + " -> " + matchItem["NowName"])


def print_likely_match(m):
    for item in m:
        for likely in item["likely"]:
            print(item["source"]["RawName"] + " - " + item["source"]["NowName"] + " -> " +
                  likely["match"]["NowName"] + ", dist:" + str(likely["dist"]))


print("--------perfectMatch--------")
print_match(perfectMatch)
print("--------multipleMatch--------")
print_match(multipleMatch)
print("--------likelyMathc--------")

for item in notMatch:
    badCount += 1
    print("not match: " + item["NowName"])

f = open("./result.json", "w")
f.write(json.dumps(match))
f.write("\n")
f.write(json.dumps(notMatch))
f.close()

print("badCount: " + str(badCount))
