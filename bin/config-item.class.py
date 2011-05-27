#!/bin/python2

import yaml, os, stat

class ConfigItem:
    defaultData = { 
        "url": "default.vizualtech.com", 
        "scriptPath": "public_html/git-post-update-hook.sh", 
        "key": "default_rsa" 
    }

    def __init__(self, repoName):
        self.repoName = repoName

        configFile = repoName + ".yml"
        stream = self.__readConfig(configFile)

        self.data = yaml.load(stream)

        if self.data == None:
            print "Error. Wrong config file: " + configFile
        else:
            for branchName in self.data.viewkeys():
                self.__checkOnKeyFileExists(branchName)

    def __readConfig(self, configFile):
        return file("conf/" + configFile)

    def __checkOnKeyFileExists(self, branchName):
        keyFile = self.getBranchKey(branchName)
        if os.path.exists("keys/" + keyFile) == False:
            print "Error. Keyfile '" + keyFile + "' for branch '" + branchName + "' is not exists"

    def __getBranchParam(self, branchName, paramName):
        if paramName in self.data[branchName]:
            return self.data[branchName][paramName]
        else:
            return self.defaultData[paramName]

    def getBranchUrl(self, branchName):
        return self.__getBranchParam(branchName, "url")

    def getBranchUser(self, branchName):
        return self.__getBranchParam(branchName, "user")

    def getBranchScriptPath(self, branchName):
        return self.__getBranchParam(branchName, "scriptPath")

    def getBranchKey(self, branchName):
        return self.__getBranchParam(branchName, "key")

    def compile(self):
        for branchName in self.data.viewkeys():
            url = self.getBranchUrl(branchName)
            user = self.getBranchUser(branchName)
            scriptPath = self.getBranchScriptPath(branchName)
            key = self.getBranchKey(branchName)

            rawContent = self.__getTemplate("common")
            replaces = {
                "%url%": url,
                "%user%": user,
                "%scriptPath%": scriptPath,
                "%key%": "keys/" + key
            }

            runScriptFile =  self.repoName + "-" + branchName
            isRunScriptExists = os.path.exists("run_scripts/" + runScriptFile)

            preparedContent = self.__getPreparedContent(rawContent, replaces)

            self.__writeToRunScript(runScriptFile, preparedContent)

            if isRunScriptExists == False:
                print "Created new script for '" + self.repoName + "' repository (branch: '" + branchName + "')"

    def __getTemplate(self, templateName):
        template = file("templates/" + templateName, "r")

        return '\n'.join(template.readlines())

    def __getPreparedContent(self, rawContent, replaces):
        result = rawContent
        for search in replaces:
            result = result.replace(search, replaces[search])

        return result

    def __writeToRunScript(self, fileName, content):
        runScript = file("run_scripts/" + fileName, "w")
        runScript.write(content)
        runScript.close()

        os.chmod("run_scripts/" + fileName, 0744)


configItem = ConfigItem("indigo-events")
configItem.compile()
#print configItem.getBranchUrl("develop")
