# -*- coding: utf-8 -*-
import os
import abc
import platform

try:
    import wget
    print('已检测到 wget 模块            ok')
    import requests
    print('已检测到 requests 模块            ok')
except ImportError:
    print('检测到依赖库缺失,现在开始安装......')
    os.system('pip install wget')
    os.system('pip install requests')
    import wget
    import requests

platform = platform.system()
print('已检测到 python 运行环境            ok')
# Windows 需要使用 python，linux 则需要使用 python3 区分 python2
python_command = 'python' if platform == 'Windows' else 'python3'
pip_command = 'pip' if platform == 'Windows' else 'pip3'


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
    def __init__(self):
        self.version_manifest = {}
        self.version_json = {}
        self.download_link = ''

    def install(self, version='latest'):
        # 获得 version_manifest，对其遍历查找 version 对应的 version_json，并在 version_json 获取下载链接。
        self.version_manifest = requests.get('https://launchermeta.mojang.com/mc/game/version_manifest.json').json()
        if version == 'latest':
            version = self.version_manifest['latest']['release']
        for self_item in self.version_manifest['versions']:
            if not self_item['id'] == version:
                continue
            self.version_json = requests.get(self_item['url']).json()
        if self.version_json == {}:
            raise Exception('错误的版本号')
        self.download_link = self.version_json['downloads']['server']['url']

        wget.download(url=self.download_link, out='server.jar')
        os.system('java -Xms1024M -Xmx2048M -jar server.jar nogui')
        replace_file_line('eula.txt', 'eula=false', 'eula=true')

        with open('vanilla_start.bat', 'w', encoding='utf-8') as f:
            f.write('java -Xms1024M -Xmx2048M -jar server.jar nogui')

        with open('vanilla_start.sh', 'w', encoding='utf-8') as f:
            f.write('java -Xms1024M -Xmx2048M -jar server.jar nogui')


class Fabric(ServerInstaller):
    """Fabric factory.

    """
    def install(self, version='latest'):
        wget.download(url='https://maven.fabricmc.net/net/fabricmc/fabric-installer/0.7.3/fabric-installer-0.7.3.jar',
                      out='fabric-installer-0.7.3.jar')
        if version == 'latest':
            os.system('java -jar fabric-installer-0.7.3.jar server -downloadMinecraft')
        else:
            os.system('java -jar fabric-installer-0.7.3.jar server -downloadMinecraft -mcversion {}'.format(version))
        os.system('java -Xms1024M -Xmx2048M -jar fabric-server-launch.jar nogui')
        replace_file_line('eula.txt', 'eula=false', 'eula=true')

        with open('fabric_start.bat', 'w', encoding='utf-8') as f:
            f.write('java -Xms1024M -Xmx2048M -jar fabric-server-launch.jar nogui')

        with open('fabric_start.sh', 'w', encoding='utf-8') as f:
            f.write('java -Xms1024M -Xmx2048M -jar fabric-server-launch.jar nogui')


class MCDR(ServerInstaller):
    """MCDR factory

    """

    def install(self):
        os.system('{} install mcdreforged'.format(pip_command))
        os.system('{} -m mcdreforged'.format(python_command))

        with open('MCDR_start.bat', 'w', encoding='utf-8') as f:
            f.write('{} -m mcdreforged'.format(python_command))


def replace_file_line(file, old_line, new_line):
    """Replacing file line.

    Args:
        file: File to replace.
        old_line: Old data string.
        new_line: New data string.

    Returns: None.

    """
    file_data = ''

    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            if old_line in line:
                line = line.replace(old_line, new_line)
            file_data = file_data + line

    with open(file, 'w', encoding='utf-8') as f:
        f.write(file_data)


if __name__ == '__main__':
    os.system('{} -m {} install --upgrade {}'.format(python_command, pip_command, pip_command))

    print('是否选择安装 MCDR [y/N]')
    select_mcdr = str(input('输入: ') or 'n').lower()

    if select_mcdr not in {'y', 'yes', 'n', 'no'}:
        raise Exception('请选择 y 或 n')
    if select_mcdr in {'y', 'yes'}:
        print('安装正在进行中，请稍等。。。')
        MCDR().install()
        os.chdir('./server/')

    print('选择服务器内核 [*Vanilla, Fabric]')
    select_core = str(input('输入:  ') or 'vanilla').lower()

    print('请选择服务器版本 [*Latest/自定义版本号]')
    select_version = str(input('输入: ') or 'latest').lower()

    if select_core in {'vanilla', 'v'}:
        print('安装正在进行中，请稍等。。。')
        Vanilla().install(version=select_version)
    elif select_core in {'fabric', 'f'}:
        print('安装正在进行中，请稍等。。。')
        Fabric().install(version=select_version)
    else:
        raise Exception('错误的内核')
