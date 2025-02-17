# const yarnVersion = version.gameVersion + version.separator + version.build;
# const url = `${YARN_JAR_URL}/${yarnVersion}/yarn-${yarnVersion}-v2.jar`;



# https://maven.fabricmc.net/net/fabricmc/yarn/1.20.5+build.1/yarn-1.20.5+build.1-v2.jar

# https://meta.fabricmc.net/v2/versions/yarn
#   {
#     "gameVersion": "1.20.5",
#     "separator": "+build.",
#     "build": 1,
#     "maven": "net.fabricmc:yarn:1.20.5+build.1",
#     "version": "1.20.5+build.1",
#     "stable": true
#   },

import requests
import zipfile
import io

def downloadMapping(version: str) -> str:
    data = requests.get("https://meta.fabricmc.net/v2/versions/yarn")
    if not data.ok:
        assert requests.exceptions.ConnectionError("bad request")
    context = [ o for o in data.json() if o['gameVersion'] == version ][0]
    yarnVersion = "%s%s%i" % (context['gameVersion'], context['separator'], context['build'])
    yarn_file = requests.get(f"https://maven.fabricmc.net/net/fabricmc/yarn/{yarnVersion}/yarn-{yarnVersion}-v2.jar")
    if not yarn_file.ok:
        assert requests.exceptions.ConnectionError("bad request with yarnfile")
    with zipfile.ZipFile( file=io.BytesIO(yarn_file.content), mode="r" ) as yarn:
        with yarn.open( "mappings/mappings.tiny", mode='r' ) as mappings_file:
            mapping = io.TextIOWrapper(mappings_file, encoding="utf-8", errors="replace").read()
    return mapping
