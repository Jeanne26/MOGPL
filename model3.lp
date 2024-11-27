\ Model model3
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  3 r3 - b13 - b23 - b33 - b43 - b53 - b63
Subject To
 R0: r3 - b13 <= 2
 R1: r3 - b23 <= 9
 R2: r3 - b33 <= 6
 R3: r3 - b43 <= 8
 R4: r3 - b53 <= 5
 R5: r3 - b63 <= 4
Bounds
End
