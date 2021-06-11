import sys; args = sys.argv[1:]
idx = int(args[0])-30

myRegexLst = [
  r"/^0$|^10[01]$/",
  r"/^[01]*$/",
  r"/^.*0$/",
  r"/\b\w*[aeiou]\w*[aeiou]\w*\b/i",
  r"/^1[01]*0$|^0$/",
  r"/^[01]*110[01]*$/",
  r"/^.{2,4}$/s",
  r"/^\d{3} *-? *\d{2} *-?\s*\d{4}$/",
  r"/^[^d^\n]*d\w*/mi",
  r"/^0[01]*0$|^1[01]*1$|^[01]?$/"
  ]

if idx < len(myRegexLst):
  print(myRegexLst[idx])