import json

from json import JSONEncoder
from com.pnfsoftware.jeb.client.api import IScript
from com.pnfsoftware.jeb.core.units.code.android import IDexUnit


class UpdateName(IScript):

    def __init__(self):
        self.dexUnit = None
        self.ctx = None
        self.mainProject = None

    def renamePerfect(self, oldFeature, newFeature):
        for idx in range(0, len(oldFeature["Field"])):
            oldField = oldFeature["Field"][idx]
            nowField = newFeature["Field"][idx]
            if oldField["NowName"] != oldField["RawName"]:
                print("rename field: " + nowField["RawSign"] + " -> " + oldField["NowName"])
                self.dexUnit.getField(nowField["RawSign"]).setName(oldField["NowName"])

        for idx in range(0, len(oldFeature["Method"])):
            oldMethod = oldFeature["Method"][idx]
            nowMethod = newFeature["Method"][idx]
            if oldMethod["NowName"] != oldMethod["RawName"]:
                print("rename method: " + nowMethod["RawSign"] + " -> " + oldMethod["NowName"])
                self.dexUnit.getMethod(nowMethod["RawSign"]).setName(oldMethod["NowName"])

        dexClz = self.dexUnit.getClass(newFeature["RawSign"])
        if oldFeature["RawName"] != oldFeature["NowName"]:
            print("rename class: " + newFeature["RawSign"] + " -> " + oldFeature["NowName"])
            dexClz.setName(oldFeature["NowName"])

    def renameLikely(self, oldFeature, newFeature):
        pass

    def run(self, ctx):
        self.ctx = ctx
        self.mainProject = ctx.getMainProject()
        self.dexUnit = self.mainProject.findUnit(IDexUnit)

        perfectJson = json.loads(open(r"D:\desktop\j8e_match_clz\perfectMatch.json").read())
        for item in perfectJson:
            self.renamePerfect(item["source"], item["match"][0])

        # perfectJson = json.loads(open(r"D:\desktop\j8e_match_clz\likelyMathc.json").read())
        # for item in perfectJson:
        #     self.renameLikely(item["source"], item["match"][0])
        #
        # perfectJson = json.loads(open(r"D:\desktop\j8e_match_clz\multipleMatch.json").read())
        # for item in perfectJson:
        #     self.renameLikely(item["source"], item["match"][0])
