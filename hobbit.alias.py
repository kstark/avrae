<drac2>
DIGITS = ''.join(str(i) for i in range(10))
GANDALF = 'ᚠ'
SAURON = '👁'
SUCCESS = 'Ⴀ'

FAVOURED = {"fav", "favoured", "adv", "advantage"}
ILLFAVOURED = {"ill", "dis", "disadvantage"}

err_usage = 'echo "!hobbit <TN> <skill points> [adv] [hope]"'
args=&ARGS&

has_adv = False
if "adv" in args:
    args.remove("adv")
    has_adv = True

has_hope = False
if "hope" in args:
    args.remove("hope")
    has_hope = True

if len(args) != 2:
  return err_usage

def valid_arg(a):
    return all(x in DIGITS for x in a)
    
if not all(valid_arg(a) for a in args):
    return err_usage

TN, Skill = int(args[0]), int(args[1])

if not (10 <= TN <= 18):
  return err_usage

footer = ""

def format_feat(x):
    if x == 12:
        return f"**{GANDALF}**"
    elif x == 0:
        return f"{SAURON}"
    else:
        return str(x)

def roll_feat(has_adv):
  rolls = [roll("1d12")]
  if has_adv:
    rolls.append(roll("1d12"))
  rolls = [r if r != 11 else 0 for r in rolls]
  rolls.sort(reverse=True)
  rolls_strs = [format_feat(rolls[0])] + [f"~~{format_feat(r)}~~" for r in rolls[1:]]
  return max(rolls), f"({', '.join(rolls_strs)})"

F, F_str = roll_feat(has_adv)

def format_success(x):
    if x == 6:
        return f"**{SUCCESS}**"
    else:
        return str(x)

def roll_success(num, weary=False):
    if not num:
        return 0, ""

    rolls = [roll("1d6") for _ in range(num)]
    if weary:
        rolls = [(r if r > 3 else 0) for r in rolls]
    return sum(rolls), f"({', '.join(format_success(r) for r in rolls)})"

S, S_str = roll_success(Skill + int(has_hope))

result = F + S
rolls_str = F_str
if S_str:
    rolls_str += f" + {S_str}"

success = False
if F == 12:
    result_str = "🎉 Automatic Success! 🎉"
    success = True
else:
    success = result >= TN
    result_str = f"**{'✅ Success' if success else '❌ Failure'}**: **{result}** vs. TN {TN}"    

# I got lazy here sorry
if success and SUCCESS in S_str:
    success_count = S_str.count(SUCCESS)
    if success_count > 2:
        footer = f"{SUCCESS}{SUCCESS}+ Extraordinary success!"
    elif success_count == 2:
        footer = f"{SUCCESS}{SUCCESS} Extraordinary success!"
    elif success_count == 1:
        footer = f"{SUCCESS} Great success!"
 
return (f'''
    embed
    -desc "{result_str}"
    -footer "{footer}"
    -f "Rolls|{rolls_str}"
'''.replace("\n", " ").strip())
</drac2>
