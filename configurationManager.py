from configparser import ConfigParser

class configuration:
    "This class controls reading and writing to the config file"

    def __init__(self, configfile: str) -> None:
        self.config = ConfigParser()
        self.config.read(configfile)

        self.ser = int(self.config['GPIO']['SERIAL_OUT'])
        self.sclk = int(self.config['GPIO']['SERIALCLOCK_OUT'])
        self.rclk_sensor = int(self.config['GPIO']['REGISTERCLOCK_SENSOR_OUT'])
        self.rclk_valve = int(self.config['GPIO']['REGISTERCLOCK_VALVE_OUT'])
        self.pump = int(self.config['GPIO']['PUMP_OUT'])
        return


    def addDict(self, section, dict_to_add: dict) -> None:
        self.config[section] = dict_to_add
        return


    def getSections(self) -> list:
        return self.config.sections()

    def getSectionContent(self, section: str) -> list:
        return list(self.config[section])

    def addSection(self, section: str) -> None:
        self.config.add_section(section)
        return


    def addOption(self, section: str, option: str, value: int) -> None:
        self.config.set(section, option, value)
        return


    def removeSection(self, section: str) -> None:
        self.config.remove_section(section)
        return


    def removeOption(self, section: str, option: str) -> None:
        self.config.remove_option(section, option)
        return


    def removeSectionEntry(self, section: str, key: str, value: int) -> None:
        self.config.remove
        return


    def writeToFile(self, filename: str) -> None:
        with open(filename, 'w') as configfile:
            self.config.write(configfile)
        return
        
