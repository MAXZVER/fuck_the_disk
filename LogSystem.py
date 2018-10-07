import traceback


class LogSystem:
    def __init__(self):
        pass

    @staticmethod
    def ERROR(error_message):
        module_name = str(traceback.extract_stack()[-2])
        module_name = module_name.replace("<FrameSummary file ", "")
        module_name = module_name.replace(" in <module>>", "")
        print("[ERROR][" + module_name + "] " + error_message)

    @staticmethod
    def CRITICAL(error_message):
        module_name = str(traceback.extract_stack()[-2])
        module_name = module_name.replace("<FrameSummary file ", "")
        module_name = module_name.replace(" in <module>>", "")
        print("[CRITICAL][" + module_name + "] " + error_message)
        exit(1)

    @staticmethod
    def INFO(error_message):
        module_name = str(traceback.extract_stack()[-2])
        module_name = module_name.replace("<FrameSummary file ", "")
        module_name = module_name.replace(" in <module>>", "")
        print("[INFO][" + module_name + "] " + error_message)

    @staticmethod
    def WARNING(error_message):
        module_name = str(traceback.extract_stack()[-2])
        module_name = module_name.replace("<FrameSummary file ", "")
        module_name = module_name.replace(" in <module>>", "")
        print("[WARNING][" + module_name + "] " + error_message)
