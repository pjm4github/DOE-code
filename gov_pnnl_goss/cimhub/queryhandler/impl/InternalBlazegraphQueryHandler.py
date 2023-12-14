class InternalBlazegraphQueryHandler:
    def __init__(self):
        #     public InternalBlazegraphQueryHandler(){
        #         File
        self.ieee8500 = open("ieee13.xml")
        #         
        #         try {
        #         } catch (Exception e) {
        #             print(e);
        #         } 
        #     }

    def query(self, szQuery, szTag):
        return None

    def construct(self, szQuery):
        return None

    def addFeederSelection(self, mRID):
        return False

    def clearFeederSelections(self):
        return False

    def getFeederSelection(self):
        return ""
