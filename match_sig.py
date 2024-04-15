import json

from pyxdameraulevenshtein import damerau_levenshtein_distance, normalized_damerau_levenshtein_distance


def listSame(l1, l2):
    if len(l1) != len(l2):
        return False
    for idx in range(0, len(l1)):
        if l1[idx] != l2[idx]:
            return False
    return True


sig1 = json.loads(open(r"D:\desktop\j8e_match_clz\sig\sig1.json", "r", encoding="utf8").read())
sig2 = json.loads(open(r"D:\desktop\j8e_match_clz\sig\sig2.json", "r", encoding="utf8").read())

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
        badCount += 1

perfectMatch = []
multipleMatch = []
likelyMathc = []

for item in match:
    if len(item["match"]) > 1:
        multipleMatch.append(item)
        badCount += len(item["match"])
    else:
        perfectMatch.append(item)


def getMethodCodeFeature(item):
    feature = []
    for method in item["Method"]:
        feature.extend(method["CodeFeature"])
        feature.append(-1)
    return feature


for item in multipleMatch:
    dists = []
    sourceFeature = getMethodCodeFeature(item["source"])
    for matched in item["match"]:
        matchFeature = getMethodCodeFeature(matched)
        dist = damerau_levenshtein_distance(sourceFeature, matchFeature)
        dists.append({
            "dist": dist,
            "match": matched
        })
    dists = sorted(dists, key=lambda v: v["dist"])
    dists = dists[:5]
    item["likely"] = dists

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


def print_match(f, m):
    for item in m:
        for matchItem in item["match"]:
            f.write(item["source"]["RawName"] + " - " + item["source"]["NowName"] + " -> " +
                    matchItem["NowName"])
            f.write("\n")


def print_likely_match(f, m):
    for item in m:
        for likely in item["likely"]:
            f.write(item["source"]["RawName"] + " - " + item["source"]["NowName"] + " -> " +
                    likely["match"]["NowName"] + ", dist:" + str(likely["dist"]))
            f.write("\n")


f = open("./result.txt", "w")
f.write("--------perfectMatch--------\n")
print_match(f, perfectMatch)
f.write("--------multipleMatch--------\n")
print_likely_match(f, multipleMatch)
f.write("--------likelyMathc--------\n")
print_likely_match(f, likelyMathc)

f = open("./perfectMatch.json", "w")
f.write(json.dumps(perfectMatch))
f.close()

f = open("./multipleMatch.json", "w")
f.write(json.dumps(multipleMatch))
f.close()

# dist越小类越相似
f = open("./likelyMathc.json", "w")
f.write(json.dumps(likelyMathc))
f.close()

print("badCount: " + str(badCount))
