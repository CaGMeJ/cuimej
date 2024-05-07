import sys
from cfg_parser import Parser

cfg = sys.argv[1]

with open(cfg) as f:
    S = f.read()
    p = Parser(S)    
    t,i = p.scan(-1, None)


if len(sys.argv) > 2:
    key = None
    for opt in sys.argv[2:]:
        if len(opt) > 1 and opt[:2] == "--":
            key = opt[2:]
            continue
        if key:
            if key == "params":
                k, v = opt.split(",", 1)
                if k in t["params"]:
                    t["params"][k] = v
                else:
                    print("Unknown params proparty!!!    " + k, file=sys.stderr)
                    for kk in t["params"]:
                        if k in kk or kk in k:
                            print("\nDo you mean '" + kk + "' ?", file=sys.stderr)
                            print("default value :", t["params"][kk])
                    sys.exit(1)
            elif key == "process":
                k, v = opt.split(",", 1)

                if "withName:"+k in t["process"]:
                    d = {}
                    flag = 1
                    tmp = ""
                    for c in v:
                        if flag and c == ",":
                            kk, vv = tmp.split("=", 1)
                            if kk in t["process"]["withName:"+k]:
                                t["process"]["withName:"+k][kk] = vv
                            else:
                                print("Unknown process proparty!!!    " + kk, file=sys.stderr)
                            tmp = ""
                        elif c in {"\"", "'"} :
                            flag *= -1
                            tmp += c
                        else:
                            tmp += c

                    if len(tmp):
                        kk, vv = tmp.split("=", 1)
                        if kk in t["process"]["withName:"+k]:
                            t["process"]["withName:"+k][kk] = vv
                        else:
                            print("Unknown process proparty!!!    " + kk, file=sys.stderr)
                else:
                    print("Unknown process proparty!!!    " + k, file=sys.stderr)
                    for kk in t["process"]:
                        if k in kk or kk in k:
                            print("\nDo you mean " + kk + " ?", file=sys.stderr)
                            print("default value :", t["process"][kk])
                    sys.exit(1)

            else:
                print("Unknown option!!!    " + key, file=sys.stderr)
                sys.exit(1)
            key = None

print("//" + (" ".join(sys.argv)))
for k in t:
    if not k in {"params", "process"}:
        print(k+" = "+t[k])
    else:
        print("\n"+k+" {")
        if k == "params":
            for kk in t[k]:
                cnt = 0
                ret = ""
                for c in t[k][kk]:
                    if c!=" ":
                        if cnt > 5:
                            ret += " \\\n" + (" "*cnt)
                        else:
                            ret += (" "*cnt)
                        cnt = 0
                        ret += c
                    else:
                        cnt += 1
                print("    "+kk+" = "+ret)
        else:
            for kk in t[k]:
                print("\n    "+(kk.replace(":", ": "))+" {")
                for kkk in t[k][kk]:
                    print("    "+kkk+" = "+t[k][kk][kkk])
                print("    }")
        print("}")
