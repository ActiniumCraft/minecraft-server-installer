# -*- coding: utf-8 -*-
import os
import wget
import abc


class ServerInstaller(object):
    """Server factory.

    """

    @abc.abstractmethod
    def install(self):
        """Install new server.

        Returns: None.

        """
        pass

    def check(self):
        """Check server install status.

        Returns: The return value. Boolean, True or False.

        """
        pass


class Vanilla(ServerInstaller):
    """Vanilla factory.

    """

    def install(self):
        wget.download(url='https://launcher.mojang.com/v1/objects/1b557e7b033b583cd9f66746b7a9ab1ec1673ced/server.jar',
                      out='server.jar')
        os.system('java -Xms1024M -Xmx2048M -jar server.jar nogui')
        replace_file_line('eula.txt', 'eula=false', 'eula=true')

        with open('vanilla_start.bat', 'w', encoding='utf-8') as f:
            f.write('java -Xms1024M -Xmx2048M -jar server.jar nogui')

    def check(self):
        return os.path.exists('server.jar')


class Fabric(ServerInstaller):
    """Fabric factory.

    """

    def install(self):
        wget.download(url='https://maven.fabricmc.net/net/fabricmc/fabric-installer/0.7.3/fabric-installer-0.7.3.jar',
                      out='fabric-installer-0.7.3.jar')
        os.system('java -jar fabric-installer-0.7.3.jar server -downloadMinecraft')
        os.system('java -Xms1024M -Xmx2048M -jar fabric-server-launch.jar nogui')
        replace_file_line('eula.txt', 'eula=false', 'eula=true')

        with open('fabric_start.bat', 'w', encoding='utf-8') as f:
            f.write('java -Xms1024M -Xmx2048M -jar fabric-server-launch.jar nogui')

    def check(self):
        return os.path.exists('fabric-server-launch.jar')


class MCDR(ServerInstaller):
    """MCDR factory.

    """

    def install(self):
        os.system('pip install mcdreforged')
        os.system('python -m mcdreforged')

        with open('MCDR_start.bat', 'w', encoding='utf-8') as f:
            f.write('python -m mcdreforged')

    def check(self):
        return os.path.exists('MCDR_start.bat')


def replace_file_line(file, old_line, new_line):
    """Replacing file line.

    Args:
        file: File to replace.
        old_line: Old data string.
        new_line: New data string.

    Returns: None.

    """
    file_data = ''

    with open(file, 'r', encoding='utf-8') as f:  # 读取文件并获得替换文本
        for line in f:
            if old_line in line:
                line = line.replace(old_line, new_line)
            file_data = file_data + line

    with open(file, 'w', encoding='utf-8') as f:  # 写入替换文本至文件
        f.write(file_data)


def menu():
    pass  # TODO select menu


if __name__ == '__main__':
    menu()
