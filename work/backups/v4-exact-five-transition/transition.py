"""Extract the native Shinta transition, with project copy; preserve Framer motion."""
from pathlib import Path
import json
from native_source import children,call
HOME='E7Gy02fTtRRJl6hMB7qcE2rxgwCUbKrxzEbR3iwtkZQ.B9xiGkhW.mjs'
j=lambda v:json.dumps(v,ensure_ascii=False)
def replace_call(s,marker,value):
 a,b=call(s,marker);return s[:a]+value+s[b:]
def build_transition(out):
 s=(out/'_source/service-transition/home.mjs.txt').read_text()
 a,b,parts=children(s,'"data-framer-name":`Main`')
 pain=parts[2]
 a,b,cards=children(pain,'className:`framer-1n8vpg7`')
 # Four approved services replace five reference questions; spacer keeps reset trigger.
 pain=pain[:a]+'['+','.join(cards[:4]+cards[-1:])+']'+pain[b:]
 for index,old in enumerate(['Influencer collaborations that bring views but no results','Posting consistently but getting low engagement','Content looks “nice”\nbut doesn’t perform','Campaigns feel\nforced and salesy']):
  pain=pain.replace('Ht1soGWUc:`'+old+'`','Ht1soGWUc:'+j(str(index)))
 # Root retains only the transition: no smooth-scroll component, footer, global overlay or metadata.
 a,b,parts=children(s,'"data-framer-name":`Main`');s=s[:a]+'['+pain+']'+s[b:]
 a,b,parts=children(s,'className:F(E,`framer-72rtr7`,d)');s=s[:a]+'['+parts[0]+']'+s[b:]
 s=replace_call(s,'p(jd,{value:', 'null')
 s=s.replace('ie(a(()=>nn({},s),[s]));','')
 s=s.replace('p(`div`,{id:`overlay`})','null')
 s=s.replace('_(x.main,{className:`framer-1daw1fe`','_(x.div,{className:`framer-1daw1fe`')
 # Copy is passed as React children, retaining original heading variant/token animations.
 title='(window.INFLUX_COPY.serviceTitle.zh.replace(/<br\\s*\\/?>/g,"\\n"))'
 s=s.replace('children:`Social media feels harder than it should be`','children:'+title)
 qstart=s.index('Qa=z(');qend=s.index('Qa.displayName',qstart)
 q=s[qstart:qend];a,b=call(q,'p(R,{__fromCanvasComponent:!0,children:')
 text=q[a:b]
 kicker='p(`div`,{className:`influx-transition-kicker`,children:window.INFLUX_COPY.serviceKicker.zh})'
 intro='p(`p`,{className:`influx-transition-intro`,children:window.INFLUX_COPY.serviceIntro.zh})'
 q=q[:a]+'p(r,{children:['+kicker+','+text+','+intro+']})'+q[b:]
 s=s[:qstart]+q+s[qend:]
 # Keep native floating containers, transform targets and card material; adapt the card content.
 start=s.index('Io=z(');end=s.index('Io.displayName',start);q=s[start:end]
 a,b=call(q,'p(Eo,{animated:!0')
 q=q[:a]+'p(`span`,{className:`influx-service-number`,children:`0${Number(m)+1}`})'+q[b:]
 a,b=call(q,'p(R,{__fromCanvasComponent:!0,children:')
 body='''_(`div`,{className:`influx-service-copy`,children:[p(`h3`,{children:window.INFLUX_COPY[`service${m}Title`].zh}),p(`p`,{children:window.INFLUX_COPY[`service${m}Desc`].zh}),p(`div`,{className:`influx-service-tags`,children:[0,1,2].map(i=>p(`span`,{children:window.INFLUX_COPY[`service${m}Point${i}`].zh},i))})]})'''
 q=q[:a]+body+q[b:];s=s[:start]+q+s[end:]
 (out/'runtime/service-transition'/HOME).write_text(s)
