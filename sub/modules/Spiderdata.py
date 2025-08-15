import requests
'''
https://site.ip138.com/
http://mtool.chinaz.com/
http://searchdns.netcraft.com/
http://tool.chinaz.com/subdomain/
http://tools.bugscaner.com/subdomain/
http://www.yumingco.com/sub/
https://bp.lmboke.com/
https://chaziyu.com/
https://datalabs.net/tools/subdomainfinder
https://devina.io/subdomain-finder
https://digger.tools/subdomains
https://dnsdumpster.com/
https://dnslytics.com/subdomains/
https://hackertarget.com/find-dns-host-records/
https://lookup.tools/subdomain
https://opentunnel.net/subdomain-finder/
https://osint.sh/subdomain/
https://ralfvanveen.com/en/tools/subdomain-finder/
https://rapiddns.io/subdomain
https://s4e.io/tools/find-subdomains
https://scan.javasec.cn/
https://seranking.com/free-tools/subdomain-finder.html
https://sitechecker.pro/subdomain-finder/
https://srcport.com/network-scanner/subdomainfinder
https://subdomainfinder.c99.nl/
https://subdomainfinder.in/
https://subdomainfinder.io/
https://subdomainradar.io/
https://subdomains.whoisxmlapi.com/
https://tool.chinaz.com/subdomain
https://tools.xty.kim/urlblast/?&rand=db0c1c70f44c76016cb87b91eae7216f
https://tools.yum6.cn/Tools/urlblast/
https://transparencyreport.google.com/https/certificates
https://www.aizhan.com/cha/
https://www.dnsgrep.cn/subdomain
https://www.merklemap.com/
https://www.nmmapper.com/sys/tools/subdomainfinder/
https://www.pkey.in/tools-i/search-subdomains
https://www.starpoc.vip/tools/subdomain/
https://www.vedbex.com/tools/subdomain_finder
https://www.webscan.cc/
https://www.secrash.com/p/subdomain-scanner.html
https://suip.biz/?act=subfinder
https://suip.biz/?act=findomain
https://hostedscan.com/subdomain-discovery-tool
https://viewdns.info/subdomains/
https://domains-subdomains-discovery.whoisxmlapi.com/
https://www.vedbex.com/subdomain-finder
https://app.pentest-tools.com/information-gathering/find-subdomains-of-domain
'''
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'
}
url = f'https://site.ip138.com/shisu.edu.cn/domain.htm'
res = requests.get(url, headers=headers)
print(res.text)