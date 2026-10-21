"""Graphviz diagrams for the FinTech study guide. Outputs SVG into ./fig"""
import subprocess, os
OUT = os.path.join(os.path.dirname(__file__), "fig")
os.makedirs(OUT, exist_ok=True)

BASE = '''
  graph [fontname="Inter", fontsize=13, bgcolor="white", pad=0.25, nodesep=0.35, ranksep=0.45];
  node  [fontname="Inter", fontsize=13, shape=box, style="rounded,filled", penwidth=1.6, margin="0.18,0.10"];
  edge  [fontname="Inter", fontsize=11, penwidth=1.5, color="#44546A", fontcolor="#33415C", arrowsize=0.8];
'''
# colour helpers: (fill, border)
B = 'fillcolor="#E6EEFB", color="#2E6FD8"'
T = 'fillcolor="#E2F4F1", color="#0F9D8A"'
O = 'fillcolor="#FDEEDF", color="#E07B26"'
R = 'fillcolor="#FBE6E3", color="#C8483B"'
P = 'fillcolor="#EEE8FA", color="#7A5AC8"'
G = 'fillcolor="#F1F3F6", color="#6B7A90"'
N = 'fillcolor="#1F3A5F", color="#1F3A5F", fontcolor="white"'

def render(name, body, engine="dot"):
    body = body.replace(" <b>", "&#160;<b>").replace("</b> ", "</b>&#160;")
    src = "digraph G {\n" + BASE + body + "\n}"
    path = os.path.join(OUT, name + ".svg")
    subprocess.run([engine, "-Tsvg", "-o", path], input=src.encode(), check=True)
    return path

D = {}


# ---------- Unit 1: Lens ----------
D["lens"] = f'''
  rankdir=LR; nodesep=0.2; ranksep=0.35;
  node [shape=cds, style="filled", margin="0.25,0.12", fontsize=13];
  c [label=<<b>1 · Customer</b><br/>WHO?<br/><font point-size="11">B2C · B2B · B2B2C · C2C</font>>, fillcolor="#E6EEFB", color="#2E6FD8"];
  p [label=<<b>2 · Pain point</b><br/>WHAT?<br/><font point-size="11">fees · delay · paperwork</font>>, fillcolor="#FBE6E3", color="#C8483B"];
  v [label=<<b>3 · Value prop</b><br/>WHY?<br/><font point-size="11">cheaper · easier · faster ·<br/>more convenient</font>>, fillcolor="#E2F4F1", color="#0F9D8A"];
  m [label=<<b>4 · Monetisation</b><br/>HOW?<br/><font point-size="11">fees · spread · AUM % · SaaS</font>>, fillcolor="#FDEEDF", color="#E07B26"];
  c -> p -> v -> m [style=invis];
'''

# ---------- Unit 2: MSP ----------
D["msp"] = f'''
  rankdir=TB; ranksep=0.55;
  plat [label=<<b>PLATFORM</b><br/><font point-size="11">matches both sides · collects data · lowers friction</font>>, {N}];
  sub [label=<<b>SUBSIDY SIDE</b> (loss leader)<br/><font point-size="11">consumers get it free/cheap<br/>e.g. free credit score, zero-fee QR</font>>, {T}];
  mon [label=<<b>MONEY SIDE</b> (profit centre)<br/><font point-size="11">lenders, merchants, insurers pay<br/>lead / referral / processing fees</font>>, {O}];
  {{rank=same; sub; mon;}}
  sub -> plat [label="  users + data  "];
  plat -> mon [label="  qualified leads  "];
  mon -> plat [label="  fees ($)  ", color="#E07B26", fontcolor="#B35A12"];
  plat -> sub [label="  free features  ", color="#0F9D8A", fontcolor="#0B7A6B"];
  sub -> mon [label="  cross-side network effect:\\n more users attract more partners  ", style=dashed, constraint=false, dir=both];
'''


# ---------- Unit 3: BigTech flywheel ----------
D["flywheel"] = f'''
  layout=circo; mindist=1.2;
  node [width=1.9];
  a [label=<<b>Platform scale</b><br/><font point-size="11">billions of users</font>>, {B}];
  b [label=<<b>Data exhaust</b><br/><font point-size="11">payments, shopping, chats</font>>, {P}];
  c [label=<<b>Predictive ML</b><br/><font point-size="11">credit &amp; risk models</font>>, {T}];
  d [label=<<b>Personalised finance</b><br/><font point-size="11">loans, wealth, insurance</font>>, {O}];
  e [label=<<b>Ecosystem lock-in</b><br/><font point-size="11">users stay &amp; engage</font>>, {R}];
  a -> b -> c -> d -> e -> a;
'''

# ---------- Unit 4: Hash-linked chain ----------
D["hashchain"] = '''
  rankdir=LR; nodesep=0.4; ranksep=0.6;
  node [shape=plain, style="", margin=0];
  b100 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="7" color="#2E6FD8">
     <tr><td bgcolor="#2E6FD8"><font color="white"><b>Block 100</b></font></td></tr>
     <tr><td bgcolor="#E6EEFB" align="left">Prev hash: <b>…</b></td></tr>
     <tr><td bgcolor="#F7F9FD" align="left">Transactions (Merkle root)</td></tr>
     <tr><td bgcolor="#F7F9FD" align="left">Timestamp · Nonce</td></tr>
     <tr><td bgcolor="#FFF6D6" align="left">This hash: <b>Hash_A</b></td></tr></table>>];
  b101 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="7" color="#C8483B">
     <tr><td bgcolor="#C8483B"><font color="white"><b>Block 101  (attacker edits a tx)</b></font></td></tr>
     <tr><td bgcolor="#E6EEFB" align="left">Prev hash: <b>Hash_A</b></td></tr>
     <tr><td bgcolor="#FBE6E3" align="left">Transactions ✎ changed</td></tr>
     <tr><td bgcolor="#F7F9FD" align="left">Timestamp · Nonce</td></tr>
     <tr><td bgcolor="#FBE6E3" align="left">This hash: <b>Hash_B → Hash_B*</b></td></tr></table>>];
  b102 [label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="7" color="#2E6FD8">
     <tr><td bgcolor="#2E6FD8"><font color="white"><b>Block 102</b></font></td></tr>
     <tr><td bgcolor="#FBE6E3" align="left">Prev hash: <b>Hash_B</b>  ≠ Hash_B*  ✗</td></tr>
     <tr><td bgcolor="#F7F9FD" align="left">Transactions (Merkle root)</td></tr>
     <tr><td bgcolor="#F7F9FD" align="left">Timestamp · Nonce</td></tr>
     <tr><td bgcolor="#FFF6D6" align="left">This hash: <b>Hash_C</b></td></tr></table>>];
  b100 -> b101 [label=" links "];
  b101 -> b102 [label=" link BROKEN ", color="#C8483B", fontcolor="#C8483B", style=dashed];
'''

# ---------- Unit 4: PoW mining flow ----------
D["pow_flow"] = f'''
  rankdir=TB; ranksep=0.32;
  a [label=<<b>1. Sign</b> transaction with <b>private key</b>>, {B}];
  b [label=<<b>2. Broadcast</b> → waits in the <b>mempool</b><br/><font point-size="11">(higher fee = picked sooner)</font>>, {B}];
  c [label=<<b>3. Miner builds candidate block header</b><br/><font point-size="11">version · prev hash · Merkle root · timestamp · difficulty · nonce</font>>, {P}];
  d [label=<<b>4. Try nonce → SHA-256(header)</b>>, {O}];
  q [label=<<b>Hash &lt; Target T ?</b><br/><font point-size="11">(enough leading zeros)</font>>, shape=diamond, style=filled, {G}, margin="0.05,0.05"];
  e [label=<<b>5. Broadcast block</b> → nodes verify in one step>, {T}];
  f [label=<<b>6. Append to chain</b> · miner earns block reward + fees>, {N}];
  a -> b -> c -> d -> q;
  q -> e [label="  yes  "];
  q -> d [label="  no: nonce + 1  ", color="#C8483B", fontcolor="#C8483B"];
  e -> f;
'''

# ---------- Unit 4: Difficulty adjustment loop ----------
D["difficulty"] = f'''
  rankdir=LR; nodesep=0.3; ranksep=0.5;
  m [label=<<b>Every 2,016 blocks</b><br/><font point-size="11">(target: 2,016 × 10 min = 20,160 min ≈ 2 weeks)</font>>, {N}];
  f [label=<<b>Took LESS than 20,160 min</b><br/><font point-size="11">hash rate rose</font>>, {R}];
  s [label=<<b>Took MORE than 20,160 min</b><br/><font point-size="11">miners switched off</font>>, {T}];
  f2 [label=<<b>T shrinks → difficulty ↑</b>>, {R}];
  s2 [label=<<b>T grows → difficulty ↓</b>>, {T}];
  m -> f -> f2; m -> s -> s2;
'''

# ---------- Unit 5: Four-party card scheme ----------
D["card4party"] = f'''
  rankdir=TB; nodesep=0.55; ranksep=0.7;
  ch [label=<<b>① Cardholder</b><br/><font point-size="11">pays $100</font>>, {B}];
  me [label=<<b>② Merchant</b><br/><font point-size="11">nets $97.39</font>>, {T}];
  gw [label=<<b>③ Gateway / processor</b><br/><font point-size="11">keeps $0.50</font>>, {P}];
  ac [label=<<b>④ Acquirer</b><br/><font point-size="11">merchant's bank · keeps $0.25</font>>, {T}];
  nw [label=<<b>⑤ Card network</b><br/><font point-size="11">Visa / Mastercard · keeps $0.11</font>>, {N}];
  is [label=<<b>⑥ Issuer</b><br/><font point-size="11">cardholder's bank · keeps $1.75</font>>, {O}];
  {{rank=same; ch; me;}}
  {{rank=same; gw; ac;}}
  {{rank=same; nw; is;}}
  ch -> me [label=" taps card "];
  me -> gw [label=" auth request "];
  gw -> ac [label=" routes "];
  ac -> nw [label=" "];
  nw -> is [label=" asks: approve? "];
'''


# ---------- Unit 5: Wise netting ----------
D["wise"] = f'''
  rankdir=LR; nodesep=0.4; ranksep=0.55;
  s [label=<<b>Sender (UK)</b><br/><font point-size="11">pays GBP</font>>, {B}];
  wuk [label=<<b>Wise GBP account</b><br/><font point-size="11">local, in the UK</font>>, {T}];
  weu [label=<<b>Wise EUR account</b><br/><font point-size="11">local, pre-funded</font>>, {T}];
  r [label=<<b>Recipient (EU)</b><br/><font point-size="11">gets EUR at<br/>mid-market rate</font>>, {O}];
  s -> wuk [label=" local\n transfer "];
  wuk -> weu [label=" NO cross-border\n wire (netted) ", style=dashed, color="#6B7A90"];
  weu -> r [label=" local\n payout "];
'''

# ---------- Unit 6: Balance-sheet vs marketplace ----------
D["lending_models"] = f'''
  rankdir=LR; nodesep=0.35; ranksep=0.5;
  subgraph cluster_a0 {{ label=<<b>BALANCE-SHEET (principal) - bank</b>>; fontname="Inter"; color="#2E6FD8"; style="rounded";
    dep [label="Depositors", {B}]; bank [label=<<b>Bank</b><br/><font point-size="11">holds loan · bears default risk<br/>earns NIM (spread)</font>>, {N}]; bor1 [label="Borrower", {B}];
    dep -> bank [label=" deposits "]; bank -> bor1 [label=" loan "]; }}
  subgraph cluster_m {{ label=<<b>MARKETPLACE / P2P (agent) - platform</b>>; fontname="Inter"; color="#0F9D8A"; style="rounded";
    inv [label="Investors\\n(retail / institutional)", {T}]; plat [label=<<b>Platform</b><br/><font point-size="11">matches · scores · services<br/>earns fees (1–6% + ~1%)</font>>, fillcolor="#0F9D8A", color="#0F9D8A", fontcolor="white"]; bor2 [label="Borrower", {T}];
    inv -> plat [label=" buys notes "]; plat -> bor2 [label=" loan "]; inv -> bor2 [label=" default risk sits\\n with investor ", style=dashed, color="#C8483B", fontcolor="#C8483B", constraint=false]; }}
'''

# ---------- Unit 6: LendingClub note model ----------
D["lendingclub"] = f'''
  rankdir=LR; nodesep=0.3; ranksep=0.45;
  a [label=<<b>Borrower</b><br/><font point-size="11">applies online</font>>, {B}];
  b [label=<<b>WebBank</b><br/><font point-size="11">FDIC bank in Utah<br/>originates loan</font>>, {G}];
  c [label=<<b>LendingClub</b><br/><font point-size="11">buys loan immediately</font>>, {T}];
  d [label=<<b>Investors</b><br/><font point-size="11">buy Member Payment<br/>Dependent Notes</font>>, {O}];
  a -> b -> c -> d;
'''


# ---------- Unit 7: Open banking consent ----------
D["openbanking"] = f'''
  rankdir=TB; ranksep=0.35;
  a [label=<<b>1.</b> Customer opens FinTech app → "Connect my bank">, {B}];
  b [label=<<b>2.</b> App redirects to the <b>bank's own login page</b><br/><font point-size="11">(app never sees the password)</font>>, {G}];
  c [label=<<b>3.</b> Customer <b>gives consent</b>: which data, for how long>, {T}];
  d [label=<<b>4.</b> Bank issues an <b>access token</b> to the app>, {O}];
  e [label=<<b>5.</b> App calls the bank's <b>open API</b> with the token<br/><font point-size="11">balances, transactions, payment initiation</font>>, {N}];
  f [label=<<b>Consent can be revoked anytime</b>>, {R}];
  a -> b -> c -> d -> e;
  e -> f [style=dashed, arrowhead=none];
'''



if __name__ == "__main__":
    for k, v in D.items():
        eng = "circo" if k == "flywheel" else "dot"
        render(k, v, eng)
    print("ok", len(D))
