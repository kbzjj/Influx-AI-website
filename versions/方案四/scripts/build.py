from pathlib import Path
import sys, json, shutil, hashlib, argparse
parser=argparse.ArgumentParser()
parser.add_argument('--page', choices=['index.html','pricing.html','free-tools.html'])
BUILD_PAGE=parser.parse_args().page
sys.path.insert(0,str(Path(__file__).parent));from dom import parse,Node
# Business-site output and source snapshots belong to this project.
ROOT=next((p for p in Path(__file__).resolve().parents if (p/'versions/方案三').is_dir() and (p/'方案四内容确认稿.md').is_file()),None)
if ROOT is None:raise SystemExit('Cannot find the Influx website project root')
OUT=ROOT/'versions/方案四';SCHEME=OUT;SOURCE=OUT/'_source'
if OUT.is_symlink():raise SystemExit('Scheme four must be a real project directory')
for name in ['index.html.txt','contact-index.html.txt']:
 if not (SOURCE/name).is_file():raise SystemExit('Missing local source snapshot: '+name)
brand=OUT/'assets/influx';brand.mkdir(exist_ok=True)
for name in ['logo.png','logo-white.png','product-ai.png','product-marketplace.png','product-campaigns.png','product-brand.png','inter-regular.ttf','inter-medium.ttf','inter-bold.ttf','d-din-regular.otf','d-din-bold.otf']:
 p=ROOT/'versions/方案三/assets'/name
 if p.exists():shutil.copy2(p,brand/name)
# Source names are checked before substituting product screenshots.
print('Brand assets:',[p.name for p in brand.iterdir()])
source=parse((SOURCE/'index.html.txt').read_text()); sections=source.all(tag='section'); contactsource=parse((SOURCE/'contact-index.html.txt').read_text())
COPY={}
ZH_COPY=json.loads((OUT/'content-zh.json').read_text())
EN_COPY=json.loads((OUT/'content-en.json').read_text())
def bind(n,key,zh,en):
 COPY[key]={'zh':zh,'en':en};n.attrs['data-copy']=key;n.set(en);return n
def text(tag,cls,key,zh,en):return bind(Node(tag,{'class':cls}),key,zh,en)
def raw(s):return parse(s).children[0]
def remove(root,node):root.remove(node)
def button(key,zh,en,href='#contact',variant=None):
 n=source.one(cls='button-arrow').clone();n.attrs['href']=href
 if variant:n.attrs['class']+=' '+variant
 for i,t in enumerate(n.all(attr={'text-1':'move'})+n.all(attr={'text-2':'move'})):
  bind(t,key,zh,en)
  if i:t.attrs['aria-hidden']='true'
 return n
def normalize_assets(n):
 for e in n.walk():
  for a in ['src','href','poster','data-poster-url','data-video-urls','srcset']:
   if a in e.attrs and e.attrs[a]:e.attrs[a]=e.attrs[a].replace('../assets/','assets/')
 return n
# Header has the exact desktop proportions and palette from scheme three; mobile access is added.
header=raw('''<header class="site-header"><a class="brand" href="index.html" aria-label="Influx AI home"><img src="assets/influx/logo.png" alt="Influx AI" width="494" height="120"></a><nav class="desktop-nav" aria-label="Main navigation"></nav><div class="nav-right"><div class="language-switch" role="group" aria-label="Language"><button type="button" data-lang="zh" aria-pressed="false">中文</button><span>/</span><button type="button" data-lang="en" aria-pressed="true">EN</button></div><a class="nav-contact" href="index.html#contact"><span data-copy="navCta">Let's talk</span><span aria-hidden="true">→</span></a><button class="mobile-menu-toggle" type="button" aria-expanded="false" aria-controls="mobile-navigation" aria-label="Open navigation"><span></span><span></span></button></div></header>''')
navs=[('navServices','营销服务','Services','index.html#managed'),('navResources','资源与能力','Resources & expertise','index.html#resources'),('navPricing','价格','Pricing','pricing.html'),('navFreeTools','工具','Tools','free-tools.html')]
for k,z,e,h in navs: header.one(cls='desktop-nav').children.append(bind(Node('a',{'href':h}),k,z,e))
COPY['navCta']={'zh':'聊聊你的营销项目','en':"Let's talk about your project"}
mobile=raw('<nav id="mobile-navigation" class="mobile-navigation" aria-label="Mobile navigation" hidden></nav>')
for k,z,e,h in navs+[('navCta','聊聊你的营销项目',"Let's talk about your project",'index.html#contact')]:mobile.children.append(bind(Node('a',{'href':h}),k,z,e))
# Original Reels hero: videos, rotation, creator ticker and platform marquee retained.
hero=sections[0].clone();hero.attrs['id']='home'
bind(hero.one(cls='pre-title'),'heroLabel','AI 驱动的达人营销 Agency','AI-powered influencer marketing agency')
bind(hero.one(tag='h1'),'heroTitle','让全球布局<br>始于<span class="hero-title-highlight">真实连接。</span>','REAL CONNECTIONS.<br>WORLDWIDE <span class="hero-title-highlight">ACCESS.</span>')
bind(hero.one(cls='hero-description'),'heroDescription','全球达人资源、自有 AI 与数据能力，加上一支推进合作的营销团队。<br>发现合适的创作者，让营销计划走向行动。','Global creator resources, our own AI and data, and a team that moves the work forward. <br>Find the right creators. Put your marketing plans in motion.')
a=hero.one(cls='button-arrow');a.attrs['href']='#contact'
for i,n in enumerate(a.all(attr={'text-1':'move'})+a.all(attr={'text-2':'move'})):
 bind(n,'navCta',COPY['navCta']['zh'],COPY['navCta']['en']);
 if i:n.attrs['aria-hidden']='true'
ctop=hero.one(cls='hero-creator-top');bind(ctop.one(tag='p'),'creatorLabel','全球创作者资源库','A world of creator profiles') if ctop.all(tag='p') else None
for n in ctop.all(tag='div'):
 if n.text().strip()=='Creators we work with':bind(n,'creatorLabel','全球创作者资源库','A world of creator profiles')
bind(hero.one(cls='hero-creator-counter'),'creatorCount','210<span class="number-suffix">M+</span>','210<span class="number-suffix">M+</span>')
# Template creator handles and avatars are visual samples; no follower counts or verified endorsements.
for n in hero.all(cls='marquee-icon')+hero.all(cls='hero-reels-verified'):hero.remove(n)
for n in hero.all(tag='img'):
 if n.attrs.get('alt','').lower()=='verified icon':hero.remove(n)
namez=['美妆与生活','时尚与文化','美食与饮品','旅行探索','运动健身','数码科技'];namee=['Beauty & lifestyle','Fashion & culture','Food & drink','Travel','Fitness','Technology']
for i,n in enumerate(hero.all(cls='marquee-avatar-name')):bind(n,'creatorCategory'+str(i%6),namez[i%6],namee[i%6])
for n in hero.all(cls='marquee-counter-info'):hero.remove(n)
for badge,original in zip(hero.all(cls='hero-reels-badge'),sections[0].all(cls='hero-reels-badge')):
 badge.children=[c.clone() if isinstance(c,Node) else c for c in original.children]
 for icon in badge.all(cls='reels-badge-icon'):badge.remove(icon)
for n in hero.all(cls='social-platform-item'):
 if 'Snapchat' in n.text():hero.remove(n)
# Platform pills have a non-obvious source class; remove only the observed Snapchat pill.
for n in list(hero.walk()):
 if n.tag in ('div','a') and n.text().strip()=='Snapchat' and n.all(tag='img'):hero.remove(n)
bind(hero.one(cls='hero-social-platform').one(tag='p'),'platformCaption','受众遍布世界，连接从他们所在的平台开始。','Your audience is everywhere. Start where they are.')
# One static set of four platforms: no marquee targets, clones or edge masks.
platforms=hero.one(cls='social-platfom-list')
items=[n.clone() for n in platforms.one(cls='marquee-item').all(cls='social-media-item')]
platforms.attrs={'class':'static-platform-list','role':'list'}
for item in items:
 item.attrs['role']='listitem'
 item.one(tag='img').attrs.update({'alt':'','aria-hidden':'true'})
 if item.one(cls='social-media-title').text().lower()=='youtube':
  item.one(tag='img').attrs['src']='assets/influx/platform-youtube.svg'
  item.one(cls='social-media-title').set('YouTube')
platforms.children=items
# Services retain Reels' four original sticky cards and timeline selectors.
services=sections[3].clone();services.attrs['id']='managed'
bind(services.one(cls='service-title'),'serviceTitle','你把握方向。<br>我们推进合作。','YOUR DIRECTION.<br>OUR TEAM IN MOTION.')
services.one(cls='section-title').children.insert(0,text('div','pre-title service-kicker','serviceKicker','INFLUX 营销服务','INFLUX SERVICES'))
services.one(cls='section-title').children.append(text('p','service-intro','serviceIntro','把品牌需求转化为可推进的营销项目。我们的 AI、创作者数据与团队经验，一起投入你的品牌。','Turn your brand brief into a campaign in motion. Our AI, creator data and marketing experience work together for your brand.'))
svc=[('目标对齐与活动规划','Direction & campaign planning','了解品牌目标、受众与市场，梳理需求，制定营销方案。','Understand your goals, audience and markets. Shape the brief and build the campaign approach.',['品牌目标','目标受众','营销方案'],['Brand goals','Audience context','Campaign approach']),('创作者研究与筛选','Creator research & selection','结合创作者及受众信息评估候选人，整理合作人选，推进达人沟通。','Evaluate creators and their audiences, build a shortlist and coordinate creator conversations.',['创作者研究','受众分析','人选沟通'],['Creator research','Audience analysis','Creator coordination']),('营销活动执行支持','Campaign execution support','按确认的内容方向与时间安排，协调内容制作、发布和交付。','Coordinate content production, publishing and delivery around the approved direction and timeline.',['内容方向','制作协调','发布跟进'],['Content direction','Production coordination','Publishing support']),('合作关系管理','Collaboration management','协调品牌与创作者之间的信息和合作事项，跟进项目进展。','Keep brands and creators aligned on collaboration details and follow the project through.',['合作事项','信息协调','项目进展'],['Collaboration details','Clear communication','Project progress'])]
for i,(card,item) in enumerate(zip(services.all(cls='service-card'),svc)):
 z,e,zd,ed,zl,el=item;bind(card.one(cls='service-card-title'),f'service{i}Title',z,e);bind(card.one(cls='service-card-description'),f'service{i}Desc',zd,ed)
 for j,n in enumerate(card.all(cls='list-title')):bind(n,f'service{i}Point{j}',zl[j%3],el[j%3])
 counter=card.one(cls='service-counter-info');counter.children=[text('h4','service-counter','serviceNum'+str(i),'0'+str(i+1),'0'+str(i+1)),text('div','','serviceCounterLabel','品牌与团队，清晰分工。','Your brand. Our team. A shared direction.')]
 # Mark reference photos; preserve source image frame and crop.
 card.one(cls='service-card-image').attrs['alt']='Reference imagery, not a client or team photograph'
quote=raw('<div class="quote-summary"></div>');quote.children=[text('div','pre-title','quoteLabel','合作方式','WORK WITH US'),text('h3','','quoteTitle','按项目范围，<br>定制报价。','CUSTOM SCOPE.<br>CUSTOM QUOTE.'),text('p','','quoteDescription','从目标、市场、预算与时间安排开始沟通，再确定工作内容、双方分工和费用。','Start with your goals, markets, budget and timeline. Together we agree on the work, responsibilities and project fee.'),button('quoteCta','沟通项目与报价','Discuss your project & quote')]
quote.children.append(bind(Node('a',{'class':'subtle-link','href':'#how-it-works'}),'processLink','了解合作流程 →','See how we work →'))
quoteSection=Node('section',{'class':'section-spacing-bottom quote-section','id':'project-quote'},[Node('div',{'class':'container-medium'},[quote])])
# Chinese editorial revision; preserve the existing English content and layout.
for card in services.all(cls='service-card'):
 card.one(attr={'data-copy':'serviceCounterLabel'}).attrs['data-en-only']=''
third=services.all(cls='service-card')[2]
last=third.all(cls='list-item')[-1];extra=last.clone()
for node in extra.walk():
 node.attrs.pop('id',None);node.attrs.pop('data-w-id',None)
extra.attrs['data-zh-only']=''
bind(extra.one(cls='list-title'),'service2Point2','发布排期','')
next(parent for parent in third.walk() if last in parent.children).children.append(extra)
# Original mission/video composition carries the global vision.
resources=sections[2].clone();resources.attrs['id']='resources'
bind(resources.one(cls='pre-title'),'visionKicker','我们的全球资源','OUR GLOBAL RESOURCES')
bind(resources.one(cls='mission-title'),'visionTitle','连接全球，<br>从理解彼此开始。','GLOBAL CONNECTIONS.<br>BUILT ON UNDERSTANDING.')
missioninfo=resources.one(cls='mission-info')
bind(missioninfo.one(tag='p'),'visionDescription','帮助品牌跨越地域与文化，理解不同市场中的人、内容与社群。让品牌与创作者找到契合彼此的合作，让连接更有意义。','Help brands cross markets and cultures by understanding people, content and communities. Build partnerships that connect brands and creators in meaningful ways.')
for i,n in enumerate(resources.all(cls='mission-badge-title')):bind(n,'resourceBadge'+str(i),['4 大平台','120+ 地区','210M+ 档案'][i],['4 platforms','120+ markets','210M+ profiles'][i])
link=resources.one(cls='button-arrow');link.attrs['href']='#network'
for i,n in enumerate(link.all(attr={'text-1':'move'})+link.all(attr={'text-2':'move'})):
 bind(n,'resourceCta','探索全球资源','Explore our global resources')
 if i:n.attrs['aria-hidden']='true'
# Source counter layout and ticker, with only approved resource figures.
network=sections[7].clone();network.attrs['id']='network'
bind(network.one(cls='counter-left-info').one(tag='h2'),'networkTitle','跨越市场与平台。<br>发现合适的创作者。','ACROSS MARKETS.<br>ACROSS PLATFORMS.')
ci=network.one(cls='counter-info');bind(ci.one(cls='pre-title'),'networkKicker','全球资源网络','OUR CREATOR NETWORK')
bind(ci.one(cls='counter-count'),'networkCount','210<span class="number-suffix">M+</span>','210<span class="number-suffix">M+</span>')
bind(ci.one(cls='counter-description'),'networkDesc','创作者档案。覆盖不同市场、平台与粉丝量级。','Creator profiles across markets, platforms and follower sizes.')
# Inspect source metrics by leaf, then preserve their containers.
metrics=network.one(cls='counter-list').children
metrics=[n for n in metrics if isinstance(n,Node)]
for i,n in enumerate(metrics):
 hs=n.all(tag='h3'); ps=n.all(tag='p')
 if hs:bind(hs[0],'networkMetric'+str(i),['120<span>+</span>','4','3'][i],['120<span>+</span>','4','3'][i])
 if ps:bind(ps[0],'networkMetricDesc'+str(i),['国家及地区','主流社交平台','官方 API 授权平台'][i],['Countries & regions','Social platforms','Official API access platforms'][i])
# Circular platform marks live below each relevant label, not beside the metric number.
platform_icons={item.one(cls='social-media-title').text().lower():item.one(tag='img').attrs['src'] for item in items}
for i,names in [(1,['Tiktok','Youtube','Instagram','X']),(2,['Tiktok','Youtube','Instagram'])]:
 row=metrics[i];label=row.one(tag='p')
 marks=Node('div',{'class':'metric-platform-logos','role':'group','data-aria-copy':'networkMetricDesc'+str(i)})
 for name in names:
  marks.children.append(Node('img',{'class':'metric-platform-logo','src':platform_icons[name.lower()],'alt':{'Tiktok':'TikTok','Youtube':'YouTube'}.get(name,name),'width':'28','height':'28','loading':'lazy'}))
 row.children[row.children.index(label)]=Node('div',{'class':'metric-details'},[label,marks])
for n in list(network.all(cls='counter-marquee-item')):
 for j,x in enumerate(n.all(cls='counter-marquee-title')):bind(x,'platformTicker'+str(j),['TikTok · 官方 API 授权','YouTube · 官方 API 授权','Instagram · 官方 API 授权','X · 平台支持'][j%4],['TikTok · Official API access','YouTube · Official API access','Instagram · Official API access','X · Platform supported'][j%4])
# Handle the source marquee's actual list text class without changing animation nodes.
for n in network.all(cls='counter-marquee-item'):
 labels=[x for x in n.walk() if x.tag=='div' and len(x.children)==1 and isinstance(x.children[0],str)]
 for j,x in enumerate(labels):bind(x,'platformTicker'+str(j%4),['TikTok · 官方 API 授权','YouTube · 官方 API 授权','Instagram · 官方 API 授权','X · 平台支持'][j%4],['TikTok · Official API access','YouTube · Official API access','Instagram · Official API access','X · Platform supported'][j%4])
# One global-resources composition: original mission imagery beside the original metrics card.
resourcecard=network.one(cls='counter-right').clone()
resourcecard.attrs.pop('scroll-item',None)
resources.one(cls='mission-right').children=[resourcecard]
# Platform coverage is shown in the resource metrics; omit the duplicate marquee.
# Restore the vision as the resource section's Chinese heading, keeping one media/data grid.
vision=sections[4].one(cls='case-study-top').clone()
vision.attrs.update({'class':'section-title resources-heading','data-zh-only':''})
bind(vision.one(cls='pre-title'),'visionKicker','我们的全球资源',COPY['visionKicker']['en'])
bind(vision.one(tag='h2'),'visionTitle','连接全球，从理解彼此开始。',COPY['visionTitle']['en'])
vision.children.append(text('p','resources-intro','visionDescription','我们希望帮品牌理解不同市场的人、内容和社群，找到真正契合的创作者。',COPY['visionDescription']['en']))
resources.one(cls='container-medium').children.insert(0,vision)
label=text('div','network-count-label','networkCountLabel','创作者档案','');label.attrs['data-zh-only']=''
caption=resources.one(cls='counter-caption');count=caption.one(cls='counter-count');caption.children.insert(caption.children.index(count)+1,label)
# Product capabilities adapt the original case-study slider (not its fictional cases).
cap=sections[4].clone();cap.attrs['id']='capabilities'
bind(cap.one(cls='case-study-top').one(cls='pre-title'),'capKicker','自有 AI 与产品能力','OUR AI & PRODUCT CAPABILITIES')
bind(cap.one(cls='case-study-top').one(tag='h2'),'capTitle','技术，服务于<br>每一次合作。','TECHNOLOGY BEHIND<br>EVERY CONNECTION.')
capIntro=text('p','capability-intro','capIntro','Influx 团队用自有工具找达人、看数据、管理项目。','');capIntro.attrs['data-zh-only']=''
cap.one(cls='case-study-top').children.append(capIntro)
mask=cap.one(cls='w-slider-mask');slides=mask.all(cls='w-slide');fourth=slides[0].clone();mask.children.append(fourth);slides.append(fourth)
files=['product-ai.png','product-marketplace.png','product-campaigns.png','product-brand.png']
# The existing brand screenshot's filename is discovered, not assumed.
if not (brand/files[3]).exists():
 choices=list((ROOT/'versions/方案三/assets').glob('product-*'))
 for p in choices:
  if p.name not in files[:3]:shutil.copy2(p,brand/p.name);files[3]=p.name;break
caps=[('AI 达人搜索','AI creator search','将创作者需求转化为搜索线索，结合平台、市场和品类等条件缩小候选范围。','Turn a creator brief into search criteria, then refine by platform, market and category.'),('达人资源库','Creator marketplace','比较创作者的受众、互动与增长信息，帮助团队评估合作人选。','Compare audience, engagement and growth information to understand potential collaborators.'),('营销活动管理','Campaign management','组织营销目标、合作条件与项目周期，跟进项目状态和时间安排。','Organize campaign goals, collaboration terms and timelines, and follow project progress.'),('品牌洞察','Brand insight','探索品牌与品类信息，了解市场背景，辅助营销方向和创作者选择。','Explore brand and category context to inform campaign direction and creator selection.')]
for i,(slide,item) in enumerate(zip(slides,caps)):
 z,e,zd,ed=item;bind(slide.one(cls='case-card-title'),f'cap{i}Title',z,e);bind(slide.one(cls='case-card-description'),f'cap{i}Desc',zd,ed)
 image=slide.one(cls='case-image');image.attrs.update({'src':'assets/influx/'+files[i],'alt':e+' interface with illustrative data','data-product-screen':'','tabindex':'0','role':'button','width':'2880','height':'1800'});image.attrs.pop('srcset',None);image.attrs.pop('sizes',None)
 labels=slide.one(cls='case-card-list').all(cls='text-small');bind(labels[0],'capIndex'+str(i),f'0{i+1} / 04',f'0{i+1} / 04');bind(labels[1],'capLabel','自有产品界面','OUR PRODUCT INTERFACE')
 slide.remove(slide.one(cls='grid-case-counter'))
 a=slide.one(cls='button-arrow');a.attrs.pop('href',None);a.attrs['role']='button';a.attrs['tabindex']='0';a.attrs['data-zoom']=str(i)
 for j,n in enumerate(a.all(attr={'text-1':'move'})+a.all(attr={'text-2':'move'})):
  bind(n,'zoomScreen','查看完整截图','View full screenshot')
  if j:n.attrs['aria-hidden']='true'
cap.one(cls='w-slider').attrs.update({'data-autoplay':'false','data-infinite':'true','data-duration':'500'})
for cls,label in [('w-slider-arrow-left','Previous capability'),('w-slider-arrow-right','Next capability')]:
 a=cap.one(cls=cls);a.attrs['class']=a.attrs['class'].replace('hide','')+' capability-arrow';a.attrs['aria-label']=label
bottom=cap.one(cls='case-study-bottom');bottom.children=[text('p','case-bottom-description','capNote','部分搜索与分析能力可独立订阅。Plus 包含 AI 搜索、达人搜索、达人数据分析及受众分析，不包含其余全部能力。','Selected search and analysis capabilities can be subscribed to separately. Plus includes AI search, creator search, creator data and audience analysis, rather than the full capability set.'),button('toolsCta','查看工具方案与价格','Explore tool plans & pricing','pricing.html')]
# Original stepped, rotating workflow cards, with true responsibilities instead of template promises.
process=sections[6].clone();process.attrs['id']='how-it-works'
bind(process.one(cls='pre-title'),'processLabel','如何开始合作','HOW WE WORK TOGETHER')
words=process.one(cls='step-title-wrap').all(tag='h2')
for i,n in enumerate(words):bind(n,'processWord'+str(i),['四个','阶段，','明确','分工。','一个','目标，','一起','行动。'][i],['FOUR','STAGES.','YOUR','BRIEF.','OUR','TEAM.','ONE','DIRECTION.'][i])
steps=[('目标与策略','Direction & strategy','提供品牌目标、目标市场与预算','Share brand goals, markets and budget','梳理需求，制定营销方案','Understand the brief and build the campaign approach'),('达人筛选','Creator selection','确认合作人选','Confirm the creator shortlist','研究评估，推进达人沟通','Research, evaluate and coordinate creators'),('内容与交付','Content & delivery','确认内容方向','Approve the content direction','协调内容制作与发布','Coordinate production and publishing'),('复盘与优化','Review & learn','共同回顾项目成果','Review outcomes together','回顾交付情况，整理复盘与建议','Review delivery and recommend next steps')]
for i,(card,item) in enumerate(zip(process.all(cls='step-card'),steps)):
 z,e,bz,be,tz,te=item;bind(card.one(cls='step-card-title'),'step'+str(i)+'Title',z,e)
 bind(card.one(cls='step-card-description'),'step'+str(i)+'Desc','<span class="role-caption">品牌方</span>'+bz+'<span class="role-caption">INFLUX</span>'+tz,'<span class="role-caption">YOUR BRAND</span>'+be+'<span class="role-caption">INFLUX</span>'+te)
# Use the same source image frame and ratio on all four workflow cards.
workflow_photos=[services.all(cls='service-card-image')[i] for i in [3,2,0,1]]
for i,(card,photo) in enumerate(zip(process.all(cls='step-card'),workflow_photos)):
 card.attrs['class']+=' workflow-card'
 info=card.one(cls='step-card-info')
 info.children=[info.one(cls='step-card-title'),info.one(cls='step-card-description')]
 frame=sections[6].one(cls='step-image-wrap').clone()
 frame.attrs['class']+=' workflow-photo'
 image=frame.one(tag='img')
 image.attrs={'src':photo.attrs['src'],'loading':'lazy','alt':['Campaign planning','Creator selection','Content production','Content review'][i],'class':'step-image','width':'400','height':'300'}
 bottom=card.one(cls='step-card-bottom');bottom.children=[frame,info]
 card.children=[card.one(cls='step-card-top'),bottom]
# Contact's source layout and input styling, with exactly the same four fields for everyone.
contact=normalize_assets(contactsource.all(tag='section')[0].clone());contact.attrs.update({'id':'contact','class':'section-spacing-bottom contact-section','data-scroll':'load'})
for n in contact.all(attr={'data':'show'}):n.attrs.pop('data',None);n.attrs['scroll-item']='show'
left=contact.one(cls='hero-contact-left');left.remove(left.one(cls='hero-client-info'));left.remove(left.one(cls='hero-team-platform'))
ctitle=contact.one(cls='hero-contact-title');ctitle.children=[text('div','pre-title','contactLabel','联系我们','GET IN TOUCH'),text('h2','hero-word','contactTitle','从一次沟通，<br>开始下一次<span class="contact-highlite-title">合作。</span>',"LET'S START<br>A <span class=\"contact-highlite-title\">CONVERSATION.</span>"),text('p','contact-description','contactDesc','营销项目、工具咨询或达人合作，都可以在这里留言。','Campaign projects, tool enquiries or creator collaborations. Tell us what you have in mind.')]
bind(contact.one(cls='contact-right-title'),'contactFormTitle','聊聊你的想法。','Tell us what you have in mind.')
form=contact.one(tag='form');form.attrs={'id':'contact-form','class':'contact-inner-form','action':'#','method':'post'};form.children=[]
for name,typ,z,e,required in [('name','text','你的姓名','Your name',True),('email','email','联系邮箱','Email address',True),('company','text','品牌 / 公司名称（选填）','Brand / company (optional)',False),('message','textarea','咨询内容','Your enquiry',True)]:
 wrap=Node('div',{'class':'label'});wrap.children.append(bind(Node('label',{'for':'contact-'+name,'class':'field-title'}),'field_'+name,z,e));attrs={'id':'contact-'+name,'name':name,'class':'form-input contact-input w-input','maxlength':'3000' if typ=='textarea' else '200'}
 if required:attrs['required']=''
 if typ=='textarea':attrs['rows']='4';attrs['data-placeholder']='messageHint';field=Node('textarea',attrs)
 else:attrs['type']=typ;attrs['autocomplete']={'name':'name','email':'email','company':'organization'}[name];field=Node('input',attrs)
 wrap.children.append(field);form.children.append(wrap)
COPY['messageHint']={'zh':'请简单介绍你的问题或合作需求。','en':'Tell us about your question or collaboration needs.'}
form.children.extend([button('submitEnquiry','提交咨询','Send enquiry'),raw('<p class="form-status" role="status" aria-live="polite"></p>')]);form.one(tag='a').tag='button';form.one(tag='button').attrs.update({'type':'submit'});form.one(tag='button').attrs.pop('href',None)
submit=form.one(tag='button');submit.attrs['class']+=' contact-submit'
submit.remove(submit.one(cls='button-icon-round'))
submit.children.append(raw('<span class="submit-arrow" aria-hidden="true">→</span>'))
for cls in ['w-form-done','w-form-fail']:
 for n in contact.all(cls=cls):contact.remove(n)
# Source footer preserved, with real navigation in place of fictitious contacts, newsletter and client links.
footer=source.one(tag='footer').clone();footer.attrs['class']='footer section-spacing-top'
logo=footer.one(cls='footer-brand-logo');logo.attrs.update({'src':'assets/influx/logo-white.png','alt':'Influx AI'});logo.attrs.pop('srcset',None)
footer.one(cls='footer-brand-link').attrs['aria-label']='Influx AI home'
bind(footer.one(cls='footer-text'),'footerDescription','一家以 AI 和数据驱动的达人营销 Agency。','An AI- and data-driven influencer marketing agency.')
footer.remove(footer.one(cls='footer-social-list'))
bind(footer.one(cls='footer-right').one(cls='footer-title'),'footerExplore','了解 Influx','EXPLORE INFLUX')
menu=footer.one(cls='grid-footer-menu');menu.children=[]
for i,(k,z,e,h) in enumerate(navs[:2]+[('footerProcess','合作流程','How we work','index.html#how-it-works'),('footerContact','联系我们','Contact us','index.html#contact')]):
 a=source.one(cls='footer-link').clone();a.attrs={'href':h,'class':'footer-link w-inline-block'};bind(a.one(cls='footer-link-title'),k,z,e);menu.children.append(a)
grids=footer.all(cls='grid-footer-info');second=grids[1]
second.children=[]
for key,z,e,links in [('footerTools','工具','TOOLS',[('navTools','工具与价格','Tools & pricing','pricing.html'),('calculatorLink','免费互动率计算器','Free engagement calculator','free-tools.html')]),('footerLegal','条款与政策','TERMS & POLICIES',[('terms','服务条款','Terms of service','terms'),('agreement','用户协议','User agreement','agreement'),('privacy','隐私政策','Privacy policy','privacy')])]:
 group=Node('div',{'class':'footer-contact-info','scroll-item':'show'});group.children.append(text('h3','footer-title',key,z,e));lst=Node('div',{'class':'footer-contact-list'})
 for k,zz,ee,h in links:
  n=Node('a' if h.endswith('.html') else 'button',{'class':'footer-contact-link','href':h} if h.endswith('.html') else {'class':'footer-contact-link','type':'button','data-legal':h});bind(n,k,zz,ee);lst.children.append(n)
 group.children.append(lst);second.children.append(group)
footer.one(cls='footer-copyright-text').set('© 2026 Influx AI <span class="template-credit">Reels template by <a href="https://webestica.com/" target="_blank" rel="noopener">Webestica</a></span>')
footer.one(cls='footer-pages-link').set('')
# Tools & pricing reuse the original pricing section and three-card composition.
pricing=sections[9].clone();pricing.attrs['class']='section-spacing pricing-page';pricing.attrs['id']='plans'
pricing.remove(pricing.one(cls='pricing-section-title').one(cls='pre-title'))
bind(pricing.one(cls='pricing-section-title').one(tag='h2'),'pricingTitle','选择适合你的<em>合作方式。</em>','Choose how we <em>work together.</em>')
pricing.one(cls='pricing-section-title').one(tag='h2').tag='h1'
pricing.one(cls='section-title').children.append(text('p','pricing-intro','pricingIntro','让你的团队用上我们的技术，或让我们的团队投入你的营销项目。','Use our technology with your team, or put our team to work on your marketing projects.'))
COPY['servicePriceNote']={'zh':'本页为工具订阅价格。营销服务按项目范围定制报价。了解营销服务 →','en':'These are tool subscription plans. Marketing services are quoted by project scope. Explore our services →'}
pricing.remove(pricing.one(cls='pricing-platform'));tabs=pricing.one(cls='w-tabs');tabs.attrs['class']='pricing-tab';tabs.attrs.pop('data-current',None);tabs.remove(tabs.one(cls='w-tab-menu'))
panes=tabs.all(cls='w-tab-pane');tabs.remove(panes[1]);panes[0].attrs={'class':'pricing-tab-pane w--tab-active'}
cards=pricing.all(cls='pricing-card')
plans=[('Free','Free','$0','体验开放安排待公布','Experience availability to be announced',['登记免费体验意向','能力、额度与开放安排待公布','登记不会直接生成账号'],['Register your interest','Scope, limits & timing to be announced','Registration does not create an account'],'free'),('Plus','Plus','$9.90','首月，次月起 $59.99 USD / 月','First month, then $59.99 USD / month',['AI 达人搜索','达人搜索','达人数据分析','受众分析'],['AI creator search','Creator search','Creator data analysis','Audience analysis'],'plus'),('Pro / Enterprise','Pro / Enterprise','—','暂未开放','Not available yet',['Pro · 功能与价格待公布','Enterprise · 功能与价格待公布'],['Pro · Features & pricing to be announced','Enterprise · Features & pricing to be announced'],None)]
for i,(card,item) in enumerate(zip(cards,plans)):
 z,e,amount,zz,ee,zl,el,intent=item;bind(card.one(cls='pricing-card-title'),'plan'+str(i)+'Title',z,e);bind(card.one(cls='pricing-pre-title'),'plan'+str(i)+'Desc',zz,ee)
 bind(card.one(cls='pricing-amount').one(tag='h4'),'plan'+str(i)+'Amount',amount,amount)
 bind(card.one(cls='pricing-amount-text'),'plan'+str(i)+'Term','首月体验价' if i==1 else '免费意向登记' if i==0 else '开放安排待公布','INTRO OFFER' if i==1 else 'REGISTER INTEREST' if i==0 else 'COMING LATER')
 lst=card.one(cls='pricing-list');prototype=lst.one(cls='list-item').clone();lst.children=[]
 for j,(a,b) in enumerate(zip(zl,el)):
  n=prototype.clone();bind(n.one(cls='list-title'),f'plan{i}Point{j}',a,b);lst.children.append(n)
 btn=card.one(cls='button-primary')
 if intent:btn.attrs['href']='index.html?intent='+intent+'#contact';btn.attrs['data-intent']=intent
 else:btn.tag='button';btn.attrs.pop('href',None);btn.attrs['disabled']='';btn.attrs['type']='button'
 for j,n in enumerate(btn.all(attr={'text-1':'move'})+btn.all(attr={'text-2':'move'})):
  bind(n,'plan'+str(i)+'Cta',['登记 Free 体验意向','咨询 Plus 方案','敬请期待'][i],['Register Free interest','Enquire about Plus','Coming soon'][i])
  if j:n.attrs['aria-hidden']='true'
 # Original "most popular" badge is replaced with a factual introductory offer label.
 for n in card.all(cls='pricing-popular-text'):bind(n,'introOffer','首月体验价','INTRO OFFER')
 for n in list(card.walk()):
  if len(n.children)==1 and isinstance(n.children[0],str) and n.children[0].strip()=='Most popular':bind(n,'introOffer','首月体验价','INTRO OFFER')
pricing.one(cls='container-medium').children.extend([text('div','plan-boundary','plusBoundary','<strong>Plus 专注达人发现与分析。</strong><br>不包含营销活动管理、达人建联、报告及数据与品牌洞察模块。具体使用额度在开通前说明。','<strong>Plus focuses on discovery and analysis.</strong><br>Campaign management, creator outreach, reports and data / brand insight modules are not included. Usage limits will be explained before activation.'),text('p','pricing-disclosure','pricingDisclosure','当前仅登记体验或工具咨询意向，不直接开通账号，不收取费用。','This preview registers tool or experience enquiries. It does not activate accounts or collect payment.'),bind(Node('a',{'href':'free-tools.html','class':'calculator-link'}),'calculatorCta','免费试用互动率计算器 →','Try the free engagement calculator →')])
# Hide only redundant Chinese plan elements; English keeps its original presentation.
for index in [0,2]:cards[index].one(cls='pricing-amount-item').attrs['data-en-only']=''
cards[0].one(cls='pricing-list').all(cls='list-item')[2].attrs['data-en-only']=''
cards[2].one(cls='pricing-list').all(cls='list-item')[1].attrs['data-en-only']=''
cards[1].one(cls='pricing-badge').attrs['data-en-only']=''
# Pricing categories share the contact layout and preserve the existing tool plans.
pricing_heading=pricing.one(cls='section-title').clone()
pricing_heading.remove(pricing_heading.one(cls='pricing-intro'))
pricing.remove(pricing.one(cls='section-title'))
category_tabs=Node('div',{'class':'pricing-categories pricing-toggle','role':'tablist','aria-label':'Pricing categories'})
for category,key,zh,en in [('services','pricingServicesTab','营销服务','Marketing services'),('tools','pricingToolsTab','工具产品','Tool products')]:
 category_tabs.children.append(bind(Node('button',{'id':'pricing-tab-'+category,'class':'toggle','type':'button','role':'tab','aria-controls':'pricing-panel-'+category,'aria-selected':'true' if category=='services' else 'false','tabindex':'0' if category=='services' else '-1','data-pricing-tab':category}),key,zh,en))
service_pricing=contact.clone()
service_pricing.attrs={'id':'pricing-panel-services','class':'section-spacing-bottom contact-section service-pricing-panel','role':'tabpanel','aria-labelledby':'pricing-tab-services','tabindex':'0','data-pricing-panel':'services'}
service_title=service_pricing.one(cls='hero-contact-title')
service_title.children=[text('div','pre-title','pricingServiceLabel','服务报价','SERVICE QUOTE'),text('h2','hero-word','pricingServiceTitle','按项目范围定制','Tailored to your project scope'),text('p','contact-description','pricingServiceDescription','先聊目标、市场和预算，再确定服务内容和费用。','Let’s discuss your goals, markets and budget, then agree on the services and fees.')]
# User requested only the centred form beneath the page title and category tabs.
service_pricing.remove(service_pricing.one(cls='hero-contact-left'))
bind(service_pricing.one(cls='contact-right-title'),'pricingFormTitle','留下你的需求，按项目范围定制','Tell us what you need')
service_pricing.one(tag='form').attrs['data-intent']='marketing-service'
pricing.attrs.update({'id':'pricing-panel-tools','role':'tabpanel','aria-labelledby':'pricing-tab-tools','tabindex':'0','hidden':'','data-pricing-panel':'tools'})
pricing_heading.one(cls='grid-pricing').children.append(category_tabs)
pricing_shell=Node('section',{'class':'pricing-shell reels-pricing-page'},[Node('div',{'class':'container-medium pricing-category-heading'},[pricing_heading]),service_pricing,pricing])
# Panels must be visible immediately when switched, independent of scroll animation setup.
for node in pricing_shell.walk():
 node.attrs.pop('scroll-item',None)
 if node.attrs.get('data')=='show':node.attrs.pop('data')
 node.attrs.pop('data-scroll',None)
# Reuse Reels' native 50px reveal with its original 0.2s stagger.
for node in [pricing_heading.one(tag='h1'),category_tabs,service_pricing.one(cls='hero-contact-right')]:
 node.attrs['data']='show'

# Calculator reuses the source contact grid and controls, with the result in its left column.
calculator=contact.clone();calculator.attrs={'class':'section-spacing-bottom calculator-page','data-scroll':'load','id':'calculator'}
cleft=calculator.one(cls='hero-contact-left');cleft.children=[text('div','pre-title','calcKicker','免费工具','FREE TOOL'),text('h1','calculator-title','calcTitle','创作者<br>互动率<span class="contact-highlite-title">计算器。</span>','CREATOR<br>ENGAGEMENT<br><span class="contact-highlite-title">CALCULATOR.</span>'),text('p','contact-description','calcIntro','输入一条内容的点赞数、评论数及创作者粉丝数，计算该条内容的互动率。','Enter likes and comments for a single post, plus the creator’s follower count, to calculate engagement.'),raw('<output id="engagement-result" class="engagement-result" for="followers likes comments" aria-live="polite">—</output>'),text('p','','calcResultLabel','按粉丝数计算的互动率','ENGAGEMENT RATE BY FOLLOWERS'),text('p','calc-formula','calcFormula','（点赞数 + 评论数）÷ 粉丝数 × 100%','(Likes + comments) ÷ followers × 100%')]
bind(calculator.one(cls='contact-right-title'),'calcFormTitle','从一条内容开始。','START WITH ONE POST.')
cf=calculator.one(tag='form');cf.attrs={'id':'engagement-calculator','class':'contact-inner-form','action':'#'};cf.children=[]
for name,z,e,minv in [('followers','粉丝数','Followers','1'),('likes','点赞数','Likes','0'),('comments','评论数','Comments','0')]:
 wrap=Node('div',{'class':'label'});wrap.children=[bind(Node('label',{'for':name,'class':'field-title'}),'calcField'+name,z,e),Node('input',{'id':name,'name':name,'type':'number','min':minv,'max':'1000000000000','step':'1','required':'','inputmode':'numeric','class':'form-input contact-input w-input'})];cf.children.append(wrap)
cb=button('calcSubmit','计算互动率','Calculate engagement');cb.tag='button';cb.attrs.pop('href',None);cb.attrs.update({'type':'submit'});cb.attrs['class']+=' calculator-submit';cb.children=[cb.one(cls='button-text-wrap'),raw('<span class="submit-arrow" aria-hidden="true">→</span>')];cf.children.append(cb)
calculator.one(cls='container-medium').children.append(bind(Node('a',{'href':'index.html#managed','class':'calculator-link'}),'calcServices','希望由团队支持达人筛选？了解营销服务 →','Need a team to help select creators? Explore our services →'))
# Common native dialogs; no fictitious remote actions or legal agreements.
dialogs=raw('''<div><dialog id="screen-dialog" class="screen-dialog"><button type="button" class="dialog-close" data-close aria-label="Close screenshot">×</button><img id="expanded-screen" alt=""></dialog><dialog id="legal-dialog" class="legal-dialog"><button type="button" class="dialog-close" data-close aria-label="Close">×</button><h2 id="legal-title"></h2><p id="legal-content"></p></dialog></div>''')
COPY.update({'termsBody':{'zh':'完整服务条款将在正式上线前公布。当前为页面预览，不构成正式协议。','en':'The full terms will be published before launch. This preview is not a binding agreement.'},'agreementBody':{'zh':'用户协议将在账号注册开放前公布。当前预览不直接开通账号。','en':'The user agreement will be published before account registration opens. This preview does not activate accounts.'},'privacyBody':{'zh':'完整隐私政策将在上线前公布。当前预览的表单信息仅保存在你的浏览器中。','en':'The full privacy policy will be available before launch. Enquiry details in this preview are only saved in your browser.'},'saved':{'zh':'内容已保存在此浏览器，尚未发送给 Influx。','en':'Your enquiry is saved in this browser and has not been sent to Influx.'},'saveFailed':{'zh':'浏览器暂时无法保存，请保留填写内容后重试。','en':'This browser could not save your enquiry. Please keep your details and try again.'}})
# Locale branches are pruned before either native animation runtime initializes.
# Reuse the original Reels service structure and its original timeline at capabilities.
capstack=services.clone();capstack.attrs.update({'id':'capabilities','class':capstack.attrs.get('class','')+' product-stack'})
bind(capstack.one(cls='service-title'),'capTitle',COPY['capTitle']['zh'],COPY['capTitle']['en'])
bind(capstack.one(cls='service-kicker'),'capKicker',COPY['capKicker']['zh'],COPY['capKicker']['en'])
bind(capstack.one(cls='service-intro'),'capIntro',COPY['capIntro']['zh'],COPY['capIntro']['en'])
for i,card in enumerate(capstack.all(cls='service-card')):
 card.attrs['data-product-card']=str(i)
 bind(card.one(cls='service-card-title'),f'cap{i}Title',COPY[f'cap{i}Title']['zh'],COPY[f'cap{i}Title']['en'])
 bind(card.one(cls='service-card-description'),f'cap{i}Desc',COPY[f'cap{i}Desc']['zh'],COPY[f'cap{i}Desc']['en'])
 card.remove(card.one(cls='service-card-detail'))
 image=card.one(cls='service-card-image');image.attrs={'src':'assets/influx/'+files[i],'alt':caps[i][1]+' interface','data-alt-copy':f'cap{i}Title','class':'service-card-image','data-product-screen':'','tabindex':'0','role':'button','width':'2880','height':'1800','loading':'lazy'}
tool_link=cap.one(cls='case-study-bottom').clone()
tool_link.remove(tool_link.one(cls='case-bottom-description'))
# Keep the CTA outside the containing block that constrains the sticky cards.
capstack.children.append(tool_link)
transition=Node('section',{'id':'managed','class':'service-transition','data-aria-copy':'serviceKicker'},[Node('div',{'id':'service-transition-root'})])
for key,zh in [('transitionTitle','这些问题，交给我们。'),('transitionQuestion0','不同市场的达人，怎么选？'),('transitionQuestion1','粉丝很多，受众适合吗？'),('transitionQuestion2','内容制作与发布，谁来跟进？'),('transitionQuestion3','合作信息分散，进度怎么掌握？'),('transitionQuestion4','服务范围和费用，如何确定？')]:
 COPY[key]={'zh':zh,'en':EN_COPY[key]}
from transition import build_transition
build_transition(OUT)

# All Chinese editorial content has one project-owned source; do not change English values.
for key,value in ZH_COPY.items():
 if key not in COPY:raise KeyError('Unknown Chinese content key: '+key)
 COPY[key]['zh']=value
for key,value in EN_COPY.items():
 if key not in COPY:raise KeyError('Unknown English content key: '+key)
 COPY[key]['en']=value
# Reuse the original engine, page ID, selectors and original script order.
body=source.one(tag='body');scripts=[n.clone() for n in body.children if isinstance(n,Node) and n.tag in ('script','link')]
# Original script elements may be nested at the end of a wrapper; get the runtime tail directly.
bodytext=(SOURCE/'index.html.txt').read_text();tail=bodytext[bodytext.index('<script src="assets/518'):bodytext.rindex('</body>')];tail=tail.replace('<script src="local-study.js"></script>','')
# Original Lenis setup is kept as a single ticker, with accessible anchors and reduced-motion support.
tail=tail.replace('const lenis = new Lenis({','const lenis = window.influxLenis = new Lenis({\n  anchors: true,\n  prevent: node => !!node.closest("dialog,textarea,input"),')
tail=tail.replace('// Lenis Smooth Scroll\nconst lenis','// Lenis Smooth Scroll\nif (!matchMedia("(prefers-reduced-motion: reduce)").matches) {\nconst lenis').replace('gsap.ticker.lagSmoothing(0);','gsap.ticker.lagSmoothing(0);\n}')
head=source.one(tag='head').clone()
for n in list(head.children):
 if not isinstance(n,Node):continue
 if n.tag=='script' and n.attrs.get('type')=='application/ld+json':head.remove(n)
 if n.tag=='meta' and (n.attrs.get('property','').startswith('og:') or n.attrs.get('name','').startswith('twitter:')):head.remove(n)
 if n.tag=='link' and n.attrs.get('rel') in ('icon','apple-touch-icon'):head.remove(n)
head.children.append(raw('<link rel="icon" type="image/png" href="assets/influx/favicon.png">'));head.children.append(raw('<link rel="stylesheet" href="influx.css">'))
head.children.append(raw('<link rel="preload" href="assets/influx/leon-sans-variable.ttf" as="font" type="font/ttf" crossorigin="anonymous">'))
head.one(tag='meta',attr={'name':'description'}).attrs['content']='Influx AI is an AI-powered influencer marketing agency with global creator resources, proprietary tools and campaign services.'
for name,content in [('index.html',[hero,transition,resources,capstack,process,contact]),('pricing.html',[pricing_shell]),('free-tools.html',[calculator])]:
 if BUILD_PAGE and name != BUILD_PAGE:continue
 # Both languages share the latest approved layout and deletions.
 for block in content:
  for node in list(block.walk()):
   if 'data-en-only' in node.attrs:block.remove(node)
   node.attrs.pop('data-zh-only',None)
 if name != 'index.html':
  for block in content:
   block.attrs.pop('data-scroll',None)
   for node in block.all(attr={'scroll-item':'show'}):
    node.attrs.pop('scroll-item',None);node.attrs['data']='show'
 h=head.clone()
 if name=='pricing.html':h.children.append(raw('<link rel="stylesheet" href="pricing-reels.css">'))
 h.one(tag='title').set({'index.html':'Influx AI — Global creator marketing','pricing.html':'Influx AI — Tools & pricing','free-tools.html':'Influx AI — Engagement calculator'}[name])
 b=Node('body',{'data-page':name,'class':'influx-site'});b.children=[raw('<a class="skip-link" href="#main" data-copy="skip">Skip to content</a>'),header.clone(),mobile.clone(),Node('main',{'id':'main'},[x.clone() for x in content]),footer.clone(),dialogs.clone(),raw('<script src="copy.js"></script>'),raw('<script src="influx.js"></script>')]+parse(tail).children+[raw('<script src="runtime-bridge.js"></script>'),raw('<script type="module" src="service-transition.js"></script>')]
 
 for n in b.all(attr={'text-2':'move'}):n.attrs['aria-hidden']='true'
 for n in [n for n in b.walk() if 'data-copy' in n.attrs]:
  if n.attrs['data-copy'] in COPY:n.set(COPY[n.attrs['data-copy']]['en'])
 for n in b.all(tag='img'):
  if 'button-icon' in n.attrs.get('class','').split():n.attrs.update({'alt':'','aria-hidden':'true'})
 html=Node('html',source.one(tag='html').attrs.copy(),[h,b]);(OUT/name).write_text('<!DOCTYPE html>'+html.html())
COPY['skip']={'zh':'跳转至正文','en':'Skip to content'}
(OUT/'copy.js').write_text('window.INFLUX_COPY = '+json.dumps(COPY,ensure_ascii=False,indent=2)+';\n')
scope={'source_url':'https://reels-wbs.webflow.io/','source_snapshots':[str(SOURCE/'index.html.txt'),str(SOURCE/'contact-index.html.txt')],'content_sources':[str(ROOT/'方案四内容确认稿.md'),str(ROOT/'方案四内部说明与待确认清单.md')],'confirmed_scope':'User requested the complete fourth Influx website, home + tools/pricing + calculator, full scroll and interactions in Chinese and English. Reuse Reels source layout/motion; scheme-three logo, fonts, purple/blue palette and top header are retained. Content may be shortened to fit the reference while preserving core meaning.','included_pages':['index.html','pricing.html','free-tools.html'],'excluded':['production publication','backend submission','payment','real product login until URL supplied','fictional cases/testimonials'],'key_interactions':['original hero motion and videos','original service stack timelines','original ticker loops','original case slider adapted to four product capabilities','original workflow movement','button hover','language selection','single four-field local enquiry','calculator','full screenshots','legal preview dialogs'],'viewports':[{'width':1440,'height':1000},{'width':390,'height':844}],'canonical_output':str(OUT),'project_entry':str(SCHEME),'approval_evidence':'User explicitly requested implementation after finalizing the two documents, and confirmed scheme-three font/color and navigation style.'}
scope.update({'task_mode':'project','output_root':str(OUT),'project_root':str(ROOT),'reference_level':'strong','template_source':['Reels local source snapshots','Scheme five Shinta native first title-and-floating-card transition (read-only local source)'],'core_content':['Agency services','creator resources','AI and product capabilities','project quotes and common contact form','tool subscriptions and calculator'],'brand_constraints':['scheme-three logo, typography, purple-blue palette and navigation'],'latest_content_revision':{'date':'2026-10-27','content_draft':'1.6','internal_notes':'1.5','language':'zh','english':'Existing copy and presentation retained','source':'content-zh.json'}})
scope['module_migration']={'date':'2026-10-27','language':'zh','services':'Native Framer title/background variants and scroll-transform question layout with the same heading and all five marketing-question cards as scheme five','capabilities':'Original native Reels service stack moved to four product capabilities; screenshots and zoom retained','english':'Original services stack and capability carousel retained','reference_runtime':'Project-owned native Framer/Motion modules; original smooth-scroll component and page metadata removed; one existing Reels Lenis instance'}
scope['storage']='Project-owned real directory; no skill template registration or symbolic link.'
scope['english_typeface']={'family':'Leon Sans','source':'User supplied Leon Sans 2.0/LeonSans[wght].ttf','weights':'100-900 variable','asset':'assets/influx/leon-sans-variable.ttf','license':'assets/influx/leon-sans-OFL.txt','language':'en only; Chinese typeface unchanged; Webflow icon font preserved'}
scope['capability_footer_refinement']={'date':'2026-10-27','subscription_note':'Removed from Chinese capabilities','price_link':'Outside the sticky-card containing block; 96px desktop margin and 64px mobile margin','resource_authorization_marquee':'Removed; platform logos remain in resource metrics'}
scope['latest_visual_refinements']={'date':'2026-10-27','transition_light_background':'Uses the same --color--gray-6 (#f7f7f5) as the cover; dark native transition retained','hero_platforms':'One static set of Instagram, X, YouTube and TikTok; no repeated marquee groups or fade masks','resource_metric_units':'Small Chinese unit after 4 and 3, removed from right-side labels','resource_logos':{'social_platforms':['TikTok','YouTube','Instagram','X'],'official_API_platforms':['TikTok','YouTube','Instagram']}}
scope['content_sha256']={Path(p).name:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in scope['content_sources']}
scope['resource_media_review']='Original Reels heights restored independently of metrics: desktop 390px, tablet 300px, phone 250px; second image offset by 80px (original 50px padding plus 30px margin).'
scope['workflow_image_review']=['Remove visible illustration and product demo notes','Use four original Reels photos with a consistent frame','Remove workflow CTA before the contact section']
scope['latest_adjustments']=['Restore template creator avatars and handles; remove hero demonstration note','Center services label','Merge mission imagery and creator network metrics into one resources section','Place slider controls on the card center line','Use a plain right arrow on contact submit']
(OUT/'scope.json').write_text(json.dumps(scope,ensure_ascii=False,indent=2)+'\n')
print('Pages generated:',OUT)

scope['pricing_redesign']={'date':'2026-10-27','task_mode':'project','reference_level':'strong','template_source':['Reels homepage pricing section','Reels contact page'],'included_pages':['pricing.html'],'excluded':['index.html','free-tools.html','other website schemes'],'preserved':['existing navigation','marketing services default tab','two categories','four-field local enquiry','tool plans and prices','bilingual support'],'source_snapshots':['_source/reels-pricing-reference.html.txt','_source/reels-contact-reference.html.txt'],'implementation':'Reels native toggle, form, plan cards and button runtime; centred single-column price label, heading, tabs and service form. Removed service quotation label, title and description at user request.'}
(OUT/'scope.json').write_text(json.dumps(scope,ensure_ascii=False,indent=2)+'\n')

scope['english_content_sync']={'date':'2026-10-27','source':'Final approved Chinese content','pages':['index.html','pricing.html','free-tools.html'],'copy_source':'content-en.json','approach':'Natural English adapted to heading, button and card lengths; same services, pricing, exclusions and enquiry behaviour','chinese_copy':'Compared all Chinese dictionary entries and content-zh.json with pre-edit snapshot: unchanged','layout':'English-only type and wrapping adjustments; shared layout retained'}
(OUT/'scope.json').write_text(json.dumps(scope,ensure_ascii=False,indent=2)+'\n')
