import imp
import LocalLab4gen
import os
import math

class TestGeneration:
    def __init__(self):
        self.lg = LocalLab4gen.LocalGeneration()
        self.lg.test = True
        self.baseIP = "172.16.51."


    #tests function outputs a unique username, the correct IP, and the last two digits of the username
    def testRandomAccount(self):
        usr, vm_IP = 0, 0
        usrSet = set()
        def asserts(c):
            assert(usr not in usrSet)
            assert(vm_IP == self.baseIP + str(c))
            x = len(str(c))
            assert(usr[-x:] == str(c))
        
        print("=====================================")
        print("Testing non-victim account generation")
        for c in range(256):
            self.lg.IPSetup(c)
            usr, vm_IP = self.lg.randomAccount(False)
            asserts(c)
            usrSet.add(usr)
        
        print("Testing victim account generation")
        for c in range(256):
            self.lg.IPSetup(c)
            usr, vm_IP = self.lg.randomAccount(True)
            asserts(c)
            assert(usr[:2] == "V_")
        
        print("Finished testing account generation.")
        print("=====================================\n")


    #test that the generated url for images is correct
    def testImageNaming(self):
        print("=====================================")
        print("Beginning Image Naming test")

        base = os.getcwd() + "\\BasicWebsite\\webapp\\cssNJava\\images\\strangeNames\\"
        
        def subRoutine(a, b, c, d, name):
            for i in range(256):
                self.lg.IPSetup(i)
                url = self.lg.listImages(name)
                temp = base + self.baseIP + str(i) + "\\" + self.lg.imageBase[a] + self.lg.imageBase[b] + self.lg.imageBase[c] + self.lg.imageBase[d]
                if name == "Icon": temp += ".ico"
                if name != "Icon": temp += ".jpg"
                assert(url == temp)
        
        subRoutine(0, 2, 1, 3, "Background")
        subRoutine(0, 2, 3, 1, "Blob")
        subRoutine(0, 1, 2, 3, "Icon")

        print("Finished naming.")
        print("=====================================\n")

    #test that the manipulation of the IP is correct
    def testIPSetup(self):
        print("=====================================")
        print("Beginning constants test")
        for c in range(256):
            c = str(c)
            IP = "172.16.51." + c
            IPr = c + ".51.16.172"
            IP_list = [c, "51", "16k", "172"]
            self.lg.IPSetup(c)
            assert(self.lg.vm_IP == IP)
            assert(self.lg.imageBase == IP_list)
        print("Constants Test completed!")
        print("=====================================\n")


class TestCreatedFiles:
    def __init__(self) -> None:
        pass

    def testDataBaseUsernameandIP():
        pass

    def testCustomImages():
        pass


if __name__ == "__main__":
    tg = TestGeneration()
    tcreated = TestCreatedFiles()

    tg.testIPSetup()
    tg.testRandomAccount()
    tg.testImageNaming()