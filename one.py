import os
import time
import re
import urllib.parse
import io


li = os.listdir('.')
with open('%s.txt' % time.asctime().replace(' ', '_').replace(':', '_'), 'w', encoding='utf8') as f:
    for i in li:
        if '.py' in i or '.txt' in i or '.md' in i or 'LICENSE' in i:
            continue
        if i[0] == '.':
            continue
        prefix = '# %s-%s-%s %s:%s' % (i[:4], i[4:6], i[6:8], i[8:10], i[10:12])
        # print(prefix)
        with open(i, encoding='utf8') as p:
            tmp = io.StringIO()
            pli = p.readlines()
            for pi in pli:
                result = re.findall("\"GET /.+HTTP/1.1\"", pi)
                if len(result) == 0:
                    continue
                r = result[0][6:-10]
                try:
                    # print(r.rindex('.'), r)
                    index = r.rindex('.')
                    if index < len(r) - 6:
                        raise ValueError
                    file_type = r[index+1:]
                except ValueError:
                    # 异常请求
                    continue
                # 正常请求
                tmp.write('[%s] %s\n' % (file_type, urllib.parse.unquote(r)[:-5]))

            if len(tmp.getvalue()) == 0:
                continue
            f.write('%s\n' % prefix)
            f.write(tmp.getvalue())
            f.write('\n')
