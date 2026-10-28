"""Extract the complete five-question transition exactly as shown in scheme five."""
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
 # User explicitly superseded the previous four-service adaptation with the full reference.
 for index,(old,new) in enumerate([
  ('Influencer collaborations that bring views but no results','不同市场的达人，怎么选？'),
  ('Posting consistently but getting low engagement','粉丝很多，受众适合吗？'),
  ('Content looks “nice”\nbut doesn’t perform','内容制作与发布，谁来跟进？'),
  ('Campaigns feel\nforced and salesy','合作信息分散，进度怎么掌握？'),
  ('No clear content\ndirection or strategy','服务范围和费用，如何确定？')]):
  pain=pain.replace('`'+old+'`','_influxText('+j('transitionQuestion'+str(index))+')')
 # Root retains only the transition: no smooth-scroll component, footer, global overlay or metadata.
 a,b,parts=children(s,'"data-framer-name":`Main`');s=s[:a]+'['+pain+']'+s[b:]
 a,b,parts=children(s,'className:F(E,`framer-72rtr7`,d)');s=s[:a]+'['+parts[0]+']'+s[b:]
 s=replace_call(s,'p(jd,{value:', 'null')
 s=s.replace('ie(a(()=>nn({},s),[s]));','')
 s=s.replace('p(`div`,{id:`overlay`})','null')
 s=s.replace('_(x.main,{className:`framer-1daw1fe`','_(x.div,{className:`framer-1daw1fe`')
 # Same text and wrapping as scheme five; native question cards/icons are untouched.
 s=s.replace('`Social media feels harder than it should be`','_influxText("transitionTitle")')
 s=s.replace('`Influencer collaborations that bring views but no results`','_influxText("transitionQuestion0")')
 s='const _influxText=key=>window.INFLUX_COPY[key][document.documentElement.lang.startsWith("zh")?"zh":"en"];\n'+s
 (out/'runtime/service-transition'/HOME).write_text(s)
