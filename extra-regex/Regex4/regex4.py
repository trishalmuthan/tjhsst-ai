import sys; args = sys.argv[1:]
idx = int(args[0])-60

myRegexLst = [
  r"/^(?!.*010)[01]*$/",
  r"/^(?!.*101)(?!.*010)[01]*$/",
  r"/^(([01])[01]*\2|[01])$/",
  r"//",
  r"//",
  r"//",
  r"//",
  r"//",
  r"//",
  r"//"
  ]

if idx < len(myRegexLst):
  print(myRegexLst[idx])