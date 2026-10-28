"""Small balanced-expression reader for the saved Framer compile output."""
def skip_string(s,i):
 q=s[i]; i+=1
 while i<len(s):
  if s[i]=='\\': i+=2; continue
  if s[i]==q:return i+1
  if q=='`' and s.startswith('${',i):i=balanced_end(s,i+1);continue
  i+=1
 raise ValueError('unterminated string')
def balanced_end(s,i):
 close={'(':')','[':']','{':'}'}[s[i]];i+=1
 while i<len(s):
  c=s[i]
  if c in '\"\'`':i=skip_string(s,i);continue
  if c in '([{':i=balanced_end(s,i);continue
  if c==close:return i+1
  i+=1
 raise ValueError('unterminated expression')
def children(s,marker):
 start=s.index(marker); a=s.index('children:[',start)+len('children:');end=balanced_end(s,a)
 vals=[];i=a+1;begin=i
 while i<end-1:
  if s[i] in '\"\'`':i=skip_string(s,i);continue
  if s[i] in '([{':i=balanced_end(s,i);continue
  if s[i]==',':vals.append(s[begin:i]);begin=i+1
  i+=1
 vals.append(s[begin:end-1]);return a,end,vals
def call(s,marker):
 i=s.index(marker);return i,balanced_end(s,s.index('(',i))
