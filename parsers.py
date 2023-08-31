# TODO: Make all that things work

# labelPlural = "labelPlural"
# labelMale = "labelMale"
# labelMalePlural = "labelMalePlural"
# labelFemale = "labelFemale"
# labelFemalePlural = "labelFemalePlural"
# lifeStages = "lifeStages"
# tab = "tab"
# scenario = "scenario"
# name = "name"
# skillLabel = "skillLabel"
# graphicData = "graphicData"
# color = "color"
# stuffProps = "stuffProps"
# stuffAdjective = "stuffAdjective"
# labelShort = "labelShort"
# category = "category"
# stuffCategories = "stuffCategories"
# costStuffCount = "costStuffCount"
# costList = "costList"
# recipeMaker = "recipeMaker"
# workSpeedStat = "workSpeedStat"
# efficiencyStat = "efficiencyStat"
# unfinishedThingDef = "unfinishedThingDef"
# defaultIngredientFilter = "defaultIngredientFilter"
# skillRequirements = "skillRequirements"
# workSkill = "workSkill"
# workSkillLearnPerTick = "workSkillLearnPerTick"
# effectWorking = "effectWorking"
# soundWorking = "soundWorking"
# recipeUsers = "recipeUsers"
# researchPrerequisite = "researchPrerequisite"
# designationCategory = "designationCategory"
# minifiedDef = "minifiedDef"
# building = "building"
# isNaturalRock = "isNaturalRock"
# isResourceRock = "isResourceRock"
# ingestible = "ingestible"
# baseIngestTicks = "baseIngestTicks"
# drugCategory = "drugCategory"
# race = "race"
# hasGenders = "hasGenders"
# intelligence = "intelligence"
# baseBodySize = "baseBodySize"
# butcherProducts = "butcherProducts"
# statBases = "statBases"
# fleshType = "fleshType"
# useLeatherFrom = "useLeatherFrom"
# useMeatFrom = "useMeatFrom"
# leatherColor = "leatherColor"
# leatherLabel = "leatherLabel"
# leatherCommonalityFactor = "leatherCommonalityFactor"
# leatherInsulation = "leatherInsulation"
# leatherStatFactors = "leatherStatFactors"
# leatherMarketValueFactor = "leatherMarketValueFactor"
# meatLabel = "meatLabel"
# meatColor = "meatColor"
# degreeDatas


def _descriptionFinder(_def):
    _description = _def.find("description")
    if _description:
        return [("description", _description.text)]


def _labelFinder(_def):
    _label = _def.find("label")
    if _label:
        return [("label", _label.text)]


def _reportStringFinder(_def):
    _reportString = _def.find("reportString")
    if _reportString:
        return [("reportString", _reportString.text)]


def _logRulesInitiatorFinder(_def):
    _results = []
    _logRulesInitiator = _def.find("logRulesInitiator")
    if _logRulesInitiator:
        _rulesStrings = _logRulesInitiator.find("rulesStrings")
        if _rulesStrings:
            rows = _rulesStrings.find_all("li")
            if rows:
                for num, row in enumerate(rows, start=0):
                    _results.append((f"logRulesInitiator.rulesStrings.{num}", row.text))
    return _results


def _logRulesRecipientFinder(_def):
    _results = []
    _logRulesRecipient = _def.find("logRulesRecipient")
    if _logRulesRecipient:
        _rulesStrings = _logRulesRecipient.find("rulesStrings")
        if _rulesStrings:
            rows = _rulesStrings.find_all("li")
            if rows:
                for num, row in enumerate(rows, start=0):
                    _results.append((f"logRulesRecipient.rulesStrings.{num}", row.text))
    return _results


def _stages(_def):
    _results = []
    _stages = _def.find("stages")
    if _stages:
        rows = _stages.find_all("li")
        if rows:
            for num, row in enumerate(rows, start=0):
                _label = row.find("label")
                if _label:
                    _results.append((f"stages.{num}.label", _label.text))


def _deathMessage(_def):
    _deathMessage = _def.find("deathMessage")
    if _deathMessage:
        return [("deathMessage", _deathMessage.text)]

def _verbFinder(_def):
    _verb = _def.find("verb")
    if _verb:
        return [("verb", _verb.text)]

def _gerund(_def):
    _gerund = _def.find("gerund")
    if _gerund:
        return [("gerund", _gerund.text)]

class DefParser:
    _parsers = [
        _descriptionFinder,
        _labelFinder,
        _reportStringFinder,
        _logRulesInitiatorFinder,
        _logRulesInitiatorFinder,
        _logRulesRecipientFinder,
        _stages,
        _deathMessage,
        _verbFinder,
        _gerund
    ]

    @classmethod
    def _defNameFinder(cls, _def):
        _defName = _def.find("defName")
        if _defName is not None and _defName != -1:
            return _defName.text

    @classmethod
    def parse(cls, _def):
        results = []
        def_name = cls._defNameFinder(_def)
        if not def_name:
            return []
        for _parser in cls._parsers:
            result = _parser(_def)
            if result:
                results.extend(
                    [(f"{def_name}.{path}", string) for path, string in result]
                )
        return results
