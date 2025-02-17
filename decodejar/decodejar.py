import subprocess
import sys
import os

class DecodeJar:
    # select java 
    attriguts = "{java} -jar {fernflower} -asc -rbr -rsy -dgs -udv -log {jarfile} {output}"

    @staticmethod
    def decode_file(path_jar: str, temp_output: str, java: str):
        if not os.path.isdir(temp_output):
            os.mkdir(temp_output)
        if hasattr(sys, '_MEIPASS'):
            # Если программа упакована
            jar_path = os.path.join(sys._MEIPASS, "fernflower.jar")
        else:
            jar_path = "libs/fernflower.jar"
        subprocess.call(DecodeJar.attriguts.format(java=java, fernflower=jar_path, jarfile=path_jar, output=temp_output))