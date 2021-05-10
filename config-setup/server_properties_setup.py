# -*- coding: utf-8 -*-
import abc


class ServerProperties(object):
    def __init__(self):
        self.config_list = []

    def set(self, path: str, config: dict):
        self.config_list = ['\n{}={}'.format(key, value) for key, value in config.items()]
        with open(path, 'w') as file_write:
            file_write.writelines(self.config_list)


class Preset(object):
    @abc.abstractmethod
    def get(self):
        pass


class RedstoneConfig(Preset):
    def get(self):
        _config = {
            'spawn-protection': '0',
            'difficulty': 'hard',
            'enable-command-block': 'true',
            'allow-flight': 'true',
            'view-distance': '12'
        }
        return _config


if __name__ == '__main__':
    location = str(input('server.properties 文件位置（默认当前目录）：') or './server.properties')
    select = str(input('==== 请选择一个预设 ===='
                       '1. 生电服（创造、生存）'))

    if select == '1':
        ServerProperties().set(location, RedstoneConfig().get())
