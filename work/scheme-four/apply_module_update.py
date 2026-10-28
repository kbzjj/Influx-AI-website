from pathlib import Path
p=Path('work/scheme-four/build.py');s=p.read_text()
marker='# All Chinese editorial content has one project-owned source; do not change English values.'
block='''# Locale branches are pruned before either native animation runtime initializes.
# Reuse the original Reels service structure and its original timeline at capabilities.
capstack=services.clone();capstack.attrs.update({'id':'capabilities','data-locale-branch':'zh','class':capstack.attrs.get('class','')+' product-stack'})
bind(capstack.one(cls='service-title'),'capTitle',COPY['capTitle']['zh'],COPY['capTitle']['en'])
bind(capstack.one(cls='service-kicker'),'capKicker',COPY['capKicker']['zh'],COPY['capKicker']['en'])
bind(capstack.one(cls='service-intro'),'capIntro',COPY['capIntro']['zh'],COPY['capIntro']['en'])
for i,card in enumerate(capstack.all(cls='service-card')):
 card.attrs['data-product-card']=str(i)
 bind(card.one(cls='service-card-title'),f'cap{i}Title',COPY[f'cap{i}Title']['zh'],COPY[f'cap{i}Title']['en'])
 bind(card.one(cls='service-card-description'),f'cap{i}Desc',COPY[f'cap{i}Desc']['zh'],COPY[f'cap{i}Desc']['en'])
 detail=card.one(cls='service-card-detail')
 detail.children=[bind(Node('div',{'class':'product-stack-label'}),'capLabel',COPY['capLabel']['zh'],COPY['capLabel']['en']),bind(Node('h4',{'class':'service-counter'}),f'capIndex{i}',COPY[f'capIndex{i}']['zh'],COPY[f'capIndex{i}']['en'])]
 zoom=button('zoomScreen',COPY['zoomScreen']['zh'],COPY['zoomScreen']['en']);zoom.tag='button';zoom.attrs.pop('href',None);zoom.attrs.update({'type':'button','data-zoom':str(i)})
 detail.children.append(zoom)
 image=card.one(cls='service-card-image');image.attrs={'src':'assets/influx/'+files[i],'alt':caps[i][1]+' interface','class':'service-card-image','data-product-screen':'','tabindex':'0','role':'button','width':'2880','height':'1800','loading':'lazy'}
capstack.one(cls='container-medium').children.append(bottom.clone())
services.attrs['data-locale-branch']='en';cap.attrs['data-locale-branch']='en'
transition=Node('section',{'id':'managed','class':'service-transition','data-locale-branch':'zh','aria-label':'Influx 营销服务'},[Node('div',{'id':'service-transition-root'})])
from transition import build_transition
build_transition(OUT)
'''
assert marker in s;s=s.replace(marker,block+'\n'+marker)
s=s.replace("[hero,services,quoteSection,resources,cap,process,contact]","[hero,transition,services,quoteSection,resources,capstack,cap,process,contact]")
s=s.replace("raw('<script src=\"runtime-bridge.js\"></script>')","raw('<script src=\"runtime-bridge.js\"></script>'),raw('<script type=\"module\" src=\"service-transition.js\"></script>')")
s=s.replace("'template_source':'Reels local source snapshots'","'template_source':['Reels local source snapshots','Scheme five Shinta native first title-and-floating-card transition (read-only local source)']")
s=s.replace("scope['storage']=","scope['module_migration']={'date':'2026-10-27','language':'zh','services':'Native Framer title/background variants and scroll-transform question layout adapted to four existing service items','capabilities':'Original native Reels service stack moved to four product capabilities; screenshots and zoom retained','english':'Original services stack and capability carousel retained','reference_runtime':'Project-owned native Framer/Motion modules; original smooth-scroll component and page metadata removed; one existing Reels Lenis instance'}\nscope['storage']=")
p.write_text(s)
p=Path('versions/方案四/influx.js');s=p.read_text().replace("  const say = key", "  document.querySelectorAll('[data-locale-branch]').forEach(node => { if (node.dataset.localeBranch !== language) node.remove(); });\n  const say = key")
s=s.replace("button.closest('.w-slide')","button.closest('.w-slide,[data-product-card]')")
p.write_text(s)
