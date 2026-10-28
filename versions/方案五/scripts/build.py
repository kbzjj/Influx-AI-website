# -*- coding: utf-8 -*-
"""Adapt the project-owned Shinta snapshot; never writes to the skill library."""
from pathlib import Path
import json, re, sys, hashlib
from source_tools import children, call
from content import COPY, CAPABILITIES, PLATFORMS, METRICS, SUBSCRIPTION, CONTACT, CALCULATOR, PRICING_INTRO, PRICING_END, FOOTER

OUT = Path(__file__).resolve().parents[1]
SRC = OUT/'_source/shinta'
RUNTIME = 'runtime/c2348627c3'
HOME = 'E7Gy02fTtRRJl6hMB7qcE2rxgwCUbKrxzEbR3iwtkZQ.B9xiGkhW.mjs'
MAIN = 'script_main.D3Et_y6-.mjs'
j = lambda value: json.dumps(value, ensure_ascii=False)

def desktop_only(source):
    # This delivery intentionally excludes responsive adaptation. Keep the
    # original desktop component variants even inside a narrow preview panel.
    return source.replace('(min-width: 810px) and (max-width: 1199.98px)', '(min-width: 1px) and (max-width: 0px)').replace('(max-width: 809.98px)', '(max-width: 0px)').replace('(min-width: 1200px)', '(min-width: 0px)')

def replace_call(s, marker, value):
    a,b = call(s, marker)
    return s[:a]+value+s[b:]

def html(text, css='influx-fragment'):
    return 'p(`div`,{className:'+j(css)+',dangerouslySetInnerHTML:{__html:'+j(text)+'}})'

def headline(text):
    return 'p(R,{__fromCanvasComponent:!0,children:p(r,{children:p(`h2`,{className:`framer-styles-preset-rrfwft`,children:'+j(text)+'})}),effect:Pu,verticalAlignment:`top`,withExternalLayout:!0})'

s = (SRC/RUNTIME/HOME).read_text()
a,b,parts = children(s, '"data-framer-name":`Main`')
# Use the original hero reveal and layout, replacing only its CMS promotion slot.
parts[0] = replace_call(parts[0], 'p(Sl,{animate:yu,className:`framer-1n5ngb0 hidden-bftmrr`',
    'p(Sl,{animate:yu,initial:bu,className:`influx-hero-stat`,children:'+html('<span>全球创作者档案</span><strong>210M+</strong><i>↗</i>')+'})')
# Original animated platform strip, with the business platforms in place of client logos.
parts[1] = replace_call(parts[1], '_ (Al,'.replace(' ',''), html(PLATFORMS))
# Retain the reference's question/error-card visual with relevant marketing questions.
for original,replacement in [
 ('Influencer collaborations that bring views but no results','不同市场的达人，怎么选？'),
 ('Posting consistently but getting low engagement','粉丝很多，受众适合吗？'),
 ('Content looks “nice”\nbut doesn’t perform','内容制作与发布，谁来跟进？'),
 ('Campaigns feel\nforced and salesy','合作信息分散，进度怎么掌握？'),
 ('No clear content\ndirection or strategy','服务范围和费用，如何确定？')]:
    parts[2]=parts[2].replace('`'+original+'`',j(replacement))
# Product capabilities reuse the original project cards and their hover variants.
cap_cards=[]
for index,(title,desc,img) in enumerate(CAPABILITIES):
    cap_cards.append('p(`a`,{href:'+j('/assets/influx/'+img)+',className:`influx-cap-card`,"data-screenshot":'+j('/assets/influx/'+img)+',"aria-label":'+j('查看完整截图：'+title)+',children:p(zt,{title:'+j(title)+',resultNumber:`产品界面`,resultName:'+j(desc)+',thumbnail:{src:'+j('/assets/influx/'+img)+'},variant:`rWc3klgKE`,style:{width:`100%`}})})')
aa,bb,cap_children = children(parts[6], 'className:`framer-1wbkw5j`')
parts[6] = parts[6][:aa]+'['+cap_children[0]+',p(`div`,{className:`influx-cap-grid`,children:['+','.join(cap_cards)+']}),'+html(SUBSCRIPTION)+']'+parts[6][bb:]
# Service metric slots become service tags, keeping the original type hierarchy.
parts[8] = parts[8].replace('QD18ObLMW:`50M+`','QD18ObLMW:`研究`',1)
second=parts[8].find('tZ4nqoYAm:`Total Impressions`')
third=parts[8].find('tZ4nqoYAm:`Total Impressions`',second+1)
if third>=0: parts[8]=parts[8][:third]+parts[8][third:].replace('tZ4nqoYAm:`Total Impressions`','tZ4nqoYAm:`内容方向 / 制作跟进 / 发布排期`',1)
quote=parts[16]
# Retain original sections in reference order. No fabricated clients, team or reviews.
home_parts=[parts[0],parts[1],parts[2],parts[3],parts[4],parts[5],html(METRICS),parts[6],
    html('<div class="service-heading"><p class="eyebrow">Influx 营销服务</p><h2>你定方向，我们负责落地。</h2><p>告诉我们目标、市场和预算。Influx 团队负责制定方案、找达人、谈合作、跟进内容发布；关键方向和最终人选由你确认。</p></div>'),
    parts[8],quote,parts[10],html(CONTACT)]
# Three original pricing-card components, without a fictitious annual billing switch.
plans=[
 dict(pricingName='Free',priceMonthly='$0',priceYearly='$0',subtitle='开放时间待公布',benefit1='可先登记体验意向',benefit2='功能和额度在开放时公布',benefit3='',benefit4='',benefit5='',buttonText='登记 Free 体验意向',buttonLink='/#contact?plan=Free',variant='qFCqawXKu'),
 dict(pricingName='Plus',priceMonthly='$9.90',priceYearly='$9.90',subtitle='之后 $59.99 / 月',benefit1='AI 达人搜索',benefit2='达人搜索',benefit3='达人数据分析',benefit4='受众分析',benefit5='使用额度在开通前说明',buttonText='咨询 Plus 方案',buttonLink='/#contact?plan=Plus',variant='FK00E4rgU',buttonVariant='White'),
 dict(pricingName='Pro / Enterprise',priceMonthly='—',priceYearly='—',subtitle='暂未开放',benefit1='功能和价格待公布',benefit2='',benefit3='',benefit4='',benefit5='',buttonText='敬请期待',buttonLink='#unavailable',variant='qFCqawXKu')
]
cards=[]
for index,plan in enumerate(plans):
    prop=','.join(k+':'+j(v) for k,v in plan.items())
    cards.append('p(Ll,{__framer__animate:{transition:Nu},__framer__animateOnce:!0,__framer__enter:ku,__framer__styleAppearEffectEnabled:!0,__framer__threshold:.2,className:`influx-plan`,children:p(qr,{'+prop+',style:{width:`100%`,height:`100%`}})})')
pricing_parts=[html(PRICING_INTRO),'p(`section`,{className:`influx-pricing-cards`,children:['+','.join(cards)+']})',html(PRICING_END)]
calc_parts=[html(CALCULATOR)]
new_array='(document.body.dataset.page===`pricing`?['+','.join(pricing_parts)+']:document.body.dataset.page===`calculator`?['+','.join(calc_parts)+']:['+','.join(home_parts)+'])'
s=s[:a]+new_array+s[b:]

# The saved CSS and code remain original except explicit copy/assets and these view compositions.
modules={p.name:p.read_text() for p in (SRC/RUNTIME).glob('*.mjs')}
modules[HOME]=s
m=modules[MAIN]
m=replace_call(m,'v(`div`,{className:`framer-ia081z`',html(FOOTER))
# Remove template purchase widget; keep the author credit in the business footer.
m=replace_call(m,'p(W,{height:96,y:840','null')
# All three business entries intentionally use the original home route's shared shell.
m=m.replace('Ee(Si,decodeURIComponent(location.pathname),!0,Ci)','Ee(Si,`/`,!0,Ci)')
badge='(function(){Ei&&E(()=>{w(document.getElementById(`__framer-badge-container`),T(y,{},T(ee(()=>import(`./PX9hIOIVM.GY6z_tlq.mjs`)))))})})()'
assert badge in m
m=m.replace(badge,'void 0')
m=re.sub(r'EditorBar:t===void 0\?[\s\S]*?,adaptLayoutToTextDirection:', 'EditorBar:void 0,adaptLayoutToTextDirection:',m,count=1)
# Three navigation items; Contact remains the main action.
nav_start=m.rfind('p(K,{links:',0,m.index('CFgvpbOXo:`Contact`'))
nav_end=call(m[nav_start:],'p(K,')[1]+nav_start
m=m[:nav_start]+'null'+m[nav_end:]
modules[MAIN]=m

logo_replacements={
 '/assets/e7fb2951cde42e9a-osXTQmLx6RntsX7CfW3A94lUHo.png':'/assets/influx/logo.png',
 '/assets/eadc11a161920912-osXTQmLx6RntsX7CfW3A94lUHo.png':'/assets/influx/logo.png',
 '/assets/75eebb2b07b43c9a-3J2iAobW3FSPLnwwcW1KCqr2pwM.png':'/assets/influx/logo-white.png',
 '/assets/a2637128181301de-3J2iAobW3FSPLnwwcW1KCqr2pwM.png':'/assets/influx/logo-white.png'
}
for name,source in modules.items():
    if name==HOME:
        source=source.replace('children:`/mo`','children:(h===`Plus`?`首月`:``)')
    for original,replacement in sorted(COPY.items(),key=lambda kv:-len(kv[0])):
        source=source.replace('`'+original+'`',j(replacement))
    source=source.replace('text:`SOCIAL MEDIA MANAGEMENT • SHORT FORM CONTENT • INFLUENCER MARKETING • `','text:'+j('AI 驱动 • 全球连接 • 达人营销 • 自有工具 • '))
    source=source.replace('`Content looks “nice”\nbut doesn’t perform`',j('跟进内容制作与发布'))
    source=source.replace('`Campaigns feel\nforced and salesy`',j('管理每一次合作的进展'))
    source=source.replace('`No clear content\ndirection or strategy`',j('按项目范围定制报价'))
    source=source.replace('`cal.com`','`/#contact`').replace('`https://cal.com`','`/#contact`')
    source=source.replace('`Shinta - Social Media Marketing Agency`',j('Influx AI · 全球达人营销'))
    if name=='shared-lib.D59l5kZ7.mjs':
        source=source.replace('title:'+j('Influx AI · 全球达人营销'),'title:(document.body.dataset.page===`pricing`?'+j('工具与价格 · Influx AI')+':document.body.dataset.page===`calculator`?'+j('达人互动率计算器 · Influx AI')+':'+j('Influx AI · 全球达人营销')+')')
        source=source.replace('description:`Shinta is a social media marketing agency template built to showcase your work, attract clients and support long term brand growth.`','description:'+j('Influx AI，用自有 AI 和全球创作者数据，帮品牌找到合适的达人。'))
        source=source.replace('favicon:`/assets/175a7ae50fb3cdd4-ocZx1fZVRNfygIeYTbGhL94tU.png`','favicon:`/assets/influx/logo.png`')
        source=source.replace('socialImage:`/assets/a2e3264144316a0b-coxQ8PcmIiNjz4jsGum1gSLeT0A.jpg`','socialImage:`/assets/influx/logo.png`')
    for original,replacement in logo_replacements.items():source=source.replace(original,replacement)
    if name=='u0cuUnpe6.Ciz4rbX0.mjs':
        source=source.replace(j('聊聊你的营销项目'),j('沟通项目与报价'))
    (OUT/RUNTIME/name).write_text(desktop_only(source),encoding='utf-8')

original=(SRC/'index.html').read_text()
head=original[original.index('<head>')+6:original.index('</head>')]
head=re.sub(r'<script\b[^>]*>[\s\S]*?</script>','',head)
head=re.sub(r'<link\b[^>]*rel="(?:icon|apple-touch-icon)"[^>]*>','',head)
head=re.sub(r'<meta\b[^>]*(?:framer-search|og:|twitter:)[^>]*>','',head)
head=head.replace('width=device-width','width=1280')
head=re.sub(r'<meta name="description"[^>]*>','<meta name="description" content="Influx AI，用自有 AI 和全球创作者数据，帮品牌找到合适的达人。">',head)
head+='<link rel="stylesheet" href="/influx.css"><link rel="icon" href="/assets/influx/logo.png">'
head=desktop_only(head)
for page,file,title in [('home','index.html','Influx AI · 全球达人营销'),('pricing','pricing.html','工具与价格 · Influx AI'),('calculator','free-tools.html','达人互动率计算器 · Influx AI')]:
    page_head=re.sub(r'<title>.*?</title>','<title>'+title+'</title>',head)
    doc='<!doctype html><html lang="zh-CN"><head>'+page_head+'</head><body data-page="'+page+'"><div id="main"></div><div id="__framer-badge-container" hidden></div><script src="/cms-assets.js"></script><script src="/influx.js"></script><script type="module" src="/'+RUNTIME+'/'+MAIN+'"></script></body></html>'
    (OUT/file).write_text(doc,encoding='utf-8')

manifest=json.loads((SRC/'asset-manifest.json').read_text())
manifest['task_mode']='project'
manifest['pages']=[{'path':file,'reference_page':'https://shinta.framer.media/','sha256':hashlib.sha256((OUT/file).read_bytes()).hexdigest()} for file in ['index.html','pricing.html','free-tools.html']]
for item in manifest['assets']:
    target=OUT/item['path']
    current=hashlib.sha256(target.read_bytes()).hexdigest()
    if current!=item.get('sha256'):
        item['source_sha256']=item.get('sha256')
        item['adaptation']='Chinese business content, view composition or desktop-only breakpoints; original saved in _source/shinta.'
        item['sha256']=current
        item['saved_bytes']=target.stat().st_size
for target in [*(OUT/'assets/influx').glob('*'),OUT/'influx.css',OUT/'influx.js',OUT/'cms-assets.js']:
    manifest['assets'].append({'path':str(target.relative_to(OUT)),'url':'project-owned:'+str(target.relative_to(OUT)),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'saved_bytes':target.stat().st_size})
(OUT/'asset-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Built 3 business pages using the saved original Framer runtime.')
