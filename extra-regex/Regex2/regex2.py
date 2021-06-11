import sys; args = sys.argv[1:]
idx = int(args[0])-40

myRegexLst = [
  r"/^[x.o]{64}$/i",
  r"/^[xo]*\.[xo]*$/i",
  r"/^(\..*|.*\.|x+o*\..*|.*\.o*x+)$/i",
  r"/^.(..)*$/s",
  r"/^(0([01]{2})*|1([01]{2})*[01])$/",
  r"/\b\w*(a[eiou]|e[aiou]|i[aeou]|o[aeiu]|u[aeio])\w*\b/i",
  r"/^(0|10)*1*$/",
  r"/^\b[bc]*a?[bc]*$/",
  r"/^\b[bc]*(a[bc]*a[bc]*)*\b$/",
  r"/^\b(2[20]*)?(1[02]*1[02]*)*\b$/"]

if idx < len(myRegexLst):
  print(myRegexLst[idx])