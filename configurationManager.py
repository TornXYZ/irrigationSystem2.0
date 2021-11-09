from configparser import ConfigParser

class configuration:
    "This class controls reading and writing to the config file"

    def __init__(self, configFile):
        self.config = ConfigParser()
        self.config.read(configFile)

        self.ser = int(self.config['GPIO']['SERIAL_OUT'])
        self.sClk = int(self.config['GPIO']['SERIALCLOCK_OUT'])
        self.rClkSensor = int(self.config['GPIO']['REGISTERCLOCK_SENSOR_OUT'])
        self.rClkValve = int(self.config['GPIO']['REGISTERCLOCK_VALVE_OUT'])
        self.pump = int(self.config['GPIO']['PUMP_OUT'])

    def addDict(self, section, dict):
        self.config[section] = dict

    def getSections(self):
        return self.config.sections()

    def getSectionContent(self, section):
        return list(self.config[section])

    def addSection(self, section):
        self.config.add_section(section)

    def addOption(self, section, option, value):
        self.config.set(section, option, value)

    def removeSection(self, section):
        self.config.remove_section(section)

    def removeOption(self, section, option):
        self.config.remove_option(section, option)

    def removeSectionEntry(self, section, key, value):
        self.config.remove

    def writeToFile(self, filename):
        with open(filename, 'w') as configfile:
            self.config.write(configfile)
