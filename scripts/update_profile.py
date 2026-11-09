#!/usr/bin/env python3
"""Generate truthful, source-linked GitHub profile stats and contribution heatmap.

Uses only GitHub's official REST/GraphQL APIs. Never fabricates activity.
"""
import json
import os
from pathlib import Path
from datetime import date, datetime, timezone
from urllib.request import Request, urlopen
from html import escape

OWNER = "ZaxMil"
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
UA = "ZaxMil-Profile-Readme/1.0"

DEFS = """
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#08162b"/><stop offset=".58" stop-color="#0e1530"/><stop offset="1" stop-color="#1b0d33"/></linearGradient>
<linearGradient id="neon" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#23e6f5"/><stop offset=".54" stop-color="#658aff"/><stop offset="1" stop-color="#b56fff"/></linearGradient>
</defs>"""

def txt(x,y,text,size=21,fill="#e3efff",weight=600,ls=0):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" letter-spacing="{ls}" font-family="Segoe UI,Arial,sans-serif">{escape(str(text))}</text>'

def save(name,w,h,content):
    ASSETS.mkdir(parents=True,exist_ok=True)
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'+DEFS+content+'</svg>\n'
    (ASSETS/name).write_text(svg,encoding="utf-8")
    print("wrote", name)

def request_json(url, body=None):
    headers={"User-Agent":UA, "Accept":"application/vnd.github+json", "X-GitHub-Api-Version":"2022-11-28"}
    if TOKEN: headers["Authorization"]="Bearer "+TOKEN
    if body is not None:
        headers["Content-Type"]="application/json"
        body=json.dumps(body).encode()
    with urlopen(Request(url,data=body,headers=headers),timeout=22) as response:
        return json.loads(response.read())

def render_stats(user,repos):
    public_repos=int(user.get("public_repos") or 0)
    stars=sum(int(r.get("stargazers_count") or 0) for r in repos if not r.get("fork"))
    followers=int(user.get("followers") or 0)
    following=int(user.get("following") or 0)
    figures=[("PUBLIC REPOS", public_repos, "#4fe5f7"),("STARS EARNED",stars,"#b47fff"),("FOLLOWERS",followers,"#788dff"),("FOLLOWING",following,"#55e8c8")]
    b='<rect x="1" y="1" width="1198" height="202" rx="24" fill="url(#bg)" stroke="#365f97" stroke-width="2"/>'
    for i,(title,num,color) in enumerate(figures):
        x=20+i*298
        b+=f'<rect x="{x}" y="22" width="266" height="159" rx="20" fill="#101e39" stroke="{color}" stroke-opacity=".55"/>'
        b+=f'<circle cx="{x+226}" cy="50" r="7" fill="{color}"/>'
        b+=txt(x+22,63,title,16,"#bdcde5",700,1.6)
        b+=txt(x+22,139,num,62,"#f5f8ff",800,1)
    save("live-stats.svg",1200,204,b)

def render_activity(payload):
    total=payload["totalContributions"]
    weeks=payload["weeks"]
    if not weeks: raise ValueError("Empty contributions data")
    weeks=weeks[-53:]
    b='<rect x="1" y="1" width="1198" height="279" rx="24" fill="url(#bg)" stroke="#365f97" stroke-width="2"/>'
    b+=txt(29,44,"CONTRIBUTION SIGNAL",21,"#f5faff",800,2)
    b+=txt(906,43,f"{total} CONTRIBUTIONS",17,"#5ff1f9",700,1)
    b+='<path d="M30 60H1170" stroke="#2f446c"/>'
    colors=["#14223e","#184969","#146b96","#168dbb","#36dcf1","#ae7bff"]
    max_count=max(int(d["contributionCount"]) for w in weeks for d in w["contributionDays"])
    for wi,w in enumerate(weeks):
        # Keep 53 weeks within 1200 px, aligned left with year-long rhythm.
        for day in w["contributionDays"]:
            day_index=(date.fromisoformat(day["date"]).weekday()+1)%7
            count=int(day["contributionCount"])
            level=0 if count==0 else min(5,1+int((count/max(1,max_count)) * 4))
            x=149+wi*18.9; y=84+day_index*23
            b+=f'<rect x="{x:.1f}" y="{y}" width="15.5" height="15.5" rx="3.5" fill="{colors[level]}"/>'
    b+=txt(30,106,"SUN",12,"#8ba9ce",600,1)
    b+=txt(30,152,"TUE",12,"#8ba9ce",600,1)
    b+=txt(30,198,"THU",12,"#8ba9ce",600,1)
    b+=txt(30,250,"GITHUB / VERIFIED PUBLIC ACTIVITY",13,"#8ca6cd",700,1)
    b+=txt(1108,251,"MORE  >",13,"#a88afd",700,1)
    save("activity.svg",1200,281,b)

def render_activity_unavailable():
    b='<rect x="1" y="1" width="1198" height="150" rx="24" fill="url(#bg)" stroke="#365f97" stroke-width="2"/>'
    b+=txt(34,59,"CONTRIBUTION SIGNAL",26,"#f5faff",800,1.4)
    b+=txt(34,105,"Live contribution data is temporarily unavailable.",19,"#a8bfdc",500)
    save("activity.svg",1200,152,b)

def main():
    user=request_json("https://api.github.com/users/"+OWNER)
    repos=request_json("https://api.github.com/users/"+OWNER+"/repos?per_page=100&type=owner")
    render_stats(user,repos)
    if not TOKEN:
        print("Missing GITHUB_TOKEN; contribution calendar not available")
        render_activity_unavailable()
        return
    query="""query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}"""
    try:
        result=request_json("https://api.github.com/graphql",{"query":query,"variables":{"login":OWNER}})
        if result.get("errors"): raise ValueError(result["errors"][0].get("message","GraphQL returned error"))
        calendar=result["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        render_activity(calendar)
    except Exception as error:
        print("GitHub contributions unavailable:",type(error).__name__,str(error)[:200])
        render_activity_unavailable()

if __name__=="__main__":
    main()
