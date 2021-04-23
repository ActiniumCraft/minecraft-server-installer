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

        with open('vanilla_start.sh', 'w', encoding='utf-8') as f:
            f.write('java -Xms1024M -Xmx2048M -jar server.jar nogui')

        os.system('chmod a+x vanilla_start.sh')

    def check(self):
        return os.path.exists('vanilla_start.sh')


class Fabric(ServerInstaller):
    """Fabric factory.

    """
    def install(self):
        wget.download(url='https://maven.fabricmc.net/net/fabricmc/fabric-installer/0.7.3/fabric-installer-0.7.3.jar',
                      out='fabric-installer-0.7.3.jar')
        os.system('java -jar fabric-installer-0.7.3.jar server -downloadMinecraft')
        os.system('java -Xms1024M -Xmx2048M -jar fabric-server-launch.jar nogui')
        replace_file_line('eula.txt', 'eula=false', 'eula=true')

        with open('fabric_start.sh', 'w', encoding='utf-8') as f:
            f.write('java -Xms1024M -Xmx2048M -jar fabric-server-launch.jar nogui')

        os.system('chmod a+x fabric_start.sh')

    def check(self):
        return os.path.exists('fabric_start.sh')


class MCDR(ServerInstaller):
    """MCDR factory

    """
    def install(self):
        os.system('pip3 install mcdreforged')
        os.system('python3 -m mcdreforged')

        with open('MCDR_start.sh', 'w', encoding='utf-8') as f:
            f.write('python3 -m mcdreforged')

        os.system('chmod a+x MCDR_start.sh')

    def check(self):
        return os.path.exists('MCDR_start.sh')


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


def main():
    pass  # TODO select menu


if __name__ == '__main__':
    main()
